#!/usr/bin/env python3
"""ini_parse - INI file parser without configparser."""
import sys, json, re

def parse_ini(text):
    result = {}; section = "DEFAULT"
    result[section] = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith(("#", ";")): continue
        m = re.match(r"\[(.+?)\]", line)
        if m:
            section = m.group(1); result.setdefault(section, {}); continue
        if "=" in line:
            k, v = line.split("=", 1)
            result[section][k.strip()] = v.strip()
        elif ":" in line:
            k, v = line.split(":", 1)
            result[section][k.strip()] = v.strip()
    if not result["DEFAULT"]: del result["DEFAULT"]
    return result

def to_ini(data):
    lines = []
    for sec, kvs in data.items():
        lines.append(f"[{sec}]")
        for k, v in kvs.items():
            lines.append(f"{k} = {v}")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ini_parse.py <parse|generate> [file]"); sys.exit(1)
    if sys.argv[1] == "parse":
        text = open(sys.argv[2]).read() if len(sys.argv) > 2 else sys.stdin.read()
        print(json.dumps(parse_ini(text), indent=2))
    elif sys.argv[1] == "generate":
        data = json.load(sys.stdin)
        print(to_ini(data))
