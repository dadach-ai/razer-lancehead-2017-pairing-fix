# Razer Lancehead 2017 wireless pairing recovery

**Unofficial experimental workaround for the original Razer Lancehead Wireless (RZ01-02120).**

A 2017 Lancehead (`1532:0059` over USB) and its original wireless receiver (`1532:005A`) were correctly detected by Windows, but Razer's published Lancehead Wireless Pairing Utility r4/r6 would not recognize the receiver. This repository documents one successful recovery using a **12-byte, SHA-256-checked modification** of two files from Razer's official r6 utility.

> [!WARNING]
> **Not affiliated with Razer. One confirmed successful pairing, not a universal or risk-free fix.** The experimental utility is built from a package intended for the later 2019 model. Incorrect use could render a mouse or receiver unusable. Never use this modified utility to flash firmware, enter a bootloader, or attempt recovery. You must obtain Razer's original software yourself. No Razer binaries or firmware are supplied here.

## What was tested

| Component | Original 2017 Lancehead | Later 2019 Lancehead |
|---|---|---|
| Model family | `RZ01-02120` | `RZ01-02570` |
| Wired USB PID | `1532:0059` | `1532:0070` |
| Wireless receiver PID | `1532:005A` | `1532:006F` |

**Test environment:** ASUS ROG Strix G15, Windows 11, no Razer Synapse; original RZ01-02120 mouse marked `RC30-021203` and its original non-pairing receiver. The owner had experienced the failure across multiple PCs over several years.

- Both official pairing utilities, **r4** and **r6**, failed to detect either the problematic receiver or a known-working 2017 receiver.
- Patching the program executable only was **not** sufficient.
- Patching **four bytes in the executable and eight in `DeviceUpdater.resources`** enabled receiver recognition and allowed normal mouse pairing.
- The owner subsequently confirmed working wired and wireless functionality.

See the [complete case study](docs/CASE_STUDY.md) for the USB diagnostics, byte offsets, SHA-256 hashes, observations, references, and limitations.

## Reproduce the detection fix (advanced users only)

1. Obtain the original **Lancehead Wireless Pairing Utility v1.00.00 r6** from [Razer's official pairing-utility guide](https://mysupport.razer.com/app/answers/detail/a_id/1506/). Do not use repacked downloads.
2. Extract the downloaded original r6 installer with a suitable archive extractor (for example 7-Zip) to a folder. Locate the extracted files `LanceheadWirelessPairingUtility.exe`, `DeviceUpdater.resources` and `FWUpdaterDLL.dll` together with the application's other files. **Do not attempt to patch the downloaded outer installer directly.**
3. Ensure Python 3 is available. Run this repository's checksum-guarded patcher, passing the folder with the **extracted** files and a new, not-yet-existing output folder:

   ```powershell
   py .\lancehead_2017_pairing_patch.py "C:\path\to\extracted-r6" "C:\path\to\lancehead-2017-test"
   ```

4. The script refuses to run unless the original EXE and resource file match the exact SHA-256 digests from the tested r6 package. It copies the full extracted folder and changes only the expected 12 bytes. It also checks the resulting output hashes. **It does not flash firmware or contact hardware.**
5. **Only if you accept the risks**, disconnect all known-working Razer wireless receivers, attach the previously non-pairing `1532:005A` receiver, and run the modified pairing application. If the receiver is recognized, the **Next** button should be enabled.
6. In the one reported successful recovery, selecting **Next** requested a USB mouse connection; attaching the 2017 mouse by Micro-USB initiated pairing. After completion, wireless and wired functions were both tested successfully.

**Stop** if any unexpected firmware-update, bootloader, or recovery operation is offered. Do not proceed on another model or on an unverified file version. Keep a spare wired mouse and avoid repeatedly experimenting with working receivers.

### What the patch changes

| File | Description | Changed bytes |
|---|---|---:|
| `LanceheadWirelessPairingUtility.exe` | Hardware-ID string changes (`006F → 005A`, `0070 → 0059`) | 4 |
| `DeviceUpdater.resources` | Two corresponding ID pairs in device metadata | 8 |
| `FWUpdaterDLL.dll` | **Unmodified** | 0 |

The native DLL and embedded firmware payloads remain unchanged. This does **not** establish that the proprietary pairing commands are safe on every firmware revision.

## Repository contents

- [`lancehead_2017_pairing_patch.py`](lancehead_2017_pairing_patch.py) — Python 3 offline patcher with input/output SHA-256 checks.
- [`docs/CASE_STUDY.md`](docs/CASE_STUDY.md) — complete technical report, hashes, offsets and source links.
- [`LICENSE`](LICENSE) — MIT license for the original repository materials only (not Razer software).

## Legal and safety notice

This independent research and script are provided for educational and repair purposes, **without warranty**. Please consider Razer's software license and applicable law before modifying software. This repository does **not** redistribute Razer programs, firmware, or trademarks as product branding. `Razer` and `Lancehead` are trademarks of their respective owners.

If you reproduce the result, an issue describing the **exact model, original USB IDs, utility version, and outcome** is more useful than a general success/failure statement. Please do not upload proprietary Razer binaries to issues.
