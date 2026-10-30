# Apply Windows Git fix — GAS Engineering v2.0.0

This maintenance patch keeps the 16 GAS skills unchanged and fixes Git for Windows `lstat(...): Filename too long` caused by deeply nested generated `dist/` files.

## Existing local Git repository

1. Extract `gas-v2.0.0-windows-git-patch.zip` **into the repository root** (where `.gitignore`, `README.md`, and `tools/` exist). Overwrite matching files.
2. Open Git Bash / PowerShell from the repository root and run:

```bash
git config --local core.longpaths true
git rm -r --cached --ignore-unmatch dist
git add -A
git status --short
git commit -m "fix: untrack generated GAS dist and preserve skill release"
git push -u origin HEAD
```

The `git rm --cached` operation untracks generated files **without deleting them from your drive**. The `.gitignore` prevents `dist/` from being re-added. An empty `git rm` result is harmless if no `dist/` file was staged. If you still encounter an OS path problem, put the repository in a short root such as `C:\gas-playbook`, then repeat the commands.

**Do not** run `git rm -r dist` without `--cached`; that would remove files from the working tree.

## New Git repository or clone

Use the full Windows-friendly ZIP. It contains no expanded generated `dist/` files, so `git add -A` should not encounter deeply nested paths. The ready-to-install artifact is `releases/v2.0.0/gas-engineering.skill`.

To regenerate `dist/` locally (optional):

```bash
python tools/gas_skill_packager.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
```

Do not stage `dist/` afterward. CI rebuilds and validates the generated distribution automatically.
