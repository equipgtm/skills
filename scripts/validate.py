"""Validate this public skill checkout without installing or executing its helpers."""
import ast
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "skill-manifest.json").read_text())
skill = root / "skills" / "equipgtm"
expected = set()
for entry in manifest["files"]:
    path = root / "skills" / entry["path"]
    assert path.resolve().is_relative_to(skill), "File outside skill directory"
    data = path.read_bytes()
    assert len(data) == entry["bytes"], f"Size mismatch: {entry['path']}"
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], f"Hash mismatch: {entry['path']}"
    expected.add(path.resolve())
actual = {path.resolve() for path in skill.rglob("*") if path.is_file()}
assert actual == expected, "Unexpected or missing skill files"
assert len(actual) == manifest["fileCount"], "File count mismatch"
text = (skill / "SKILL.md").read_text()
assert text.startswith("---\n") and re.search(r"^name: equipgtm$", text, re.M)
assert re.search(r"^description:", text, re.M)
for path in sorted(actual):
    source = path.read_text()
    assert not re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|/Users/", source), f"Private data pattern: {path.name}"
    if path.suffix == ".py":
        ast.parse(source, filename=path.name)
    if path.suffix == ".md":
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source):
            target = target.split("#", 1)[0]
            if not target or re.match(r"[a-z]+://", target):
                continue
            assert (path.parent / target).resolve() in expected, f"Missing skill reference: {target}"
assert (root / "LICENSE").read_bytes() == (skill / "LICENSE.skill").read_bytes()
print(f"Validated {len(actual)} skill files: hashes, inventory, references and Python syntax.")
