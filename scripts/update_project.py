#!/usr/bin/env python3
import json,sys
from datetime import datetime,timezone
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"data/projects.json"
d=json.loads(p.read_text(encoding="utf-8"))
if len(sys.argv)<4: raise SystemExit("update_project.py <id> <field> <value>")
i,f,v=sys.argv[1],sys.argv[2]," ".join(sys.argv[3:])
x=next((q for q in d["projects"] if q["id"]==i),None)
if not x: raise SystemExit("project not found")
if f in {"mvp","prod"}: v=max(0,min(100,int(v)))
elif f=="pinned": v=v.lower() in {"1","true","yes","да"}
x[f]=v;x["lastActivity"]=datetime.now(timezone.utc).isoformat();d["generatedAt"]=datetime.now(timezone.utc).isoformat();d["source"]="update_project.py"
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
print("updated",i,f,v)
