"""
Criterion 4: every appeal changes status and is recorded.

run_eval.py only sends text, and an appeal needs a content_id from a real
submission first, so this does both: 10 submissions, then 10 appeals against
the ids that came back, three trials. For each appeal it checks the response
says under_review AND the log holds an appeal entry with that content_id and
a timestamp.

    python app.py                            # in one terminal
    python appeal_eval.py --label before     # in another
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import requests

URL = "http://127.0.0.1:5000"
TEXT = ("Regular exercise is important for maintaining good health. It helps to "
        "strengthen the heart and improve overall fitness.")


def trial(n: int) -> dict:
    rows = []
    for i in range(1, 11):
        sub = requests.post(f"{URL}/submit", json={"text": TEXT, "creator_id": f"eval_appeal_{i}"}).json()
        cid = sub.get("content_id")
        resp = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": f"Trial {n}: I wrote this myself."})
        body = resp.json()
        logged = [e for e in requests.get(f"{URL}/log").json()["entries"]
                  if e.get("content_id") == cid and e.get("event") == "appeal" and e.get("timestamp")]
        ok = resp.status_code == 200 and body.get("status") == "under_review" and len(logged) == 1
        rows.append({"content_id": cid, "status_code": resp.status_code, "response": body,
                     "log_entry": logged[0] if logged else None, "pass": ok})
    return {"trial": n, "passed": sum(r["pass"] for r in rows), "of": len(rows), "rows": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="run")
    args = parser.parse_args()

    trials = [trial(n) for n in (1, 2, 3)]
    for t in trials:
        print(f"trial {t['trial']}: {t['passed']}/{t['of']} appeals changed status and were logged")

    out = Path("results") / f"appeal_eval_{datetime.now():%Y-%m-%d_%H%M}_{args.label}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(trials, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
