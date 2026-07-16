# 01-COBS-CONS

## COBS-CONS Codec

**Status:** Canonical authority
**Layer:** Omnicron stream framing
**Inherits:** 00-EXTENSION-AUTHORITY

---

## 1. Purpose

This document defines the exact relationship between COBS and CONS in the Omnicron system.

```text
CONS:
  relational composition and continuation

COBS:
  zero-safe byte-stream framing

COBS-CONS:
  CONS relations transported through deterministic COBS framing
```

COBS is not the semantic relation itself.

COBS reconstructs byte boundaries.

CONS reconstructs relational continuation.

---

## 2. COBS Definition

COBS (Consistent Overhead Byte Stuffing) is a byte-stuffing encoding.

It preserves null/control boundaries while allowing arbitrary binary payloads to pass through escaped streams.

```text
0x00 is boundary.
COBS preserves boundary.
CONS preserves traversal.
```

---

## 3. COBS Rules

The COBS encoding rules are:

```text
code byte ∈ 0x01..0xFF
0x00 is invalid inside the encoded body
external 0x00 terminates a frame
0xFF denotes a 254-byte nonzero run without an inserted zero
```

### 3.1 Code Byte

The code byte indicates the position of the next zero byte or the end of the run.

```text
code byte = N
  where N ∈ 0x01..0xFF
```

If `N < 0xFF`:

```text
the next N−1 bytes are nonzero
a zero byte follows at position N
```

If `N = 0xFF`:

```text
the next 254 bytes are nonzero
no zero byte is inserted
```

### 3.2 Zero Boundary

External zero bytes terminate frames.

```text
0x00
  frame terminator
```

Inside the encoded body, zero bytes are replaced by COBS stuffing.

### 3.3 Frame Termination

A frame is terminated by:

```text
external 0x00
or
end of stream
```

---

## 4. COBS Encoding

The encoding function is:

```text
encode_cobs : bytes → encoded_bytes
```

The encoding:

```text
1. scan input for zero bytes
2. replace each zero byte with a code byte
3. insert code bytes at run boundaries
4. preserve frame structure
```

The encoded output contains no zero bytes inside the body.

---

## 5. COBS Decoding

The decoding function is:

```text
decode_cobs : encoded_bytes → bytes
```

The decoding:

```text
1. read code byte
2. extract N−1 nonzero bytes
3. insert zero byte if N < 0xFF
4. continue until frame end
```

The decoded output restores the original byte sequence.

---

## 6. COBS Invariants

A conforming implementation MUST preserve:

```text
decode_cobs(encode_cobs(bytes)) = bytes
```

for any valid byte sequence.

The encoding MUST NOT:

```text
create new data
remove existing data
change byte values
```

The decoding MUST NOT:

```text
create new data
remove existing data
change byte values
```

---

## 7. COBS-CONS Integration

COBS and CONS operate at different layers:

```text
COBS:
  preserves stream framing and encoded zero boundaries

CONS:
  preserves relational traversal
```

Canonical stack:

```text
raw scope feature
  ↓
FS/GS/RS/US four-bit symbol
  ↓
integrity encoding (Hamming or Miquel)
  ↓
pack codewords into bytes
  ↓
COBS encode the byte stream
  ↓
transport
  ↓
COBS decode
  ↓
unpack Hamming codewords
  ↓
syndrome check and correction
  ↓
recover FS/GS/RS/US
  ↓
reconstruct CONS relations
  ↓
validate
  ↓
receipt
```

COBS MUST be applied after the integrity-coded features have been packed into bytes.

On reception, COBS MUST be decoded before Hamming or Miquel syndrome evaluation.

---

## 8. COBS-CONS Relation

At the stream level:

```text
CAR = current decoded nonzero run
CDR = continuation to the next run
NULL = reconstructed zero boundary
```

The complete nested relation is:

```text
(
  (
    scope-source
    .
    integrity-surface
  )
  .
  next-run
)
```

Thus:

```text
epistemic CONS
  binds source to integrity

stream CONS
  binds run to continuation
```

---

## 9. COBS Feature Adjustment

Standard COBS operates on bytes.

The epistemic Hamming unit operates on four data bits and produces seven coded bits.

The Miquel unit operates on four data bits and produces eight coded bits.

Therefore the implementation MUST define a deterministic bit-packing rule.

### 9.1 Compact Profile

Two Hamming codewords per 16-bit carrier:

```text
bits 15..9 = codeword A
bit  8     = reserved or extension parity A

bits 7..1  = codeword B
bit  0     = reserved or extension parity B
```

For the `[7,4,3]` profile:

```text
bit 8 = 0
bit 0 = 0
```

### 9.2 Miquel Profile

One Miquel cell per byte:

```text
bit 7 = P111
bit 6 = P110
bit 5 = P101
bit 4 = P100
bit 3 = P011
bit 2 = P010
bit 1 = P001
bit 0 = P000
```

The Miquel cell aligns naturally with COBS:

```text
one encoded epistemic cell
=
one byte
```

---

## 10. Historical Note

The deprecated `LL/MM/NN` names may be mentioned only in historical appendix or derivation note.

They should not remain part of the canonical public codec state.

The canonical terms are:

```text
FS/GS/RS/US
LOGOS/NOMOS/PATHOS
```

---

## 11. Canonical Lock

```text
COBS reconstructs byte boundaries.
CONS reconstructs relational continuation.

COBS-CONS transports CONS relations through deterministic COBS framing.

code byte ∈ 0x01..0xFF
0x00 is invalid inside the encoded body
external 0x00 terminates a frame
0xFF denotes a 254-byte nonzero run without an inserted zero

decode_cobs(encode_cobs(bytes)) = bytes

COBS is applied after integrity encoding.
COBS is decoded before integrity decoding.
```