#!/usr/bin/env bash
set -euo pipefail

proofs=$(cd -- "$(dirname -- "$0")" && pwd)
cd -- "${1:?pass the pinned OpenSymbolicRules/Lean checkout}"
revision=$(cat "$proofs/lean-revision")
if [[ $(git rev-parse HEAD) != "$revision" ]]; then
    echo "Expected OpenSymbolicRules/Lean at $revision" >&2
    exit 1
fi

baseline=(OSRTest/LinearAlgebraPilot.lean OSRTest/LinearAlgebraCounterexamples.lean)
git diff --exit-code HEAD -- lean-toolchain lake-manifest.json lakefile.toml "${baseline[@]}"
mathlib=$(python3 -c 'import json; print(next(p["rev"] for p in json.load(open("lake-manifest.json"))["packages"] if p["name"] == "mathlib"))')
if [[ $(git -C .lake/packages/mathlib rev-parse HEAD) != "$mathlib" ]]; then
    echo "Expected Mathlib at $mathlib" >&2
    exit 1
fi

lake env lean --version
for source in "${baseline[@]}" "$proofs"/MatrixExponential.lean "$proofs"/PilotFormulations.lean; do
    echo "Checking $source"
    lake env lean -DwarningAsError=true "$source"
done
