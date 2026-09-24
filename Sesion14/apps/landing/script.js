// Todo este código corre en el navegador del visitante, no en un servidor.
// En la Sesion 10, server.py armaba el enlace de WhatsApp. En un sitio
// estático no hay servidor, así que lo arma el navegador.

// 1. Configuración: cambia estos dos valores por los tuyos.
// Número en formato internacional, solo dígitos (sin +, sin espacios).
const WHATSAPP_NUMBER = "51999999999";
const WHATSAPP_MESSAGE = "Hola, vengo de la web y quisiera una cotización.";

// 2. Enlace de WhatsApp con el mensaje ya escrito
const whatsappLink =
  "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(WHATSAPP_MESSAGE);

document.querySelectorAll(".js-whatsapp").forEach((enlace) => {
  enlace.href = whatsappLink;
});

document.getElementById("whatsapp-number").textContent = "Escríbenos al +" + WHATSAPP_NUMBER;

// 3. Año actual en el pie de página
document.getElementById("year").textContent = new Date().getFullYear();
