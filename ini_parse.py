import sys, json, argparse, configparser, io

def main():
    p = argparse.ArgumentParser(description="INI parser")
    sub = p.add_subparsers(dest="cmd")
    r = sub.add_parser("read")
    r.add_argument("file")
    r.add_argument("-s", "--section")
    r.add_argument("-k", "--key")
    sub.add_parser("to-json").add_argument("file")
    w = sub.add_parser("set")
    w.add_argument("file"); w.add_argument("section"); w.add_argument("key"); w.add_argument("value")
    args = p.parse_args()
    if args.cmd == "read":
        cp = configparser.ConfigParser()
        cp.read(args.file)
        if args.section and args.key:
            print(cp.get(args.section, args.key))
        elif args.section:
            for k, v in cp.items(args.section): print(f"{k} = {v}")
        else:
            for sec in cp.sections():
                print(f"[{sec}]")
                for k, v in cp.items(sec): print(f"  {k} = {v}")
    elif args.cmd == "to-json":
        cp = configparser.ConfigParser()
        cp.read(args.file)
        d = {s: dict(cp.items(s)) for s in cp.sections()}
        print(json.dumps(d, indent=2))
    elif args.cmd == "set":
        cp = configparser.ConfigParser()
        cp.read(args.file)
        if not cp.has_section(args.section): cp.add_section(args.section)
        cp.set(args.section, args.key, args.value)
        with open(args.file, "w") as f: cp.write(f)
        print(f"Set [{args.section}] {args.key} = {args.value}")
    else:
        p.print_help()

if __name__ == "__main__":
    main()
