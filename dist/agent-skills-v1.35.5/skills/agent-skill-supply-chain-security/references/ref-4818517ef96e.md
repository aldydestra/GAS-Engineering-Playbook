# Code, dependencies, archive safety, source integrity, and signatures



Generated from `skills/18-agent-skill-supply-chain-security/SKILL.md`.



# 40. Dangerous Code

Static code review should identify patterns such as:

- arbitrary `exec`;
- insecure deserialization;
- unsafe temp-file use;
- path traversal;
- command injection;
- unvalidated downloads;
- dynamic import from untrusted path.

Use language-specific AST tools where possible.

---

# 41. Dependency Supply Chain

Review dependency manifests:

```text
npm
pip
uv
cargo
go
system packages
```

Check:

- unexpected packages;
- install scripts;
- git dependencies;
- unpinned URLs;
- typosquatting;
- known CVEs.

---

# 42. Live Vulnerability Lookup

Use current vulnerability databases such as OSV when appropriate.

Offline fallback is useful, but:

```text
offline database age
```

should be visible.

Do not call a dependency clean based on stale vulnerability data.

---

# 43. Package Installation

Review installation behavior:

- package manager invoked?
- global install?
- postinstall scripts?
- network?
- shell?
- elevated privileges?

A skill should not install unrelated tooling silently.

---

# 44. Symlinks

Symlinks can escape the apparent skill root.

During package copy/install:

- resolve/validate targets;
- reject external targets unless explicitly allowed;
- avoid dereferencing untrusted links blindly.

Recent skill installer ecosystems continue to harden symlink handling.

---

# 45. Path Traversal

Validate:

```text
target path
relative path
archive member path
config path
MCP project path
```

against an allowed base.

Reject `../` escape.

---

# 46. Archive Extraction

Use safe extraction.

Reject or isolate:

- absolute paths;
- parent traversal;
- suspicious links;
- malformed archive metadata;
- excessive expansion.

Do not use naive unzip on untrusted skill bundles.

---

# 47. Concealed Executables

Executable content hidden inside document/archive containers is high risk.

Do not execute or unpack into trusted locations automatically.

---

# 48. Installer vs Skill Review

Review both:

```text
skill package
```

and:

```text
installer / CLI used to install it
```

The installer can introduce risks not present in the skill itself.

---

# 49. Source vs Published Artifact

Compare:

```text
reviewed repository revision
```

with:

```text
published package/archive
```

when possible.

A release artifact can differ from source.

---

# 50. Integrity Hash

Record a cryptographic hash of the reviewed release artifact.

Example:

```text
SHA-256
```

This provides local integrity evidence.

It does not establish publisher identity by itself.

---

# 51. Signatures

A detached signature can establish:

```text
this artifact matches what the signer approved
```

when signer trust is established.

Scanning, evaluation, and signing solve different problems:

```text
scan
→ appears safe?

evaluate
→ does it help?

sign
→ is this what was reviewed?
```

---

# 52. Verify Before Install

If a signed artifact is available:

```text
verify signer/certificate
↓
verify signature
↓
verify expected artifact
↓
install
```

Do not verify after installation as the primary control.

---
