#!/usr/bin/env python3
"""Execute a real host lifecycle smoke test and capture fail-closed evidence.

The runner currently implements Gemini CLI because its terminal skill-management
lifecycle is documented and automatable. A blocked runtime/auth/network attempt is
recorded as diagnostic evidence but is never promoted into host-smoke PASS/FAIL.
Only an actual lifecycle execution record can affect the v2 gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
import time
import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SECRET_NAME_RE = re.compile(r"(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|AUTH)", re.I)
AUTH_MARKERS = (
    "api key", "authentication", "authenticate", "credentials", "login", "oauth",
    "not logged in", "unauthorized", "permission denied",
)
NETWORK_MARKERS = (
    "enotfound", "econnreset", "econnrefused", "network", "fetch failed", "timed out",
    "timeout", "temporary failure in name resolution", "dns",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def resolve_release_artifact(root: Path, cfg: dict[str, Any], artifact: str | None) -> Path:
    package_root = root / cfg["package_distribution"]
    if artifact:
        p = Path(artifact)
        candidates = [p] if p.is_absolute() else [root / p, package_root / p, package_root / "packages" / p]
        for c in candidates:
            if c.exists() and c.is_file():
                try:
                    c.resolve().relative_to(root.resolve())
                except ValueError as exc:
                    raise ValueError("artifact must be inside the repository release") from exc
                return c.resolve()
        raise FileNotFoundError(f"release artifact not found: {artifact}")
    default = package_root / "packages" / "agent-skill-engineering.skill"
    if not default.exists():
        skills = sorted((package_root / "packages").glob("*.skill"))
        if not skills:
            raise FileNotFoundError("no .skill artifacts found in package distribution")
        default = skills[0]
    return default.resolve()


def parse_skill_name(skill_archive: Path) -> str:
    with zipfile.ZipFile(skill_archive) as zf:
        names = [n for n in zf.namelist() if n.endswith("/SKILL.md") or n == "SKILL.md"]
        if not names:
            raise ValueError("artifact does not contain SKILL.md")
        raw = zf.read(sorted(names, key=lambda x: (x.count("/"), len(x)))[0]).decode("utf-8", errors="replace")
    m = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", raw)
    if not m:
        raise ValueError("cannot determine skill name from SKILL.md")
    return m.group(1).strip()


def redaction_values(env: dict[str, str]) -> list[str]:
    values: list[str] = []
    for k, v in env.items():
        if SECRET_NAME_RE.search(k) and isinstance(v, str) and len(v) >= 6:
            values.append(v)
    return sorted(set(values), key=len, reverse=True)


def redact(text: str, secrets: Iterable[str]) -> str:
    out = text
    for secret in secrets:
        out = out.replace(secret, "[REDACTED]")
    return out


@dataclass
class CommandResult:
    name: str
    command: list[str]
    returncode: int | None
    started_at: str
    finished_at: str
    duration_ms: int
    stdout_ref: str
    stderr_ref: str
    stdout_sha256: str
    stderr_sha256: str
    timed_out: bool = False
    exception: str | None = None

    @property
    def passed(self) -> bool:
        return self.returncode == 0 and not self.timed_out and not self.exception

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "command": self.command,
            "returncode": self.returncode,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": self.duration_ms,
            "stdout_ref": self.stdout_ref,
            "stderr_ref": self.stderr_ref,
            "stdout_sha256": self.stdout_sha256,
            "stderr_sha256": self.stderr_sha256,
            "timed_out": self.timed_out,
            "exception": self.exception,
            "passed": self.passed,
        }


def run_command(
    *, root: Path, run_dir: Path, name: str, command: list[str], cwd: Path,
    env: dict[str, str], timeout: int, input_text: str | None = None,
) -> tuple[CommandResult, str, str]:
    started = utc_now()
    t0 = time.monotonic()
    stdout = stderr = ""
    rc: int | None = None
    timed_out = False
    exc_text: str | None = None
    try:
        cp = subprocess.run(
            command,
            cwd=str(cwd),
            env=env,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        rc, stdout, stderr = cp.returncode, cp.stdout or "", cp.stderr or ""
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        exc_text = f"TimeoutExpired after {timeout}s"
    except Exception as exc:  # runner evidence must survive unexpected host errors
        exc_text = f"{type(exc).__name__}: {exc}"
    finished = utc_now()
    duration_ms = int((time.monotonic() - t0) * 1000)
    secrets = redaction_values(env)
    stdout = redact(stdout, secrets)
    stderr = redact(stderr, secrets)
    if exc_text:
        exc_text = redact(exc_text, secrets)
    out_path = run_dir / f"{name}.stdout.log"
    err_path = run_dir / f"{name}.stderr.log"
    out_path.write_text(stdout, encoding="utf-8")
    err_path.write_text(stderr, encoding="utf-8")
    result = CommandResult(
        name=name,
        command=[redact(x, secrets) for x in command],
        returncode=rc,
        started_at=started,
        finished_at=finished,
        duration_ms=duration_ms,
        stdout_ref=rel(root, out_path),
        stderr_ref=rel(root, err_path),
        stdout_sha256=sha256_file(out_path),
        stderr_sha256=sha256_file(err_path),
        timed_out=timed_out,
        exception=exc_text,
    )
    return result, stdout, stderr


def classify_blocker(text: str) -> str | None:
    low = text.lower()
    if any(x in low for x in AUTH_MARKERS):
        return "BLOCKED_AUTH"
    if any(x in low for x in NETWORK_MARKERS):
        return "BLOCKED_NETWORK"
    return None


def activation_observed(text: str, skill_name: str) -> bool:
    low = text.lower()
    return "activate_skill" in low and skill_name.lower() in low


def load_host_evidence(path: Path, repository_version: str) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "repository_version": repository_version, "records": []}
    data = load_json(path)
    if data.get("repository_version") != repository_version or not isinstance(data.get("records"), list):
        raise ValueError("host-smoke.json does not match repository version/schema")
    return data


def upsert_host_record(path: Path, repository_version: str, record: dict[str, Any]) -> None:
    data = load_host_evidence(path, repository_version)
    # Preserve history; run_id is unique. Avoid duplicate append when replaying the same run.
    run_id = record.get("run_id")
    records = [r for r in data["records"] if r.get("run_id") != run_id]
    records.append(record)
    data["records"] = records
    dump_json(path, data)


def execute_gemini(
    root: Path,
    cfg: dict[str, Any],
    artifact: Path,
    tester: str,
    binary: str,
    timeout: int,
    activation_prompt: str | None,
    inherit_home: bool,
    keep_runtime: bool,
    npx_bootstrap: bool = False,
) -> dict[str, Any]:
    run_id = f"gemini-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    evidence_root = root / cfg["evidence_root"]
    run_dir = evidence_root / "runs" / run_id
    attempt_path = evidence_root / "attempts" / f"{run_id}.json"
    run_dir.mkdir(parents=True, exist_ok=True)
    attempt_path.parent.mkdir(parents=True, exist_ok=True)

    skill_name = parse_skill_name(artifact)
    digest = sha256_file(artifact)
    started_at = utc_now()
    attempt: dict[str, Any] = {
        "schema_version": 1,
        "repository_version": cfg["repository_version"],
        "run_id": run_id,
        "host_id": "gemini-cli",
        "tester": tester,
        "platform": platform.platform(),
        "started_at": started_at,
        "finished_at": None,
        "artifact": rel(root, artifact),
        "artifact_sha256": digest,
        "skill_name": skill_name,
        "outcome": "RUNNING",
        "blocker": None,
        "promoted_to_host_smoke": False,
        "commands": [],
        "lifecycle": {},
        "runtime_isolation": "inherit-home" if inherit_home else "isolated-home",
    }
    dump_json(attempt_path, attempt)

    exe = shutil.which(binary)
    launcher: list[str]
    bootstrap_mode = False
    if exe:
        launcher = [exe]
    elif npx_bootstrap:
        npx = shutil.which("npx")
        if not npx:
            attempt.update({
                "finished_at": utc_now(),
                "outcome": "BLOCKED_RUNTIME",
                "blocker": f"executable not found: {binary}; npx bootstrap unavailable",
            })
            dump_json(attempt_path, attempt)
            return attempt
        launcher = [npx, "-y", "@google/gemini-cli@latest"]
        bootstrap_mode = True
        attempt["runtime_bootstrap"] = "npx:@google/gemini-cli@latest"
    else:
        attempt.update({
            "finished_at": utc_now(),
            "outcome": "BLOCKED_RUNTIME",
            "blocker": f"executable not found: {binary}",
        })
        dump_json(attempt_path, attempt)
        return attempt

    temp_obj = tempfile.TemporaryDirectory(prefix="gas-playbook-live-")
    runtime_root = Path(temp_obj.name)
    workspace = runtime_root / "workspace"
    sandbox_home = runtime_root / "home"
    workspace.mkdir(parents=True)
    sandbox_home.mkdir(parents=True)
    env = os.environ.copy()
    env["NO_COLOR"] = "1"
    env["CI"] = "1"
    if not inherit_home:
        env["HOME"] = str(sandbox_home)
        env["USERPROFILE"] = str(sandbox_home)

    command_results: list[CommandResult] = []
    host_version = "unknown"
    lifecycle: dict[str, dict[str, Any]] = {}
    blocker: str | None = None
    true_host_failure = False

    def do(name: str, args: list[str], input_text: str | None = None) -> tuple[CommandResult, str, str]:
        result, out, err = run_command(
            root=root, run_dir=run_dir, name=name, command=[*launcher, *args], cwd=workspace,
            env=env, timeout=timeout, input_text=input_text,
        )
        command_results.append(result)
        attempt["commands"] = [x.as_dict() for x in command_results]
        dump_json(attempt_path, attempt)
        return result, out, err

    try:
        ver_res, ver_out, ver_err = do("00-version", ["--version"])
        if ver_res.passed:
            host_version = (ver_out or ver_err).strip().splitlines()[0][:200] or "unknown"
        else:
            blocker = classify_blocker(ver_out + "\n" + ver_err)
            if blocker is None:
                blocker = "BLOCKED_NETWORK" if bootstrap_mode and ver_res.timed_out else "BLOCKED_RUNTIME"

        if blocker is None:
            install_res, install_out, install_err = do(
                "10-install", ["skills", "install", str(artifact), "--scope", "workspace", "--consent"]
            )
            list_res, list_out, list_err = do("11-list-after-install", ["skills", "list"])
            install_ok = install_res.passed and list_res.passed and skill_name.lower() in (list_out + list_err).lower()
            lifecycle["install"] = {
                "status": "PASS" if install_ok else "FAIL",
                "evidence_ref": rel(root, run_dir / "10-install.stdout.log"),
                "operation": "install+discover",
            }
            if not install_ok:
                combined = install_out + install_err + list_out + list_err
                blocker = classify_blocker(combined)
                true_host_failure = blocker is None

        if blocker is None and lifecycle.get("install", {}).get("status") == "PASS":
            prompt = activation_prompt or (
                f"Use the {skill_name} skill for this request. Explain in one short sentence what this skill is for. "
                "Do not edit files and do not run shell commands."
            )
            act_res, act_out, act_err = do(
                "20-activation",
                ["--skip-trust", "--approval-mode", "yolo", "--output-format", "stream-json", "-p", prompt],
            )
            observed = act_res.passed and activation_observed(act_out + "\n" + act_err, skill_name)
            lifecycle["activation"] = {
                "status": "PASS" if observed else "FAIL",
                "evidence_ref": rel(root, run_dir / "20-activation.stdout.log"),
                "operation": "headless activate_skill observation",
            }
            if not observed:
                blocker = classify_blocker(act_out + "\n" + act_err)
                true_host_failure = blocker is None

        if blocker is None and lifecycle.get("activation", {}).get("status") == "PASS":
            dis_res, dis_out, dis_err = do("30-disable", ["skills", "disable", skill_name, "--scope", "workspace"])
            en_res, en_out, en_err = do("31-enable", ["skills", "enable", skill_name, "--scope", "workspace"])
            ref_res, ref_out, ref_err = do("32-list-after-refresh", ["skills", "list"])
            refresh_ok = dis_res.passed and en_res.passed and ref_res.passed and skill_name.lower() in (ref_out + ref_err).lower()
            lifecycle["update"] = {
                "status": "PASS" if refresh_ok else "FAIL",
                "evidence_ref": rel(root, run_dir / "32-list-after-refresh.stdout.log"),
                "operation": "disable-enable-rescan",
                "note": "Gemini CLI lifecycle refresh; not a cross-version package upgrade.",
            }
            if not refresh_ok:
                blocker = classify_blocker(dis_out + dis_err + en_out + en_err + ref_out + ref_err)
                true_host_failure = blocker is None

        # Cleanup is attempted whenever installation was attempted, even after activation/update failure.
        if "install" in lifecycle:
            un_res, un_out, un_err = do(
                "40-uninstall", ["skills", "uninstall", skill_name, "--scope", "workspace"], input_text="y\n"
            )
            post_res, post_out, post_err = do("41-list-after-uninstall", ["skills", "list"])
            uninstall_ok = un_res.passed and post_res.passed and skill_name.lower() not in (post_out + post_err).lower()
            lifecycle["uninstall"] = {
                "status": "PASS" if uninstall_ok else "FAIL",
                "evidence_ref": rel(root, run_dir / "40-uninstall.stdout.log"),
                "operation": "uninstall+absence-check",
            }
            if not uninstall_ok and blocker is None:
                blocker = classify_blocker(un_out + un_err + post_out + post_err)
                true_host_failure = blocker is None

        attempt["lifecycle"] = lifecycle
        all_steps = cfg.get("required_host_steps", ["install", "activation", "update", "uninstall"])
        complete = all(step in lifecycle for step in all_steps)
        all_pass = complete and all(lifecycle[step].get("status") == "PASS" for step in all_steps)

        if blocker in {"BLOCKED_AUTH", "BLOCKED_NETWORK", "BLOCKED_RUNTIME"}:
            outcome = blocker
        elif all_pass:
            outcome = "PASS"
        elif complete and true_host_failure:
            outcome = "FAIL"
        elif true_host_failure:
            outcome = "FAIL"
        else:
            outcome = "BLOCKED_PREREQUISITE"

        attempt.update({
            "host_version": host_version,
            "finished_at": utc_now(),
            "outcome": outcome,
            "blocker": blocker if outcome.startswith("BLOCKED_") else None,
            "commands": [x.as_dict() for x in command_results],
            "lifecycle": lifecycle,
        })

        if outcome in {"PASS", "FAIL"} and complete:
            refs = sorted({item["evidence_ref"] for item in lifecycle.values() if item.get("evidence_ref")})
            record = {
                "run_id": run_id,
                "host_id": "gemini-cli",
                "claimed_status": outcome,
                "host_version": host_version,
                "platform": platform.platform(),
                "tester": tester,
                "tested_at": attempt["finished_at"],
                "artifact": rel(root, artifact),
                "artifact_sha256": digest,
                "lifecycle": lifecycle,
                "evidence_refs": refs + [rel(root, attempt_path)],
            }
            host_path = evidence_root / "host-smoke.json"
            upsert_host_record(host_path, cfg["repository_version"], record)
            attempt["promoted_to_host_smoke"] = True

        dump_json(attempt_path, attempt)
        return attempt
    finally:
        if keep_runtime:
            retained = run_dir / "runtime-path.txt"
            retained.write_text(str(runtime_root) + "\n", encoding="utf-8")
            # Prevent TemporaryDirectory cleanup when explicitly requested.
            temp_obj._finalizer.detach()  # type: ignore[attr-defined]
        else:
            temp_obj.cleanup()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="packaging/live-validation/live-v1.31.0.json")
    ap.add_argument("--host", default="gemini-cli", choices=["gemini-cli"])
    ap.add_argument("--artifact", help="Release .skill path or package filename")
    ap.add_argument("--tester", default=os.environ.get("USER") or os.environ.get("USERNAME") or "live-runner")
    ap.add_argument("--binary", default="gemini")
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--activation-prompt")
    ap.add_argument("--inherit-home", action="store_true", help="Use the caller HOME instead of an isolated temporary HOME")
    ap.add_argument("--keep-runtime", action="store_true")
    ap.add_argument("--npx-bootstrap", action="store_true", help="If gemini is absent, opt in to npx @google/gemini-cli@latest")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg_path = root / args.config
    cfg = load_json(cfg_path)
    artifact = resolve_release_artifact(root, cfg, args.artifact)
    result = execute_gemini(
        root=root,
        cfg=cfg,
        artifact=artifact,
        tester=args.tester,
        binary=args.binary,
        timeout=args.timeout,
        activation_prompt=args.activation_prompt,
        inherit_home=args.inherit_home,
        keep_runtime=args.keep_runtime,
        npx_bootstrap=args.npx_bootstrap,
    )
    print(json.dumps({
        "run_id": result["run_id"],
        "host": result["host_id"],
        "outcome": result["outcome"],
        "blocker": result.get("blocker"),
        "promoted_to_host_smoke": result.get("promoted_to_host_smoke", False),
    }, indent=2))
    if result["outcome"] == "PASS":
        raise SystemExit(0)
    if str(result["outcome"]).startswith("BLOCKED_"):
        raise SystemExit(10)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
