#!/usr/bin/env python3
"""Tests for skill files: links, linter paths and manifests."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
LINK_RX = re.compile(r"\]\(([^)#\s]+)\)")
COMMAND_RX = re.compile(r"python3 ([\w./-]+\.py)")

docs = sorted(SKILLS.rglob("*.md"))
assert docs, "no Markdown files under skills/"

for doc in docs:
    for target in LINK_RX.findall(doc.read_text(encoding="utf-8")):
        if "://" not in target:
            assert (doc.parent / target).is_file(), f"{doc.relative_to(ROOT)}: broken link {target}"
print("OK   relative links in skill files resolve")

for doc in docs:
    skill_dir = SKILLS / doc.relative_to(SKILLS).parts[0]
    for script in COMMAND_RX.findall(doc.read_text(encoding="utf-8")):
        assert (skill_dir / script).is_file(), f"{doc.relative_to(ROOT)}: {script} not found from {skill_dir.name}/"
print("OK   linter paths resolve from the skill directory")

for skill in ("plain-talk", "tech-doc"):
    head = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
    assert re.search(rf"^name: {skill}$", head, re.M), skill
    assert "description:" in head, skill
    assert (SKILLS / skill / "agents" / "openai.yaml").is_file(), skill
print("OK   each skill has frontmatter and Codex metadata")

manifests = {
    name: json.loads((ROOT / name).read_text(encoding="utf-8"))
    for name in (
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        ".codex-plugin/plugin.json",
        ".agents/plugins/marketplace.json",
    )
}
claude, market, codex, codex_market = manifests.values()
assert claude["name"] == codex["name"] == market["plugins"][0]["name"] == codex_market["plugins"][0]["name"]
assert claude["version"] == codex["version"] == market["plugins"][0]["version"] == market["metadata"]["version"]
assert (ROOT / codex["skills"]).is_dir()
print("OK   plugin manifests agree on name and version")

print("\nAll skill path tests passed.")
