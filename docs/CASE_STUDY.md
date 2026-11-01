# Recovering wireless pairing on the original Razer Lancehead (2017, RZ01-02120)

**A verified single-device case study using a minimally modified 2019 Lancehead pairing utility**  
**Date:** 1 November 2026  
**Status:** Successful wireless pairing; wired and wireless operation confirmed by the device owner  
**Affiliation:** Independent troubleshooting; not affiliated with, authorized by, or endorsed by Razer

## Executive summary

An original 2017 Razer Lancehead wireless mouse worked when connected by Micro-USB, but would not communicate with its original USB receiver. Windows recognized both devices; however, Razer's publicly available Lancehead Wireless Pairing Utility, versions **v1.00.00 r4** and **v1.00.00 r6**, refused to detect the receiver. Its **Next** button remained disabled. A second, known-working 2017 Lancehead receiver was equally unrecognized by these utilities.

Static inspection of the r6 utility showed that its device-identification fields refer to the **later Lancehead Wireless RZ01-02570** (`1532:006F` receiver and `1532:0070` wired mouse), rather than the original **RZ01-02120** (`1532:005A` receiver and `1532:0059` wired mouse). The test was to substitute the original model's IDs at the relevant locations, while leaving the native DLL and embedded firmware payload bytes unchanged.

An initial patch of the program executable alone failed. A second patch that also changed two metadata ID pairs in `DeviceUpdater.resources` enabled **Next**, accepted the connected mouse, and completed pairing. The owner subsequently confirmed that **everything works**, including wireless and wired operation. No firmware update was intentionally initiated.

**Key finding:** In this particular case, the published pairing utility's hardware-ID matching blocked otherwise successful pairing between the original 2017 Lancehead and its receiver. A single successful test does not establish compatibility across all devices or firmware revisions.

## 1. Hardware and test environment

| Component | Details |
|---|---|
| Mouse | Razer Lancehead, original 2017 wireless model, **RZ01-02120**; reported underside marking **RC30-021203** |
| Mouse over USB cable | Vendor ID **1532**, product ID **0059** |
| Original wireless receiver | Vendor ID **1532**, product ID **005A** |
| Later 2019 Lancehead Wireless model | **RZ01-02570** |
| Later model receiver | **1532:006F** |
| Later model wired connection | **1532:0070** |
| Confirmed test computer | ASUS ROG Strix G15 running Windows 11 |
| Razer Synapse | Not installed on the confirmed test computer |
| USB connection | Mouse via Micro-USB cable; receiver via USB |
| Available controls | Owner had three original wireless Lanceheads, three wired Lancehead variants, and a known-working wireless receiver |

The owner had tried to solve the problem across approximately five computers over several years. Those historical systems' complete configurations were not recorded. The final successful result was observed on the Windows 11 system above.

The IDs for both Lancehead generations are independently listed by the OpenRazer project (see Sources). A correctly enumerated USB receiver is **not** proof of an established 2.4 GHz wireless pairing.

## 2. Original failure and diagnostics

Windows PowerShell was used with both the problem receiver and the mouse plugged in:

```powershell
Get-PnpDevice -PresentOnly |
Where-Object { $_.InstanceId -match 'VID_1532&PID_(0059|005A)' } |
Select-Object Status, FriendlyName, InstanceId |
Format-Table -AutoSize
```

The output included multiple HID interfaces with `Status: OK` under **`USB\VID_1532&PID_0059`** (wired mouse) and **`USB\VID_1532&PID_005A`** (wireless receiver). This established that the computer could independently enumerate both USB devices; it did not establish that they were wirelessly paired.

| Test | Observed outcome |
|---|---|
| Wired mouse attached to Windows | Recognized; worked through cable |
| Original receiver attached to Windows | Recognized as `1532:005A` |
| Official pairing utility r6 | Did not recognize receiver; **Next** disabled |
| Official pairing utility r4 | Same failure |
| Substitute known-working 2017 receiver in official utility | Same failure |
| Experimental v1, executable ID edits only | Same failure |
| Experimental v2, executable + resource metadata ID edits | **Next** enabled |
| v2, connected wired mouse at utility's prompt | Pairing succeeded |
| Mouse after completing procedure | Owner reports all tested functions working, wired and wireless |

The known-working receiver was used **only to test detection**, not to perform experimental re-pairing.

## 3. Analysis of the original Razer software

Razer's official support site lists **Lancehead Wireless Pairing Utility v1.00.00 r6** and the earlier **r4**. It instructs users to connect the dongle first, then connect the mouse by cable. Razer publishes separate firmware updaters for **RZ01-02120** and **RZ01-02570**, confirming that these are distinct device families.

The user supplied original copies of r4 and r6 for offline inspection. Their expanded package contents were compared without executing either installer. Both bundles contain the same native `FWUpdaterDLL.dll` (**identical SHA-256**); their main programs and resource files are not identical. Static examination of the r6 executable and resource data identified product IDs `006F` and `0070` used in hardware identification. Both versions' unmodified detection stages had rejected `005A` devices.

This suggested an **identification/eligibility mismatch** rather than a Windows 11 USB-enumeration failure. It did **not**, by itself, prove that the two Lancehead generations shared a compatible pairing protocol; that hypothesis was tested on the owner's already-nonfunctional wireless setup.

## 4. Exact experimental changes in successful v2

All changes were length-preserving byte substitutions on files extracted from the original **r6** package. The source installer was not modified. **The successful v2 differs from the original expanded r6 in just 12 bytes: four in the pairing executable and eight in the resource file.**

### 4.1 `LanceheadWirelessPairingUtility.exe`

| Original field | Replacement | Byte offsets (hexadecimal) |
|---|---|---|
| `006F` (later receiver) | `005A` (2017 receiver) | `0xF416`, `0xF418` |
| `0070` (later wired mouse) | `0059` (2017 wired mouse) | `0xF548`, `0xF54A` |

These edits are within UTF-16-encoded device-ID strings. Each of the four listed offsets is **one changed byte**; the surrounding characters and the file length are unchanged.

### 4.2 `DeviceUpdater.resources`

This file contained two further occurrences of the later model's receiver/mouse ID pair in structured metadata:

| Original field | Replacement | Byte offsets (hexadecimal) |
|---|---|---|
| First `006F` | `005A` | `0x4F57B`, `0x4F57C` |
| First `0070` | `0059` | `0x4F581`, `0x4F582` |
| Second `006F` | `005A` | `0xA0236`, `0xA0237` |
| Second `0070` | `0059` | `0xA023C`, `0xA023D` |

The eight offsets are individual changed bytes; the resource file's length is unchanged. The resource file also contains embedded firmware data, but a byte-level comparison confirmed that **those firmware payload bytes were not altered**. The native DLL was also left completely unchanged.

### 4.3 SHA-256 verification values

These values identify the **specific examined files**. Offsets must not be applied to a different version or a different package without first verifying its content.

| File | SHA-256 |
|---|---|
| Original downloaded r6 installer | `f55a3fcbc2d8216dbd6efa15369ed8f11628e51c328fe03943ebaa10f47ef7b5` |
| Expanded original r6 pairing executable | `4c81719693e246ff07f9067ab71af3a6237ded7a963b1fb135b6d19c3805e304` |
| Patched v2 pairing executable | `5e1b481b51e224849aaa7216767fb2b660aa967d642a56eb8277b0bd19a22b6e` |
| Expanded original r6 resource file | `11b32d6502be305762c95f336d7c4223a356ab14a2a2c397e33b966e02bba4d1` |
| Patched v2 resource file | `60f6bf3f1bd77303fd131bd81480190da8036cc69824fb6a49e24e0633b6ec42` |
| Native `FWUpdaterDLL.dll`, unchanged in r4, r6, and patched v2 | `ae1f7e32894e9dc57bfc0bfa661e9bbb69eb2c83087d3c97f8d3c75509cca4cf` |

An accompanying Python patch script was independently tested against the extracted original r6 directory. It produced files **byte-for-byte identical** to the successful v2 artifacts. The script verifies input and output SHA-256 values, refuses unknown source versions, and does not contain Razer's executable or firmware data. The original package must be obtained from Razer and expanded locally.

## 5. Controlled pairing attempt and result

The pairing attempt used the receiver whose wireless functionality had already failed, with other working Lancehead receivers disconnected:

1. Confirm the mouse operated via its USB cable.
2. Insert the problematic `1532:005A` receiver into the PC.
3. Launch the patched **r6 v2** utility and observe that **Next** is enabled (it was disabled in both official builds and in v1).
4. Click **Next**. The utility displays the instruction to connect the mouse.
5. Connect the original 2017 mouse through the Micro-USB data cable.
6. Allow the pairing step to complete and verify operation after disconnecting the cable and enabling wireless mode.

**Observed outcome:** The owner reported that pairing worked and subsequently confirmed that **everything works**. The mouse retained wired functionality. No firmware-update workflow was deliberately run, and no bootloader or firmware-flash prompt was approved. We did not capture a USB protocol trace or verify the internal nonvolatile changes made by the pairing commands, so it would be inaccurate to claim that the program made *no* persistent writes: successful pairing ordinarily requires storing or exchanging association information.

## 6. Why the patch appears to have worked

The evidence supports this explanation:

- The original hardware was properly recognized by Windows through USB; this was not a missing USB driver problem.
- The published utility's device metadata specified the newer USB IDs, rejecting even a 2017 receiver known to work wirelessly.
- Editing executable-only identifiers did not suffice; editing the **two resource metadata ID pairs as well** allowed detection.
- Once those checks passed, the utility's pairing operation worked on this 2017 mouse/receiver pair.

**Inference, not proof:** The pairing commands used by the later utility are compatible with at least this particular earlier device/firmware configuration. The experiment does not prove that all radio firmware is interchangeable, that the application is free of unsafe code paths, or that mixed-generation hardware can be paired.

## 7. Important limitations and safety considerations

- **One confirmed success:** This is a single-device case study, not a validated general recovery tool.
- **Unofficial executable:** Modifying an EXE may invalidate its Authenticode signature and can trigger Windows security warnings. Do not bypass security controls or obtain modified binaries from unknown sources.
- **Firmware hazard:** Both bundles contain firmware-capable components, and the later model's firmware data remains embedded. **Do not use the experimental utility for firmware updates or bootloader recovery.**
- **Pairing is a write operation:** Although static inspection did not identify a direct firmware-flashing call in the analyzed pairing routine, the behavior of proprietary native commands has not been exhaustively audited.
- **Other hardware:** Do not experiment on known-working receivers first. Use the exact USB IDs to distinguish the 2017 and 2019 models.
- **Long-term reliability:** Continued operation over days/weeks, behavior after reboot or battery depletion, and compatibility with other firmware versions were not systematically tested.
- **Copyright and licenses:** A technical description and an independent patching script are easier to share responsibly than Razer's modified proprietary executables. Review the applicable software license and local law before publication or redistribution.

## 8. Reproducibility and publication

For a technically proficient owner of the original 2017 Lancehead who is willing to accept an unknown device risk:

1. Obtain the **official r6** download from Razer, not a third-party mirror.
2. Extract the original r6 installer to a folder containing `LanceheadWirelessPairingUtility.exe`, `DeviceUpdater.resources`, and `FWUpdaterDLL.dll` (and the rest of the application files). The extraction method must preserve these files exactly.
3. Verify the source hashes above. Do not modify or patch a package whose hashes differ.
4. Apply the exact 12-byte changes described in section 4, preferably using the checksum-guarded companion script against a *copy* of the extracted folder.
5. Preserve the entire application folder, not just the modified EXE.
6. For any experimental pairing, isolate the intended mouse and receiver and avoid any firmware update action.

The companion script is called `lancehead_2017_pairing_patch.py`. Run:

```bash
python lancehead_2017_pairing_patch.py PATH_TO_EXTRACTED_R6 PATH_TO_NEW_OUTPUT_FOLDER
```

The source and destination folders must be different and the destination must not exist. **Neither the script nor this report includes redistributed Razer executables.** The script has been tested to recreate the same two patched files byte-for-byte. Its inclusion is informational, not a safety guarantee.

## 9. Related public reports and primary sources

1. **Razer:** [Razer Lancehead Wireless Pairing Utility Guide](https://mysupport.razer.com/app/answers/detail/a_id/1506/) — official r4/r6 downloads and connection sequence.
2. **Razer:** [Original Lancehead RZ01-02120 support](https://mysupport.razer.com/app/answers/detail/a_id/3784/) and [original-model firmware updater](https://mysupport.razer.com/app/answers/detail/a_id/1796/) — device and firmware family.
3. **Razer:** [Later Lancehead Wireless RZ01-02570 firmware updater](https://mysupport.razer.com/app/answers/detail/a_id/1634/) — separate later-model firmware.
4. **OpenRazer:** [Supported device IDs](https://github.com/openrazer/openrazer/blob/master/README.md) — `0059`, `005A`, `006F`, and `0070` mapping.
5. **Razer Insider, July 2020:** [Replacement receiver not recognized by pairing utility](https://insider.razer.com/razer-support-45/razer-lancehead-wireless-dongle-doesn-t-work-13724).
6. **Razer Insider, October 2021:** [Two replacement receivers not recognized across computers](https://insider.razer.com/razer-support-45/lancehead-pairing-utility-not-working-31238).
7. **Razer Insider, February 2026:** [Another reported dongle-detection failure](https://insider.razer.com/razer-support-45/razer-lancehead-problems-86291).

**Publication note:** We found similar unresolved reports but have not established that this is the first time anyone has identified or used an equivalent workaround. The test should be described as a **confirmed local success**, not as a universally supported fix.
