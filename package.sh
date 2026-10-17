#!/bin/bash
set -e

echo "Limpiando metadatos y archivos temporales..."
find . -name ".DS_Store" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

OUTPUT="agentforce-observability-guide.skill"
rm -f "$OUTPUT"

echo "Empaquetando $OUTPUT limpio..."
zip -r -X "$OUTPUT" agentforce-observability-guide -x "*.DS_Store" -x "__MACOSX*" -x "*/__pycache__/*"

echo "Listo: $OUTPUT generado sin basura de sistema."
