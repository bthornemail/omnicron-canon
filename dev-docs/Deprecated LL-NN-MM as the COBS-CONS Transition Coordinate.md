## Deprecated LL/NN/MM as the COBS-CONS Transition Coordinate

### Status

Normative codec interpretation.

This section does not restore LL/NN/MM as canonical OMI scope authority.

FS/GS/RS/US remains the canonical pre-language memory topology.

LL/NN/MM is retained only as an internal transition coordinate for the deterministic COBS-CONS codec.

---

### 1. Authority Boundary

The canonical distinction is:

```text
FS/GS/RS/US:
  scope topology

LL/NN/MM:
  codec traversal state
```

Therefore:

```text
FS/GS/RS/US defines where a declaration is scoped.

LL/NN/MM defines how an encoded run is traversed and decoded.
```

LL/NN/MM MUST NOT replace FS/GS/RS/US in public canonical addresses, OMI-IMO frame fields, document scopes, or accepted memory identity.

LL/NN/MM MAY be used internally by the Omnicron COBS-CONS encoder, decoder, verifier, and diagnostic trace.

---

### 2. Transition Meaning

For an encoded COBS-CONS stream:

```text
LL = current length/lens code
NN = current code-byte cursor
MM = derived next code-byte cursor
```

The transition law is:

```text
MM = NN + LL
```

The current payload run is:

```text
encoded[NN + 1 .. MM - 1]
```

Canonical reading:

```text
LL selects the run.
NN begins the run.
MM resolves the continuation.
```

This preserves the historical transition mnemonic without restoring its former authority.

---

### 3. CONS Interpretation

Each COBS run lowers into one CONS relation:

```text
CAR = current nonzero payload run
CDR = continuation at MM
```

Conceptually:

```lisp
(run . continuation)
```

The recovered zero boundary is NULL.

Therefore:

```text
NULL preserves the frame boundary.
CAR carries the current run.
CDR identifies the next run.
CONS joins run and continuation.
```

Canonical lock:

```text
LL/NN/MM traverses.
CONS relates.
COBS frames.
FS/GS/RS/US scopes.
```

---

### 4. Decode State Machine

Given an encoded frame `E` of length `encoded_length`:

```text
NN := 0
```

For each run:

```text
LL := E[NN]
```

The decoder MUST reject if:

```text
LL = 0
```

because a zero code byte is reserved as the external frame delimiter and is not legal inside a COBS-encoded frame.

Derive:

```text
MM := NN + LL
```

The decoder MUST reject if:

```text
MM > encoded_length
```

Copy:

```text
E[NN + 1 .. MM - 1]
```

to the decoded output.

If:

```text
LL < 0xFF
and
MM < encoded_length
```

the decoder reconstructs one:

```text
0x00
```

Then:

```text
NN := MM
```

Decoding succeeds only when:

```text
NN = encoded_length
```

Canonical loop:

```text
read LL
derive MM
copy CAR
restore NULL when required
follow CDR
```

---

### 5. FS/GS/RS/US Preservation

The bytes:

```text
0x1C FS
0x1D GS
0x1E RS
0x1F US
0x20 SP
```

are ordinary nonzero payload bytes to the COBS layer.

The codec MUST reproduce them exactly.

After decoding, the pre-language resolver interprets them as:

```text
FS = file scope
GS = group scope
RS = record scope or closure witness
US = unit scope
SP = readable boundary
```

The codec MUST NOT infer, alter, reorder, validate, or accept these scopes.

Canonical invariant:

```text
COBS preserves scope bytes.
It does not interpret their authority.
```

---

### 6. F* Gauge Boundary

An OMI gauge pre-header has the form:

```text
G 00 1C 1D 1E 1F 20 G
```

where:

```text
G ∈ 0xF0..0xFF
```

Within decoded content:

```text
G selects the operator dialect.
00 preserves origin.
FS/GS/RS/US defines scope topology.
SP opens readability.
G closes the gauge boundary.
```

When carried through COBS-CONS, the interior `0x00` is represented by the COBS run structure and reconstructed during decoding.

The F* gauge does not replace the COBS code byte.

The COBS code byte does not replace the F* gauge.

They occupy different layers:

```text
COBS code:
  transport framing

F* gauge:
  operator dialect

FS/GS/RS/US:
  scope topology
```

---

### 7. Canonical Pipeline

```text
Omicron CONS candidate
↓
canonical FS/GS/RS/US scoped bytes
↓
F* gauge selection
↓
COBS stuffing
↓
LL/NN/MM encoded-run traversal
↓
COBS decoding
↓
CONS reconstruction
↓
FS/GS/RS/US scope resolution
↓
OMI-Lisp or Lambda Canon Block candidate
↓
validation
↓
receipt
```

No codec stage accepts state.

No traversal cursor creates identity.

No restored separator proves truth.

---

### 8. Normative Invariants

A conforming COBS-CONS implementation MUST preserve:

```text
decode(encode(payload)) = payload
```

for every bounded payload.

It MUST also preserve:

```text
all original 0x00 positions
all FS bytes
all GS bytes
all RS bytes
all US bytes
all SP bytes
all payload byte order
```

It MUST reject:

```text
zero code bytes inside an encoded frame
run lengths extending beyond frame bounds
truncated runs
unterminated external frames
noncanonical alternative encodings, if canonical encoding is required
arena or output overflow
```

It MUST remain:

```text
deterministic
bounded
round-trippable
non-authoritative
```

---

### 9. Final Authority Statement

```text
LL/NN/MM is deprecated as memory-topology authority.

LL/NN/MM is retained as the internal three-coordinate traversal
state of COBS-CONS:

LL = current run code
NN = current cursor
MM = next cursor

FS/GS/RS/US remains the canonical four-scope topology.

The old model traverses the encoding.
The new model defines the memory.
```
