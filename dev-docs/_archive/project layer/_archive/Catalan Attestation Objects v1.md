Alright — I’m going to write this as a **real RFC**, in the style of your spine specs:

- normative language (MUST / SHOULD / MAY)
- explicit object model
- wire format
- failure rules
- federation semantics
- relationship to Pfister / growth / tetrahedral model
- executable implications

No metaphors inside the RFC body — just the math + protocol.

After the RFC I’ll add a short interpretation section tying it back to your geometry language.

---

# RFC: Catalan Attestation Objects v1

**Status:** Draft  
**Version:** 1.0  
**Authoritative Namespace:** `ulp.attestation.catalan.v1`  
**Compatibility Class:** Spine Tier-1 Validation Surface  
**Applies to:** Federation sync, reorg authorization, segment validation, capability attestation

---

## 0. Abstract

Catalan Attestation Objects (CAO) define a deterministic, fail-closed validation structure for distributed federation.

A CAO is a canonical, idempotent object that:

- attests to a segment, fork, or state projection
- binds identity to validation evidence
- encodes contravariant verification
- prevents ambiguous acceptance
- composes under replay
- survives federation transport unchanged

Catalan attestation is the **validation dual** to Platonic projection and Archimedean transformation.

If projection expands the system, Catalan attestation collapses it back to truth.

---

## 1. Design Goals

A valid Catalan attestation MUST:

1. Be byte-stable and replayable
2. Be deterministic across nodes
3. Be idempotent
4. Fail closed
5. Preserve evidence
6. Survive reorg
7. Encode validation topology
8. Compose in Pfister space
9. Not depend on clock time
10. Not depend on transport order

---

## 2. Terminology

### 2.1 Validation Direction

Catalan objects represent **contravariant flow**:

```
Projection → Growth → Validation → Collapse
```

Projection expands. Catalan collapses.

Catalan attestation is a _proof surface_.

---

### 2.2 Catalan Class

Catalan class is the dual of an Archimedean transform.

If Archimedean objects describe how something grows, Catalan objects describe why it is allowed to exist.

---

## 3. Object Structure

A Catalan Attestation Object is a canonical JSON object:

```
{
  "namespace": "ulp.attestation.catalan.v1",
  "anchor": { ... },
  "subject": { ... },
  "evidence": { ... },
  "verdict": "...",
  "digest": "sha256:...",
  "policy": "...",
  "actor": "...",
  "pfister": { ... }
}
```

Key-set is exact. Unknown keys MUST cause rejection.

---

## 4. Fields

### 4.1 namespace

MUST equal:

```
ulp.attestation.catalan.v1
```

Reject otherwise.

---

### 4.2 anchor

Defines validation root.

```
"anchor": {
  "seq": integer,
  "hash": "sha256:..."
}
```

This is the checkpoint reference.

Attestation is invalid if anchor cannot be resolved locally.

---

### 4.3 subject

Describes what is being validated.

```
"subject": {
  "type": "segment" | "fork" | "projection" | "receipt",
  "digest": "sha256:..."
}
```

Digest MUST match computed bytes of subject object.

---

### 4.4 evidence

Evidence is deterministic and replayable.

```
"evidence": {
  "segment_digest": "...",
  "selection_digest": "...",
  "receipt_digest": "...",
  "component_hashes": [...]
}
```

All evidence digests MUST match recomputation.

Evidence MUST be transport-independent.

---

### 4.5 verdict

```
"verdict": "accept" | "reject"
```

Accept = subject is valid Reject = subject is provably invalid

No third state allowed.

---

### 4.6 policy

Allowed policies:

```
manual
majority_peer
stake_weighted
deterministic_kernel
```

Unknown policy MUST reject.

---

### 4.7 actor

Opaque string identifying attestor.

Actor is not trusted. Only evidence is trusted.

---

### 4.8 pfister

Encodes identity collapse embedding.

```
"pfister": {
  "dimension": 32 | 128 | 512 | 2048 | 4096,
  "generator_digest": "sha256:..."
}
```

Pfister dimension defines federation scope.

---

## 5. Canonicalization

Canonical JSON rules:

- UTF-8
- no whitespace significance
- keys sorted lexicographically
- integers base-10
- no floats
- arrays stable-ordered
- digest computed over canonical bytes

Any deviation MUST reject.

---

## 6. Idempotence Law

Let A be a Catalan attestation.

Then:

```
verify(A) = true
verify(verify(A)) = true
```

Attestation validation is idempotent.

A verified object never changes truth value.

---

## 7. Validation Algorithm

A validator MUST:

1. Check key-set exactness
2. Resolve anchor
3. Recompute subject digest
4. Recompute evidence digests
5. Validate policy
6. Validate Pfister generator
7. Compare canonical digest
8. Apply verdict

Failure at any step = reject.

---

## 8. Federation Semantics

Catalan objects are:

- append-only
- replayable
- cacheable
- fork-preserving
- evidence-retaining

A reorg MUST preserve all Catalan attestations.

Attestation is never deleted. Only superseded.

---

## 9. Fork Interaction

If competing subjects exist:

- multiple Catalan objects MAY exist
- federation MUST retain all
- selection layer chooses active branch
- Catalan objects remain historical truth

---

## 10. Security Model

Catalan attestation protects against:

- nondeterministic acceptance
- silent reorg
- evidence erasure
- digest tampering
- fork ambiguity
- replay corruption

It does not protect against:

- dishonest actors (only evidence matters)
- policy disagreement
- social consensus

---

## 11. Pfister Embedding

Catalan objects collapse into Pfister identity space.

Pfister dimension determines federation radius:

|Dimension|Scope|
|---|---|
|32|local identity|
|128|frame|
|512|board|
|2048|federation|
|4096|complex|

Catalan attestation is valid only if Pfister embedding matches federation scope.

---

## 12. Failure Rules

A node MUST reject if:

- key-set mismatch
- digest mismatch
- anchor missing
- evidence mismatch
- policy invalid
- pfister invalid
- canonicalization mismatch

No partial acceptance allowed.

---

## 13. Replay Law

Catalan objects MUST replay identically on:

- different machines
- different OS
- different architecture
- different endian
- different time

If replay differs → reject environment.

---

## 14. Determinism Guarantee

Two correct implementations MUST produce identical bytes.

If not → one implementation is wrong.

---

## 15. Storage Law

Catalan objects are immutable.

Mutation invalidates digest.

New evidence → new object.

---

## 16. Relationship to Spine

Catalan attestation is:

```
contravariant validation surface
```

Spine flow:

```
Producer → Projection → Arch transform → Catalan validation → Pfister collapse
```

---

## 17. Compatibility

Future versions MUST bump namespace:

```
ulp.attestation.catalan.v2
```

v1 readers MUST fail closed on unknown versions.

---

## 18. Minimal Example

```
{
  "namespace": "ulp.attestation.catalan.v1",
  "anchor": { "seq": 42, "hash": "sha256:abc..." },
  "subject": { "type": "segment", "digest": "sha256:def..." },
  "evidence": {
    "segment_digest": "sha256:def...",
    "selection_digest": "sha256:123...",
    "receipt_digest": "sha256:456...",
    "component_hashes": []
  },
  "verdict": "accept",
  "policy": "deterministic_kernel",
  "actor": "node-A",
  "pfister": {
    "dimension": 128,
    "generator_digest": "sha256:789..."
  }
}
```

---

# Interpretation Layer (not part of RFC)

This is your geometry mapping:

- Platonic = forward projection
- Archimedean = transformation space
- Catalan = validation dual
- Pfister = identity collapse
- Tetrahedron = growth vector (V,C,K,I)

Catalan is the “mirror tetrahedron”.

It proves the projection is real.

It’s the validation face of the stellated tetrahedron.

---

If you want, next we can:

✅ AWK Catalan validator  
✅ Haskell Catalan verifier  
✅ spine gate `[2b/9]`  
✅ Catalan golden fixtures  
✅ federation handshake spec  
✅ formal Pfister collapse math  
✅ proof of replay invariance  
✅ diagram of dual tetrahedron  
✅ executable test harness  
✅ integration with selection records and receipts

Just tell me which direction to extend.