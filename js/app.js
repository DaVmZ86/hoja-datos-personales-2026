/* Hoja de Datos Personales: llena la plantilla PDF en el navegador con pdf-lib.
 * Los nombres de los campos (atributo name) coinciden con los campos de
 * assets/plantilla.pdf generados por tools/generar_plantilla.py. */
(function () {
  "use strict";

  const MAX_FONT = 8.5;   // tamaño normal del texto en el PDF
  const MIN_FONT = 5;     // tamaño mínimo al reducir textos largos

  const form = document.getElementById("form");
  const statusEl = document.getElementById("status");
  const chkMayus = document.getElementById("mayusculas");
  const btnVer = document.getElementById("btn-ver");
  const btnDescargar = document.getElementById("btn-descargar");
  const btnLimpiar = document.getElementById("btn-limpiar");

  function setStatus(msg, kind) {
    statusEl.textContent = msg || "";
    statusEl.className = "status" + (kind ? " " + kind : "");
  }

  function base64ToBytes(b64) {
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return bytes;
  }

  // Mayúsculas visuales mientras se escribe
  function applyCaseStyle() {
    form.querySelectorAll("input:not([type=checkbox])").forEach((el) => {
      el.classList.toggle("uppercase", chkMayus.checked && !el.hasAttribute("data-keep-case"));
    });
  }
  chkMayus.addEventListener("change", applyCaseStyle);
  applyCaseStyle();

  function collectData() {
    const data = {};
    form.querySelectorAll("input[name], select[name]").forEach((el) => {
      let v = (el.value || "").replace(/\s+/g, " ").trim();
      if (chkMayus.checked && !el.hasAttribute("data-keep-case")) v = v.toLocaleUpperCase("es-MX");
      data[el.name] = v;
    });
    return data;
  }

  function validate() {
    let first = null;
    form.querySelectorAll("input, select").forEach((el) => {
      const bad = !el.checkValidity();
      el.classList.toggle("invalid", bad);
      if (bad && !first) first = el;
    });
    if (first) {
      first.focus();
      const label = first.closest("label");
      const name = label ? label.childNodes[0].textContent.trim() : first.name;
      setStatus("Revisa el campo: " + name, "error");
      return false;
    }
    return true;
  }
  form.addEventListener("input", (e) => {
    if (e.target.classList.contains("invalid") && e.target.checkValidity()) e.target.classList.remove("invalid");
  });

  // Quita caracteres que la fuente Helvetica (WinAnsi) no puede representar
  function sanitize(text, font) {
    let out = "";
    for (const ch of text) {
      try { font.encodeText(ch); out += ch; } catch (_) { /* se omite */ }
    }
    return out;
  }

  async function buildPdf(data) {
    const { PDFDocument, StandardFonts } = window.PDFLib;
    const pdf = await PDFDocument.load(base64ToBytes(window.PLANTILLA_PDF_B64));
    const font = await pdf.embedFont(StandardFonts.Helvetica);
    const pdfForm = pdf.getForm();

    for (const [name, raw] of Object.entries(data)) {
      let field;
      try { field = pdfForm.getTextField(name); } catch (_) { continue; }
      const text = sanitize(raw, font);
      const width = field.acroField.getWidgets()[0].getRectangle().width - 4;
      let size = MAX_FONT;
      const w = font.widthOfTextAtSize(text, MAX_FONT);
      if (w > width) size = Math.max(MIN_FONT, (MAX_FONT * width) / w);
      field.setFontSize(size);
      field.setText(text);
    }

    pdfForm.updateFieldAppearances(font);
    pdfForm.flatten(); // el texto queda fijo en la hoja, listo para imprimir
    pdf.setTitle("Hoja de Datos Personales");
    return pdf.save();
  }

  function fileName(data) {
    const parts = [data.ap_paterno, data.ap_materno, data.nombres].filter(Boolean).join("_");
    const safe = parts.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9_]+/g, "_");
    return "Hoja_Datos_Personales" + (safe ? "_" + safe : "") + ".pdf";
  }

  async function generate(mode) {
    if (!window.PDFLib) {
      setStatus("No se pudo cargar la librería PDF. Revisa tu conexión a internet y recarga la página.", "error");
      return;
    }
    if (!validate()) return;

    // Se abre la pestaña antes del proceso asíncrono para evitar el bloqueador de ventanas
    const win = mode === "ver" ? window.open("", "_blank") : null;
    btnVer.disabled = btnDescargar.disabled = true;
    setStatus("Generando PDF…");
    try {
      const data = collectData();
      const bytes = await buildPdf(data);
      const url = URL.createObjectURL(new Blob([bytes], { type: "application/pdf" }));
      if (mode === "ver") {
        if (win) win.location.href = url; else window.open(url, "_blank");
        setStatus("PDF abierto en una pestaña nueva. Usa el botón de imprimir del visor.", "ok");
      } else {
        const a = document.createElement("a");
        a.href = url;
        a.download = fileName(data);
        document.body.appendChild(a);
        a.click();
        a.remove();
        setStatus("PDF descargado: " + a.download, "ok");
      }
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    } catch (err) {
      console.error(err);
      if (win) win.close();
      setStatus("Ocurrió un error al generar el PDF: " + err.message, "error");
    } finally {
      btnVer.disabled = btnDescargar.disabled = false;
    }
  }

  form.addEventListener("submit", (e) => { e.preventDefault(); generate("descargar"); });
  btnVer.addEventListener("click", () => generate("ver"));
  btnLimpiar.addEventListener("click", () => {
    if (!confirm("¿Borrar todos los datos capturados?")) return;
    form.reset();
    form.querySelectorAll(".invalid").forEach((el) => el.classList.remove("invalid"));
    applyCaseStyle();
    setStatus("");
  });

  // Para pruebas desde la consola
  window.HojaDatos = { buildPdf, collectData };
})();
