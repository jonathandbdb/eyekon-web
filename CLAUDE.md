# EyeKon Medical — propuesta de sitio web modernizado

Proyecto **separado** del simulador IOLSIMULATOR. Respondé siempre en español.

## Qué es
- **Cliente potencial**: EyeKon Medical, Inc. — fabricante de LIOs (PMMA, hidrofílica acrílica,
  hidrofóbica, precargada), CTR, viscoelásticos y eye wipes. Clearwater, Florida (planta de
  17.000 ft²), +30 años, FDA desde 1989, CE desde 1996, +100 países. Web actual:
  https://www.eyekonmedical.com/ (vieja, solo inglés, blog abandonado).
- **Entregable**: sitio estático de ejemplo (rediseño completo de su web actual + sección de
  nuestro producto IOLSIMULATOR) deployado en Vercel con `noindex` y aviso "propuesta de diseño".
- **Nuestro producto**: IOLSIMULATOR — simulador VR de LIOs. El paciente usa un Meta Quest 3 y ve
  cómo vería con cada lente; el médico lo guía desde una tablet Android. Se vende como kit
  (Quest 3 + estuche + tablet). EyeKon ya está cargada en nuestro backend como empresa de lentes
  (línea "Natural LivingLens", catálogo y escenas propios).

## Contexto en el repo del simulador (solo lectura, NO modificar)
`~/PersonalProject/VR-UNITY/simulador-LIOS-Unity/`
- `docs/empresas-lentes.md` — cómo funciona EyeKon como empresa de lentes en el sistema.
- `docs/comercial/` — deck, folletos (imágenes en `folletos/src/`: headset, simulaciones
  consultorio/noche mono vs multifocal), videos promo.

## Estructura
- `brief/` — PDF de análisis vs competencia (Rayner Galaxy), relevamiento del sitio actual.
- `media/raw/` — material recibido por WhatsApp (no se publica). `media/frames/` — extracciones.
- `site/` — el sitio estático (HTML/CSS/JS sin framework, i18n EN/ES/PT).

## Reglas
- Sin commits ni deploys a Vercel sin pedido explícito del usuario.
- `media/raw/` no se versiona ni se publica.
