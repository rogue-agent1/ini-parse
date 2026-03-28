#!/usr/bin/env python3
"""ini_parse - Parse and query INI/config files."""
import sys, configparser, json
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: ini_parse <file> [section] [key]"); sys.exit(1)
    c = configparser.ConfigParser(); c.read(sys.argv[1])
    if len(sys.argv) == 2:
        for s in c.sections(): print(f"[{s}]"); [print(f"  {k} = {v}") for k, v in c[s].items()]; print()
    elif len(sys.argv) == 3:
        s = sys.argv[2]; [print(f"{k} = {v}") for k, v in c[s].items()]
    else: print(c[sys.argv[2]][sys.argv[3]])
