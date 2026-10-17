// Usage: node build_docx.js <render-config.json> <output.docx>
// The render config is written by build_guide.py (client, colors, logo, contact, industry wording).
const fs = require('fs');
let docx;
try { docx = require('docx'); } catch (e) { console.error('Missing npm package "docx". Run: npm install -g docx'); process.exit(2); }
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, ExternalHyperlink, Footer, PageNumber, ImageRun } = docx;

const C = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = process.argv[3];
const ACCENT = C.accent_text.replace('#', ''), NAVY = '032D60', BLUE = '0176D3', GREY = '5C5C5C', LIGHT = 'EAF5FE';
const FONT = 'Arial';
const CL = C.client;

const t = (text, o = {}) => new TextRun({ text, font: FONT, size: 21, ...o });
const p = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 120, line: 276 }, ...o });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, keepNext: true, children: [new TextRun({ text, font: FONT, size: 30, bold: true, color: NAVY })], spacing: { before: 320, after: 140 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 4 } } });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, children: [new TextRun({ text, font: FONT, size: 24, bold: true, color: BLUE })], spacing: { before: 220, after: 100 } });
const bullet = (runs) => new Paragraph({ numbering: { reference: 'b', level: 0 }, children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 80, line: 276 } });
const num = (runs, ref) => new Paragraph({ numbering: { reference: ref, level: 0 }, children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 80, line: 276 } });
const b = (text) => t(text, { bold: true });
const code = (text) => t(text, { bold: true, color: NAVY });
const link = (text, url) => new ExternalHyperlink({ link: url, children: [t(text, { color: BLUE, underline: {} })] });
const border = { style: BorderStyle.SINGLE, size: 4, color: 'C9C9C9' };
const borders = { top: border, bottom: border, left: border, right: border };
const cell = (content, width, o = {}) => new TableCell({
  width: { size: width, type: WidthType.DXA }, borders,
  shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
  margins: { top: 90, bottom: 90, left: 120, right: 120 },
  children: [new Paragraph({ children: [t(content, { bold: !!o.bold, color: o.color || '222222', size: 19 })] })]
});
const table = (widths, header, rows) => new Table({
  width: { size: widths.reduce((a, c) => a + c, 0), type: WidthType.DXA }, columnWidths: widths,
  rows: [
    new TableRow({ tableHeader: true, cantSplit: true, children: header.map((h, i) => cell(h, widths[i], { fill: NAVY, color: 'FFFFFF', bold: true })) }),
    ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], { fill: ri % 2 ? 'F6F8FA' : undefined, bold: i === 0 })) }))
  ]
});
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const callout = (title, text, fill = LIGHT, color = NAVY) => new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: [9360],
  rows: [new TableRow({ cantSplit: true, children: [new TableCell({
    width: { size: 9360, type: WidthType.DXA }, borders: { top: NONE, bottom: NONE, right: NONE, left: { style: BorderStyle.SINGLE, size: 24, color } },
    shading: { type: ShadingType.CLEAR, color: 'auto', fill }, margins: { top: 120, bottom: 120, left: 200, right: 200 },
    children: [new Paragraph({ children: [t(title + ' ', { bold: true, color }), t(text)] })]
  })] })]
});
const spacer = () => new Paragraph({ children: [], spacing: { after: 60 } });

const logoRun = C.logo_docx
  ? new ImageRun({ type: C.logo_docx.type, data: fs.readFileSync(C.logo_docx.path), transformation: { width: C.logo_docx.width, height: C.logo_docx.height } })
  : new TextRun({ text: CL, font: FONT, size: 40, bold: true, color: ACCENT });

const children = [
  new Paragraph({ children: [logoRun, new TextRun({ text: '    ×    ', font: FONT, size: 28, color: GREY }),
    new ImageRun({ type: 'png', data: fs.readFileSync(C.sf_logo), transformation: { width: 69, height: 48 } })], spacing: { after: 200 } }),
  new Paragraph({ children: [new TextRun({ text: 'Agentforce Observability', font: FONT, size: 48, bold: true, color: NAVY })], spacing: { after: 60 } }),
  new Paragraph({ children: [new TextRun({ text: 'Guía de activación y acceso autogestionado', font: FONT, size: 28, color: BLUE })], spacing: { after: 200 } }),
  p([t('Preparado para: ', { color: GREY }), b(`Equipo de administración Salesforce de ${CL}`), t(`   |   Versión: ${C.version}`, { color: GREY })]),
  spacer(),
  callout('Objetivo.', `Que el equipo de ${CL} pueda activar por sus propios medios la observabilidad de sus agentes de Agentforce (analítica, optimización, monitoreo de salud y trazas de sesión), asignar accesos y empezar a medir el desempeño de los agentes en producción.`),

  h1('1. Qué es Agentforce Observability'),
  p('Es el conjunto de herramientas, dentro de Agentforce Studio, que muestra qué hacen los agentes en producción, por qué toman cada decisión y cómo rinden. Se organiza en cuatro piezas:'),
  table([2400, 6960], ['Componente', 'Para qué sirve'], [
    ['Agent Analytics', 'KPIs de desempeño y tendencias: sesiones, engagement, escalamiento, tasa de éxito, satisfacción, calidad, salud y trust. Se puede filtrar por agente, canal, subagente, acción e intención.'],
    ['Agent Optimization', 'Registra cada paso del razonamiento del agente, agrupa pedidos similares por intención y ayuda a detectar patrones de falla y oportunidades de mejora.'],
    ['Agent Health Monitoring', 'Monitoreo casi en tiempo real (intervalos de 5 minutos) de tasa de error, latencia y escalamientos, con alertas por email según umbrales configurables.'],
    ['Session Tracing (STDM)', 'El modelo de datos base (Session Tracing Data Model) en Data Cloud que guarda cada sesión turno por turno: input del usuario, decisiones del planner, acciones, prompts, errores y respuesta final. Alimenta todo lo anterior.'],
  ]),
  spacer(),
  callout('Costo.', 'Según las Release Notes oficiales de Salesforce (2026), para las funcionalidades de observabilidad de agentes la recolección de datos, el cálculo de métricas, las consultas, los reportes y los dashboards ya no consumen créditos de Data 360, para todos los SKUs de Agentforce. El consumo sigue visible en Digital Wallet como referencia, pero no descuenta créditos.', 'EAF7EC', '2E844A'),
  spacer(),
  table([4680, 4680], ['NO consume créditos', 'SÍ consume créditos'], [
    ['Session Tracing e ingesta de telemetría', 'Crear dashboards nuevos desde cero'],
    ['Métricas y agregaciones (Analytics, Health, Optimization)', 'Ingerir fuentes de datos externas (ej. Snowflake)'],
    ['Consultas y visualizaciones de los dashboards estándar', 'Crear objetos nuevos en el modelo semántico'],
    ['Modificar o extender los dashboards estándar', 'Las acciones del agente en sí (Flex Credits por acción)'],
    ['Drill-downs, evaluación de alertas y trazas de sesión', '—'],
  ]),

  h1('2. Prerrequisitos'),
  p(`Antes de empezar, verificar que la org de ${CL} cumpla con lo siguiente:`),
  table([3200, 6160], ['Requisito', 'Cómo verificarlo'], [
    ['Data Cloud (Data 360) aprovisionado', 'Setup → Data Cloud Setup. Si no está activo: Get Started y esperar a que se inicialice la instancia.'],
    ['Einstein activado', 'Setup → Einstein Setup → toggle "Turn on Einstein".'],
    ['Al menos un agente activo', 'Agentforce Studio → Agents. Los agentes en borrador o inactivos no generan trazas.'],
    ['Salesforce Standard Data Model ≥ 1.130', 'Setup → Installed Packages → "Salesforce Standard Data Model". Si la versión es menor, actualizar con el link que provee Salesforce.'],
    ['Usuario que configura', 'System Administrator con los permission sets Data Cloud User y Data Cloud Architect.'],
  ]),

  h1('3. Activación paso a paso'),
  h2('Paso 1 — Activar Session Tracing y Optimization'),
  num([t('Ir a '), code('Setup → Einstein Audit, Analytics, and Monitoring Setup'), t('.')], 's1'),
  num([t('Activar '), b('Agentforce Session Tracing'), t(' (incluye el Data Model).')], 's1'),
  num([t('Verificar que '), b('Agent Optimization'), t(' quede activado (se activa automáticamente con Session Tracing).')], 's1'),
  num([b('No'), t(' activar el toggle legacy de "Agent Analytics": está marcado para retiro y reemplazado por Session Tracing.')], 's1'),
  num([b('Agent Platform Tracing'), t(' es opcional: da visibilidad profunda de acciones Flow y Apex dentro del agente.')], 's1'),
  num('Si la org tiene más de un data space, el sistema pide elegir dónde guardar las trazas. Elegir el data space principal de Agentforce.', 's1'),
  callout('Nota.', 'En orgs con un solo data space, Session Tracing suele venir activado por defecto al encender Agentforce. Conviene revisar primero si ya está activado.'),
  h2('Paso 2 — Instalar las apps de Agent Analytics'),
  num([t('Ir a '), code('Setup → Agent Analytics'), t('.')], 's2'),
  num([t('Instalar '), b('Service Agent Analytics'), t(' (agentes de cara al cliente) y '), b('Employee Agent Analytics'), t(' (agentes internos / Agentforce Coworker).')], 's2'),
  num('Esperar a que el estado pase a "Installed".', 's2'),
  h2('Paso 3 — Asignar permisos a los usuarios'),
  p(`Para cada persona de ${CL} que deba ver la observabilidad:`),
  table([3800, 5560], ['Permiso', 'Habilita'], [
    ['Access Agentforce Optimization', 'Acceso a Agent Optimization.'],
    ['Tableau Next Limited Consumer o Tableau Next Platform Analyst', 'Acceso a los dashboards de Analytics (Consumer = solo ver; Analyst = ver y editar).'],
    ['Data Cloud User', 'Acceso a los datos de sesión en Data Cloud.'],
    ['API Enabled = true en el perfil', 'Sin esto, las tarjetas de métricas en Tableau Next no cargan (sin mostrar error claro).'],
  ]),
  h2('Paso 4 — Proteger los datos de sesión'),
  bullet('Los permisos se aplican a nivel data space: solo los usuarios autorizados pueden ver o consultar las trazas.'),
  bullet([t('El permission set Data Cloud Architect accede a todos los datos por defecto. Se recomienda '), b('quitar o acotar la política "Allow All"'), t(' a usuarios específicos.')]),
  bullet([t(`Las conversaciones pueden contener ${C.sensitive}. Se recomienda configurar `), b('Dynamic Data Masking'), t(' para enmascarar o anular campos sensibles.')]),
  h2('Paso 5 — Configurar alertas de salud (Health Monitoring)'),
  num([t('En Agentforce Studio → Observe → '), b('Health Monitoring'), t('.')], 's3'),
  num('Definir umbrales por métrica: tasa de error, latencia promedio y escalamientos.', 's3'),
  num('Configurar destinatarios de email. Las alertas tienen un "cooldown" (30 min por defecto) para evitar exceso de notificaciones.', 's3'),

  h1('4. Cómo acceder día a día'),
  num([t('Abrir el '), b('App Launcher'), t(' y buscar '), b('Agentforce Studio'), t('.')], 's4'),
  num([t('En el panel izquierdo, ir a la sección '), b('Observe'), t(' (Observe & Optimize).')], 's4'),
  num([t('Elegir la herramienta: '), b('Analytics'), t(', '), b('Optimization'), t(' o '), b('Health Monitoring'), t('.')], 's4'),
  num(`Filtrar por agente, canal (${C.channels}) y período.`, 's4'),
  p('Funcionalidades destacadas:'),
  bullet('Vista de sesión individual con la traza completa, fuentes consultadas y scores de calidad.'),
  bullet(`Métricas de deflection y abandonment evaluadas por LLM con prompts editables, para ajustarlas a la definición de éxito de ${CL}.`),
  bullet('Scores personalizados tipo "LLM-as-judge" (sentimiento, tono, menciones de competencia, interés de producto, señales de precio).'),
  bullet('Traza tipo "waterfall" para flujos multiagente: si un agente deriva a un subagente, la traza lo sigue.'),
  bullet('Citas inline con el fragmento exacto del artículo de Knowledge u otra fuente usada en la respuesta.'),
  bullet('Descarga masiva de sesiones y dashboard unificado (Trust, RAG, salud y calidad en una sola vista).'),

  h1('5. Qué preguntas responde cada tablero'),
  table([2400, 6960], ['Tablero', `Ejemplo para ${CL}`], [
    ['Analytics', `¿Cuántas sesiones atiende el agente, cuánto resuelve sin derivar y cuáles son las intenciones más frecuentes? (ej. ${C.intents.slice(0, 3).map(i => i.name).join(', ')}).`],
    ['Health Monitoring', `¿Está funcionando bien ahora? Ej.: alerta por email si el escalamiento supera el 15% durante 15 minutos en el canal ${C.ch1}.`],
    ['Optimization', `¿Dónde rinde peor el agente y por qué? Ej.: "${C.intents[2].name}" con calidad ${String(C.intents[2].quality).replace('.', ',')} → ${C.intents[2].signal.toLowerCase()}.`],
    ['Traza de sesión', 'Paso a paso de una conversación: intención detectada, subagente, acciones ejecutadas, fuentes de Knowledge citadas y tiempos de cada etapa.'],
  ]),
  p([t('La guía interactiva en HTML incluye maquetas de cada tablero con datos ilustrativos.', { color: GREY, italics: true })]),

  h1('6. Consideraciones importantes'),
  bullet([b('Sin datos retroactivos: '), t('la analítica solo muestra conversaciones ocurridas después de activar Session Tracing. Los datos pueden demorar en aparecer.')]),
  bullet([b('Apagar Session Tracing '), t('detiene la recolección y desactiva funciones dependientes. Los datos existentes se conservan, pero queda un hueco en los dashboards.')]),
  bullet([b('Exportación técnica: '), t('existe una API (beta) que exporta la traza de una sesión en formato OpenTelemetry (OTLP). Autenticación vía OAuth 2.0 con External Client App; una sesión por request.')]),
  bullet([b('Recomendación: '), t('validar primero en un sandbox y luego replicar en producción. Los nombres de menús pueden variar levemente según el release de la org.')]),

  h1('7. Checklist de activación'),
  table([600, 6360, 2400], ['#', 'Tarea', 'Responsable / OK'], [
    ['1', 'Data Cloud y Einstein activos', ''], ['2', 'Standard Data Model ≥ 1.130', ''],
    ['3', 'Session Tracing + Agent Optimization activados', ''], ['4', 'Service y Employee Agent Analytics instalados', ''],
    ['5', 'Permission sets asignados + API Enabled en perfiles', ''], ['6', 'Política "Allow All" revisada y Data Masking configurado', ''],
    ['7', 'Alertas de Health Monitoring configuradas', ''], ['8', 'Primera revisión de dashboards con el equipo (a los 7 días)', ''],
  ]),

  h1('8. Documentación oficial'),
  ...C.docs.map(d => bullet([link(`${d[0]} (${d[1]})`, d[2])])),
  spacer(),
  callout('¿Dudas?', C.contact_text),
];

const numbering = ['s1', 's2', 's3', 's4'].map(r => ({ reference: r, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] }));
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }, ...numbering] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1200, bottom: 1200, left: 1273, right: 1273 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [t(`${CL} × Salesforce · Agentforce Observability · Página `, { size: 16, color: GREY }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: GREY })] })] }) },
    children
  }]
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log('docx ok:', OUT); });
