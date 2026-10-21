"""Disable PT_GNU_RELRO in the prebuilt ZKTeco arm64 libraries.

The vendor .so files were built with GCC 4.9 (NDK <= r17). Their LOAD segments
are already 64 KB aligned, but the GNU_RELRO segment ends on a 4 KB boundary.
On 16 KB page devices the dynamic linker rounds the RELRO end up to 16 KB when
calling mprotect(), which makes part of .data read-only -> SIGSEGV on write.

Rewriting the RELRO program header type to PT_NULL stops the linker from
applying that mprotect. Offsets and sizes are untouched (4 bytes per file).

Usage: python tool/patch_relro.py [--check] [lib_dir]
"""

import glob
import hashlib
import os
import struct
import sys

PT_NULL = 0
PT_LOAD = 1
PT_GNU_RELRO = 0x6474E552
PAGE_16K = 0x4000


def program_headers(data):
    if data[:4] != b"\x7fELF" or data[4] != 2 or data[5] != 1:
        raise ValueError("not a 64-bit little-endian ELF")
    phoff = struct.unpack_from("<Q", data, 0x20)[0]
    phentsize, phnum = struct.unpack_from("<HH", data, 0x36)
    for i in range(phnum):
        off = phoff + i * phentsize
        p_type, _, _, vaddr, _, _, memsz, align = struct.unpack_from(
            "<IIQQQQQQ", data, off
        )
        yield off, p_type, vaddr, memsz, align


def describe(path, data):
    loads = []
    relro = None
    for _, p_type, vaddr, memsz, align in program_headers(data):
        if p_type == PT_LOAD:
            loads.append(align)
        elif p_type == PT_GNU_RELRO:
            relro = vaddr + memsz
    status = "none" if relro is None else (
        "ok" if relro % PAGE_16K == 0 else "end 0x%x not 16K aligned" % relro
    )
    load_ok = all(a >= PAGE_16K for a in loads)
    print(
        "%-22s LOAD align %s (%s)  RELRO %s"
        % (
            os.path.basename(path),
            ",".join(hex(a) for a in loads),
            "ok" if load_ok else "BAD",
            status,
        )
    )
    return load_ok and status != "ok" and status != "none"


def patch(path):
    with open(path, "rb") as f:
        data = bytearray(f.read())
    before = hashlib.sha256(data).hexdigest()
    patched = False
    for off, p_type, *_ in list(program_headers(data)):
        if p_type == PT_GNU_RELRO:
            struct.pack_into("<I", data, off, PT_NULL)
            patched = True
    if patched:
        with open(path, "wb") as f:
            f.write(data)
        print("patched %s\n  sha256 %s -> %s" % (
            os.path.basename(path), before, hashlib.sha256(data).hexdigest()))
    return patched


def main():
    args = sys.argv[1:]
    check_only = "--check" in args
    args = [a for a in args if a != "--check"]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_dir = args[0] if args else os.path.join(root, "android", "libs", "arm64-v8a")

    libs = sorted(glob.glob(os.path.join(lib_dir, "*.so")))
    if not libs:
        sys.exit("no .so files in %s" % lib_dir)

    unsafe = [p for p in libs if describe(p, open(p, "rb").read())]
    if check_only:
        sys.exit(1 if unsafe else 0)
    for p in unsafe:
        patch(p)
    for p in libs:
        describe(p, open(p, "rb").read())


if __name__ == "__main__":
    main()
