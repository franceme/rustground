#!/usr/bin/env python3
import argparse, os, sys, requests

def base(url,args,verify:bool=True):
    print(url)
    try:
        resp = requests.post(f"https://play.rust-lang.org/{url}", json=args, verify=verify).json()
        print(resp)
        return {
            'Response':resp['success'],
            'Code':None if 'code' not in resp else resp['code'],
            'StdOut':resp['stdout'],
            'StdErr':resp['stderr']
        }
    except Exception as e:
        return {
            'Response':False,
            'Code':None,
            'StdOut':None,
            'StdErr':e
        }

def base_resp(resp):
    return f"""Status: {resp['Response']}
{resp['Code']}
============
STDOUT:> {resp['StdOut']}
STDERR:> {resp['StdErr']}"""

execute = lambda contents,verify=True: base("execute", {
    "channel": "stable",
    "mode": "debug",
    "edition": "2021",
    "crateType": "bin",
    "tests": False,
    "code": '\n'.join(contents),
    "backtrace": False
}, verify)
compile = lambda contents,format,verify=True: base("compile", {
    "channel": "nightly",
    "mode": "debug",
    "edition": "2021",
    "crateType": "bin",
    "tests": False,
    "code": '\n'.join(contents),
    "target": format,
    "assemblyFlavor": "att",
    "demangleAssembly": "demangle",
    "processAssembly": "filter",
    "backtrace": False
}, verify)
tools = lambda contents, tool, verify=True: base(tool,{
    "edition": "2021",
    "code": '\n'.join(contents),
    "crateType": "bin"
},verify)

def save(filecontents):
    try:
        resp = requests.post("https://play.rust-lang.org/meta/gist", json={
            "code": '\n'.join(filecontents),
        }).json()
        return {
            'Response':True,
            'PlaygroundID':"https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=" + resp['id'],
            'GistID':resp['url'],
            'Message':None
        }
    except Exception as e:
        return {
            'Response':False,
            'PlaygroundID':None,
            'GistID':None,
            'Message':e
        }


def main():
    parser, output = argparse.ArgumentParser("RustGround - Upload Contents of Rust files to the Rust playground, and grab their output"),""
    parser.add_argument("-f","--file", help="The Rust file to be used", nargs=1, default=None)
    parser.add_argument("-n","--no-execute", help="Don't compile the Rust code", action="store_true")
    parser.add_argument("--hir", help="Show the Mir Output", action="store_true")
    parser.add_argument("--mir", help="Show the Hir Output", action="store_true")
    parser.add_argument("--asm", help="Show the ASM Output", action="store_true")
    parser.add_argument("--llvm", help="Show the LLVM Output", action="store_true")
    parser.add_argument("--wasm", help="Show the WASM Output", action="store_true")
    parser.add_argument("--save", help="Save the Rust PlayGround", action="store_true")
    parser.add_argument("--format", help="Format the code", action="store_true")
    parser.add_argument("--clippy", help="Run Clippy on the code", action="store_true")
    parser.add_argument("--miri", help="Get the Miri output", action="store_true")
    parser.add_argument("--macro", help="Expand the macros", action="store_true")

    args = parser.parse_args()

    foil = args.file[0]

    if foil and os.path.exists(foil) and foil.endswith('.rs'):
        with open(foil, 'r') as reader:
            contents = reader.readlines()

        if not args.file:
            output += base_resp(execute(contents))

        if args.hir:
            output += "\n" + base_resp(compile(contents,"hir"))
        if args.mir:
            output += "\n" + base_resp(compile(contents,"mir"))
        if args.asm:
            output += "\n" + base_resp(compile(contents,"asm"))
        if args.llvm:
            output += "\n" + base_resp(compile(contents,"llvm-ir"))
        if args.wasm:
            output += "\n" + base_resp(compile(contents,"wasm"))
        if args.save:
            output += "\n" + save(contents)
        if args.format:
            output += "\n" + base_resp(tools(contents, 'format'))
        if args.clippy:
            output += "\n" + base_resp(tools(contents, 'clippy'))
        if args.miri:
            output += "\n" + base_resp(tools(contents, 'miri'))
        if args.macro:
            output += "\n" + base_resp(tools(contents, 'macro-expansion'))

    print(output)

if __name__ == '__main__':
    main()
