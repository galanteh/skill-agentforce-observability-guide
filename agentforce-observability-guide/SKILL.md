---
name: "agentforce-observability-guide"
description: Genera, para cualquier cliente de Salesforce, una guía con su marca para activar y usar Agentforce Observability (Session Tracing, Agent Analytics, Agent Optimization, Health Monitoring). Entrega un HTML interactivo con checklist, progreso y tableros de ejemplo, un Word (.docx) y una carpeta lista para Netlify, con el logo y los colores del cliente. Usar siempre que el usuario quiera compartir con un cliente cómo activar la observabilidad de agentes, armar una guía o un paso a paso de Observability/Session Tracing/Agent Analytics para un cliente, "personalizar la guía de observabilidad con el logo de X", repetir para otro cliente la guía hecha para Coral Clouds, o aclarar qué consume y qué no consume créditos de observabilidad, aunque no diga "skill" ni "guía".
---

# Guía de Agentforce Observability con la marca del cliente

Este skill produce una guía para el equipo de administración Salesforce de un cliente, de modo que pueda activar la observabilidad de sus agentes por su cuenta. El contenido técnico es el mismo para todos los clientes (ver `references/content.md`). Lo que cambia por cliente es la marca (logo, colores), la industria (ejemplos de tableros, canales, datos sensibles) y el contacto.

## Qué se necesita del usuario

Solicita solo lo que falte. Todo tiene un valor por defecto, salvo el nombre:

| Dato | Obligatorio | Si falta |
|---|---|---|
| Nombre del cliente | Sí | Preguntar |
| Logo (PNG, JPG o SVG) | Recomendado | Se muestra el nombre en texto con el color de acento |
| Color de acento | No | Se extrae del logo |
| Industria | No | Se infiere del cliente (retail, banca, seguros, telco) o queda `generic` |
| Contacto (nombre y email) | No | Usar el nombre y el email del usuario si los tienes en contexto; si no, texto genérico |
| Hero | No | `salesforce` (navy → azul). `brand` usa los colores del cliente |
| Formatos | No | `html,docx,netlify` |

**El logo:** si el usuario lo adjunta, está en la carpeta de uploads. Si no, búscalo en su carpeta de trabajo (`find -iname '*logo*'`, o dentro de HTML de demos anteriores del cliente como imagen base64). No inventes ni dibujes un logo: si no aparece, solicítalo, y mientras tanto genera con el nombre en texto. Si el logo tiene fondo blanco, pasa `--transparent-bg`.

## Cómo generarla

```bash
python3 <skill-dir>/scripts/build_guide.py \
  --client "Coral Clouds" --logo /ruta/logo-coral-clouds.png --transparent-bg \
  --industry retail --contact-name "Alex Rivera" --contact-email alex@salesforce.com \
  --out "/ruta/carpeta/del/cliente"
```

Opciones útiles: `--accent "#CC2131"` (fuerza el color), `--hero brand` o `--hero "#111111,#333333"`, `--formats html,docx`, `--version "noviembre 2026"`, `--config cliente.json` (las mismas claves en JSON).

El script imprime un JSON con el color elegido (`accent_source` indica si salió del logo) y las rutas generadas. Si aparece un error de `docx` (npm), ejecuta `npm install -g docx` y vuelve a ejecutar el script.

Guarda la salida en la carpeta del cliente dentro de la carpeta de trabajo del usuario (por ejemplo `CoralClouds/<Cliente>/` o `<cliente>/`). Si no existe, créala con el nombre del cliente.

## Verificar antes de entregar

1. Presenta el HTML con `present_files` y toma un screenshot: el logo debe verse bien en la barra superior, y el acento (botones, números de sección, gráficos) debe ser el color del cliente.
2. La vista previa solo muestra la parte de arriba de la página. Para revisar los tableros, genera una copia temporal que oculte todas las secciones salvo `#tableros` y muestre los paneles (`.panel{display:block!important}`). No la entregues.
3. Convierte el Word a PDF (`soffice --convert-to pdf`) y revisa la portada.
4. Si el color extraído no es el de la marca (logos multicolor o con fondo de color), vuelve a generar con `--accent`.

## Entregar

- Presenta el HTML y el Word con `present_files`. En pocas líneas: qué color se usó y de dónde salió, qué industria, dónde quedaron los archivos.
- **Netlify:** no hay conector. Indica: entrar a https://app.netlify.com/drop, arrastrar la carpeta `netlify-<slug>`, y después renombrar el sitio en *Site configuration → Change site name*. Para actualizarlo: *Deploys* y arrastrar de nuevo. Advierte que la URL es pública para quien tenga el link.
- Los tableros son **maquetas ilustrativas con datos ficticios**, y la página lo aclara. No las presentes como capturas reales.

## Mantener el contenido al día

Los datos de costo (qué consume y qué no consume créditos), los nombres de menús y los permisos cambian con cada release. `references/content.md` tiene la fecha de la última verificación y las fuentes. Si pasaron más de ~3 meses, o el usuario pregunta específicamente por costos, busca en la web las Release Notes y la ayuda de Salesforce antes de generar. Si algo cambió, actualiza el texto en `assets/guide.template.html` y `scripts/build_docx.js` (los dos tienen el mismo contenido) y la fecha en `content.md`.

Para que el usuario lo transmita al cliente: la observabilidad estándar no consume créditos de Data 360. Sí consumen los dashboards nuevos desde cero, las fuentes externas y los objetos semánticos nuevos, y las acciones del agente siguen consumiendo Flex Credits. Si el cliente tiene condiciones contractuales particulares, sugerí validarlo con el equipo de pricing.

## Agregar una industria

Copia un bloque en `scripts/industries.py` (agente, canales, datos sensibles, 6 intenciones con métricas y una traza de ejemplo) y agrega sinónimos en `ALIASES`. Los datos deben ser verosímiles para esa industria, porque son los que el cliente ve en los tableros de ejemplo.

## Datos sensibles

La guía no lleva datos de clientes finales. En los ejemplos de traza, enmascara siempre los identificadores (por ejemplo, "tarjeta terminada en XXXX").
