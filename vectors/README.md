# Omnicron Conformance Vectors

This directory contains the canonical conformance vectors for the Omnicron extension.

## Purpose

These vectors define expected behavior for:

- Scope4 encoding/decoding
- Compact Hamming [7,4,3] integrity
- Miquel [8,4,4] integrity
- Projection masks
- Activation requests/results
- COBS framing (parameterized NULL-ring)
- Delta3 temporal coordinates

## Consumer Policy

Each repository should **consume** these vectors, not copy-edit them.

```text
omnicron-port
  projection and non-authority vectors

omnicron-isa
  scope4, compact743, miquel844, cobs vectors

omnicron-lisp
  scope4, projection, activation, delta3 vectors
```

A repo may mirror generated test fixtures, but the canonical source remains:

```text
omnicron-canon/vectors/
```

## Phase Lock

```text
Vectors define expected behavior.
Implementations consume vectors.
Implementations do not redefine vectors.
Canon owns conformance.

Canonical vectors must be generated from frozen equations
and independently verified before implementations consume them.

A committed example is not an exhaustive conformance corpus.

A declared invariant is not established until the vector data
actually satisfies it.
```

## Vector Files

| File | Description | Consumed By |
|------|-------------|-------------|
| `scope4.yaml` | All 16 Scope4 combinations + invalid cases | omnicron-isa, omnicron-lisp |
| `compact743.yaml` | Compact [7,4,3] Hamming vectors (generated) | omnicron-isa |
| `miquel844.yaml` | Miquel [8,4,4] integrity vectors (generated) | omnicron-isa |
| `projection.yaml` | All 16 projection masks with identity witnesses | omnicron-port, omnicron-lisp |
| `activation.yaml` | Activation request/result vectors (split) | omnicron-lisp |
| `delta3.yaml` | Delta3 temporal coordinate vectors | omnicron-lisp, omnicron-isa |
| `cobs-core.yaml` | COBS delimiter-independent vectors | omnicron-isa |
| `cobs-null-00.yaml` | Standard octet COBS (0x00 delimiter) | omnicron-isa |
| `cobs-omi-null-ring.yaml` | OMI NULL-ring profile (symbolic) | omnicron-isa |
| `cobs-gnomic-fdelta-ring.yaml` | Gnomic FΔ ring profile (symbolic) | omnicron-isa |

## Generators

Generated vectors are produced by Python scripts:

```text
generators/
  generate_compact743.py
  generate_miquel844.py
  generate_cobs.py
```

To regenerate:

```text
python3 generators/generate_compact743.py > generated/compact743.yaml
python3 generators/generate_miquel844.py > generated/miquel844.yaml
```

## Verification

All vectors are verified by:

```text
python3 verify/verify_vectors.py
```

This script fails the build if any canonical vector is inconsistent.

## Schema

Per-profile schemas are in `schema/`:

```text
schema/
  scope4.schema.json
  compact743.schema.json
  miquel844.schema.json
  projection.schema.json
  activation.schema.json
  delta3.schema.json
  cobs-core.schema.json
  cobs-null-00.schema.json
  cobs-omi-null-ring.schema.json
  cobs-gnomic-fdelta-ring.schema.json
```

## Commit History

Vectors are created in phases:

- D1: Scope4 vectors
- D2: Compact [7,4,3] vectors (generated)
- D3: Miquel [8,4,4] vectors (generated)
- D4: Projection vectors (with identity witnesses)
- D5: Activation vectors (request/result split)
- D6: COBS vectors (parameterized NULL-ring)
- D7: Delta3 temporal coordinate vectors

## Authority

These vectors are **canonical**. They inherit from:

- `00-EXTENSION-AUTHORITY.md`
- `01-COBS-CONS.md`
- `02-EPISTEMIC-CELL.md`
- `03-EPISTEMIC-SCOPE.md`
- `04-LOGOS-NOMOS-PATHOS.md`
- `05-MIQUEL-INTEGRITY.md`
- `06-LL-MM-NN-DELTA-RING.md`

Any conflict between these vectors and an implementation resolves in favor of these vectors.
