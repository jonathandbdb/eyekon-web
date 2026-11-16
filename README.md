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

## Variante "sitio actual + IOLSIMULATOR" (`site-actual/`)
Copia fiel de la home de eyekonmedical.com (bajada con wget, sin el tracker de estadísticas) con una
sección IOLSIMULATOR insertada entre "Intraocular Lens Manufacturer" y "Customer Service".
- Sección: `site-actual/iolsimulator/` (CSS/JS propios con prefijo `iols-`, fotos, video comprimido).
- Los links del menú apuntan a las páginas reales de eyekonmedical.com.
- Foto del kit: `tools/compose.py` (recorte con rembg + fondo de estudio + pantalla de tablet
  generada desde `tools/screen.html`). Re-clonar assets: `tools/localize_clone.py`.
- Ver local: `cd site-actual && python3 -m http.server 8790`. Deploy: `cd site-actual && npx vercel --prod`.
