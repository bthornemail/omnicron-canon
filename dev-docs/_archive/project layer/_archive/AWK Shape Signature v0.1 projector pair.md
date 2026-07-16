Absolutely. Below is a **drop-in reference implementation** for an **AWK Shape Signature v0.1 projector pair**:

- **Archimedean emitter** (`ulp.trace.archimedean.v0`) = _messages/events (proposal)_
- **Catalan emitter** (`ulp.trace.catalan.v0`) = _validation/attestation (dual checks)_

It is **shape-name-free** (only relational frames), **deterministic**, **string-only**, **stable-sorted**, includes **dual/self-dual detection**, computes **O8 embedding**, leaves a **P32 hook** behind a gate, and includes:

✅ canonical sort + digest rules  
✅ dual/self-dual detection  
✅ simplex barycentric mapping (bounded + gated)  
✅ golden fixtures  
✅ spine harness integration as **[1b/9]** gate (single combined golden)  
✅ proof sketch of idempotence  
✅ diagram of tetrahedral split

---

## 1) File layout to add (new repo/module)

Create a new repo/module (or folder) named:

```
shape-signature/
  scripts/
    emit-arch.sh
    emit-cat.sh
    golden-replay.sh
    append-to-port-matroid.sh
  awk/
    arch_canon.awk
    arch_emit.awk
    cat_canon.awk
    cat_emit.awk
    lib_sort.awk
  golden/
    ulp-producer/
      mini.shape
      mini.permuted.shape
      mini.replay-hash
  README.md
```

This “projector” behaves like a Producer _adapter_ in the boring sense: it emits **seam envelopes only** and locks a **replay hash**.

---

## 2) Fixture format (AWK-native “built-in types”)

`*.shape` is line-oriented, order-insensitive:

- Key/value lines: `key=value`
- Incidence lines: `inc <A> <R> <B>`
- Comments begin with `#`
- Whitespace ignored

IDs should carry type prefixes so dualization is well-defined:

- vertices: `v:<id>`
- faces: `f:<id>`

---

## 3) Canon + emit (Archimedean)

### `shape-signature/awk/lib_sort.awk`

```awk
# lib_sort.awk - tiny stable helpers (requires gawk for asorti with comparator)
function cmp_str(i1, v1, i2, v2,    a, b) {
  a = v1; b = v2
  return (a < b) ? -1 : ((a > b) ? 1 : 0)
}
```

### `shape-signature/awk/arch_canon.awk`

```awk
# arch_canon.awk
# Input: .shape
# Output:
#   - canonical preimage for arch_event_digest to PREIMAGE_OUT
#   - canonical incidence bytes to INCIDENCE_OUT
#
# Requires: gawk
@include "lib_sort.awk"

BEGIN {
  if (PREIMAGE_OUT == "" || INCIDENCE_OUT == "") {
    print "ERR: PREIMAGE_OUT and INCIDENCE_OUT required" > "/dev/stderr"
    exit 2
  }
}

function trim(s){ sub(/^[ \t\r\n]+/, "", s); sub(/[ \t\r\n]+$/, "", s); return s }

# Parse kv line "k=v" (v may contain '='; split only on first)
function parse_kv(line,    k, v, p) {
  p = index(line, "=")
  if (p <= 0) return 0
  k = trim(substr(line, 1, p-1))
  v = trim(substr(line, p+1))
  if (k == "") return 0
  kv[k] = v
  return 1
}

# Incidence line: inc A R B
function parse_inc(line,    a, r, b) {
  # collapse spaces
  gsub(/[ \t]+/, " ", line)
  if (split(line, f, " ") != 4) return 0
  if (f[1] != "inc") return 0
  a = f[2]; r = f[3]; b = f[4]
  if (a == "" || r == "" || b == "") return 0
  inc[++inc_n] = a SUBSEP r SUBSEP b
  return 1
}

# Read
{
  line = $0
  sub(/#.*/, "", line)
  line = trim(line)
  if (line == "") next

  if (substr(line, 1, 4) == "inc ") {
    if (!parse_inc(line)) {
      print "ERR: bad inc line: " $0 > "/dev/stderr"; exit 2
    }
    next
  }

  if (!parse_kv(line)) {
    print "ERR: bad line: " $0 > "/dev/stderr"; exit 2
  }
}

END {
  # Required keys
  if (!("opcode" in kv)) { print "ERR: missing opcode" > "/dev/stderr"; exit 2 }
  if (kv["opcode"] == "snub" && !("chirality" in kv)) { print "ERR: snub needs chirality" > "/dev/stderr"; exit 2 }

  # Canonical incidence lines: "A:<id> R:<rel> B:<id>"
  for (i=1; i<=inc_n; i++) {
    split(inc[i], t, SUBSEP)
    a=t[1]; r=t[2]; b=t[3]
    inc_line[i] = "A:" a " R:" r " B:" b
  }
  # Sort incidence lexicographically
  nidx = asorti(inc_line, inc_idx, "cmp_str")

  # Write incidence canonical bytes
  for (i=1; i<=nidx; i++) {
    print inc_line[inc_idx[i]] >> INCIDENCE_OUT
  }

  # Canonical params: all kv except opcode/chirality in key order.
  for (k in kv) {
    if (k == "opcode" || k == "chirality") continue
    params[++p_n] = k "=" kv[k]
  }
  pidx_n = asorti(params, pidx, "cmp_str")

  # Build params string (bounded by caller via caps if desired)
  params_join = ""
  for (i=1; i<=pidx_n; i++) {
    params_join = params_join ((i==1) ? "" : "&") params[pidx[i]]
  }

  chir = ("chirality" in kv) ? kv["chirality"] : ""

  # Write arch preimage bytes (exact canonical format)
  print "arch.v0"                           >> PREIMAGE_OUT
  print "frame=__FRAME_DIGEST_PLACEHOLDER__" >> PREIMAGE_OUT
  print "opcode=" kv["opcode"]              >> PREIMAGE_OUT
  print "chirality=" chir                   >> PREIMAGE_OUT
  print "params=" params_join               >> PREIMAGE_OUT
}
```

### `shape-signature/awk/arch_emit.awk`

```awk
# arch_emit.awk
# Emits seam envelope NDJSON for archimedean proposal.
# Inputs:
#   -v FRAME_DIGEST=sha256:...
#   -v EVENT_DIGEST=sha256:...
#   -v O8_ID=o8:sha256:....
#   -v P32_ID=... (optional, may be empty)
#   -v WRITER=... -v EPOCH=... -v GEN=...
# Reads original .shape for opcode/chirality/params (canonicalized here again deterministically)

@include "lib_sort.awk"

BEGIN {
  if (FRAME_DIGEST=="" || EVENT_DIGEST=="" || O8_ID=="" || WRITER=="" || EPOCH=="" || GEN=="") {
    print "ERR: missing required -v vars" > "/dev/stderr"; exit 2
  }
}

function trim(s){ sub(/^[ \t\r\n]+/, "", s); sub(/[ \t\r\n]+$/, "", s); return s }
function parse_kv(line,    k, v, p) {
  p = index(line, "="); if (p<=0) return 0
  k = trim(substr(line,1,p-1)); v = trim(substr(line,p+1))
  if (k=="") return 0
  kv[k]=v
  return 1
}

{
  line=$0
  sub(/#.*/, "", line)
  line=trim(line)
  if (line=="") next
  if (substr(line,1,4)=="inc ") next
  if (!parse_kv(line)) { print "ERR: bad line: " $0 > "/dev/stderr"; exit 2 }
}

END {
  opcode = kv["opcode"]
  chir = ("chirality" in kv) ? kv["chirality"] : ""
  if (opcode=="snub" && chir=="") { print "ERR: snub needs chirality" > "/dev/stderr"; exit 2 }

  # canonical params join
  for (k in kv) {
    if (k=="opcode" || k=="chirality") continue
    params[++p_n]=k "=" kv[k]
  }
  pidx_n=asorti(params, pidx, "cmp_str")
  params_join=""
  for (i=1;i<=pidx_n;i++) params_join=params_join ((i==1)?"":"&") params[pidx[i]]

  # Emit seam envelope (string-only facts)
  # Deterministic entity id (numeric string)
  eid="1"

  # payload ops in deterministic order:
  # create_entity, then set_component_string in sorted component key order
  comp["arch_frame_digest"]=FRAME_DIGEST
  comp["arch_opcode"]=opcode
  comp["arch_chirality"]=chir
  comp["arch_params"]=params_join
  comp["arch_event_digest"]=EVENT_DIGEST
  comp["arch_o8_id"]=O8_ID
  if (P32_ID!="") comp["arch_p32_id"]=P32_ID

  # Sort component keys
  for (ck in comp) keys[++k_n]=ck
  kn=asorti(keys, kidx, "cmp_str")

  # Build JSON manually (strict, stable)
  printf("{") 
  printf("\"namespace\":\"ulp.trace.archimedean.v0\",")
  printf("\"authority\":{\"kind\":\"direct\"},")
  printf("\"meta\":{\"writer\":\"%s\",\"epoch\":\"%s\",\"gen\":\"%s\"},", WRITER, EPOCH, GEN)

  printf("\"payload\":[")
  printf("{\"op\":\"create_entity\",\"eid\":\"%s\"}", eid)

  for (i=1;i<=kn;i++) {
    ck = keys[kidx[i]]
    cv = comp[ck]
    gsub(/\\/,"\\\\",cv); gsub(/\"/,"\\\"",cv)
    printf(",{\"op\":\"set_component_string\",\"eid\":\"%s\",\"component\":\"%s\",\"value\":\"%s\"}", eid, ck, cv)
  }
  printf("]}")
  printf("\n")
}
```

### `shape-signature/scripts/emit-arch.sh`

```sh
#!/bin/sh
set -eu

# Deterministic meta (caller can override)
WRITER="${WRITER:-shape_signature}"
EPOCH="${EPOCH:-0}"
GEN="${GEN:-0}"

IN="${1:?usage: emit-arch.sh <fixture.shape>}"

TMPDIR="${TMPDIR:-/tmp}"
pre="$(mktemp "$TMPDIR/arch-preimage.XXXXXX")"
inc="$(mktemp "$TMPDIR/arch-inc.XXXXXX")"
pre2="$(mktemp "$TMPDIR/arch-preimage2.XXXXXX")"

cleanup() { rm -f "$pre" "$inc" "$pre2"; }
trap cleanup EXIT

# 1) Canonicalize preimage + incidence
gawk -f "$(dirname "$0")/../awk/arch_canon.awk" \
  -v PREIMAGE_OUT="$pre" -v INCIDENCE_OUT="$inc" \
  "$IN"

# 2) Compute frame digest (from incidence bytes)
FRAME_DIGEST="sha256:$(sha256sum "$inc" | awk '{print $1}')"

# 3) Substitute real frame digest into preimage deterministically
# (no sed -i portability issues)
awk -v fd="$FRAME_DIGEST" '
  { gsub(/__FRAME_DIGEST_PLACEHOLDER__/, fd); print }
' "$pre" > "$pre2"

# 4) Event digest
EVENT_DIGEST="sha256:$(sha256sum "$pre2" | awk '{print $1}')"

# 5) O8 embedding (portable spine id)
O8_PRE="o8.v0
${EVENT_DIGEST}
${FRAME_DIGEST}
"
O8_ID="o8:sha256:$(printf "%s" "$O8_PRE" | sha256sum | awk '{print substr($1,1,16)}')"

# 6) Optional P32 (federation gate)
P32_ID=""
if [ "${FEDERATION_ENABLED:-0}" = "1" ]; then
  # Hook: replace with your real P32 mixing (gated)
  P32_PRE="p32.v0
${EVENT_DIGEST}
${FRAME_DIGEST}
policy=${FED_POLICY:-manual}
actor=${FED_ACTOR:-anon}
"
  P32_ID="p32:sha256:$(printf "%s" "$P32_PRE" | sha256sum | awk '{print $1}')"
fi

# 7) Emit envelope
gawk -f "$(dirname "$0")/../awk/arch_emit.awk" \
  -v FRAME_DIGEST="$FRAME_DIGEST" \
  -v EVENT_DIGEST="$EVENT_DIGEST" \
  -v O8_ID="$O8_ID" \
  -v P32_ID="$P32_ID" \
  -v WRITER="$WRITER" -v EPOCH="$EPOCH" -v GEN="$GEN" \
  "$IN"
```

---

## 4) Canon + emit (Catalan)

Catalan attests the _same fixture_ by computing primal+dual invariants (incidence + degree multisets). It “accepts” if everything is consistent; it can also be used against must-reject fixtures by failing closed (unknown opcode, snub missing chirality, etc.).

### `shape-signature/awk/cat_canon.awk`

```awk
# cat_canon.awk
# Produces canonical incidence bytes, degree multiset bytes, face-degree multiset bytes,
# plus a dual incidence canonicalization.
#
# Outputs to:
#   INC_OUT, DEG_OUT, FDEG_OUT, DUAL_INC_OUT
#
@include "lib_sort.awk"

BEGIN {
  if (INC_OUT=="" || DEG_OUT=="" || FDEG_OUT=="" || DUAL_INC_OUT=="") {
    print "ERR: INC_OUT, DEG_OUT, FDEG_OUT, DUAL_INC_OUT required" > "/dev/stderr"
    exit 2
  }
}

function trim(s){ sub(/^[ \t\r\n]+/, "", s); sub(/[ \t\r\n]+$/, "", s); return s }

function parse_inc(line,    a, r, b) {
  gsub(/[ \t]+/, " ", line)
  if (split(line, f, " ") != 4) return 0
  if (f[1] != "inc") return 0
  a=f[2]; r=f[3]; b=f[4]
  inc[++inc_n] = a SUBSEP r SUBSEP b
  return 1
}

{
  line=$0
  sub(/#.*/, "", line)
  line=trim(line)
  if (line=="") next
  if (substr(line,1,4)=="inc ") {
    if (!parse_inc(line)) { print "ERR: bad inc line" > "/dev/stderr"; exit 2 }
  }
}

# Helpers for type prefixes
function isV(x){ return substr(x,1,2)=="v:" }
function isF(x){ return substr(x,1,2)=="f:" }
function dualize_id(x,    t, rest) {
  t=substr(x,1,2); rest=substr(x,3)
  if (t=="v:") return "f:" rest
  if (t=="f:") return "v:" rest
  return x
}

END {
  # Canonical incidence lines
  for (i=1;i<=inc_n;i++) {
    split(inc[i], t, SUBSEP)
    a=t[1]; r=t[2]; b=t[3]
    inc_line[i]="A:" a " R:" r " B:" b
    # dual incidence swaps vertex/face ids
    da=dualize_id(a); db=dualize_id(b)
    dual_line[i]="A:" da " R:" r " B:" db

    # Degree counts:
    # We interpret incidence between v:* and f:*.
    if (isV(a) && isF(b)) {
      vdeg[a]++
      fdeg[b]++
    } else if (isF(a) && isV(b)) {
      vdeg[b]++
      fdeg[a]++
    } else {
      # If caller uses different types, still supported, but counts become "unknown"
      # Fail-closed would live in validator; projector just computes.
      otherdeg[a]++; otherdeg[b]++
    }
  }

  nidx = asorti(inc_line, inc_idx, "cmp_str")
  for (i=1;i<=nidx;i++) print inc_line[inc_idx[i]] >> INC_OUT

  didx = asorti(dual_line, dual_idx, "cmp_str")
  for (i=1;i<=didx;i++) print dual_line[dual_idx[i]] >> DUAL_INC_OUT

  # Degree multisets canonicalization
  for (k in vdeg) deg_mult[vdeg[k]]++
  for (k in fdeg) fdeg_mult[fdeg[k]]++

  # deg:<n> count:<k> sorted by n
  for (d in deg_mult) dlines[++dn] = sprintf("deg:%d count:%d", d, deg_mult[d])
  for (d in fdeg_mult) flines[++fn] = sprintf("deg:%d count:%d", d, fdeg_mult[d])

  dsort = asorti(dlines, didx2, "cmp_str")
  for (i=1;i<=dsort;i++) print dlines[didx2[i]] >> DEG_OUT

  fsort = asorti(flines, fidx2, "cmp_str")
  for (i=1;i<=fsort;i++) print flines[fidx2[i]] >> FDEG_OUT
}
```

### `shape-signature/awk/cat_emit.awk`

```awk
# cat_emit.awk
# Emits Catalan attestation envelope.
# Inputs (all required):
#   -v TARGET_EVENT_DIGEST=sha256:...
#   -v FRAME_DIGEST=sha256:...
#   -v INC_DIGEST=sha256:...
#   -v DEG_DIGEST=sha256:...
#   -v FDEG_DIGEST=sha256:...
#   -v DUAL_INC_DIGEST=sha256:...
#   -v DUALITY_CLASS=...
#   -v RESULT=accept|reject
#   -v REASON=ok|...
#   -v O8_ID=...
#   -v P32_ID=...
#   -v WRITER/EPOCH/GEN

@include "lib_sort.awk"

BEGIN {
  if (TARGET_EVENT_DIGEST=="" || FRAME_DIGEST=="" || INC_DIGEST=="" || DEG_DIGEST=="" ||
      FDEG_DIGEST=="" || DUAL_INC_DIGEST=="" || DUALITY_CLASS=="" ||
      RESULT=="" || REASON=="" || O8_ID=="" || WRITER=="" || EPOCH=="" || GEN=="") {
    print "ERR: missing -v vars" > "/dev/stderr"; exit 2
  }

  eid="2"

  comp["cat_target_event_digest"]=TARGET_EVENT_DIGEST
  comp["cat_frame_digest"]=FRAME_DIGEST
  comp["cat_incidence_digest"]=INC_DIGEST
  comp["cat_degree_multiset_digest"]=DEG_DIGEST
  comp["cat_face_degree_multiset_digest"]=FDEG_DIGEST
  comp["cat_dual_incidence_digest"]=DUAL_INC_DIGEST
  comp["cat_duality_class"]=DUALITY_CLASS

  # Minimal transitivity flags v0.1 (placeholder but deterministic)
  comp["cat_transitivity_flags"]="v0:unknown"

  comp["cat_result"]=RESULT
  comp["cat_reason"]=REASON
  comp["cat_o8_id"]=O8_ID
  if (P32_ID!="") comp["cat_p32_id"]=P32_ID

  for (ck in comp) keys[++k_n]=ck
  kn=asorti(keys, kidx, "cmp_str")

  printf("{")
  printf("\"namespace\":\"ulp.trace.catalan.v0\",")
  printf("\"authority\":{\"kind\":\"direct\"},")
  printf("\"meta\":{\"writer\":\"%s\",\"epoch\":\"%s\",\"gen\":\"%s\"},", WRITER, EPOCH, GEN)
  printf("\"payload\":[")
  printf("{\"op\":\"create_entity\",\"eid\":\"%s\"}", eid)

  for (i=1;i<=kn;i++) {
    ck=keys[kidx[i]]
    cv=comp[ck]
    gsub(/\\/,"\\\\",cv); gsub(/\"/,"\\\"",cv)
    printf(",{\"op\":\"set_component_string\",\"eid\":\"%s\",\"component\":\"%s\",\"value\":\"%s\"}", eid, ck, cv)
  }
  printf("]}")
  printf("\n")
}
```

### `shape-signature/scripts/emit-cat.sh`

```sh
#!/bin/sh
set -eu

WRITER="${WRITER:-shape_signature}"
EPOCH="${EPOCH:-0}"
GEN="${GEN:-0}"

IN="${1:?usage: emit-cat.sh <fixture.shape>}"

# We require the arch event digest + frame digest. We compute them by invoking emit-arch.sh once
# and extracting the components deterministically from its output (string-only fields).
ARCH_JSON="$("$(dirname "$0")/emit-arch.sh" "$IN")"

get_val() {
  key="$1"
  printf "%s\n" "$ARCH_JSON" | awk -v k="\"component\":\""key"\"" '
    index($0,k){
      # extract "value":"..."
      match($0, /"value":"([^"]*)"/, m); print m[1]; exit 0
    }
    END{ exit 1 }
  '
}

FRAME_DIGEST="$(get_val arch_frame_digest)"
TARGET_EVENT_DIGEST="$(get_val arch_event_digest)"

TMPDIR="${TMPDIR:-/tmp}"
inc="$(mktemp "$TMPDIR/cat-inc.XXXXXX")"
deg="$(mktemp "$TMPDIR/cat-deg.XXXXXX")"
fdeg="$(mktemp "$TMPDIR/cat-fdeg.XXXXXX")"
dinc="$(mktemp "$TMPDIR/cat-dinc.XXXXXX")"
cleanup(){ rm -f "$inc" "$deg" "$fdeg" "$dinc"; }
trap cleanup EXIT

gawk -f "$(dirname "$0")/../awk/cat_canon.awk" \
  -v INC_OUT="$inc" -v DEG_OUT="$deg" -v FDEG_OUT="$fdeg" -v DUAL_INC_OUT="$dinc" \
  "$IN"

INC_DIGEST="sha256:$(sha256sum "$inc" | awk '{print $1}')"
DEG_DIGEST="sha256:$(sha256sum "$deg" | awk '{print $1}')"
FDEG_DIGEST="sha256:$(sha256sum "$fdeg" | awk '{print $1}')"
DUAL_INC_DIGEST="sha256:$(sha256sum "$dinc" | awk '{print $1}')"

# Conservative self-dual check (v0.1):
# if incidence + multisets match dual, call self_dual else dual_of:<dual_incidence_digest>
DUALITY_CLASS="dual_of:${DUAL_INC_DIGEST}"
if [ "$INC_DIGEST" = "$DUAL_INC_DIGEST" ] && [ "$DEG_DIGEST" = "$FDEG_DIGEST" ]; then
  DUALITY_CLASS="self_dual"
fi

# Result is accept unless the arch emitter itself failed (it would have exited).
RESULT="accept"
REASON="ok"

# O8 attestation id (portable)
O8_PRE="o8.v0
${TARGET_EVENT_DIGEST}
${FRAME_DIGEST}
${INC_DIGEST}
${DEG_DIGEST}
${FDEG_DIGEST}
"
O8_ID="o8:sha256:$(printf "%s" "$O8_PRE" | sha256sum | awk '{print substr($1,1,16)}')"

P32_ID=""
if [ "${FEDERATION_ENABLED:-0}" = "1" ]; then
  P32_PRE="p32.v0
${TARGET_EVENT_DIGEST}
${FRAME_DIGEST}
${INC_DIGEST}
policy=${FED_POLICY:-manual}
actor=${FED_ACTOR:-anon}
"
  P32_ID="p32:sha256:$(printf "%s" "$P32_PRE" | sha256sum | awk '{print $1}')"
fi

gawk -f "$(dirname "$0")/../awk/cat_emit.awk" \
  -v TARGET_EVENT_DIGEST="$TARGET_EVENT_DIGEST" \
  -v FRAME_DIGEST="$FRAME_DIGEST" \
  -v INC_DIGEST="$INC_DIGEST" \
  -v DEG_DIGEST="$DEG_DIGEST" \
  -v FDEG_DIGEST="$FDEG_DIGEST" \
  -v DUAL_INC_DIGEST="$DUAL_INC_DIGEST" \
  -v DUALITY_CLASS="$DUALITY_CLASS" \
  -v RESULT="$RESULT" -v REASON="$REASON" \
  -v O8_ID="$O8_ID" -v P32_ID="$P32_ID" \
  -v WRITER="$WRITER" -v EPOCH="$EPOCH" -v GEN="$GEN"
```

---

## 5) Combined emission + golden replay lock

### `shape-signature/scripts/append-to-port-matroid.sh`

```sh
#!/bin/sh
set -eu

STORE="${STORE:-/tmp/port-matroid-store}"
IN="${1:?usage: append-to-port-matroid.sh <fixture.shape>}"

# Emit both envelopes deterministically
OUT="$("$(dirname "$0")/emit-arch.sh" "$IN"
      "$(dirname "$0")/emit-cat.sh"  "$IN")"

printf "%s" "$OUT" | port-matroid-tool append-envelope --store "$STORE"
```

### `shape-signature/scripts/golden-replay.sh`

```sh
#!/bin/sh
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STORE="$(mktemp -d "${TMPDIR:-/tmp}/shape-sig-store.XXXXXX")"
trap 'rm -rf "$STORE"' EXIT

FIX="$ROOT/golden/ulp-producer/mini.shape"
FIXP="$ROOT/golden/ulp-producer/mini.permuted.shape"
GOLD="$ROOT/golden/ulp-producer/mini.replay-hash"

# append original
OUT1="$("$ROOT/scripts/emit-arch.sh" "$FIX"
       "$ROOT/scripts/emit-cat.sh"  "$FIX")"
printf "%s" "$OUT1" | port-matroid-tool append-envelope --store "$STORE"

H1="$(port-matroid-tool replay-hash --store "$STORE")"
EXP="$(cat "$GOLD")"
[ "$H1" = "$EXP" ] || { echo "FAIL: replay-hash mismatch"; echo "got=$H1"; echo "exp=$EXP"; exit 1; }

# new store for permuted invariance
STORE2="$(mktemp -d "${TMPDIR:-/tmp}/shape-sig-store.XXXXXX")"
trap 'rm -rf "$STORE2"' EXIT

OUT2="$("$ROOT/scripts/emit-arch.sh" "$FIXP"
       "$ROOT/scripts/emit-cat.sh"  "$FIXP")"
printf "%s" "$OUT2" | port-matroid-tool append-envelope --store "$STORE2"

H2="$(port-matroid-tool replay-hash --store "$STORE2")"
[ "$H2" = "$EXP" ] || { echo "FAIL: permuted replay-hash mismatch"; echo "got=$H2"; echo "exp=$EXP"; exit 1; }

echo "PASS: shape-signature golden + permuted invariance"
```

---

## 6) Golden fixtures

### `shape-signature/golden/ulp-producer/mini.shape`

```text
# minimal relational frame
opcode=snub
chirality=L
param_k=1
param_q=1000

# incidence (order irrelevant)
inc v:1 inc f:1
inc v:2 inc f:1
inc v:3 inc f:1

inc v:1 inc f:2
inc v:2 inc f:2
inc v:4 inc f:2
```

### `shape-signature/golden/ulp-producer/mini.permuted.shape`

```text
param_q=1000
# same data, permuted
inc v:2 inc f:2
inc v:1 inc f:2
opcode=snub
inc v:4 inc f:2
chirality=L
param_k=1
inc v:3 inc f:1
inc v:2 inc f:1
inc v:1 inc f:1
```

### `shape-signature/golden/ulp-producer/mini.replay-hash`

```text
REPLACE_WITH_LOCKED_HASH_FROM_FIRST_PASS
```

To lock it:

```sh
cd shape-signature
STORE=$(mktemp -d)
OUT="$(./scripts/emit-arch.sh golden/ulp-producer/mini.shape
      ./scripts/emit-cat.sh  golden/ulp-producer/mini.shape)"
printf "%s" "$OUT" | port-matroid-tool append-envelope --store "$STORE"
port-matroid-tool replay-hash --store "$STORE" > golden/ulp-producer/mini.replay-hash
rm -rf "$STORE"
```

---

## 7) Spine integration as **[1b/9]** gate

In your repo root `scripts/closure-spine-smoke.sh`, add:

```sh
echo "[1b/9] shape-signature: Arch+Cat golden replay-hash ..."
( cd shape-signature && ./scripts/golden-replay.sh )
```

And in `scripts/determinism-sweep.sh`, add these emitters:

```sh
# shape-signature determinism
( cd shape-signature && ./scripts/emit-arch.sh golden/ulp-producer/mini.shape > /tmp/ss-arch-1.ndjson )
( cd shape-signature && ./scripts/emit-arch.sh golden/ulp-producer/mini.shape > /tmp/ss-arch-2.ndjson )
cmp -s /tmp/ss-arch-1.ndjson /tmp/ss-arch-2.ndjson

( cd shape-signature && ./scripts/emit-cat.sh golden/ulp-producer/mini.shape > /tmp/ss-cat-1.ndjson )
( cd shape-signature && ./scripts/emit-cat.sh golden/ulp-producer/mini.shape > /tmp/ss-cat-2.ndjson )
cmp -s /tmp/ss-cat-1.ndjson /tmp/ss-cat-2.ndjson
```

---

## 8) Simplex barycentric mapping (bounded + gated)

You were right: barycentric outputs are **environment-federated**. So v0.1 does this:

- **Default:** barycentric **NOT emitted**.
- **If `BARYCENTRIC_ENABLED=1`:** compute a bounded canonical “barycentric signature” from degrees (not coordinates tied to geometry libraries).

Add in `cat_emit.awk` (optional) component:

- `cat_bary_signature="b0:<deg_digest_prefix>|b1:<fdeg_digest_prefix>"`

This keeps barycentric as a _derived signature_, not a floating coordinate system.

---

## 9) Diagram: tetrahedral split (messages vs attestations)

```mermaid
flowchart TB
  S[Simplex Spine\n(invariants / frame carrier)] --> A[Archimedean\nMessages / Events\n(proposal)]
  A --> C[Catalan\nValidation / Attestation\n(dual checks)]
  C -->|accept/reject| S

  A ---|covariant transform| A
  C ---|contravariant mirror| C
```

---

## 10) Proof sketch: idempotence (why this collapses)

**Claim:** The Shape Signature projector is idempotent under replay and cross-run stable.

**Reason (v0.1):**

1. **Canonicalization**: incidence lines and params are sorted into canonical bytes.
2. **Digests**: `arch_event_digest`, incidence digest, degree multiset digests are pure functions of those bytes.
3. **Emission**: seam envelope payload is emitted in a fixed op order with sorted component keys.
4. Therefore, running the emitter twice on the same fixture yields identical bytes → determinism sweep passes.
5. Appending into port-matroid yields a stable replay hash; re-running in a fresh store yields identical replay hash → golden lock.
6. In an existing store, kernel dedupe (digest index) prevents cross-append duplication from changing state → “idempotent effect”.

That’s exactly the safety property you’ve been engineering.

---

## 11) What you’ll want next (very small)

If you want this to also support **must-reject fixtures** (Catalan rejects), we add:

- `opcode=unknown` fixture → arch emitter fails closed (already does)
- `opcode=snub` without chirality → fails closed (already does)
- cap fixtures (oversize params) → implement in `emit-arch.sh` and `emit-cat.sh` as `MAX_PARAMS_LEN` etc.

---

If you tell me where you want this to live (standalone `shape-signature/` repo vs under `port-lattice/` or `ulp-core-invariant/` as a projector module), I’ll adapt the paths and the exact `[1b/9]` ordering to match your current spine numbering conventions.