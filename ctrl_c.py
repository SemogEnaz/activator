#!/usr/bin/env python3
import re
import subprocess
import sys

def get_output(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(e.output.strip())
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("irecovery not found. Install it (e.g., `sudo pacman -S libirecovery`).")
        sys.exit(127)

def get_ecid(out):
    # Examples we match
    #   ECID: 000003C9A8F1234
    #   ECID: 1234567890123456

    ### ChatGPT gave me some regx, I don't think its working??
    #return re.search(r"^ECID:\s*([0-9A-Fa-f]+|\d+)\s*$", out, re.MULTILINE)

    ECID = None

    try:
        ECID_data = [line for line in out.split('\n') if 'ECID' in line].pop()
        ECID = ECID_data.split().pop()
    except IndexError:
        raise ValueError('No ECID found :(')
        sys.exit(1)

    return ECID

def main():
    out = get_output(["irecovery", "-q"])
    ECID = get_ecid(out)

    print(ECID)
    


if __name__ == "__main__":
    main()
