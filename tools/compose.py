import sys, numpy as np, cv2
from PIL import Image, ImageFilter
S = sys.argv[1]
def warp_screen(quad, size, ss=4):
    # warp supermuestreado (ss x) y luego reducción con INTER_AREA: bordes sin escalones
    scr = cv2.imread(f"{S}/screen.png")
    h, w = scr.shape[:2]
    W, H = size
    q = np.float32(quad)*ss
    src = np.float32([[0,0],[w,0],[w,h],[0,h]])
    pre = cv2.resize(scr, (int(np.linalg.norm(q[1]-q[0])), int(np.linalg.norm(q[3]-q[0]))), interpolation=cv2.INTER_AREA)
    ph, pw = pre.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0,0],[pw,0],[pw,ph],[0,ph]]), q)
    big = cv2.warpPerspective(pre, M, (W*ss, H*ss), flags=cv2.INTER_LINEAR)
    mbig = cv2.warpPerspective(np.full((ph,pw),255,np.uint8), M, (W*ss, H*ss), flags=cv2.INTER_LINEAR)
    out = cv2.resize(big, (W,H), interpolation=cv2.INTER_AREA)
    mask = cv2.resize(mbig, (W,H), interpolation=cv2.INTER_AREA)
    # brillo suave: reflejo diagonal del vidrio
    yy, xx = np.mgrid[0:H,0:W].astype(np.float32)
    glare = np.clip(1 - np.abs((xx - quad[0][0]) * 0.55 + (yy - quad[0][1]) - 120) / 160, 0, 1) * 0.06
    out = out.astype(np.float32) * 0.90
    out = out + 255 * glare[..., None]
    return cv2.cvtColor(np.clip(out,0,255).astype(np.uint8), cv2.COLOR_BGR2RGB), mask
def build(name, quad, out, canvas=(1600,1000), scale=1.0, offset=(0,0), bg_top=(246,249,252), bg_bot=(222,231,240)):
    photo = np.array(Image.open(f"{S}/in/{name}.jpg").convert("RGB")).astype(np.float32)
    cut = np.array(Image.open(f"{S}/{name}_cut.png"))
    alpha = cut[...,3].astype(np.float32)/255
    H, W = photo.shape[:2]
    # 0) neutralizar dominante cálida del piso en zonas de bajo croma (estuche, visor, controles)
    hsv = cv2.cvtColor(photo.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    sat = hsv[...,1]/255
    k = np.clip((sat-0.10)/0.35, 0, 1)            # 0 = gris -> neutralizar fuerte
    hsv[...,1] = hsv[...,1]*(0.25 + 0.75*k)
    photo = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
    # 1) pantalla: contenido nuevo + reflejos originales (screen blend suave)
    scr, m = warp_screen(quad, (W,H))
    m = (m.astype(np.float32)/255)[...,None]
    refl = np.clip(photo - 18, 0, 255)  # reflejos de la foto
    s = scr.astype(np.float32)
    s = 255 - (255 - s)*(255 - refl*0.55)/255   # screen blend
    photo = photo*(1-m) + s*m
    # 2) leve corrección de color: un poco más neutro/limpio
    photo = np.clip((photo - 128)*1.06 + 128 + 4, 0, 255)
    # 3) componer sobre fondo de estudio
    CW, CH = canvas
    yy = np.linspace(0,1,CH)[:,None,None]
    bg = np.array(bg_top,np.float32)*(1-yy) + np.array(bg_bot,np.float32)*yy
    bg = np.repeat(bg, CW, axis=1)
    # viñeta radial suave
    xx = np.linspace(-1,1,CW)[None,:]; y2 = np.linspace(-1,1,CH)[:,None]
    vig = 1 - 0.10*np.clip(xx**2*0.6 + y2**2*0.5, 0, 1)
    bg = bg*vig[...,None]
    sw, sh = int(W*scale), int(H*scale)
    ph = cv2.resize(photo, (sw, sh), interpolation=cv2.INTER_LANCZOS4)
    al = cv2.resize(alpha, (sw, sh), interpolation=cv2.INTER_LINEAR)
    ox, oy = offset
    full_a = np.zeros((CH,CW),np.float32); full_p = np.zeros((CH,CW,3),np.float32)
    full_a[oy:oy+sh, ox:ox+sw] = al; full_p[oy:oy+sh, ox:ox+sw] = ph
    # sombras: contacto (corta, oscura) + ambiente (larga, suave)
    def shadow(blur, dy, strength):
        a = np.roll(full_a, dy, axis=0)
        a = cv2.GaussianBlur(a, (0,0), blur)
        return a*strength
    sh_ = np.clip(shadow(4, 3, 0.55) + shadow(18, 12, 0.30) + shadow(45, 30, 0.18), 0, 0.75)
    bg = bg*(1 - sh_[...,None])
    comp = bg*(1-full_a[...,None]) + full_p*full_a[...,None]
    Image.fromarray(np.clip(comp,0,255).astype(np.uint8)).save(out, quality=90)
q2 = [(705.4,210.4),(1125.5,230.6),(1139.0,499.9),(672.5,453.2)]
build("kit2", q2, f"{S}/out_kit_set.jpg", canvas=(1360,780), scale=1.0, offset=(40,40))
