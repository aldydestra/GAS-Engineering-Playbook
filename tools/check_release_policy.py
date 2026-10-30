#!/usr/bin/env python3
"""Validate the stable v2 archive freeze and optional SemVer release intent.

This utility NEVER creates a tag, publishes a release, or changes a version.
It verifies repository policy and the immutable stable artifact independently
of in-progress development builds in dist/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def parse_version(value: str) -> tuple[int, int, int]:
    match = SEMVER.fullmatch(value)
    if not match:
        raise ValueError('expected stable MAJOR.MINOR.PATCH (no v prefix or prerelease)')
    return tuple(map(int, match.groups()))


def classify_candidate(stable: str, candidate: str, change: str) -> bool:
    """SemVer intent check, not a decision to publish."""
    old = parse_version(stable)
    new = parse_version(candidate)
    if change == 'major':
        return new[0] > old[0] and new[1:] == (0, 0)
    if change == 'minor':
        return new[0] == old[0] and new[1] > old[1] and new[2] == 0
    if change == 'patch':
        return new[:2] == old[:2] and new[2] > old[2]
    raise ValueError('change must be major, minor, or patch')


def validate(root: Path, candidate_version: str | None = None,
             change: str | None = None, check_git: bool = True) -> list[str]:
    problems: list[str] = []
    cfg = root / 'packaging/release-policy.json'
    try:
        policy = json.loads(cfg.read_text(encoding='utf-8'))
        stable = policy['stable_release']
        version = stable['version']
        parse_version(version)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f'invalid release policy: {exc}']

    if policy.get('product') != 'gas-engineering' or policy.get('scope') != 'Google Apps Script and Google Workspace engineering skill':
        problems.append('release policy must remain GAS-only')
    if policy.get('schema_version') != 1:
        problems.append('unknown release-policy schema')
    if len(policy.get('roadmap', [])) != 4:
        problems.append('expected four explicit GAS milestone checkpoints')
    stages = policy.get('roadmap', [])
    for i, rec in enumerate(stages, 1):
        expected = f'{version.split(".")[0]}.{i}.0'
        if rec.get('milestone') != expected or rec.get('stage') not in {'planned', 'in_development', 'candidate', 'released'}:
            problems.append(f'invalid roadmap milestone {i}: expected {expected}')

    if policy.get('development', {}).get('commits_are_releases') is not False:
        problems.append('development commits must not auto-publish GitHub releases')
    if policy.get('development', {}).get('generated_dist_tracked') is not False:
        problems.append('generated dist must remain untracked')
    if '/dist/' not in (root / '.gitignore').read_text(encoding='utf-8').splitlines():
        problems.append('missing /dist/ ignore needed for Windows Git')
    if policy.get('release_requirements', {}).get('specialist_count') != 16:
        problems.append('16 specialist baseline missing')
    if policy.get('release_requirements', {}).get('six_task_families') != 6:
        problems.append('six task families baseline missing')
    for f in ('docs/release-policy.md', 'docs/v2-roadmap.md', 'CONTRIBUTING.md'):
        if not (root / f).is_file():
            problems.append('required policy/documentation missing: ' + f)

    expected_path = f'releases/v{version}/gas-engineering.skill'
    if stable.get('artifact') != expected_path:
        problems.append('release artifact path must match its immutable version')
    archive_path = root / stable.get('artifact', '')
    expected_hash = stable.get('sha256', '')
    if not re.fullmatch(r'[0-9a-f]{64}', expected_hash):
        problems.append('invalid pinned SHA256')
    if not archive_path.is_file():
        problems.append('immutable stable release archive missing')
    elif hashlib.sha256(archive_path.read_bytes()).hexdigest() != expected_hash:
        problems.append('immutable stable release archive changed: refuse overwrite')

    sums_path = root / stable.get('checksum_file', '')
    if stable.get('checksum_file') != f'releases/v{version}/SHA256SUMS':
        problems.append('stable checksum path must match the version')
    if not sums_path.is_file() or sums_path.read_text(encoding='utf-8') != f'{expected_hash}  gas-engineering.skill\n':
        problems.append('stable release checksum file changed')

    # A repository may have a .git directory OR a worktree .git file.
    if check_git and (root / '.git').exists():
        try:
            result = subprocess.run(['git', 'ls-files', '--', 'dist'], cwd=root,
                                    text=True, capture_output=True, check=True)
            if result.stdout.strip():
                problems.append('generated dist is tracked in Git; remove with git rm --cached')
        except (OSError, subprocess.CalledProcessError):
            problems.append('unable to inspect tracked dist paths')

    if (candidate_version is None) != (change is None):
        problems.append('candidate-version and change must be given together')
    if candidate_version is not None and change is not None:
        try:
            if not classify_candidate(version, candidate_version, change):
                problems.append(f'{change} candidate {candidate_version} is incompatible with stable {version}')
        except ValueError as exc:
            problems.append(f'invalid candidate version: {exc}')
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--candidate-version')
    parser.add_argument('--change', choices=['major', 'minor', 'patch'])
    args = parser.parse_args()
    problems = validate(args.root, args.candidate_version, args.change)
    if problems:
        for problem in problems:
            print('FAIL:', problem)
        return 2
    print('PASS: frozen stable release integrity + GAS development policy')
    if args.candidate_version:
        print(f'PASS: {args.candidate_version} classified {args.change}; NOT a published release or readiness claim')
    else:
        print('STATUS: DEVELOPMENT — stable v2.0.0 unchanged; no release published')
    return 0


if __name__ == '__main__':
    sys.exit(main())
