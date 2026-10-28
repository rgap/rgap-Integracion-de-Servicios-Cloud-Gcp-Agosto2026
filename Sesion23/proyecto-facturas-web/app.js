const users = [
  { name: "Laura", email: "laura@pedidosexpress.com", password: "demo2026", role: "Administración", canIssue: true },
  { name: "Diego", email: "diego@pedidosexpress.com", password: "demo2026", role: "Solo lectura", canIssue: false },
];
// Tiene permiso para guardar los comprobantes en la nube, pero no es una persona: no inicia sesión.
const serviceAccount = { name: "Servicio de facturación", email: "sa-generador-facturas@pedidos-express-prod.iam.gserviceaccount.com" };

const example = { client: "Cafetería Norte S.A.C.", ruc: "20609481752", concept: "Servicio de entrega de pedidos", total: "495.60" };

const initialInvoices = [
  { number: "F001-001202", client: "Librería Central E.I.R.L.", ruc: "20104481236", date: "22 oct 2026", total: 100.3 },
  { number: "F001-001201", client: "Cafetería Norte S.A.C.", ruc: "20609481752", date: "21 oct 2026", total: 57.23 },
];
let invoices = [...initialInvoices];

const money = new Intl.NumberFormat("es-PE", { style: "currency", currency: "PEN" });
const today = () => new Intl.DateTimeFormat("es-PE", { day: "numeric", month: "short", year: "numeric" }).format(new Date()).replace(".", "");
// Acepta "495.60" y "495,60".
const parseTotal = (value) => Math.round((Number(value.replace(",", ".")) || 0) * 100) / 100;

const $ = (id) => document.getElementById(id);

// Inicio de sesión

const loginForm = $("login-form");
const loginError = $("login-error");

const showLoginError = (text) => {
  loginError.textContent = text;
  loginError.hidden = false;
};

const logIn = (email, password) => {
  const address = email.trim().toLowerCase();
  const user = users.find((candidate) => candidate.email === address && candidate.password === password);
  if (user) showBilling(user);
  else if (address === serviceAccount.email) showLoginError("Las cuentas de servicio no pueden iniciar sesión.");
  else showLoginError("Correo o contraseña incorrectos.");
};

const quickButton = (name, role, email, password) => {
  const button = document.createElement("button");
  button.type = "button";
  button.innerHTML = "<b></b><small></small>";
  button.querySelector("b").textContent = name;
  button.querySelector("small").textContent = role;
  button.addEventListener("click", () => {
    $("email").value = email;
    $("password").value = password;
    logIn(email, password);
  });
  return button;
};

users.forEach((user) => $("quick").append(quickButton(user.name, user.role, user.email, user.password)));
$("quick").append(quickButton(serviceAccount.name, "Cuenta de servicio", serviceAccount.email, ""));

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  logIn($("email").value, $("password").value);
});

// Facturación

const invoiceForm = $("invoice-form");
const invoiceMessage = $("invoice-message");
const fields = invoiceForm.elements;

const showBilling = (user) => {
  $("user-label").textContent = user.email + (user.canIssue ? "" : " · Solo lectura");
  invoiceForm.hidden = !user.canIssue;
  $("layout").classList.toggle("single", !user.canIssue);
  $("login").hidden = true;
  $("billing").hidden = false;
  renderInvoices();
};

const showLogin = () => {
  loginForm.reset();
  loginError.hidden = true;
  invoiceForm.reset();
  invoiceMessage.hidden = true;
  invoices = [...initialInvoices];
  updateTotal();
  $("billing").hidden = true;
  $("login").hidden = false;
};

const renderInvoices = () => {
  $("invoices").replaceChildren(...invoices.map((invoice) => {
    const row = document.createElement("tr");
    row.innerHTML = '<td><b></b><small></small></td><td class="amount"></td><td class="files">PDF · XML</td>';
    row.querySelector("b").textContent = invoice.number;
    row.querySelector("small").textContent = `${invoice.client} · ${invoice.date}`;
    row.querySelector(".amount").textContent = money.format(invoice.total);
    return row;
  }));
};

const updateTotal = () => {
  $("issue").textContent = `Emitir factura · ${money.format(parseTotal(fields.total.value))}`;
};

const showMessage = (ok, text) => {
  invoiceMessage.className = ok ? "success" : "error";
  invoiceMessage.textContent = text;
  invoiceMessage.hidden = false;
};

fields.ruc.addEventListener("input", () => (fields.ruc.value = fields.ruc.value.replace(/\D/g, "")));
fields.total.addEventListener("input", updateTotal);

$("use-example").addEventListener("click", () => {
  for (const [field, value] of Object.entries(example)) fields[field].value = value;
  updateTotal();
});

invoiceForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const client = fields.client.value.trim();
  const ruc = fields.ruc.value;
  const total = parseTotal(fields.total.value);
  if (!client || !fields.concept.value.trim() || total <= 0) return showMessage(false, "Completa todos los campos.");
  if (!/^\d{11}$/.test(ruc)) return showMessage(false, "El RUC debe tener 11 dígitos.");
  const number = "F001-" + String(1203 + invoices.length - initialInvoices.length).padStart(6, "0");
  invoices = [{ number, client, ruc, date: today(), total }, ...invoices];
  renderInvoices();
  invoiceForm.reset();
  updateTotal();
  showMessage(true, `Factura ${number} emitida. El PDF y el XML ya están guardados.`);
});

$("logout").addEventListener("click", showLogin);
$("home").addEventListener("click", (event) => {
  event.preventDefault();
  showLogin();
});

updateTotal();
