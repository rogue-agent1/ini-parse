#!/usr/bin/env python3
"""ini_parse - INI parser and editor."""
import sys, argparse, json, configparser, io

def parse_ini(text):
    cp = configparser.ConfigParser()
    cp.read_string(text)
    result = {}
    for section in cp.sections():
        result[section] = dict(cp[section])
    if cp.defaults():
        result["DEFAULT"] = dict(cp.defaults())
    return result

def main():
    p = argparse.ArgumentParser(description="INI parser")
    p.add_argument("file", help="INI file path")
    p.add_argument("--get", help="section.key to get")
    p.add_argument("--set", help="section.key=value to set")
    p.add_argument("--sections", action="store_true")
    args = p.parse_args()
    with open(args.file) as f: text = f.read()
    data = parse_ini(text)
    if args.get:
        sec, key = args.get.rsplit(".", 1)
        print(json.dumps({"key": args.get, "value": data.get(sec, {}).get(key)}))
    elif args.set:
        path, val = args.set.split("=", 1)
        sec, key = path.rsplit(".", 1)
        cp = configparser.ConfigParser()
        cp.read_string(text)
        if not cp.has_section(sec): cp.add_section(sec)
        cp.set(sec, key, val)
        buf = io.StringIO()
        cp.write(buf)
        with open(args.file, "w") as f: f.write(buf.getvalue())
        print(json.dumps({"updated": path, "value": val}))
    elif args.sections:
        print(json.dumps({"sections": list(data.keys())}))
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__": main()
