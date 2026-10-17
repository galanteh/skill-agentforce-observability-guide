#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="agentforce-observability-guide"
OUTPUT="${SKILL_NAME}.skill"

rm -f "$OUTPUT"
zip -r "$OUTPUT" "$SKILL_NAME/"
echo "Paquete generado: $OUTPUT"
