from pathlib import Path
import base64
import json
import re

root = Path(__file__).resolve().parent
payload = json.loads(base64.b64decode((root / "skild-source-payload.b64").read_text(encoding="ascii")))
assert set(payload) == {"skild-ai.md", "skild-ai-data.json"}
for name, body in payload.items():
    (root / name).write_text(body, encoding="utf-8")
profile = (root / "skild-ai.md").read_text(encoding="utf-8")
data = json.loads((root / "skild-ai-data.json").read_text(encoding="utf-8"))
headings = re.findall(r"^## .+$", profile, re.M)
expected = ["## 1 Funding & valuation", "## 2 Technology", "## 3 Commercial traction", "## 4 Manufacturing & scale", "## 5 Team, partners & risks"]
assert headings == expected, headings
bullets = re.findall(r"^- .+$", profile, re.M)
assert all(re.search(r"\*\([^*]+\)\* (?:\[\d+\])+$", line) for line in bullets)
assert data["company"] == "Skild AI"
assert data["valuation_usd_billion"] == 14 and data["valuation_comparator"] == ">"
assert data["total_capital_usd_billion"] is None
assert data["latest_round_usd_billion"] == 1.4
assert len(data["spot_checks"]) == 3
assert all("2025-10-17" <= check["publication_date"] <= "2026-10-17" for check in data["spot_checks"])
print(json.dumps({"status": "passed", "headings": len(headings), "dated_cited_bullets": len(bullets), "material_spot_checks": len(data["spot_checks"]), "outputs": ["skild-ai.md", "skild-ai-data.json"]}))
