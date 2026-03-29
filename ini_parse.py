#!/usr/bin/env python3
"""ini_parse - INI file parser and writer."""
import sys

def parse_ini(text):
    sections = {}
    current = ""
    sections[current] = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1].strip()
            if current not in sections:
                sections[current] = {}
        elif "=" in line:
            key, val = line.split("=", 1)
            sections[current][key.strip()] = val.strip()
    if not sections.get("", {}):
        del sections[""]
    return sections

def to_ini(sections):
    lines = []
    if "" in sections:
        for k, v in sections[""].items():
            lines.append(f"{k} = {v}")
        lines.append("")
    for section, values in sections.items():
        if section == "":
            continue
        lines.append(f"[{section}]")
        for k, v in values.items():
            lines.append(f"{k} = {v}")
        lines.append("")
    return "\n".join(lines).rstrip()

def get_typed(sections, section, key, default=None):
    val = sections.get(section, {}).get(key)
    if val is None:
        return default
    if val.lower() in ("true", "yes", "on"): return True
    if val.lower() in ("false", "no", "off"): return False
    try: return int(val)
    except ValueError:
        try: return float(val)
        except ValueError: return val

def test():
    ini = """
[database]
host = localhost
port = 5432
name = mydb

[app]
debug = true
workers = 4
; comment
"""
    sections = parse_ini(ini)
    assert "database" in sections
    assert sections["database"]["host"] == "localhost"
    assert sections["database"]["port"] == "5432"
    assert sections["app"]["debug"] == "true"
    assert get_typed(sections, "database", "port") == 5432
    assert get_typed(sections, "app", "debug") == True
    assert get_typed(sections, "app", "workers") == 4
    assert get_typed(sections, "app", "missing", "default") == "default"
    output = to_ini(sections)
    reparsed = parse_ini(output)
    assert reparsed["database"]["host"] == "localhost"
    assert reparsed["app"]["workers"] == "4"
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("ini_parse: INI parser. Use --test")
