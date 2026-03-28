#!/usr/bin/env python3
"""INI file parser and editor without configparser."""
import sys, re, json

def parse(text):
    sections = {}; current = 'DEFAULT'
    for line in text.split('\n'):
        line = line.strip()
        if not line or line.startswith(('#', ';')): continue
        m = re.match(r'\[(.+)\]', line)
        if m: current = m.group(1); sections.setdefault(current, {}); continue
        if '=' in line:
            k, v = line.split('=', 1)
            sections.setdefault(current, {})[k.strip()] = v.strip()
    return sections

def to_ini(sections):
    lines = []
    for section, kvs in sections.items():
        if section != 'DEFAULT': lines.append(f'[{section}]')
        for k, v in kvs.items(): lines.append(f'{k} = {v}')
        lines.append('')
    return '\n'.join(lines)

def get_value(sections, path):
    parts = path.split('.')
    if len(parts) == 2: return sections.get(parts[0], {}).get(parts[1])
    return sections.get('DEFAULT', {}).get(parts[0])

if __name__ == '__main__':
    if len(sys.argv) < 2: print("Usage: ini_parse.py <file.ini> [get section.key | set section.key value | json]"); sys.exit(1)
    text = open(sys.argv[1]).read()
    sections = parse(text)
    if len(sys.argv) == 2 or sys.argv[2] == 'json':
        print(json.dumps(sections, indent=2))
    elif sys.argv[2] == 'get':
        print(get_value(sections, sys.argv[3]))
    elif sys.argv[2] == 'set':
        parts = sys.argv[3].split('.')
        sections.setdefault(parts[0], {})[parts[1]] = ' '.join(sys.argv[4:])
        open(sys.argv[1], 'w').write(to_ini(sections))
        print(f"Set {sys.argv[3]} = {' '.join(sys.argv[4:])}")
