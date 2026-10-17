# Contenido de referencia: Agentforce Observability

**Última verificación:** octubre 2026. Si pasaron más de 3 meses, vuelve a verificar costos, menús y permisos antes de generar.

## Componentes
- **Agent Analytics:** KPIs (sesiones, engagement, escalamiento, éxito, CSAT, calidad, salud, trust), filtrables por agente, canal, subagente, acción e intención. Incluye vista de voz.
- **Agent Optimization:** razonamiento paso a paso y agrupación por intención.
- **Agent Health Monitoring:** tasa de error, latencia y escalamientos cada 5 minutos. Alertas por email con umbrales y un cooldown de 30 min.
- **Session Tracing Data Model (STDM):** DLOs y DMOs en Data Cloud (AIAgentSession, AIAgentSessionParticipant, interacciones y pasos). Es la base de todo lo anterior.

## Costo (Release Notes 2026 + blog de Salesforce del 21/07/2026)
- **No consume créditos de Data 360:** recolección de datos, ingesta de telemetría, cálculo de métricas, consultas, reportes, dashboards estándar (también modificarlos o extenderlos), drill-downs, alertas y trazas. Aplica a todos los SKUs de Agentforce. El uso sigue apareciendo en Digital Wallet, pero no descuenta créditos.
- **Sí consume:** dashboards nuevos desde cero, ingesta de fuentes externas (por ejemplo Snowflake) y objetos nuevos en el modelo semántico. Las acciones del agente siguen consumiendo Flex Credits.
- La página "Billing Considerations for Agentforce Session Tracing" no se pudo leer automáticamente porque la ayuda de Salesforce se carga con JS. Conviene verificarla a mano.

## Prerrequisitos
Data Cloud aprovisionado, Einstein activado, al menos un agente activo (los borradores no generan trazas), Salesforce Standard Data Model ≥ 1.130, y un administrador con los permission sets Data Cloud User y Data Cloud Architect.

## Activación
1. Setup → Einstein Audit, Analytics, and Monitoring Setup: activar Agentforce Session Tracing (incluye el Data Model). Agent Optimization se activa automáticamente. No activar el toggle legacy de Agent Analytics (se retira desde mayo de 2026). Agent Platform Tracing es opcional (Flow y Apex). Si hay varios data spaces, se elige uno. En orgs con un solo data space suele venir activado.
2. Setup → Agent Analytics: instalar Service Agent Analytics y Employee Agent Analytics.
3. Permisos: Access Agentforce Optimization; Tableau Next Limited Consumer o Platform Analyst; Data Cloud User; API Enabled en el perfil (si falta, las métricas no cargan y no aparece ningún error).
4. Seguridad: permisos por data space, quitar o acotar la política "Allow All" y configurar Dynamic Data Masking.
5. Health Monitoring: umbrales y destinatarios de email.

## Consideraciones
Sin datos retroactivos. Apagar Session Tracing deja un hueco en los datos. La OTel API (beta) exporta una sesión por request, con OAuth 2.0 vía External Client App, y solo sesiones de las últimas 72 h. Digital Wallet reporta con hasta 72 h de demora.

## Fuentes
- https://help.salesforce.com/s/articleView?id=005237036&language=en_US&type=1
- https://help.salesforce.com/s/articleView?language=en_US&id=ai.generative_ai_session_trace_setup.htm&type=5
- https://help.salesforce.com/s/articleView?language=en_US&id=ai.generative_ai_session_trace_data_model.htm&type=5
- https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_usage_types.htm&language=en_US&type=5
- https://help.salesforce.com/s/articleView?id=release-notes.rn_einstein_copilot.htm ("Gain Agent Observability Insights Without Consuming Data 360 Credits")
- https://www.salesforce.com/blog/agentforce-observability/
- https://developer.salesforce.com/docs/ai/agentforce/guide/otel-api.html
- https://salesforcebreak.com/2026/05/28/setting-up-agentforce-observability/ (externa: versión 1.130 e instalación de las apps de Analytics)
- https://www.xavor.com/blog/salesforce-agentforce-observability/ (externa: límites de la OTel API y de Digital Wallet)
