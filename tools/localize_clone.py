"""Localiza en site-actual/ los assets de www.eyekonmedical.com que wget no bajó (lazy-load)."""
import re, sys, os, urllib.request, urllib.parse, pathlib
root = pathlib.Path(sys.argv[1])
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120"}
pat = re.compile(r'https?://(?:www\.)?eyekonmedical\.com/((?:wp-content|wp-includes)/[^"\'\s)>,]+)')
def fetch(rel):
    rel_clean = urllib.parse.unquote(rel.split('?')[0].split('#')[0])
    dst = root / rel_clean
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            req = urllib.request.Request("https://www.eyekonmedical.com/" + rel.split('#')[0], headers=UA)
            dst.write_bytes(urllib.request.urlopen(req, timeout=60).read())
            print("ok", rel_clean)
        except Exception as e:
            print("FAIL", rel, e); return None
    return rel_clean
for f in [root/"index.html"] + list(root.glob("wp-content/**/*.css")):
    txt = f.read_text(encoding="utf-8", errors="replace")
    def rep(m):
        local = fetch(m.group(1))
        if not local: return m.group(0)
        return os.path.relpath(root/local, f.parent)
    new = pat.sub(rep, txt)
    if new != txt: f.write_text(new, encoding="utf-8"); print("rewrote", f)
