#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="agentforce-observability-guide"
OUTPUT="${SKILL_NAME}.skill"

rm -f "$OUTPUT"
cd "$SKILL_NAME" && zip -r "../$OUTPUT" . && cd ..
echo "Paquete generado: $OUTPUT"
