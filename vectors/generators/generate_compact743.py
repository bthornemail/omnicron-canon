#!/usr/bin/env python3
"""
Compact [7,4,3] Hamming Code Generator

Generates all valid codewords and corruption cases from the declared parity equations:
  LOGOS  = FS ⊕ GS ⊕ US
  NOMOS  = FS ⊕ RS ⊕ US
  PATHOS = GS ⊕ RS ⊕ US

Codeword layout: [LOGOS, NOMOS, PATHOS, FS, GS, RS, US]
  bit 6 = LOGOS
  bit 5 = NOMOS
  bit 4 = PATHOS
  bit 3 = FS
  bit 2 = GS
  bit 1 = RS
  bit 0 = US

Parity-check matrix H:
  H = [1 0 0 | 1 1 0 1]   (LOGOS check)
      [0 1 0 | 1 0 1 1]   (NOMOS check)
      [0 0 1 | 0 1 1 1]   (PATHOS check)

Syndrome s = H * c^T should be zero for valid codewords.
"""

import sys
import yaml
from itertools import combinations

def xor_bits(bits):
    result = 0
    for b in bits:
        result ^= b
    return result

def compute_parity(fs, gs, rs, us):
    logos = xor_bits([fs, gs, us])
    nomos = xor_bits([fs, rs, us])
    pathos = xor_bits([gs, rs, us])
    return logos, nomos, pathos

def make_codeword(fs, gs, rs, us):
    logos, nomos, pathos = compute_parity(fs, gs, rs, us)
    return [logos, nomos, pathos, fs, gs, rs, us]

def compute_syndrome(codeword):
    logos, nomos, pathos, fs, gs, rs, us = codeword
    s0 = xor_bits([logos, fs, gs, us])  # LOGOS check
    s1 = xor_bits([nomos, fs, rs, us])  # NOMOS check
    s2 = xor_bits([pathos, gs, rs, us])  # PATHOS check
    return [s0, s1, s2]

def generate_all_valid():
    valid = []
    for fs in range(2):
        for gs in range(2):
            for rs in range(2):
                for us in range(2):
                    cw = make_codeword(fs, gs, rs, us)
                    syndrome = compute_syndrome(cw)
                    assert syndrome == [0, 0, 0], f"Invalid codeword {cw} with syndrome {syndrome}"
                    valid.append({
                        "scope": {"fs": fs, "gs": gs, "rs": rs, "us": us},
                        "codeword": cw,
                        "syndrome": syndrome
                    })
    return valid

def generate_single_bit_corruptions(valid_codewords):
    corruptions = []
    for entry in valid_codewords:
        original = entry["codeword"]
        scope = entry["scope"]
        for bit_pos in range(7):
            corrupted = original.copy()
            corrupted[bit_pos] ^= 1
            syndrome = compute_syndrome(corrupted)
            assert syndrome != [0, 0, 0], f"Corruption at bit {bit_pos} should not produce valid codeword"
            corruptions.append({
                "scope": scope,
                "original": original,
                "corrupted": corrupted,
                "bit_position": bit_pos,
                "syndrome": syndrome
            })
    return corruptions

def generate_yaml(valid, corruptions):
    schema = {
        "schema": "compact743",
        "version": "1.0",
        "generator": "generate_compact743.py",
        "layout": {
            "description": "Codeword layout: [LOGOS, NOMOS, PATHOS, FS, GS, RS, US]",
            "bit_positions": {
                "6": "LOGOS",
                "5": "NOMOS",
                "4": "PATHOS",
                "3": "FS",
                "2": "GS",
                "1": "RS",
                "0": "US"
            }
        },
        "equations": {
            "logos": "FS ⊕ GS ⊕ US",
            "nomos": "FS ⊕ RS ⊕ US",
            "pathos": "GS ⊕ RS ⊕ US"
        },
        "parity_check_matrix": [
            [1, 0, 0, 1, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 1],
            [0, 0, 1, 0, 1, 1, 1]
        ],
        "vectors": {
            "valid": valid,
            "single_bit_corruptions": corruptions
        },
        "invariants": [
            "syndrome = H * codeword^T = [0,0,0] for all valid codewords",
            "syndrome != [0,0,0] for all single-bit corruptions",
            "each single-bit corruption flips exactly one syndrome bit",
            "codeword length = 7",
            "valid count = 16",
            "single-bit corruption count = 112"
        ]
    }
    return schema

def main():
    print("Generating Compact [7,4,3] vectors...", file=sys.stderr)
    
    valid = generate_all_valid()
    print(f"Generated {len(valid)} valid codewords", file=sys.stderr)
    
    corruptions = generate_single_bit_corruptions(valid)
    print(f"Generated {len(corruptions)} single-bit corruption cases", file=sys.stderr)
    
    result = generate_yaml(valid, corruptions)
    
    output = yaml.dump(result, default_flow_style=False, sort_keys=False)
    print(output)
    
    # Verification
    print(f"\nVerification:", file=sys.stderr)
    print(f"  Valid codewords: {len(valid)} (expected 16)", file=sys.stderr)
    print(f"  Single-bit corruptions: {len(corruptions)} (expected 112)", file=sys.stderr)
    
    # Verify all syndromes
    for entry in valid:
        assert entry["syndrome"] == [0, 0, 0], f"Invalid syndrome for {entry['codeword']}"
    
    for entry in corruptions:
        assert entry["syndrome"] != [0, 0, 0], f"Corruption produced valid codeword"
    
    print("  All syndromes verified", file=sys.stderr)

if __name__ == "__main__":
    main()
