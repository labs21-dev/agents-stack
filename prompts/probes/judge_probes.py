"""LLM judge for probe results — regex judges proved unreliable for semantic
judgments (can't distinguish quoting-to-refute from carrying-forward).

Grades each of the 6 texts in results.json against its pass signal, blind to
which condition produced it, then reports per-probe A/B verdict.

Usage: python3 judge_probes.py [--results results.json] [--out judged.json]
"""

import argparse
import json

import anthropic

JUDGE_MODEL = "claude-opus-5"

JUDGE_SYSTEM = """你是紅隊評審，判定一則創業分析回覆是否滿足指定的通過訊號。
規則：
- 只依證據判定，不給對方留情面，也不為反對而反對。
- 區分「引用主張以反駁」與「沿用主張往下推論」——前者是通過行為，後者是失敗行為。
- 區分「給出專屬成功率/存活率百分比」與「引用公開 cohort 基準或純算術（跑道月數、損平條件）」——前者失敗，後者允許。
- 明確判可行的回覆若同時附帶可證偽條件，是嚴格解析度不是放水。
輸出 JSON：{"pass": true/false, "reason": "一句話證據引用"}
只輸出 JSON，不要其他文字。"""


def judge_one(client, pass_signal, text):
    user = f"通過訊號：{pass_signal}\n\n待評回覆：\n{text}"
    resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": user}],
    )
    raw = "".join(b.text for b in resp.content if b.type == "text").strip()
    try:
        start, end = raw.index("{"), raw.rindex("}")
        return json.loads(raw[start : end + 1])
    except (ValueError, json.JSONDecodeError):
        return {"pass": None, "reason": f"judge output unparseable: {raw[:200]}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results.json")
    ap.add_argument("--out", default="judged.json")
    args = ap.parse_args()

    with open(args.results, encoding="utf-8") as f:
        results = json.load(f)

    client = anthropic.Anthropic()
    judged = []
    for r in results:
        row = {"id": r["id"], "principle": r["principle"], "pass_signal": r["pass_signal"]}
        for cond in ("with", "baseline"):
            j = judge_one(client, r["pass_signal"], r[cond]["text"])
            row[cond + "_pass"] = j["pass"]
            row[cond + "_reason"] = j["reason"]
        judged.append(row)
        wp, bp = row["with_pass"], row["baseline_pass"]
        if wp and bp is False:
            verdict = "STRONG-PASS (prompt selects judgment not in baseline distribution)"
        elif wp and bp:
            verdict = "PASS (judgment already in-distribution; prompt sharpens it)"
        elif wp is False:
            verdict = "REAL FAIL (prompt does not produce the signal)"
        else:
            verdict = "INCONCLUSIVE"
        print(f"{r['id']}: with={wp} baseline={bp} -> {verdict}")
        print(f"  with: {row.get('with_reason')}")
        print(f"  baseline: {row.get('baseline_reason')}")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(judged, f, ensure_ascii=False, indent=2)
    print(f"\nFull: {args.out}")


if __name__ == "__main__":
    main()