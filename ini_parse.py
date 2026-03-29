#!/usr/bin/env python3
"""INI config file parser."""
import re, sys
class INIParser:
    def __init__(self): self.sections = {"DEFAULT": {}}; self.cur = "DEFAULT"
    def parse(self, text):
        for line in text.split("\n"):
            line = line.strip()
            if not line or line[0] in '#;': continue
            m = re.match(r'\[(.+?)\]', line)
            if m: self.cur = m.group(1); self.sections.setdefault(self.cur, {}); continue
            m = re.match(r'([\w.]+)\s*[=:]\s*(.*)', line)
            if m: self.sections[self.cur][m.group(1)] = m.group(2).strip()
    def get(self, section, key, fb=None): return self.sections.get(section, {}).get(key, fb)
if __name__ == "__main__":
    ini = "[db]\nhost = localhost\nport = 5432\n[server]\nport = 8080"
    p = INIParser(); p.parse(ini)
    print(p.sections)
