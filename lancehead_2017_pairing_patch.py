#!/usr/bin/env python3
"""Reproduce a narrowly scoped Lancehead 2017 ID-remapping test from EXTRACTED
Razer Lancehead Wireless Pairing Utility v1.00.00 r6 files.

The user must obtain the original r6 software from Razer and expand it themselves.
This script does not download, execute or redistribute Razer software, and does
not flash firmware. Its generated EXE is unofficial and untrusted; use at own risk.

Usage: python lancehead_2017_pairing_patch.py <extracted_r6_folder> <output_folder>
"""
import hashlib
import shutil
import sys
from pathlib import Path

EXPECTED = {
    'LanceheadWirelessPairingUtility.exe': '4c81719693e246ff07f9067ab71af3a6237ded7a963b1fb135b6d19c3805e304',
    'DeviceUpdater.resources': '11b32d6502be305762c95f336d7c4223a356ab14a2a2c397e33b966e02bba4d1',
}
# Exact byte offsets. Matching ASCII values are within the source's .NET UTF-16
# string fields in the .exe and two metadata entries in the .resources file.
PATCHES = {
    'LanceheadWirelessPairingUtility.exe': [
        (0xF416, 0x36, 0x35), (0xF418, 0x46, 0x41),  # 006F -> 005A
        (0xF548, 0x37, 0x35), (0xF54A, 0x30, 0x39),  # 0070 -> 0059
    ],
    'DeviceUpdater.resources': [
        (0x4F57B, 0x36, 0x35), (0x4F57C, 0x46, 0x41),
        (0x4F581, 0x37, 0x35), (0x4F582, 0x30, 0x39),
        (0xA0236, 0x36, 0x35), (0xA0237, 0x46, 0x41),
        (0xA023C, 0x37, 0x35), (0xA023D, 0x30, 0x39),
    ],
}
EXPECTED_OUTPUT = {
    'LanceheadWirelessPairingUtility.exe': '5e1b481b51e224849aaa7216767fb2b660aa967d642a56eb8277b0bd19a22b6e',
    'DeviceUpdater.resources': '60f6bf3f1bd77303fd131bd81480190da8036cc69824fb6a49e24e0633b6ec42',
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: python lancehead_2017_pairing_patch.py <extracted_r6_folder> <output_folder>')
    source = Path(sys.argv[1]).resolve()
    dest = Path(sys.argv[2]).resolve()
    if not source.is_dir():
        sys.exit('Input must be an existing directory of extracted official r6 files.')
    if dest.exists():
        sys.exit('Output directory already exists; refusing to overwrite it.')
    if source == dest or source in dest.parents:
        sys.exit('Output directory must not be inside the input directory.')

    # Complete validation and in-memory patching BEFORE creating an output folder.
    patched = {}
    for filename, expected_digest in EXPECTED.items():
        original = (source / filename).read_bytes()
        if sha256(original) != expected_digest:
            sys.exit(f'{filename}: unrecognized source file; SHA-256 mismatch. Aborting.')
        data = bytearray(original)
        for off, old, new in PATCHES[filename]:
            if data[off] != old:
                sys.exit(f'{filename}: unexpected byte at 0x{off:X}. Aborting.')
            data[off] = new
        if sha256(data) != EXPECTED_OUTPUT[filename]:
            sys.exit(f'{filename}: patched SHA-256 mismatch. Aborting.')
        patched[filename] = data

    # Preserve all other files including the DLL and original firmware data.
    shutil.copytree(source, dest)
    for filename, data in patched.items():
        (dest / filename).write_bytes(data)
        print(f'{filename}: patched and validated: {sha256(data)}')
    print(f'Output: {dest}')
    print('CAUTION: Unofficial binary; do not use for firmware updates or distribute executables.')


if __name__ == '__main__':
    main()
