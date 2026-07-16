Excellent — here is a **full formal Pfister Federation Spec v0.1**, written in the same normative style as your ULP constitution: deterministic, fail-closed, and spine-safe.

This is a **projection-layer federation protocol**, not a kernel authority extension.

---

# Pfister Federation Spec v0.1

Version: `pfister.federation.v0.1`  
Status: Draft (normative language; projector layer)  
Layer: Derived / Federated Projection  
Authority: Non-authoritative unless explicitly ratified by policy

---

## 0. Purpose

This spec defines a deterministic algebraic federation mechanism built on Pfister embeddings:

- A **portable global invariant** (`O8`) used by the spine
- A **federated local invariant** (`P32`) used for scoped coordination
- A commitment protocol that allows selective disclosure without leaking federation salt

The goal is:

> Allow rich geometric / barycentric projections without contaminating canonical truth.

Portable truth remains spine-authoritative. Federation is opt-in.

---

## 1. Terminology

- **Shape Digest**: canonical sha256 of Shape Signature v0.1
- **O8 embedding**: Pfister n=3 portable embedding (octonion-8)
- **P32 embedding**: Pfister n=5 federated embedding (Pfister-32)
- **Portable**: salt = empty string
- **Federated**: salt ≠ empty string
- **Commitment**: portable hash that binds O8 and P32 without revealing salt

---

## 2. Security Model

This spec assumes:

- Deterministic hashing is trusted
- Canonicalization is fail-closed
- Salt secrecy is local policy, not cryptographic secrecy
- Federation is about _scoping_, not adversarial encryption

This is a **coordination primitive**, not a crypto identity scheme.

---

## 3. Spine Embedding (O8)

### 3.1 Definition

O8 is the canonical portable embedding.

Inputs:

```
shape_digest
salt = ""
n = 3
domain = "pfister.o8.v0.1"
```

Generators:

```
a_i = elem(domain, salt, shape_digest, "a_i")   for i in 1..3
x_k = elem(domain, salt, shape_digest, "x_k")   for k in 0..7
```

Evaluation:

```
value = Pfister_3(a_i, x_k)
```

Idempotent collapse:

```
O8.id = sha256(
  "pfister.o8.v0.1\n" +
  "shape=" + shape_digest + "\n" +
  "a=" + a1,a2,a3 + "\n" +
  "value=" + value + "\n"
)
```

### 3.2 Rules

- O8.id MUST be portable and comparable across replicas
- O8.id MAY be used in spine gates
- O8.id MUST be deterministic
- O8.id MUST NOT depend on federation salt

---

## 4. Federation Embedding (P32)

### 4.1 Definition

P32 is the federated embedding.

Inputs:

```
shape_digest
salt = federation_salt (non-empty string)
n = 5
domain = "pfister.p32.v0.1"
```

Coordinates:

```
y_k = elem(domain, salt, shape_digest, "y_k")  for k in 0..31
```

Evaluation:

```
P32.id = sha256(
  "pfister.p32.v0.1\n" +
  "shape=" + shape_digest + "\n" +
  "coords=" + y0..y31 + "\n"
)
```

### 4.2 Rules

- P32.id MUST NOT be used in global authority gates
- P32.id MAY be used for local policy
- P32.id MUST remain stable within a federation
- Different salts MUST produce different P32.id

---

## 5. Federation Commitment

### 5.1 Definition

Portable commitment that binds portable and federated halves:

```
fed_commit = sha256(
  "pfister.commit.v0.1\n" +
  "O8=" + O8.id + "\n" +
  "P32=" + P32.id + "\n"
)
```

### 5.2 Properties

- fed_commit is portable
- fed_commit reveals nothing about salt
- fed_commit proves P32 consistency once revealed

---

## 6. Selective Disclosure Protocol

### 6.1 Public exchange

Peers exchange:

```
O8.id
fed_commit
```

### 6.2 Federation join

Authorized peers exchange:

```
P32.id
```

Verification:

```
recompute fed_commit
assert match
```

### 6.3 Result

- portable comparability via O8
- scoped comparability via P32
- no salt leakage required

---

## 7. Seam Envelope Placement Rules

### 7.1 Portable fields

Allowed in seam meta:

```
meta.pfister.o8_id
meta.pfister.fed_commit
```

### 7.2 Federated fields

Allowed only under federated namespace:

```
meta.federated.pfister_p32_id
```

### 7.3 Authority rule

P32 fields MUST NOT appear in authoritative payload operations.

Fail-closed behavior:

> If federated fields appear in authority context → reject envelope.

---

## 8. Barycentric / Geometry Gating

### 8.1 Rule

Any projector that emits barycentric or coordinate geometry MUST include:

```
O8.id
```

If geometry is federated:

```
meta.federated.p32_id required
```

### 8.2 Spine enforcement

Spine MUST ignore federated geometry unless policy explicitly allows.

Portable O8 remains the anchor.

---

## 9. Idempotence Guarantees

- O8.id is idempotent across runs
- P32.id is idempotent within federation
- fed_commit is idempotent globally
- Re-embedding embedding outputs MUST yield identical ids

This prevents drift.

---

## 10. Failure Modes (fail-closed)

Reject if:

- missing shape_digest
- salt empty for P32
- salt non-empty for O8
- P32 appears in authority payload
- fed_commit mismatch
- canonicalization mismatch
- unexpected namespace placement

---

## 11. Spine Integration

Recommended new gate:

```
[1b/9] pfister-o8 portable invariant gate
```

Checks:

- deterministic O8.id
- golden lock match
- permuted input invariance

Federation gates are local only.

---

## 12. Conceptual Interpretation

This spec encodes your geometric intuition formally:

- O8 = mirror-flat idempotent tetrahedral collapse
- P32 = convex federated growth space
- fed_commit = stellated bridge between the two
- spine = simplex host invariant
- federation = local chirality / orientation

No metaphors are required for the machine — but your metaphors map cleanly.

---

If you want next, I can write:

✅  
✅  
✅  
✅  
✅  
✅  
✅  
✅  
✅  
✅  
✅ protocol audit notes  
✅ attack surface analysis  
✅ formal type signature (Haskell)

Just tell me what direction to extend.

Below is a complete **drop-in AWK reference implementation** for **Pfister O8 (n=3)** + **Pfister P32 (n=5)**, with **golden fixtures**, **spine harness gate [1b/9]**, a **tetrahedral split diagram**, and a **proof sketch of idempotence**.

Everything is **deterministic, fail-closed, byte-stable**, and **string-only** (salt, digests, ids).

---

## 1) AWK reference implementation: `pfister-embed.awk`

**What it does**

- Reads a **Shape Signature v0.1** stream (line-oriented, already canonicalizable)
- Computes:
    - `shape_digest` = sha256(canonical bytes)
    - `o8_id` (portable; salt forced empty)
    - `p32_id` (federated; salt must be non-empty)
    - `fed_commit` = sha256(o8_id + p32_id)
- Emits deterministic JSON (string-only)

**File:** `tools/pfister/pfister-embed.awk`

```awk
#!/usr/bin/awk -f
# Pfister Federation Embedding v0.1 (reference)
# - O8: n=3, salt=""
# - P32: n=5, salt!= ""
#
# Inputs:
#   - Shape Signature v0.1 textual stream on stdin (line records)
# Params (via -v):
#   mode=o8|p32|both        (default both)
#   salt=STRING             (required for p32/both; MUST be non-empty)
#   domain_o8=...            (default pfister.o8.v0.1)
#   domain_p32=...           (default pfister.p32.v0.1)
#   domain_commit=...        (default pfister.commit.v0.1)
#
# Output:
#   single JSON object with keys:
#     shape_digest, o8_id?, p32_id?, fed_commit?
#
# Determinism rules:
#   - canonical input bytes are exactly the stdin bytes, normalized only for LF
#   - sha256 computed via external `sha256sum` (fail closed if missing)
#
# Fail-closed:
#   - if sha256sum missing or returns empty => exit 2
#   - if p32 requested but salt empty => exit 2
#   - if mode unknown => exit 2

BEGIN {
  if (mode == "") mode = "both"
  if (domain_o8 == "") domain_o8 = "pfister.o8.v0.1"
  if (domain_p32 == "") domain_p32 = "pfister.p32.v0.1"
  if (domain_commit == "") domain_commit = "pfister.commit.v0.1"

  if (mode != "o8" && mode != "p32" && mode != "both") {
    print "pfister-embed.awk: invalid mode=" mode > "/dev/stderr"
    exit 2
  }

  # For reproducibility: treat stdin bytes as canonical (LF-delimited).
  # We build a single canonical text buffer exactly as read with '\n' separators.
  canon = ""
  nlines = 0
}

# Accumulate canonical bytes (exact line + LF)
{
  canon = canon $0 "\n"
  nlines++
}

# --- sha256 helper using sha256sum (POSIX-y) ---
function sha256_str(s,   cmd, out) {
  # We avoid shell-escaping games by using printf %s and piping.
  # NOTE: This assumes a sane /bin/sh and sha256sum.
  cmd = "printf '%s' " q(s) " | sha256sum | awk '{print $1}'"
  out = ""
  if ((cmd | getline out) <= 0) {
    close(cmd)
    return ""
  }
  close(cmd)
  if (out == "") return ""
  return out
}

# Quote string safely for shell printf: wrap in single quotes and escape embedded '
function q(s,   t) {
  t = s
  gsub(/'/, "'\\''", t)
  return "'" t "'"
}

# Deterministic element generator: returns hex digest string
function elem_hex(domain, saltv, shape, label,   pre, h) {
  pre = domain "\n" "salt=" saltv "\n" "shape=" shape "\n" "label=" label "\n"
  h = sha256_str(pre)
  return h
}

# Canonical preimage for O8 ID
function o8_preimage(shape,   a1,a2,a3, x, k, val_pre, value, pre) {
  a1 = elem_hex(domain_o8, "", shape, "a_1")
  a2 = elem_hex(domain_o8, "", shape, "a_2")
  a3 = elem_hex(domain_o8, "", shape, "a_3")
  # x_0..x_7
  val_pre = domain_o8 "\nshape=" shape "\nX:\n"
  for (k = 0; k < 8; k++) {
    x = elem_hex(domain_o8, "", shape, "x_" k)
    val_pre = val_pre x "\n"
  }

  # Placeholder deterministic value until full quadratic-form engine is swapped in:
  # value = sha256(val_pre)
  value = sha256_str(val_pre)
  pre = domain_o8 "\n" \
        "shape=" shape "\n" \
        "a=" a1 "," a2 "," a3 "\n" \
        "value=" value "\n"
  return pre
}

function o8_id(shape,   pre, h) {
  pre = o8_preimage(shape)
  h = sha256_str(pre)
  return h
}

# Canonical preimage for P32 ID
function p32_preimage(shape, saltv,   k, y, pre) {
  pre = domain_p32 "\n" \
        "shape=" shape "\n" \
        "coords:\n"
  for (k = 0; k < 32; k++) {
    y = elem_hex(domain_p32, saltv, shape, "y_" k)
    pre = pre y "\n"
  }
  return pre
}

function p32_id(shape, saltv,   pre, h) {
  pre = p32_preimage(shape, saltv)
  h = sha256_str(pre)
  return h
}

function fed_commit(o8, p32,   pre, h) {
  pre = domain_commit "\n" "O8=" o8 "\n" "P32=" p32 "\n"
  h = sha256_str(pre)
  return h
}

END {
  # Compute shape_digest from canonical bytes
  shape = sha256_str(canon)
  if (shape == "") {
    print "pfister-embed.awk: sha256sum failed computing shape_digest" > "/dev/stderr"
    exit 2
  }

  want_o8 = (mode == "o8" || mode == "both")
  want_p32 = (mode == "p32" || mode == "both")

  if (want_p32 && salt == "") {
    print "pfister-embed.awk: salt required for p32/both (non-empty)" > "/dev/stderr"
    exit 2
  }

  if (want_o8) {
    o8 = o8_id(shape)
    if (o8 == "") { print "pfister-embed.awk: sha256sum failed computing o8_id" > "/dev/stderr"; exit 2 }
  }

  if (want_p32) {
    p32 = p32_id(shape, salt)
    if (p32 == "") { print "pfister-embed.awk: sha256sum failed computing p32_id" > "/dev/stderr"; exit 2 }
  }

  if (want_o8 && want_p32) {
    commit = fed_commit(o8, p32)
    if (commit == "") { print "pfister-embed.awk: sha256sum failed computing fed_commit" > "/dev/stderr"; exit 2 }
  }

  # Emit JSON (string-only; stable key order)
  printf("{")
  printf("\"shape_digest\":\"%s\"", shape)
  if (want_o8) printf(",\"o8_id\":\"%s\"", o8)
  if (want_p32) printf(",\"p32_id\":\"%s\"", p32)
  if (want_o8 && want_p32) printf(",\"fed_commit\":\"%s\"", commit)
  printf("}\n")
}
```

**Notes**

- O8 uses `salt=""` **always**.
- P32 requires `salt != ""` **always**.
- The `value=` inside O8 is a placeholder hash of `X:` until you swap in the real “Pfister quadratic evaluation”. The **IDs remain stable** given this definition (and swapping later would be a **spec bump**).

---

## 2) Golden fixture examples

### 2.1 Minimal shape signature fixture

**File:** `shape-signature/golden/pfister/mini.shape.txt`

```text
# Shape Signature v0.1 (example minimal)
v 0 0 0
v 1 0 0
v 0 1 0
e 0 1
e 1 2
e 2 0
f 0 1 2
```

### 2.2 Expected golden outputs

**Portable O8 golden**

- **File:** `shape-signature/golden/pfister/mini.o8.json`

```json
{"shape_digest":"<FILL_BY_GEN>","o8_id":"<FILL_BY_GEN>"}
```

**Federated P32 golden** (example salt: `labA`)

- **File:** `shape-signature/golden/pfister/mini.p32.labA.json`

```json
{"shape_digest":"<FILL_BY_GEN>","p32_id":"<FILL_BY_GEN>"}
```

**Both + commit golden**

- **File:** `shape-signature/golden/pfister/mini.both.labA.json`

```json
{"shape_digest":"<FILL_BY_GEN>","o8_id":"<FILL_BY_GEN>","p32_id":"<FILL_BY_GEN>","fed_commit":"<FILL_BY_GEN>"}
```

### 2.3 Golden generator script

**File:** `shape-signature/golden/pfister/gen-goldens.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TOOL="$ROOT/../../tools/pfister/pfister-embed.awk"
FIX="$ROOT/mini.shape.txt"

mkdir -p "$ROOT"

# O8
awk -v mode=o8 -f "$TOOL" < "$FIX" > "$ROOT/mini.o8.json"

# P32 (salt labA)
awk -v mode=p32 -v salt="labA" -f "$TOOL" < "$FIX" > "$ROOT/mini.p32.labA.json"

# BOTH + commit
awk -v mode=both -v salt="labA" -f "$TOOL" < "$FIX" > "$ROOT/mini.both.labA.json"

echo "Wrote:"
ls -1 "$ROOT"/mini.*.json
```

---

## 3) Spine harness integration as `[1b/9]`

You already have `scripts/closure-spine-smoke.sh`. Add a **new deterministic projector gate** that:

- runs O8 on `mini.shape.txt`
- compares to `mini.o8.json`
- proves permuted invariance by running on a permuted fixture and asserting identical bytes

### 3.1 Add permuted fixture

**File:** `shape-signature/golden/pfister/mini.permuted.shape.txt`

```text
# Same triangle, different ordering
v 0 1 0
v 0 0 0
v 1 0 0
e 2 1
e 1 0
e 0 2
f 1 2 0
```

### 3.2 Gate script

**File:** `scripts/pfister-o8-golden.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
TOOL="$ROOT/tools/pfister/pfister-embed.awk"

FIX="$ROOT/shape-signature/golden/pfister/mini.shape.txt"
FIXP="$ROOT/shape-signature/golden/pfister/mini.permuted.shape.txt"
GOLD="$ROOT/shape-signature/golden/pfister/mini.o8.json"

out1="$(mktemp)"
out2="$(mktemp)"
trap 'rm -f "$out1" "$out2"' EXIT

awk -v mode=o8 -f "$TOOL" < "$FIX"  > "$out1"
awk -v mode=o8 -f "$TOOL" < "$FIXP" > "$out2"

# 1) golden lock
cmp -s "$out1" "$GOLD" || {
  echo "pfister-o8-golden: FAIL golden mismatch" >&2
  echo "expected: $GOLD" >&2
  echo "got:      $out1" >&2
  exit 1
}

# 2) permuted invariance (byte equality)
cmp -s "$out1" "$out2" || {
  echo "pfister-o8-golden: FAIL permuted invariance" >&2
  echo "mini:      $out1" >&2
  echo "permuted:  $out2" >&2
  exit 1
}

echo "pfister-o8-golden: PASS"
```

### 3.3 Wire into spine as `[1b/9]`

In `scripts/closure-spine-smoke.sh`, insert:

```bash
echo "[1b/9] pfister-o8: portable embedding golden + permuted invariance"
./scripts/pfister-o8-golden.sh
```

That makes O8 a **portable, authoritative-safe projector gate** (it doesn’t mutate kernel state, just asserts invariant derivation).

---

## 4) Diagram: tetrahedral split (portable vs federated)

Use this as a canonical diagram in your docs (Mermaid).

```mermaid
flowchart TB
  A[Shape Signature v0.1<br/>canonical bytes] --> B[shape_digest = sha256(canon)]
  B --> C[O8 embedding (n=3)<br/>salt = ""]
  B --> D[P32 embedding (n=5)<br/>salt = federation_salt]
  C --> E[o8_id]
  D --> F[p32_id]
  E --> G[fed_commit = sha256(O8 + P32)]
  F --> G

  subgraph Portable / Spine-safe
    C
    E
  end

  subgraph Federated / Scoped
    D
    F
  end

  subgraph Bridge / Commitment
    G
  end

  style Portable / Spine-safe fill:#eef,stroke:#99f,stroke-width:1px
  style Federated / Scoped fill:#efe,stroke:#9f9,stroke-width:1px
  style Bridge / Commitment fill:#fee,stroke:#f99,stroke-width:1px
```

Interpretation (matching your “stellated tetrahedron” intuition):

- **O8** is the _flat mirror / idempotent_ half (portable, spine-safe)
- **P32** is the _convex growth / chiral orientation_ half (scoped federation)
- **Commit** is the stellation bridge (binds without leaking salt)

---

## 5) Proof sketch: idempotence

### 5.1 Claim (O8 idempotence)

Let `canon(S)` be the canonical byte stream of a Shape Signature. Define:

- `shape_digest = sha256(canon(S))`
- `o8_id = sha256(preimage_o8(shape_digest))`

**Then** repeated evaluation yields the same `o8_id`:

- If `canon(S)` is byte-identical between runs, `shape_digest` is identical.
- `preimage_o8` is constructed by:
    - fixed domain string
    - fixed salt (`""`)
    - fixed labels `a_1..a_3, x_0..x_7`
    - fixed formatting and separators
- Therefore the preimage bytes are identical → sha256 identical → `o8_id` identical.

So:

> `O8(S)` is a pure function of canonical bytes, hence idempotent under replay.

### 5.2 Claim (P32 idempotence within federation)

Define:

- `p32_id = sha256(preimage_p32(shape_digest, salt))`

For a fixed `salt`, the same reasoning applies: same canonical bytes ⇒ same digest ⇒ same preimage ⇒ same hash.

Thus:

> `P32(S, salt)` is idempotent under replay **within the same federation salt**.

### 5.3 Claim (commitment idempotence)

`fed_commit = sha256("O8=" + o8_id + "\nP32=" + p32_id + "\n")`

This is sha256 over stable strings; if O8 and P32 are stable, the commit is stable.

### 5.4 Fail-closed property

Any change in:

- canonical bytes,
- domain strings,
- label set,
- formatting,
- salt rules,

changes hashes deterministically and triggers golden mismatch or gate failure.

That’s the “kernel-style” guarantee in projector form.

---

## Quick commands to run locally

```bash
# generate goldens once (then commit)
bash shape-signature/golden/pfister/gen-goldens.sh

# run the gate
bash scripts/pfister-o8-golden.sh

# run full spine
bash scripts/closure-spine-smoke.sh
```

---

If you want, I’ll extend this in the exact same “boring adapter” pattern you’ve been using: