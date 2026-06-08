#!/usr/bin/env python3
"""Restore the factory all-zero/whitebox PSK on the Goodix 55a2 after Windows
re-provisioned it (device PMK hash drifted from 81b8ff49... to 23dce6fd...).
PSK provisioning ONLY -- no firmware erase, no config flash."""
import sys
import goodix, protocol, driver_55x4 as d

PRODUCT = 0x55a2

def main():
    dev = goodix.Device(PRODUCT, protocol.USBProtocol)
    dev.nop()
    try:
        ok = d.check_psk(dev)
        print(f"BEFORE: check_psk matches factory PMK_HASH? {ok}")
    except Exception as e:
        print(f"BEFORE check_psk error: {e}")
    print("Writing PSK_WHITE_BOX (flags 0xbb010003)...")
    if d.write_psk(dev):
        print("RESULT: write_psk OK -- PMK hash now matches factory 81b8ff49...")
    else:
        print("RESULT: write_psk FAILED")
        return 1
    print(f"AFTER: check_psk matches? {d.check_psk(dev)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
