# Safety notes

The patcher checks SHA-256 hashes of the extracted original r6 files before
modifying their metadata and embedded device-ID strings. It does not communicate
with hardware or flash firmware.

The **patched Razer pairing application**, when run by the user, is an unofficial
cross-generation experiment. Its native pairing calls have not been fully audited,
and the package retains the 2019 model's embedded firmware resources. Do **not**
use it for firmware updates, bootloader entry, or firmware recovery. A loss of
wired or wireless function is possible.

Do not post unmodified or modified proprietary Razer executables in GitHub issues.
If you discover a vulnerability in the repository's own patch script, open an issue
without sharing exploit material or private information.
