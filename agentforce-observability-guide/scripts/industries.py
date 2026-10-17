"""Industry presets: realistic (fictitious) data for the mock dashboards and the
industry-specific wording (channels, sensitive data). Add a new preset by copying
one block; every key is required."""

def _intent(name, share, sessions, quality, success, signal):
    return dict(name=name, share=share, sessions=sessions, quality=quality, success=success, signal=signal)

INDUSTRIES = {
    "retail": dict(
        label="Retail / supermercados",
        agent="Agente de Atención al Cliente",
        channels="web, WhatsApp, app",
        ch1="WhatsApp",
        sensitive="DNI, teléfono, email o datos de tarjeta de los clientes",
        intents=[
            _intent("Estado de pedido", 28, 3494, 4.4, 91, "Resuelve bien; pocas derivaciones"),
            _intent("Consulta de stock", 21, 2621, 4.2, 88, "Mejorable: falta stock por sucursal"),
            _intent("Cambios y devoluciones", 16, 1997, 3.6, 74, "Política ambigua en la instrucción"),
            _intent("Promociones y descuentos", 14, 1747, 4.0, 85, "Interés alto en cuotas sin interés"),
            _intent("Carrito abandonado", 11, 1373, 3.9, 69, "Oportunidad: ofrecer cupón"),
            _intent("Hablar con un asesor", 10, 1248, 3.1, 40, "Escalamiento esperado"),
        ],
        trace=dict(
            user="Hola, ¿mi pedido de ayer ya salió? Quiero saber cuándo llega.",
            answer="¡Hola! Tu pedido ya salió del centro de distribución y llega mañana entre las 14 y las 18 h. Te aviso por aquí si cambia algo.",
            source="Knowledge · Política de envíos a domicilio",
            steps=[["Mensaje del usuario","Canal WhatsApp",0,40,"u"],["Planner","Clasifica intención: Estado de pedido",40,420,"p"],
                   ["Subagente","Pedidos y envíos",460,90,"s"],["Acción","Consultar pedido (Flow)",550,780,"a"],
                   ["Knowledge retrieval","Política de envíos",1330,510,"k"],["Respuesta","Generada y validada (Trust Layer)",1840,960,"r"]]),
    ),
    "banca": dict(
        label="Banca / servicios financieros",
        agent="Agente de Banca Digital",
        channels="home banking, WhatsApp, app",
        ch1="app",
        sensitive="DNI, CBU, número de tarjeta o datos de cuenta de los clientes",
        intents=[
            _intent("Consulta de saldo y movimientos", 26, 3245, 4.5, 94, "Resuelve bien"),
            _intent("Bloqueo de tarjeta", 19, 2371, 4.3, 90, "Flujo rápido; mantener"),
            _intent("Desconocimiento de consumo", 17, 2122, 3.4, 62, "Falta acción para iniciar reclamo"),
            _intent("Préstamos personales", 15, 1872, 3.9, 71, "Interés alto en tasas"),
            _intent("Turnos en sucursal", 12, 1498, 4.1, 86, "Mejorable: horarios por sucursal"),
            _intent("Hablar con un asesor", 11, 1372, 3.0, 38, "Escalamiento esperado"),
        ],
        trace=dict(
            user="Perdí mi tarjeta de débito, ¿la pueden bloquear ya?",
            answer="Listo, tu tarjeta terminada en XXXX quedó bloqueada. ¿Quieres que solicitemos una reposición al domicilio registrado?",
            source="Knowledge · Procedimiento de bloqueo y reposición",
            steps=[["Mensaje del usuario","Canal app",0,40,"u"],["Planner","Clasifica intención: Bloqueo de tarjeta",40,390,"p"],
                   ["Subagente","Tarjetas",430,80,"s"],["Acción","Bloquear tarjeta (API core bancario)",510,920,"a"],
                   ["Knowledge retrieval","Procedimiento de reposición",1430,460,"k"],["Respuesta","Generada y validada (Trust Layer)",1890,880,"r"]]),
    ),
    "seguros": dict(
        label="Seguros",
        agent="Agente de Atención a Asegurados",
        channels="web, WhatsApp, teléfono",
        ch1="WhatsApp",
        sensitive="DNI, número de póliza, datos de salud o del vehículo de los asegurados",
        intents=[
            _intent("Estado de siniestro", 27, 3370, 4.0, 82, "Mejorable: falta detalle de etapas"),
            _intent("Cotización", 20, 2496, 4.3, 87, "Interés alto en seguro de hogar"),
            _intent("Renovación de póliza", 17, 2122, 4.1, 84, "Oportunidad de upsell"),
            _intent("Coberturas", 15, 1872, 3.5, 70, "Respuestas largas; simplificar"),
            _intent("Pago de cuota", 11, 1373, 4.4, 93, "Resuelve bien"),
            _intent("Hablar con un asesor", 10, 1248, 3.1, 41, "Escalamiento esperado"),
        ],
        trace=dict(
            user="¿En qué estado está el siniestro que denuncié la semana pasada?",
            answer="Tu siniestro está en etapa de peritaje; el perito te va a contactar dentro de las próximas 48 h. Te aviso cuando avance.",
            source="Knowledge · Etapas de gestión de siniestros",
            steps=[["Mensaje del usuario","Canal WhatsApp",0,40,"u"],["Planner","Clasifica intención: Estado de siniestro",40,410,"p"],
                   ["Subagente","Siniestros",450,90,"s"],["Acción","Consultar siniestro (Flow)",540,840,"a"],
                   ["Knowledge retrieval","Etapas de siniestros",1380,490,"k"],["Respuesta","Generada y validada (Trust Layer)",1870,930,"r"]]),
    ),
    "telco": dict(
        label="Telecomunicaciones",
        agent="Agente de Atención Digital",
        channels="web, WhatsApp, app",
        ch1="app",
        sensitive="DNI, número de línea, domicilio o datos de pago de los clientes",
        intents=[
            _intent("Factura y pagos", 27, 3370, 4.3, 89, "Resuelve bien"),
            _intent("Cambio de plan", 19, 2371, 4.0, 80, "Oportunidad de upsell"),
            _intent("Falla técnica", 18, 2246, 3.3, 58, "Falta diagnóstico automático"),
            _intent("Portabilidad", 13, 1622, 3.8, 72, "Riesgo de baja: priorizar"),
            _intent("Roaming", 12, 1498, 4.2, 86, "Mejorable: tarifas por país"),
            _intent("Hablar con un asesor", 11, 1373, 3.0, 39, "Escalamiento esperado"),
        ],
        trace=dict(
            user="Me llegó la factura más alta que el mes pasado, ¿por qué?",
            answer="La diferencia es por el consumo de roaming del 3 al 7 de este mes. ¿Quieres que te sugiera un paquete para tu próximo viaje?",
            source="Knowledge · Cargos de roaming internacional",
            steps=[["Mensaje del usuario","Canal app",0,40,"u"],["Planner","Clasifica intención: Factura y pagos",40,400,"p"],
                   ["Subagente","Facturación",440,80,"s"],["Acción","Consultar detalle de factura (API)",520,860,"a"],
                   ["Knowledge retrieval","Cargos de roaming",1380,470,"k"],["Respuesta","Generada y validada (Trust Layer)",1850,900,"r"]]),
    ),
    "generic": dict(
        label="Genérico",
        agent="Agente de Atención",
        channels="web, WhatsApp, voz",
        ch1="web",
        sensitive="datos personales de los clientes (identificación, contacto o pago)",
        intents=[
            _intent("Consulta general", 26, 3245, 4.3, 90, "Resuelve bien"),
            _intent("Estado de solicitud", 21, 2621, 4.1, 85, "Mejorable: más detalle de etapas"),
            _intent("Soporte técnico", 17, 2122, 3.4, 63, "Falta acción de diagnóstico"),
            _intent("Facturación", 14, 1747, 4.0, 82, "Resuelve bien"),
            _intent("Actualización de datos", 12, 1498, 3.8, 76, "Validación de identidad lenta"),
            _intent("Hablar con un asesor", 10, 1248, 3.1, 40, "Escalamiento esperado"),
        ],
        trace=dict(
            user="¿En qué estado está mi solicitud?",
            answer="Tu solicitud está en revisión y debería resolverse en las próximas 24 h. Te aviso por este canal cuando cambie.",
            source="Knowledge · Tiempos de gestión de solicitudes",
            steps=[["Mensaje del usuario","Canal web",0,40,"u"],["Planner","Clasifica intención: Estado de solicitud",40,400,"p"],
                   ["Subagente","Solicitudes",440,80,"s"],["Acción","Consultar solicitud (Flow)",520,800,"a"],
                   ["Knowledge retrieval","Tiempos de gestión",1320,480,"k"],["Respuesta","Generada y validada (Trust Layer)",1800,900,"r"]]),
    ),
}

ALIASES = {"supermercado": "retail", "supermercados": "retail", "ecommerce": "retail", "consumo": "retail",
           "banco": "banca", "bancos": "banca", "finanzas": "banca", "fintech": "banca", "financial": "banca", "banking": "banca",
           "seguro": "seguros", "aseguradora": "seguros", "insurance": "seguros",
           "telecom": "telco", "telecomunicaciones": "telco"}

def get_industry(key):
    k = (key or "generic").strip().lower()
    k = ALIASES.get(k, k)
    return INDUSTRIES.get(k, INDUSTRIES["generic"]), (k if k in INDUSTRIES else "generic")
