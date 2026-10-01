#!/usr/bin/env python3
"""Re-derive risk_level from risk_score in care_ai_output.json so labels match the dashboard bands.
Bands (score): High >= 70, Medium 45-69, Low < 45.
Usage: python fix_levels.py care_ai_output.json            # writes care_ai_output.fixed.json + prints a report
       python fix_levels.py in.json out.json
"""
import json, sys

def band(score):
    s = float(score)
    return "High" if s >= 70 else "Medium" if s >= 45 else "Low"

src = sys.argv[1] if len(sys.argv) > 1 else "care_ai_output.json"
dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".json", ".fixed.json")
data = json.load(open(src, encoding="utf-8"))

changes = 0
def fix(rec, where):
    global changes
    new = band(rec["risk_score"])
    if rec.get("risk_level") != new:
        print(f"{where}: {rec.get('risk_level')} -> {new}  (score {rec['risk_score']})")
        rec["risk_level"] = new
        changes += 1

for dname, d in data["districts"].items():
    fix(d, dname)
    for c in d.get("communities", []):
        fix(c, f"{dname} / {c['name']}")

json.dump(data, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n{changes} label(s) corrected -> {dst}")
