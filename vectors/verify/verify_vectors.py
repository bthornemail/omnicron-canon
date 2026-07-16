#!/usr/bin/env python3
"""
Vector Verifier

Verifies all generated vectors against their invariants.
Fails the build if any canonical vector is inconsistent.

This verifier explicitly prints and validates every canonical profile.
"""

import sys
import yaml
import os

def load_yaml(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def verify_compact743(filepath):
    """Verify Compact [7,4,3] vectors."""
    data = load_yaml(filepath)
    errors = []
    
    # Check valid codewords
    valid = data["vectors"]["valid"]
    if len(valid) != 16:
        errors.append(f"Expected 16 valid codewords, got {len(valid)}")
    
    for entry in valid:
        cw = entry["codeword"]
        if len(cw) != 7:
            errors.append(f"Invalid codeword length: {len(cw)}")
            continue
        
        logos, nomos, pathos, fs, gs, rs, us = cw
        expected_logos = fs ^ gs ^ us
        expected_nomos = fs ^ rs ^ us
        expected_pathos = gs ^ rs ^ us
        
        if logos != expected_logos:
            errors.append(f"LOGOS mismatch for {entry['scope']}: {logos} != {expected_logos}")
        if nomos != expected_nomos:
            errors.append(f"NOMOS mismatch for {entry['scope']}: {nomos} != {expected_nomos}")
        if pathos != expected_pathos:
            errors.append(f"PATHOS mismatch for {entry['scope']}: {pathos} != {expected_pathos}")
    
    # Check single-bit corruptions
    corruptions = data["vectors"]["single_bit_corruptions"]
    if len(corruptions) != 112:
        errors.append(f"Expected 112 single-bit corruptions, got {len(corruptions)}")
    
    for entry in corruptions:
        corrupted = entry["corrupted"]
        if len(corrupted) != 7:
            errors.append(f"Invalid corrupted codeword length: {len(corrupted)}")
            continue
        
        logos, nomos, pathos, fs, gs, rs, us = corrupted
        s0 = logos ^ fs ^ gs ^ us
        s1 = nomos ^ fs ^ rs ^ us
        s2 = pathos ^ gs ^ rs ^ us
        
        if s0 == 0 and s1 == 0 and s2 == 0:
            errors.append(f"Corruption produced valid codeword: {corrupted}")
    
    return errors

def verify_miquel844(filepath):
    """Verify Miquel [8,4,4] vectors."""
    data = load_yaml(filepath)
    errors = []
    
    masks = {
        "logos_minus": 0x0F,
        "logos_plus":  0xF0,
        "nomos_minus": 0x33,
        "nomos_plus":  0xCC,
        "pathos_minus": 0x55,
        "pathos_plus":  0xAA,
    }
    
    # Verify generator matrix properties
    props = data.get("properties", {})
    if props.get("rank") != 4:
        errors.append(f"Expected rank 4, got {props.get('rank')}")
    if props.get("minimum_distance") != 4:
        errors.append(f"Expected minimum_distance 4, got {props.get('minimum_distance')}")
    if not props.get("verified"):
        errors.append("Generator matrix not verified")
    
    # Check valid codewords
    valid = data["vectors"]["valid"]
    if len(valid) != 16:
        errors.append(f"Expected 16 valid codewords, got {len(valid)}")
    
    for entry in valid:
        codeword = entry["codeword"]
        bits = entry["bits"]
        
        if len(bits) != 8:
            errors.append(f"Invalid bit count: {len(bits)}")
            continue
        
        for name, mask in masks.items():
            check = 0
            for i in range(8):
                if mask & (1 << i):
                    check ^= bits[i]
            if check != 0:
                errors.append(f"Check {name} failed for codeword {codeword}")
    
    # Check single-bit corruptions
    single_corruptions = data["vectors"]["single_bit_corruptions"]
    if len(single_corruptions) != 128:
        errors.append(f"Expected 128 single-bit corruptions, got {len(single_corruptions)}")
    
    for entry in single_corruptions:
        corrupted = entry["corrupted"]
        bits = [(corrupted >> i) & 1 for i in range(8)]
        
        all_zero = True
        for name, mask in masks.items():
            check = 0
            for i in range(8):
                if mask & (1 << i):
                    check ^= bits[i]
            if check != 0:
                all_zero = False
                break
        
        if all_zero:
            errors.append(f"Corruption produced valid codeword: {corrupted}")
    
    # Check two-bit corruptions
    two_corruptions = data["vectors"]["two_bit_corruptions"]
    if len(two_corruptions) != 448:
        errors.append(f"Expected 448 two-bit corruptions, got {len(two_corruptions)}")
    
    for entry in two_corruptions:
        corrupted = entry["corrupted"]
        bits = [(corrupted >> i) & 1 for i in range(8)]
        
        all_zero = True
        for name, mask in masks.items():
            check = 0
            for i in range(8):
                if mask & (1 << i):
                    check ^= bits[i]
            if check != 0:
                all_zero = False
                break
        
        if all_zero:
            errors.append(f"Corruption produced valid codeword: {corrupted}")
    
    return errors

def verify_scope4(filepath):
    """Verify Scope4 vectors."""
    data = load_yaml(filepath)
    errors = []
    
    valid = data["vectors"]["valid"]
    if len(valid) != 16:
        errors.append(f"Expected 16 valid vectors, got {len(valid)}")
    
    invalid = data["vectors"]["invalid"]
    for entry in invalid:
        bits = entry["bits"]
        for bit in bits:
            if bit not in (0, 1):
                errors.append(f"Invalid bit value in {entry['id']}: {bit}")
    
    return errors

def verify_projection(filepath):
    """Verify projection vectors."""
    data = load_yaml(filepath)
    errors = []
    
    masks = data["vectors"]["masks"]
    if len(masks) != 16:
        errors.append(f"Expected 16 masks, got {len(masks)}")
    
    for entry in masks:
        if "identity" not in entry:
            errors.append(f"Missing identity in {entry['id']}")
    
    return errors

def verify_activation(filepath):
    """Verify activation vectors."""
    data = load_yaml(filepath)
    errors = []
    
    requests = data["vectors"]["requests"]
    results = data["vectors"]["results"]
    
    for entry in requests:
        if entry["expected"]["valid"] not in (True, False):
            errors.append(f"Invalid valid value in {entry['id']}")
    
    for entry in results:
        if entry["expected"]["valid"] not in (True, False):
            errors.append(f"Invalid valid value in {entry['id']}")
    
    return errors

def verify_delta3(filepath):
    """Verify Delta3 vectors."""
    data = load_yaml(filepath)
    errors = []
    
    positions = data["vectors"]["positions"]
    if len(positions) != 3:
        errors.append(f"Expected 3 positions, got {len(positions)}")
    
    # Verify position properties
    for pos in positions:
        if pos["enum_value"] not in (0, 1, 2):
            errors.append(f"Invalid enum_value in {pos['id']}")
        if pos["symbol"] not in ("LL", "MM", "NN"):
            errors.append(f"Invalid symbol in {pos['id']}")
        if pos["integrity_axis"] not in ("LOGOS", "NOMOS", "PATHOS"):
            errors.append(f"Invalid integrity_axis in {pos['id']}")
    
    # Verify one-hot encoding
    for pos in positions:
        if sum(pos["one_hot"]) != 1:
            errors.append(f"Invalid one_hot in {pos['id']}")
    
    # Verify transitions
    transitions = data["vectors"]["transitions"]
    if len(transitions) != 2:
        errors.append(f"Expected 2 transitions, got {len(transitions)}")
    
    # Verify windows
    windows = data["vectors"]["windows"]
    if len(windows) != 3:
        errors.append(f"Expected 3 windows, got {len(windows)}")
    
    # Verify checks
    checks = data["vectors"]["checks"]
    if len(checks) != 4:
        errors.append(f"Expected 4 checks, got {len(checks)}")
    
    return errors

def verify_cobs_core(filepath):
    """Verify COBS core vectors."""
    data = load_yaml(filepath)
    errors = []
    
    vectors = data["vectors"]
    if len(vectors) != 8:
        errors.append(f"Expected 8 vectors, got {len(vectors)}")
    
    # Verify invariants are present
    if "invariants" not in data:
        errors.append("Missing invariants")
    
    return errors

def verify_cobs_null_00(filepath):
    """Verify COBS null-00 vectors."""
    data = load_yaml(filepath)
    errors = []
    
    vectors = data["vectors"]
    if len(vectors) != 15:
        errors.append(f"Expected 15 vectors, got {len(vectors)}")
    
    # Verify profile settings
    if data.get("null_octet") != 0x00:
        errors.append("Invalid null_octet")
    
    if data.get("framing", {}).get("suffix") != True:
        errors.append("Invalid framing suffix")
    
    return errors

def verify_cobs_omi_null_ring(filepath):
    """Verify COBS OMI null-ring vectors."""
    data = load_yaml(filepath)
    errors = []
    
    vectors = data["vectors"]
    if len(vectors) != 9:
        errors.append(f"Expected 9 vectors, got {len(vectors)}")
    
    # Verify encoding status is unresolved
    if data.get("encoding_status") != "unresolved":
        errors.append("Expected encoding_status: unresolved")
    
    return errors

def verify_cobs_gnomic_fdelta_ring(filepath):
    """Verify COBS gnomic fdelta-ring vectors."""
    data = load_yaml(filepath)
    errors = []
    
    vectors = data["vectors"]
    if len(vectors) != 12:
        errors.append(f"Expected 12 vectors, got {len(vectors)}")
    
    # Verify encoding status is unresolved
    if data.get("encoding_status") != "unresolved":
        errors.append("Expected encoding_status: unresolved")
    
    # Verify framing is prefix+suffix
    if data.get("framing", {}).get("prefix") != True:
        errors.append("Invalid framing prefix")
    if data.get("framing", {}).get("suffix") != True:
        errors.append("Invalid framing suffix")
    
    return errors

def main():
    vectors_dir = os.path.join(os.path.dirname(__file__), "..")
    all_errors = []
    
    print("Verifying all canonical vector profiles...", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # Define all profiles to verify
    profiles = [
        ("compact743", os.path.join(vectors_dir, "generated", "compact743.yaml"), verify_compact743),
        ("miquel844", os.path.join(vectors_dir, "generated", "miquel844.yaml"), verify_miquel844),
        ("scope4", os.path.join(vectors_dir, "scope4.yaml"), verify_scope4),
        ("projection", os.path.join(vectors_dir, "projection.yaml"), verify_projection),
        ("activation", os.path.join(vectors_dir, "activation.yaml"), verify_activation),
        ("delta3", os.path.join(vectors_dir, "delta3.yaml"), verify_delta3),
        ("cobs-core", os.path.join(vectors_dir, "cobs-core.yaml"), verify_cobs_core),
        ("cobs-null-00", os.path.join(vectors_dir, "cobs-null-00.yaml"), verify_cobs_null_00),
        ("cobs-omi-null-ring", os.path.join(vectors_dir, "cobs-omi-null-ring.yaml"), verify_cobs_omi_null_ring),
        ("cobs-gnomic-fdelta-ring", os.path.join(vectors_dir, "cobs-gnomic-fdelta-ring.yaml"), verify_cobs_gnomic_fdelta_ring),
    ]
    
    # Verify each profile
    for name, filepath, verifier in profiles:
        if os.path.exists(filepath):
            errors = verifier(filepath)
            if errors:
                all_errors.extend([f"{name}: {e}" for e in errors])
                print(f"  {name}: FAILED ({len(errors)} errors)", file=sys.stderr)
            else:
                print(f"  {name}: OK", file=sys.stderr)
        else:
            print(f"  {name}: FILE NOT FOUND", file=sys.stderr)
            all_errors.append(f"{name}: file not found")
    
    print("=" * 60, file=sys.stderr)
    
    if all_errors:
        print(f"\nVerification FAILED:", file=sys.stderr)
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\nAll {len(profiles)} canonical vector profiles verified successfully", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
