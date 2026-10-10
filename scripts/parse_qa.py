#!/usr/bin/env python3
"""解析标准 Q/A 单行标记的问答 Markdown 文档，输出成对结构。

用法：
    python parse_qa.py <input.md>

仅支持标准格式：
    Q
    问题内容……
    A
    答案内容（可多行）……
"""
import sys


def parse_qa(text: str):
    """解析 Q/A 成对结构，返回 (header_lines, qa_pairs)。

    qa_pairs 为 [(question, answer), ...]，question/answer 为字符串。
    """
    lines = text.splitlines()
    header = []
    qa_pairs = []
    i = 0
    n = len(lines)

    # 收集顶部标题/来源信息（在第一个 Q 标记之前的非空行）
    while i < n:
        stripped = lines[i].strip()
        if stripped == "Q":
            break
        if stripped:
            header.append(lines[i])
        i += 1

    question = None
    answer_lines = []

    def flush():
        nonlocal question, answer_lines
        if question is not None:
            answer = "\n".join(answer_lines).strip()
            qa_pairs.append((question.strip(), answer))
        question = None
        answer_lines = []

    while i < n:
        stripped = lines[i].strip()
        if stripped == "Q":
            flush()
            question = ""
            i += 1
            continue
        if stripped == "A":
            i += 1
            continue
        # 正文行
        if question is None:
            # 在 Q 之前出现的非标题正文，跳过
            i += 1
            continue
        # 判断当前正文属于问题还是答案：若 answer_lines 为空且 question 为空 → 问题行
        if question == "" and not answer_lines:
            question = lines[i]
        else:
            answer_lines.append(lines[i])
        i += 1

    flush()
    return header, qa_pairs


def main():
    if len(sys.argv) < 2:
        print("用法: python parse_qa.py <input.md>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()

    header, qa_pairs = parse_qa(text)

    print("=== 标题/来源 ===")
    for line in header:
        print(line)
    print(f"\n=== 共 {len(qa_pairs)} 对问答 ===\n")
    for idx, (q, a) in enumerate(qa_pairs, 1):
        print(f"[{idx}] Q: {q}")
        print(f"    A: {a[:80]}{'...' if len(a) > 80 else ''}")
        print()


if __name__ == "__main__":
    main()
