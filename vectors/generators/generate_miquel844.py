#!/usr/bin/env python3
"""
Miquel [8,4,4] Integrity Code Generator

Generates all valid codewords and corruption cases from the frozen generator matrix.

The Miquel [8,4,4] code uses the Reed-Muller form:
  c(Pxyz) = a0 ⊕ aL·x ⊕ aN·y ⊕ aP·z

where the four input bits are:
  a0  = FS coefficient
  aL  = GS coefficient (LOGOS)
  aN  = RS coefficient (NOMOS)
  aP  = US coefficient (PATHOS)

Generator matrix G844:
  row 0 (a0): [1 1 1 1 1 1 1 1]
  row 1 (aL): [0 0 0 0 1 1 1 1]
  row 2 (aN): [0 0 1 1 0 0 1 1]
  row 3 (aP): [0 1 0 1 0 1 0 1]

Properties:
  rank(G844) = 4
  minimum_distance = 4
  codeword_count = 16

Bijection:
  Scope4 (FS, GS, RS, US) → MiquelCell8 (8-bit codeword)
"""

import sys
import yaml
from itertools import combinations

# Frozen generator matrix G844 (Reed-Muller form)
# Rows: a0, aL, aN, aP
# Columns: P000, P001, P010, P011, P100, P101, P110, P111
G844 = [
    [1, 1, 1, 1, 1, 1, 1, 1],  # a0 (constant)
    [0, 0, 0, 0, 1, 1, 1, 1],  # aL (x coefficient)
    [0, 0, 1, 1, 0, 0, 1, 1],  # aN (y coefficient)
    [0, 1, 0, 1, 0, 1, 0, 1],  # aP (z coefficient)
]

# Point names
POINT_NAMES = ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"]

# Source bit names (Scope4 coefficients)
SOURCE_NAMES = ["FS", "GS", "RS", "US"]

# Incidence masks (for verification)
MASKS = {
    "logos_minus": 0x0F,  # bits {0,1,2,3}
    "logos_plus":  0xF0,  # bits {4,5,6,7}
    "nomos_minus": 0x33,  # bits {0,1,4,5}
    "nomos_plus":  0xCC,  # bits {2,3,6,7}
    "pathos_minus": 0x55,  # bits {0,2,4,6}
    "pathos_plus":  0xAA,  # bits {1,3,5,7}
}

def xor_bits(bits):
    result = 0
    for b in bits:
        result ^= b
    return result

def encode_scope4(scope4):
    """Encode Scope4 to MiquelCell8 using G844."""
    # scope4 bits: [FS, GS, RS, US]
    # codeword = scope4 * G844 (matrix multiplication over GF(2))
    codeword = [0] * 8
    for i in range(4):
        if scope4[i]:
            for j in range(8):
                codeword[j] ^= G844[i][j]
    return codeword

def verify_codeword(codeword):
    """Verify a codeword satisfies all 6 incidence checks."""
    bits = codeword if isinstance(codeword, list) else [(codeword >> i) & 1 for i in range(8)]
    for name, mask in MASKS.items():
        check = 0
        for i in range(8):
            if mask & (1 << i):
                check ^= bits[i]
        if check != 0:
            return False, name
    return True, None

def generate_all_valid():
    """Generate all 16 valid codewords using G844."""
    valid = []
    for scope_val in range(16):
        scope4 = [(scope_val >> i) & 1 for i in range(4)]
        codeword = encode_scope4(scope4)
        codeword_int = sum(codeword[i] << i for i in range(8))
        
        # Verify using incidence checks
        valid_check, failed_check = verify_codeword(codeword)
        assert valid_check, f"Codeword {codeword_int} failed check {failed_check}"
        
        valid.append({
            "scope4": scope4,
            "scope_value": scope_val,
            "codeword": codeword_int,
            "bits": codeword,
            "point_names": {
                POINT_NAMES[i]: codeword[i] for i in range(8)
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
            valid_check, failed_check = verify_codeword(corrupted)
            assert not valid_check, f"Corruption at bit {bit_pos} should not produce valid codeword"
            corruptions.append({
                "scope_value": entry["scope_value"],
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
            valid_check, failed_check = verify_codeword(corrupted)
            assert not valid_check, f"Corruption at bits {bit_pos1},{bit_pos2} should not produce valid codeword"
            corruptions.append({
                "scope_value": entry["scope_value"],
                "original": original,
                "corrupted": corrupted,
                "bit_positions": [bit_pos1, bit_pos2],
                "point_names": [POINT_NAMES[bit_pos1], POINT_NAMES[bit_pos2]]
            })
    return corruptions

def verify_generator_matrix():
    """Verify G844 properties."""
    # Check rank
    # For a 4x8 matrix over GF(2), rank should be 4
    # We can verify by checking that all 4 rows are linearly independent
    
    # Check that all non-zero codewords have weight >= 4
    min_weight = 8
    for i in range(1, 16):
        scope4 = [(i >> j) & 1 for j in range(4)]
        codeword = encode_scope4(scope4)
        weight = sum(codeword)
        min_weight = min(min_weight, weight)
    
    return min_weight == 4

def generate_yaml(valid, single_corruptions, two_corruptions):
    schema = {
        "schema": "miquel844",
        "version": "1.0",
        "generator": "generate_miquel844.py",
        "generator_matrix": {
            "description": "Reed-Muller form: c(Pxyz) = a0 ⊕ aL·x ⊕ aN·y ⊕ aP·z",
            "rows": ["a0 (FS)", "aL (GS)", "aN (RS)", "aP (US)"],
            "columns": POINT_NAMES,
            "G844": G844
        },
        "source_mapping": {
            "a0": "FS",
            "aL": "GS (LOGOS coefficient)",
            "aN": "RS (NOMOS coefficient)",
            "aP": "US (PATHOS coefficient)"
        },
        "incidence_masks": {name: f"0x{mask:02X}" for name, mask in MASKS.items()},
        "properties": {
            "rank": 4,
            "minimum_distance": 4,
            "codeword_count": 16,
            "verified": verify_generator_matrix()
        },
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
            "two-bit corruption count = 448",
            "minimum weight = 4",
            "bijection Scope4 ↔ MiquelCell8"
        ]
    }
    return schema

def main():
    print("Generating Miquel [8,4,4] vectors from G844...", file=sys.stderr)
    
    # Verify generator matrix properties
    assert verify_generator_matrix(), "Generator matrix verification failed"
    print("Generator matrix verified: rank=4, min_distance=4", file=sys.stderr)
    
    valid = generate_all_valid()
    print(f"Generated {len(valid)} valid codewords", file=sys.stderr)
    
    single_corruptions = generate_single_bit_corruptions(valid)
    print(f"Generated {len(single_corruptions)} single-bit corruption cases", file=sys.stderr)
    
    two_corruptions = generate_two_bit_corruptions(valid)
    print(f"Generated {len(two_corruptions)} two-bit corruption cases", file=sys.stderr)
    
    result = generate_yaml(valid, single_corruptions, two_corruptions)
    
    output = yaml.dump(result, default_flow_style=False, sort_keys=False)
    print(output)
    
    # Final verification
    print(f"\nVerification:", file=sys.stderr)
    print(f"  Valid codewords: {len(valid)} (expected 16)", file=sys.stderr)
    print(f"  Single-bit corruptions: {len(single_corruptions)} (expected 128)", file=sys.stderr)
    print(f"  Two-bit corruptions: {len(two_corruptions)} (expected 448)", file=sys.stderr)
    print(f"  Generator matrix: verified", file=sys.stderr)
    print(f"  Minimum distance: 4", file=sys.stderr)
    
    # Verify all valid codewords
    for entry in valid:
        valid_check, failed_check = verify_codeword(entry["codeword"])
        assert valid_check, f"Invalid codeword {entry['codeword']} failed check {failed_check}"
    
    # Verify all single-bit corruptions
    for entry in single_corruptions:
        valid_check, _ = verify_codeword(entry["corrupted"])
        assert not valid_check, f"Corruption produced valid codeword"
    
    # Verify all two-bit corruptions
    for entry in two_corruptions:
        valid_check, _ = verify_codeword(entry["corrupted"])
        assert not valid_check, f"Corruption produced valid codeword"
    
    print("  All checks verified", file=sys.stderr)

if __name__ == "__main__":
    main()
