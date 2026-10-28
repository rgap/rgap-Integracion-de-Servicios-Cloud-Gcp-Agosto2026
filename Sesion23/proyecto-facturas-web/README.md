# Facturas protegidas

Página web en HTML, CSS y JavaScript puros (sin frameworks ni compilación) que simula la facturación de Pedidos Express para el caso de IAM. No se conecta a Google Cloud ni guarda datos fuera del navegador.

## Qué muestra

- El login tiene tres botones de **Entrar como** (la contraseña de las personas es `demo2026`):
  - **Laura** (Administración) emite facturas y las ve.
  - **Diego** entra en solo lectura: ve las facturas pero no puede emitirlas.
  - **Servicio de facturación** (`sa-generador-facturas`) es rechazado: una cuenta de servicio no inicia sesión.
- Emite una factura: cliente, RUC de 11 dígitos, concepto y total. **Usar ejemplo** llena el formulario.
- La factura aparece en **Facturas emitidas** con su PDF y XML. Esos archivos los guarda el servicio de facturación con su propia cuenta de servicio (`sa-generador-facturas`), no la cuenta de Laura.

El diagrama del sistema desplegado está en [`../diagramas/17_iam_sistema_de_facturas_desplegado.md`](../diagramas/17_iam_sistema_de_facturas_desplegado.md) (se abre con **Abrir** en SystemModeler).

## Ejecutar

Abre `index.html` en el navegador, o sírvelo con cualquier servidor estático:

```bash
python3 -m http.server 5173
```

Archivos: `index.html` (estructura), `styles.css` (estilos) y `app.js` (lógica).
