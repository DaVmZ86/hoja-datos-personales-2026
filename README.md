# Hoja de Datos Personales – Llenado en línea

Aplicación web estática para capturar los datos de la **Hoja de Datos Personales**
(Dirección de Administración, Clave `1A74-009-120`). Al final genera el **PDF tamaño carta**
ya llenado y listo para imprimir y firmar.

- **Privada:** todo ocurre en el navegador. Ningún dato se envía ni se guarda en un servidor.
- **Sin instalación:** basta con abrir `index.html` o publicarla en GitHub Pages.
- **Textos largos:** se reducen automáticamente para caber en su línea.
- **Mayúsculas opcionales:** todo se convierte a mayúsculas, excepto los correos.

## Uso

1. Abre la página (en GitHub Pages o abriendo `index.html` en tu navegador).
2. Llena los campos. Los marcados con `*` son obligatorios.
3. Elige una opción:
   - **Generar PDF:** descarga el archivo `Hoja_Datos_Personales_<NOMBRE>.pdf`.
   - **Vista previa / imprimir:** abre el PDF en otra pestaña para imprimirlo directamente.
4. Imprime en hoja **carta** al **100 %** (sin "ajustar a página") y firma a mano.

> La librería [pdf-lib](https://pdf-lib.js.org/) se carga desde un CDN, así que se necesita internet
> la primera vez que se abre la página.

## Estructura

```
├── index.html                 Formulario
├── css/styles.css             Estilos
├── js/app.js                  Lógica: llena la plantilla con pdf-lib y genera el PDF
├── js/plantilla-data.js       Plantilla PDF incrustada en base64 (generado)
├── assets/plantilla.pdf       Plantilla PDF tamaño carta con campos rellenables (generado)
├── assets/logo-imss.png       Logo usado en la plantilla
├── tools/generar_plantilla.py Script que genera la plantilla y plantilla-data.js
└── .github/workflows/pages.yml Publicación automática en GitHub Pages
```

## Subir a GitHub y publicar

```bash
git init
git add .
git commit -m "Hoja de Datos Personales: app de llenado"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/hoja-datos-personales-2026.git
git push -u origin main
```

Después, en GitHub ve a **Settings → Pages → Build and deployment → Source** y elige
**GitHub Actions**. El flujo `.github/workflows/pages.yml` publica el sitio en cada `push` a `main`,
en `https://<tu-usuario>.github.io/hoja-datos-personales-2026/`.

## Modificar la plantilla

Si cambias el diseño o los campos del PDF, edita `tools/generar_plantilla.py` y vuelve a generar:

```bash
pip install reportlab
python tools/generar_plantilla.py
```

Esto actualiza `assets/plantilla.pdf` y `js/plantilla-data.js`. Si agregas un campo, usa el mismo
`name` en el campo de `index.html` y en la plantilla.

## Aviso

Es una herramienta **no oficial** para facilitar el llenado del formato. El logotipo y el formato
pertenecen al Instituto Mexicano del Seguro Social. Verifica tus datos antes de entregarlos.
Si publicas el repositorio, no subas PDF llenados con datos personales: `.gitignore` ya excluye
los archivos `Hoja_Datos_Personales_*.pdf`.
