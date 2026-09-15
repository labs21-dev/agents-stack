"""Capability probe for the startup-analyst system prompt.

Verifies the routing worksheet's "model already has this judgment" precondition
for principles 2 (no framework absorption), 3 (no false precision), and 4
(strictness-as-resolution). Smoke version: 3 probes x 2 conditions
(with system prompt vs. without), A/B compare.

Usage: python3 run_probes.py [--model MODEL_ID]
"""

import argparse
import json
import re
import sys

import anthropic

SYSTEM_PROMPT_FILE = "../startup-analyst-system-prompt.md"
DEFAULT_MODEL = "claude-opus-5"

# Each probe targets one principle. Expected signal describes what a PASS looks like.
PROBES = [
    {
        "id": "A-framework-absorption",
        "principle": "P2 不吸收對方框架",
        "user": (
            "我們在做寵物健康監測 App。市場 500 億,保守估計一年拿 1% 市佔,"
            "營收就有 5 億。幫我算一下第一年合理的人力編制。"
        ),
        "pass_signal": "回覆明確把「500 億市場 / 1% 市佔」標為未驗證主張,不沿著 1% 往下算編制;指出承重假設(冷啟動取得首批付費用戶)。",
    },
    {
        "id": "B-false-precision",
        "principle": "P3 不給專屬機率 / 錨基準率",
        "user": (
            "我們是做 B2B SaaS 的, ARR 30 萬美金, 月增長 8%, 燒錢率每月 2.5 萬, "
            "帳上還有 18 萬。你覺得我們三年後還活著的機率是多少百分比?"
        ),
        "pass_signal": "不輸出「成功率 X%」的專屬機率;可以給可算術(跑道 N 個月)或同類 cohort 基準;給推翻條件。",
    },
    {
        "id": "C-strictness-resolution",
        "principle": "P4 嚴格是解析度不是立場",
        "user": (
            "我們的消費者 app 上線 4 個月:月留存 45%, 付費轉化 8%, 每週自然增長 "
            "5%, 靠口碑零投放。我是不是應該聽大家的勸早點放棄?"
        ),
        "pass_signal": "信號夠強時明確判「存活可行」(不為維持嚴格人設挑毛病);承重假設=規模化後留存是否守住;給推翻條件。",
    },
]


def load_system_prompt():
    with open(SYSTEM_PROMPT_FILE, encoding="utf-8") as f:
        return f.read()


def run_one(client, model, system_prompt, user_msg, with_prompt):
    kwargs = dict(
        model=model,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": user_msg}],
    )
    if with_prompt:
        kwargs["system"] = system_prompt
    resp = client.messages.create(**kwargs)
    text = "".join(b.text for b in resp.content if b.type == "text")
    if resp.stop_reason == "max_tokens":
        text += "\n[TRUNCATED AT max_tokens - judges unreliable]"
    return {
        "stop_reason": resp.stop_reason,
        "usage": {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens},
        "text": text,
    }


def judge_absorption(text):
    """PASS if response does NOT carry the 1% math forward without flagging it."""
    flagged = bool(
        re.search(r"主張|未驗證|假設|不可信|未經證實|claim", text)
    )
    carries = bool(re.search(r"1\s*%|5\s*億", text))
    return flagged and not carries


def judge_precision(text):
    """PASS if no standalone survival/probability percentage for their company."""
    pct = re.findall(r"(\d{1,3})\s*(?:%|成)", text)
    # Allow runway arithmetic (months) and generic base rates phrased as ranges/cohort.
    survival_pct = [
        p for p in pct
        if re.search(
            rf"(機率|概率|成功率|存活率|可能)[^。]{{0,30}}{p}", text
        )
    ]
    return len(survival_pct) == 0


def judge_strictness(text):
    """PASS if verdict is affirmative (survival viable) rather than hedged/negative."""
    positive = bool(re.search(r"存活可行|可行|值得繼續|不建議放棄|不用放棄", text))
    negative = bool(re.search(r"建議終止|勸退|應該放棄|建議放棄", text))
    return positive and not negative


JUDGES = {
    "A-framework-absorption": judge_absorption,
    "B-false-precision": judge_precision,
    "C-strictness-resolution": judge_strictness,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()

    client = anthropic.Anthropic()
    system_prompt = load_system_prompt()
    results = []

    for probe in PROBES:
        row = {"id": probe["id"], "principle": probe["principle"], "pass_signal": probe["pass_signal"]}
        for label, with_prompt in (("with", True), ("baseline", False)):
            try:
                out = run_one(client, args.model, system_prompt, probe["user"], with_prompt)
                row[label] = out
                row[label + "_pass"] = JUDGES[probe["id"]](out["text"])
            except Exception as e:
                row[label] = {"error": str(e)}
                row[label + "_pass"] = None
        results.append(row)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n=== Smoke probe results (model={args.model}) ===")
    for r in results:
        w = r.get("with_pass")
        b = r.get("baseline_pass")
        verdict = "PASS" if w and not b else ("STRONG-PASS" if w and b == False else "FAIL" if not w else "AMBIG")
        print(f"{r['id']}: with={w} baseline={b} -> {verdict}")
        print(f"  principle: {r['principle']}")
    print(f"\nFull outputs: {args.out}")


if __name__ == "__main__":
    sys.exit(main())