#!/usr/bin/env python3
"""
Miquel [8,4,4] Integrity Code Generator

Generates all valid codewords and corruption cases from the frozen generator matrix.

The Miquel [8,4,4] code uses 8 points on a projective plane with 6 incidence checks:
  LOGOS+: bits {0,1,2} = 0x07
  LOGOS-: bits {3,4,5} = 0x38
  NOMOS+: bits {0,1,3} = 0x0B
  NOMOS-: bits {2,4,5} = 0x34
  PATHOS+: bits {0,2,3} = 0x0D
  PATHOS-: bits {1,4,5} = 0x32

Source bits: {0, 1, 4, 5} = {P000, P001, P100, P101}
Parity bits: {2, 3, 6, 7} = {P010, P011, P110, P111}

For a valid codeword, all 6 checks must equal 0.
"""

import sys
import yaml
from itertools import combinations

# Frozen incidence masks
MASKS = {
    "logos_plus":  0x07,  # bits 0,1,2
    "logos_minus": 0x38,  # bits 3,4,5
    "nomos_plus":  0x0B,  # bits 0,1,3
    "nomos_minus": 0x34,  # bits 2,4,5
    "pathos_plus": 0x0D,  # bits 0,2,3
    "pathos_minus": 0x32,  # bits 1,4,5
}

# Source and parity bit positions
SOURCE_BITS = [0, 1, 4, 5]  # P000, P001, P100, P101
PARITY_BITS = [2, 3, 6, 7]  # P010, P011, P110, P111

# Point names
POINT_NAMES = ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"]

def check_codeword(codeword):
    """Check if a codeword satisfies all 6 incidence checks."""
    for name, mask in MASKS.items():
        bits = [(codeword >> i) & 1 for i in range(8)]
        check = 0
        for i in range(8):
            if mask & (1 << i):
                check ^= bits[i]
        if check != 0:
            return False, name
    return True, None

def generate_all_valid():
    """Generate all 16 valid codewords by brute force."""
    valid = []
    for source_val in range(16):
        for parity_val in range(16):
            codeword = 0
            for i, bit_pos in enumerate(SOURCE_BITS):
                if source_val & (1 << i):
                    codeword |= (1 << bit_pos)
            for i, bit_pos in enumerate(PARITY_BITS):
                if parity_val & (1 << i):
                    codeword |= (1 << bit_pos)
            
            valid_check, failed_check = check_codeword(codeword)
            if valid_check:
                bits = [(codeword >> i) & 1 for i in range(8)]
                valid.append({
                    "source_value": source_val,
                    "parity_value": parity_val,
                    "codeword": codeword,
                    "bits": bits,
                    "point_names": {
                        POINT_NAMES[i]: bits[i] for i in range(8)
                    }
                })
    return valid

def generate_single_bit_corruptions(valid_codewords):
    """Generate all 128 single-bit corruption cases."""
    corruptions = []
    for entry in valid_codewords:
        original = entry["codeword"]
        for bit_pos in range(8):
            corrupted = original ^ (1 << bit_pos)
            valid_check, failed_check = check_codeword(corrupted)
            assert not valid_check, f"Corruption at bit {bit_pos} should not produce valid codeword"
            corruptions.append({
                "source_value": entry["source_value"],
                "original": original,
                "corrupted": corrupted,
                "bit_position": bit_pos,
                "point_name": POINT_NAMES[bit_pos]
            })
    return corruptions

def generate_two_bit_corruptions(valid_codewords):
    """Generate all 448 two-bit corruption cases."""
    corruptions = []
    for entry in valid_codewords:
        original = entry["codeword"]
        for bit_pos1, bit_pos2 in combinations(range(8), 2):
            corrupted = original ^ (1 << bit_pos1) ^ (1 << bit_pos2)
            valid_check, failed_check = check_codeword(corrupted)
            assert not valid_check, f"Corruption at bits {bit_pos1},{bit_pos2} should not produce valid codeword"
            corruptions.append({
                "source_value": entry["source_value"],
                "original": original,
                "corrupted": corrupted,
                "bit_positions": [bit_pos1, bit_pos2],
                "point_names": [POINT_NAMES[bit_pos1], POINT_NAMES[bit_pos2]]
            })
    return corruptions

def generate_yaml(valid, single_corruptions, two_corruptions):
    schema = {
        "schema": "miquel844",
        "version": "1.0",
        "generator": "generate_miquel844.py",
        "incidence_masks": {name: f"0x{mask:02X}" for name, mask in MASKS.items()},
        "source_bits": {POINT_NAMES[i]: i for i in SOURCE_BITS},
        "parity_bits": {POINT_NAMES[i]: i for i in PARITY_BITS},
        "vectors": {
            "valid": valid,
            "single_bit_corruptions": single_corruptions,
            "two_bit_corruptions": two_corruptions
        },
        "invariants": [
            "all 6 checks equal 0 for valid codewords",
            "all 6 checks do not all equal 0 for corrupted codewords",
            "codeword length = 8",
            "valid count = 16",
            "single-bit corruption count = 128",
            "two-bit corruption count = 448"
        ]
    }
    return schema

def main():
    print("Generating Miquel [8,4,4] vectors...", file=sys.stderr)
    
    valid = generate_all_valid()
    print(f"Generated {len(valid)} valid codewords", file=sys.stderr)
    
    single_corruptions = generate_single_bit_corruptions(valid)
    print(f"Generated {len(single_corruptions)} single-bit corruption cases", file=sys.stderr)
    
    two_corruptions = generate_two_bit_corruptions(valid)
    print(f"Generated {len(two_corruptions)} two-bit corruption cases", file=sys.stderr)
    
    result = generate_yaml(valid, single_corruptions, two_corruptions)
    
    output = yaml.dump(result, default_flow_style=False, sort_keys=False)
    print(output)
    
    # Verification
    print(f"\nVerification:", file=sys.stderr)
    print(f"  Valid codewords: {len(valid)} (expected 16)", file=sys.stderr)
    print(f"  Single-bit corruptions: {len(single_corruptions)} (expected 128)", file=sys.stderr)
    print(f"  Two-bit corruptions: {len(two_corruptions)} (expected 448)", file=sys.stderr)
    
    # Verify all valid codewords
    for entry in valid:
        valid_check, failed_check = check_codeword(entry["codeword"])
        assert valid_check, f"Invalid codeword {entry['codeword']} failed check {failed_check}"
    
    # Verify all single-bit corruptions
    for entry in single_corruptions:
        valid_check, _ = check_codeword(entry["corrupted"])
        assert not valid_check, f"Corruption produced valid codeword"
    
    # Verify all two-bit corruptions
    for entry in two_corruptions:
        valid_check, _ = check_codeword(entry["corrupted"])
        assert not valid_check, f"Corruption produced valid codeword"
    
    print("  All checks verified", file=sys.stderr)

if __name__ == "__main__":
    main()
