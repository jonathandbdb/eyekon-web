# EyeKon Medical — sitio de ejemplo (propuesta)

Rediseño completo de eyekonmedical.com + sección IOLSIMULATOR. Sitio estático, EN/ES/PT.

## Editar y generar
- Textos: `src/i18n/{en,es,pt}.json` (si falta una clave en es/pt, cae a en).
- Estructura: `src/layout.html` y `src/pages/*.html` (marcadores `{{clave}}`).
- CSS/JS/imágenes: directo en `site/assets/`.
- Generar: `python3 build.py` → escribe `site/*.html`, `site/es/`, `site/pt/`.
- Ver local: `cd site && python3 -m http.server 8765` → http://localhost:8765

## Imágenes
- `site/assets/img/products/` — fotos bajadas del sitio actual de EyeKon (baja resolución; pedirles originales).
- `site/assets/img/sim/eyekon/` — capturas del simulador con la piel EyeKon y su catálogo
  (`<escena>-<lente>.webp`; escenas ventana/lectura/living/ruta; lentes catarata/monofocal/multifocal/edof).
- Foto del kit (Quest 3 + estuche + tablet): PENDIENTE — buscar `FOTO DEL KIT PENDIENTE` en `src/pages/`.

## Deploy (Vercel)
`cd site && npx vercel --prod` (proyecto estático, sin build; `vercel.json` agrega `noindex`).

## Contenido marcado como ejemplo
Testimonios y 2 de las 3 novedades llevan la etiqueta "Sample content": reemplazar con material real del cliente.
