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

def main():
    out = get_output(["irecovery", "-q"])
    # Examples we match:
    #   ECID: 000003C9A8F1234
    #   ECID: 1234567890123456
    m = re.search(r"^ECID:\s*([0-9A-Fa-f]+|\d+)\s*$", out, re.MULTILINE)
    if not m:
        print("Could not find ECID. Is the iPhone in Recovery/DFU and detected by irecovery?")
        print(out.strip())
        sys.exit(1)

    token = m.group(1)
    # Interpret as hex if it contains A–F, otherwise decimal
    base = 16 if re.search(r"[A-Fa-f]", token) else 10
    try:
        ecid_int = int(token, base)
    except ValueError:
        print(f"Unrecognized ECID format: {token}")
        sys.exit(2)

    print(f"ECID (hex): 0x{ecid_int:X}")
    print(f"ECID (dec): {ecid_int}")

if __name__ == "__main__":
    main()
