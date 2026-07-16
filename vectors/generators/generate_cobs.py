#!/usr/bin/env python3
"""
COBS (Consistent Overhead Byte Stuffing) Generator

Generates conformance vectors for COBS encoding/decoding.

COBS rules:
  code byte ∈ 0x01..0xFF
  0x00 is invalid inside the encoded body
  external 0x00 terminates a frame
  0xFF denotes a 254-byte nonzero run without an inserted zero

Invariant: decode(encode(x)) = x

Body vs Framed:
  encoded_body: the COBS-encoded payload (no delimiter)
  framed: encoded_body + [0x00] delimiter
"""

import sys
import yaml

def cobs_encode(data):
    """Encode data using COBS."""
    if not data:
        return bytes([0x01])
    
    result = bytearray()
    i = 0
    
    while i < len(data):
        # Find the next zero byte
        zero_pos = i
        while zero_pos < len(data) and data[zero_pos] != 0:
            zero_pos += 1
        
        # Calculate code byte
        run_length = zero_pos - i
        if run_length >= 254:
            code = 0xFF
            result.append(code)
            result.extend(data[i:i+254])
            i += 254
        else:
            code = run_length + 1
            result.append(code)
            result.extend(data[i:zero_pos])
            if zero_pos < len(data):
                result.append(0x00)  # This will be replaced by next code byte
                i = zero_pos + 1
            else:
                i = zero_pos
    
    return bytes(result)

def cobs_decode(encoded):
    """Decode COBS-encoded data."""
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
            # Read 254 bytes
            if i + 254 > len(encoded):
                raise ValueError("Truncated block")
            result.extend(encoded[i:i+254])
            i += 254
        else:
            # Read code-1 bytes, then add a zero
            run_length = code - 1
            if i + run_length > len(encoded):
                raise ValueError("Truncated block")
            result.extend(encoded[i:i+run_length])
            i += run_length
            if i < len(encoded):
                result.append(0x00)
    
    return bytes(result)

def generate_test_vectors():
    """Generate COBS test vectors."""
    vectors = []
    
    # Empty payload
    vectors.append({
        "id": "cobs-empty",
        "input": [],
        "encoded_body": [0x01],
        "framed": [0x01, 0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # Single zero
    vectors.append({
        "id": "cobs-single-zero",
        "input": [0x00],
        "encoded_body": [0x01, 0x01],
        "framed": [0x01, 0x01, 0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # Leading zero
    vectors.append({
        "id": "cobs-leading-zero",
        "input": [0x00, 0x01, 0x02, 0x03],
        "encoded_body": [0x01, 0x04, 0x01, 0x02, 0x03],
        "framed": [0x01, 0x04, 0x01, 0x02, 0x03, 0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # Trailing zero
    vectors.append({
        "id": "cobs-trailing-zero",
        "input": [0x01, 0x02, 0x03, 0x00],
        "encoded_body": [0x04, 0x01, 0x02, 0x03, 0x01],
        "framed": [0x04, 0x01, 0x02, 0x03, 0x01, 0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # Embedded zeros
    vectors.append({
        "id": "cobs-embedded-zeros",
        "input": [0x01, 0x00, 0x02, 0x00, 0x03],
        "encoded_body": [0x02, 0x01, 0x02, 0x02, 0x02, 0x03],
        "framed": [0x02, 0x01, 0x02, 0x02, 0x02, 0x03, 0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # Single nonzero byte
    vectors.append({
        "id": "cobs-single-nonzero",
        "input": [0x42],
        "encoded_body": [0x02, 0x42],
        "framed": [0x02, 0x42, 0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # All zeros
    vectors.append({
        "id": "cobs-all-zeros",
        "input": [0x00, 0x00, 0x00],
        "encoded_body": [0x01, 0x01, 0x01, 0x01],
        "framed": [0x01, 0x01, 0x01, 0x01, 0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # 254 nonzero bytes
    input_254 = list(range(1, 255))  # 1..254
    encoded_254 = [0xFF] + input_254
    vectors.append({
        "id": "cobs-254-nonzero",
        "description": "254 nonzero bytes require 0xFF code byte",
        "input": input_254,
        "encoded_body": encoded_254,
        "framed": encoded_254 + [0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # 255 nonzero bytes
    input_255 = list(range(1, 256))  # 1..255
    encoded_255 = [0xFF] + list(range(1, 255)) + [0x02, 0xFF]
    vectors.append({
        "id": "cobs-255-nonzero",
        "description": "255 nonzero bytes: 0xFF + 254 bytes + code byte + 1 byte",
        "input": input_255,
        "encoded_body": encoded_255,
        "framed": encoded_255 + [0x00],
        "expected": {"valid": True, "roundtrip": True}
    })
    
    # Invalid zero code byte
    vectors.append({
        "id": "cobs-invalid-zero-code",
        "description": "0x00 as code byte is invalid",
        "encoded_body": [0x00],
        "framed": [0x00],
        "expected": {"valid": False, "error": "zero code byte"}
    })
    
    # Truncated block
    vectors.append({
        "id": "cobs-truncated-block",
        "description": "Code byte claims more bytes than available",
        "encoded_body": [0x05, 0x01, 0x02],
        "framed": [0x05, 0x01, 0x02],
        "expected": {"valid": False, "error": "truncated block"}
    })
    
    # Missing external delimiter
    vectors.append({
        "id": "cobs-missing-delimiter",
        "description": "Frame without terminating zero (body is valid, frame is incomplete)",
        "encoded_body": [0x03, 0x01, 0x02, 0x03],
        "framed": [0x03, 0x01, 0x02, 0x03],
        "expected": {"valid": True, "frame_valid": False, "error": "missing external delimiter"}
    })
    
    return vectors

def generate_yaml(vectors):
    schema = {
        "schema": "cobs",
        "version": "1.0",
        "generator": "generate_cobs.py",
        "rules": {
            "code_byte_range": "0x01..0xFF",
            "zero_boundary": "0x00 is invalid inside encoded body",
            "frame_termination": "external 0x00 terminates a frame",
            "long_run": "0xFF denotes 254-byte nonzero run"
        },
        "vectors": vectors,
        "invariants": [
            "decode(encode(x)) = x for all valid payloads",
            "encoded body contains no zero bytes inside body",
            "code byte is always 0x01..0xFF",
            "0xFF code byte means 254-byte nonzero run",
            "frame termination is external 0x00",
            "truncation is detected and rejected",
            "missing delimiter is detected and rejected",
            "body without delimiter is valid COBS, incomplete frame"
        ]
    }
    return schema

def main():
    print("Generating COBS vectors...", file=sys.stderr)
    
    vectors = generate_test_vectors()
    print(f"Generated {len(vectors)} vectors", file=sys.stderr)
    
    # Verify roundtrip for valid vectors
    for vec in vectors:
        if vec["expected"].get("roundtrip"):
            input_data = bytes(vec["input"])
            encoded = cobs_encode(input_data)
            decoded = cobs_decode(encoded)
            assert decoded == input_data, f"Roundtrip failed for {vec['id']}"
            assert list(encoded) == vec["encoded_body"], f"Encoding mismatch for {vec['id']}"
    
    result = generate_yaml(vectors)
    
    output = yaml.dump(result, default_flow_style=False, sort_keys=False)
    print(output)
    
    print(f"\nVerification:", file=sys.stderr)
    print(f"  Vectors: {len(vectors)}", file=sys.stderr)
    print(f"  All roundtrips verified", file=sys.stderr)

if __name__ == "__main__":
    main()
