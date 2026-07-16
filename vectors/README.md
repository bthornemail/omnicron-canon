# Omnicron Conformance Vectors

This directory contains the canonical conformance vectors for the Omnicron extension.

## Purpose

These vectors define expected behavior for:

- Scope4 encoding/decoding
- Compact Hamming [7,4,3] integrity
- Miquel [8,4,4] integrity
- Projection masks
- Activation requests/results
- COBS framing

## Consumer Policy

Each repository should **consume** these vectors, not copy-edit them.

```text
omnicron-port
  projection and non-authority vectors

omnicron-isa
  Scope4, compact743, miquel844, cobs vectors

omnicron-lisp
  scope4, projection, activation vectors
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
```

## Vector Files

| File | Description | Consumed By |
|------|-------------|-------------|
| `scope4.yaml` | All 16 Scope4 combinations + invalid cases | omnicron-isa, omnicron-lisp |
| `compact743.yaml` | Compact [7,4,3] Hamming vectors | omnicron-isa |
| `miquel844.yaml` | Miquel [8,4,4] integrity vectors | omnicron-isa |
| `projection.yaml` | All 16 projection masks | omnicron-port, omnicron-lisp |
| `activation.yaml` | Activation request/result vectors | omnicron-lisp |
| `cobs.yaml` | COBS framing vectors | omnicron-isa |

## Schema

Each vector file follows the schema in `schema/vector.schema.json`.

## Commit History

Vectors are created in phases:

- D1: Scope4 vectors
- D2: Compact [7,4,3] vectors
- D3: Miquel [8,4,4] vectors
- D4: Projection vectors
- D5: Activation vectors
- D6: COBS vectors

## Authority

These vectors are **canonical**. They inherit from:

- `00-EXTENSION-AUTHORITY.md`
- `01-COBS-CONS.md`
- `02-EPISTEMIC-CELL.md`
- `03-EPISTEMIC-SCOPE.md`
- `04-LOGOS-NOMOS-PATHOS.md`
- `05-MIQUEL-INTEGRITY.md`
- `06-EPISTEMIC-ACTIVATION.md`

Any conflict between these vectors and an implementation resolves in favor of these vectors.
