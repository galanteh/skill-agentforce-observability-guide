# Skill: Guía de Agentforce Observability con marca del cliente

Skill para Claude que genera, para cualquier cliente de Salesforce, una guía personalizada con su marca para activar y usar **Agentforce Observability** (Session Tracing, Agent Analytics, Agent Optimization, Health Monitoring).

La guía incluye:
- HTML interactivo con checklist, progreso y tableros de ejemplo.
- Documento Word (`.docx`) listo para compartir.
- Carpeta lista para desplegar en Netlify (drag & drop).

El logo y los colores del cliente se aplican automáticamente a todos los formatos de salida.

---

## Estructura del proyecto

```
agentforce-observability-guide/
├── SKILL.md                  Instrucciones y configuración del skill (punto de entrada para Claude)
├── assets/
│   ├── guide.template.html   Plantilla HTML de la guía (contiene el contenido y la lógica de inyección de marca)
│   └── salesforce-logo.png   Logo de Salesforce por defecto (se reemplaza con el logo del cliente)
├── references/
│   └── content.md            Referencia técnica: componentes, costos, prerequisitos, activación y fuentes
└── scripts/
    ├── build_guide.py        Script principal: genera HTML, Word y carpeta Netlify
    ├── build_docx.js         Generador del .docx (invocado automáticamente por build_guide.py)
    └── industries.py         Presets de industria: datos ficticios verosímiles para los tableros de ejemplo
```

---

## Requisitos previos

| Herramienta | Versión mínima | Instalación |
|---|---|---|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| Pillow (Python) | Última | `pip install pillow` |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| docx (npm global) | Última | `npm install -g docx` |
| LibreOffice (opcional) | Cualquier reciente | [libreoffice.org](https://www.libreoffice.org/) — solo para convertir a PDF |

---

## Empaquetado del skill

Los archivos `.skill` son archivos comprimidos en formato ZIP con una estructura interna específica: la carpeta `agentforce-observability-guide/` debe quedar en la **raíz** del comprimido.

### Generar el archivo `.skill`

**Opción A — script incluido (recomendado):**

```bash
./package.sh
```

**Opción B — comando directo:**

```bash
zip -r agentforce-observability-guide.skill agentforce-observability-guide
```

Ejecutar desde la **raíz del repositorio** para que la estructura interna sea correcta.

### Instalar el skill en Claude

1. Abrir **Claude Desktop** (o **Claude Code** / **Coworker**).
2. Ir a *Settings → Skills* (o la sección de skills de tu interfaz).
3. Hacer clic en **Cargar skill** y seleccionar `agentforce-observability-guide.skill`.
4. Una vez cargado, Claude reconocerá automáticamente las instrucciones de `SKILL.md`.

---

## Prueba de ejecución local

Para verificar que el entorno está correctamente configurado y ver todas las opciones disponibles:

```bash
python3 agentforce-observability-guide/scripts/build_guide.py --help
```

Ejemplo de generación completa:

```bash
python3 agentforce-observability-guide/scripts/build_guide.py \
  --client "Acme Corp" \
  --logo /ruta/al/logo.png \
  --industry retail \
  --contact-name "María García" \
  --contact-email maria@salesforce.com \
  --out ./salida
```

El script imprime un JSON con el color de acento elegido y las rutas de los archivos generados.

---

## Industrias disponibles

El skill incluye presets con datos ficticios pero verosímiles para:

- `retail` — Retail / supermercados
- `banca` — Banca y servicios financieros
- `seguros` — Seguros
- `telco` — Telecomunicaciones
- `generic` — Genérico (por defecto si no se especifica industria)

Para agregar una industria, copiar un bloque en `scripts/industries.py` y agregar sinónimos en `ALIASES`.

---

## Notas sobre contenido técnico

El contenido de referencia (`references/content.md`) tiene fecha de última verificación. Los datos de costo, los nombres de menús y los permisos cambian con cada release de Salesforce. Se recomienda verificar las Release Notes si han pasado más de tres meses desde esa fecha.

**Regla general de costos (octubre 2026):** la observabilidad estándar no consume créditos de Data 360. Sí consumen los dashboards nuevos desde cero, las fuentes externas y los objetos semánticos nuevos. Las acciones del agente siguen consumiendo Flex Credits.

---

## Licencia

Este proyecto es de uso interno. Adaptar según la política de distribución de tu organización.
