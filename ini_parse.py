#!/usr/bin/env python3
"""ini_parse: INI file parser and writer."""
import sys, re

def parse(text):
    result = {}
    current_section = None
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        m = re.match(r"^\[(.+?)\]$", line)
        if m:
            current_section = m.group(1)
            result.setdefault(current_section, {})
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            # Remove inline comments
            for comment_char in (";", "#"):
                if comment_char in val:
                    # Only if not inside quotes
                    if not (val.startswith('"') and val.endswith('"')):
                        val = val[:val.index(comment_char)].strip()
            # Remove quotes
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            if current_section:
                result[current_section][key] = val
            else:
                result.setdefault("DEFAULT", {})[key] = val

    return result

def format_ini(data):
    lines = []
    for section, kvs in data.items():
        lines.append(f"[{section}]")
        for k, v in kvs.items():
            if " " in str(v) or ";" in str(v):
                lines.append(f'{k} = "{v}"')
            else:
                lines.append(f"{k} = {v}")
        lines.append("")
    return "\n".join(lines)

def get(data, section, key, default=None):
    return data.get(section, {}).get(key, default)

def test():
    text = """
[database]
host = localhost
port = 5432
name = mydb

[server]
debug = true
workers = 4
path = "/usr/local/bin"

# Comment
[auth]
secret = my-secret ; inline comment
"""
    r = parse(text)
    assert r["database"]["host"] == "localhost"
    assert r["database"]["port"] == "5432"
    assert r["server"]["debug"] == "true"
    assert r["server"]["path"] == "/usr/local/bin"
    assert r["auth"]["secret"] == "my-secret"
    assert get(r, "database", "host") == "localhost"
    assert get(r, "missing", "key", "default") == "default"
    # Roundtrip
    formatted = format_ini(r)
    assert "[database]" in formatted
    assert "host = localhost" in formatted
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: ini_parse.py test")
