#!/usr/bin/env python3
"""Genera el sitio estático en site/ (EN en la raíz, ES en /es, PT en /pt).

Plantillas: src/layout.html + src/pages/*.html con marcadores {{clave}}.
Textos: src/i18n/{en,es,pt}.json (planos). Si falta una clave en es/pt cae a en (y avisa).
Marcadores especiales: {{base}} (prefijo de idioma), {{lang}}, {{page}}, {{cur:<page>}}
(aria-current en el menú), {{langurl:<xx>}} (misma página en otro idioma).
Uso: python3 build.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC, OUT = ROOT / "src", ROOT / "site"
LANGS = {"en": "", "es": "/es", "pt": "/pt"}
TOKEN = re.compile(r"\{\{\s*([\w:.-]+)\s*\}\}")


def main() -> int:
    strings = {l: json.loads((SRC / "i18n" / f"{l}.json").read_text(encoding="utf-8")) for l in LANGS}
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    missing = set()
    pages = sorted((SRC / "pages").glob("*.html"))
    for lang, base in LANGS.items():
        for p in pages:
            name = p.stem

            def render(text: str, depth: int = 0) -> str:
                def sub(m):
                    k = m.group(1)
                    if k == "base":
                        return base
                    if k == "lang":
                        return lang
                    if k == "page":
                        return name
                    if k.startswith("cur:"):
                        return ' aria-current="page"' if k[4:] == name else ""
                    if k.startswith("langurl:"):
                        l2 = k[8:]
                        return f"{LANGS[l2]}/{name}.html" if name != "index" else (LANGS[l2] + "/")
                    if k.startswith("langcur:"):
                        return ' aria-current="true"' if k[8:] == lang else ""
                    if k in strings[lang]:
                        v = strings[lang][k]
                    elif k in strings["en"]:
                        missing.add(f"{lang}:{k}")
                        v = strings["en"][k]
                    else:
                        raise SystemExit(f"Clave sin texto: {k} (en {p.name})")
                    return render(v, depth + 1) if depth < 3 else v
                return TOKEN.sub(sub, text)

            body = p.read_text(encoding="utf-8")
            title_key = f"title.{name}"
            html = layout.replace("<!--CONTENT-->", body)
            html = html.replace("{{title}}", "{{" + title_key + "}}")
            out = OUT / base.lstrip("/") / f"{name}.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(html), encoding="utf-8")
    for m in sorted(missing):
        print("falta traducción:", m, file=sys.stderr)
    print(f"OK: {len(pages)} páginas x {len(LANGS)} idiomas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
