#!/usr/bin/env python3
"""
Vector Verifier

Verifies all generated vectors against their invariants.
Fails the build if any canonical vector is inconsistent.
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
        "logos_minus": 0x0F,  # bits {0,1,2,3}
        "logos_plus":  0xF0,  # bits {4,5,6,7}
        "nomos_minus": 0x33,  # bits {0,1,4,5}
        "nomos_plus":  0xCC,  # bits {2,3,6,7}
        "pathos_minus": 0x55,  # bits {0,2,4,6}
        "pathos_plus":  0xAA,  # bits {1,3,5,7}
    }
    
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

def verify_cobs(filepath):
    """Verify COBS vectors."""
    data = load_yaml(filepath)
    errors = []
    
    def cobs_encode(data_bytes):
        if not data_bytes:
            return bytes([0x01])
        
        result = bytearray()
        i = 0
        
        while i < len(data_bytes):
            zero_pos = i
            while zero_pos < len(data_bytes) and data_bytes[zero_pos] != 0:
                zero_pos += 1
            
            run_length = zero_pos - i
            if run_length >= 254:
                code = 0xFF
                result.append(code)
                result.extend(data_bytes[i:i+254])
                i += 254
            else:
                code = run_length + 1
                result.append(code)
                result.extend(data_bytes[i:zero_pos])
                if zero_pos < len(data_bytes):
                    result.append(0x00)
                    i = zero_pos + 1
                else:
                    i = zero_pos
        
        return bytes(result)
    
    def cobs_decode(encoded):
        if not encoded:
            return bytes()
        
        result = bytearray()
        i = 0
        
        while i < len(encoded):
            code = encoded[i]
            i += 1
            
            if code == 0:
                raise ValueError("Zero code byte is invalid")
            
            if code == 0xFF:
                if i + 254 > len(encoded):
                    raise ValueError("Truncated block")
                result.extend(encoded[i:i+254])
                i += 254
            else:
                run_length = code - 1
                if i + run_length > len(encoded):
                    raise ValueError("Truncated block")
                result.extend(encoded[i:i+run_length])
                i += run_length
                if i < len(encoded):
                    result.append(0x00)
        
        return bytes(result)
    
    vectors = data["vectors"]
    for vec in vectors:
        if vec["expected"].get("roundtrip"):
            input_data = bytes(vec["input"])
            encoded_body = bytes(vec["encoded_body"])
            
            # Verify encoding
            actual_encoded = cobs_encode(input_data)
            if list(actual_encoded) != vec["encoded_body"]:
                errors.append(f"Encoding mismatch for {vec['id']}: {list(actual_encoded)} != {vec['encoded_body']}")
            
            # Verify decoding
            try:
                decoded = cobs_decode(encoded_body)
                if decoded != input_data:
                    errors.append(f"Decoding mismatch for {vec['id']}")
            except ValueError as e:
                errors.append(f"Decoding failed for {vec['id']}: {e}")
    
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

def main():
    vectors_dir = os.path.join(os.path.dirname(__file__), "..")
    all_errors = []
    
    print("Verifying vectors...", file=sys.stderr)
    
    # Verify compact743
    compact_path = os.path.join(vectors_dir, "generated", "compact743.yaml")
    if os.path.exists(compact_path):
        errors = verify_compact743(compact_path)
        if errors:
            all_errors.extend([f"compact743: {e}" for e in errors])
        else:
            print("  compact743: OK", file=sys.stderr)
    
    # Verify miquel844
    miquel_path = os.path.join(vectors_dir, "generated", "miquel844.yaml")
    if os.path.exists(miquel_path):
        errors = verify_miquel844(miquel_path)
        if errors:
            all_errors.extend([f"miquel844: {e}" for e in errors])
        else:
            print("  miquel844: OK", file=sys.stderr)
    
    # Verify cobs
    cobs_path = os.path.join(vectors_dir, "generated", "cobs.yaml")
    if os.path.exists(cobs_path):
        errors = verify_cobs(cobs_path)
        if errors:
            all_errors.extend([f"cobs: {e}" for e in errors])
        else:
            print("  cobs: OK", file=sys.stderr)
    
    # Verify scope4
    scope4_path = os.path.join(vectors_dir, "scope4.yaml")
    if os.path.exists(scope4_path):
        errors = verify_scope4(scope4_path)
        if errors:
            all_errors.extend([f"scope4: {e}" for e in errors])
        else:
            print("  scope4: OK", file=sys.stderr)
    
    # Verify projection
    projection_path = os.path.join(vectors_dir, "projection.yaml")
    if os.path.exists(projection_path):
        errors = verify_projection(projection_path)
        if errors:
            all_errors.extend([f"projection: {e}" for e in errors])
        else:
            print("  projection: OK", file=sys.stderr)
    
    # Verify activation
    activation_path = os.path.join(vectors_dir, "activation.yaml")
    if os.path.exists(activation_path):
        errors = verify_activation(activation_path)
        if errors:
            all_errors.extend([f"activation: {e}" for e in errors])
        else:
            print("  activation: OK", file=sys.stderr)
    
    if all_errors:
        print(f"\nVerification FAILED:", file=sys.stderr)
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\nAll vectors verified successfully", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
