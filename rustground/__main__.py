#!/usr/bin/env python3
import argparse, os, sys, requests


def execute(filecontents):
    try:
        if filecontents:
            resp = requests.post("https://play.rust-lang.org/execute", json={
                "channel":"stable",
                "mode":"debug",
                "edition":"2021",
                "crateType":"bin",
                "tests":False,
                "code": '\n'.join(filecontents),
                "backtrace":False
            }).json()
            return f"""Status: {resp['success']}
============
{resp['stdout'] if resp['success'] else resp['stderr']}"""
    except Exception as e:
        return f"""Exception @ {format}:> {e}"""

def compile(filecontents, format:str="hir"):
    try:
        if filecontents:
            resp = requests.post("https://play.rust-lang.org/compile", json={
                "channel":"nightly",
                "mode":"debug",
                "edition":"2021",
                "crateType":"bin",
                "tests":False,
                "code": '\n'.join(filecontents),
                "target":format,
                "assemblyFlavor":"att",
                "demangleAssembly":"demangle",
                "processAssembly":"filter",
                "backtrace":False
            }).json()
            return f"""Status: {resp['success']} @ {format}
============
{resp['code'] if resp['success'] else resp['stderr']}
"""
    except Exception as e:
        return f"""Exception @ {format}:> {e}"""


def main():
    parser, output = argparse.ArgumentParser("RustGround - Upload Contents of Rust files to the Rust playground, and grab their output"),""
    parser.add_argument("-f","--file", help="The Rust file to be used", nargs=1, default=None)
    parser.add_argument("--hir", help="Show the Mir Output", action="store_true")
    parser.add_argument("--mir", help="Show the Hir Output", action="store_true")
    parser.add_argument("--asm", help="Show the ASM Output", action="store_true")
    parser.add_argument("--llvm", help="Show the LLVM Output", action="store_true")
    parser.add_argument("--wasm", help="Show the WASM Output", action="store_true")

    args = parser.parse_args()

    foil = args.file[0]
    if foil and os.path.exists(foil) and foil.endswith('.rs'):
        with open(foil, 'r') as reader:
            contents = reader.readlines()

        output += execute(contents)

        if args.hir:
            output += "\n" + compile(contents,"hir")
        if args.mir:
            output += "\n" + compile(contents,"mir")
        if args.asm:
            output += "\n" + compile(contents,"asm")
        if args.llvm:
            output += "\n" + compile(contents,"llvm-ir")
        if args.wasm:
            output += "\n" + compile(contents,"wasm")
    
    print(output)

if __name__ == '__main__':
    main()