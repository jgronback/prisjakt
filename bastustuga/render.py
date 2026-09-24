"""Ritar SVG-vyer och bygger HTML-sidan från beräkningarna i generate.py."""
import math
from html import escape


def fmt(v, dec=0):
    s = f"{v:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s


def render(G):
    L, B, T, XP = G["L"], G["B"], G["T"], G["XP"]
    FLOOR, HB, HF, HEAD = G["FLOOR"], G["HB"], G["HF"], G["HEAD"]
    SEC, ANGLE, zr = G["SEC"], G["ANGLE"], G["zr"]
    OVH_F, OVH_B, RAFTER, ROOF_TOP = G["OVH_F"], G["OVH_B"], G["RAFTER"], G["ROOF_TOP"]
    FRONT_OPEN, BACK_OPEN, SD = G["FRONT_OPEN"], G["BACK_OPEN"], G["SAUNA_DOOR"]
    ridge = G["GEOM"]["ridge"]
    roof_th = RAFTER * SEC + ROOF_TOP

    # ---------- SVG-hjälp ----------
    def svg(vb, body, cls="", minw=720, label=""):
        x, y, w, h = vb
        return (f'<div class="dwg-scroll"><svg class="dwg {cls}" viewBox="{x} {y} {w} {h}" '
                f'style="min-width:{minw}px" role="img" aria-label="{escape(label)}">{body}</svg></div>')

    def rect(x, y, w, h, c="", extra=""):
        if w < 0: x, w = x + w, -w
        if h < 0: y, h = y + h, -h
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" class="{c}" {extra}/>'

    def line(x1, y1, x2, y2, c="ln"):
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{c}"/>'

    def poly(pts, c=""):
        return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" class="{c}"/>'

    def text(x, y, s, c="t", size=None, anchor="middle", rot=None):
        st = f' font-size="{size}"' if size else ""
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
        return f'<text x="{x:.1f}" y="{y:.1f}" class="{c}" text-anchor="{anchor}"{st}{tr}>{escape(str(s))}</text>'

    def tick(x, y):
        return line(x - 40, y + 40, x + 40, y - 40, "dim tk")

    def dim_h(xs, y, ext_from=None, size=95, labels=None):
        o = [line(xs[0], y, xs[-1], y, "dim")]
        for i, x in enumerate(xs):
            o.append(tick(x, y))
            if ext_from is not None:
                o.append(line(x, ext_from, x, y + (60 if y > ext_from else -60), "dim ext"))
        for i in range(len(xs) - 1):
            a, b = xs[i], xs[i + 1]
            lab = labels[i] if labels else fmt(round(b - a))
            sz = size if b - a > 330 else size * 0.72
            o.append(text((a + b) / 2, y - 35, lab, "t dimt", sz))
        return "".join(o)

    def dim_v(zs, x, ext_from=None, size=95, labels=None):
        # zs i svg-y
        o = [line(x, zs[0], x, zs[-1], "dim")]
        for z in zs:
            o.append(line(x - 40, z + 40, x + 40, z - 40, "dim tk"))
            if ext_from is not None:
                o.append(line(ext_from, z, x + (60 if x > ext_from else -60), z, "dim ext"))
        for i in range(len(zs) - 1):
            a, b = zs[i], zs[i + 1]
            lab = labels[i] if labels else fmt(round(abs(b - a)))
            o.append(text(x - 35, (a + b) / 2, lab, "t dimt", size, rot=-90))
        return "".join(o)

    def tag(x, y, s):
        box = rect(x - 125, y - 75, 250, 150, "tagbox", 'rx="30"')
        return f'<g class="tag">{box}{text(x, y + 34, s, "t tagt", 95)}</g>'

    def level(x, zsvg, s, anchor="start"):
        d = 1 if anchor == "start" else -1
        return (poly([(x, zsvg), (x - 45, zsvg - 70), (x + 45, zsvg - 70)], "lvl")
                + line(x - 120 * d, zsvg, x + 140 * d, zsvg, "ln thin")
                + text(x + 90 * d, zsvg - 25, s, "t lvlt", 88, anchor))

    # ================= PLAN =================
    Y = lambda y: B - y
    p = []
    inner = [(T, T, XP - 47.5, B - T), (XP + 47.5, T, L - T, B - T)]
    d = f"M0,0 H{L} V{B} H0 Z " + " ".join(
        f"M{x0},{Y(y0)} V{Y(y1)} H{x1} V{Y(y0)} Z" for x0, y0, x1, y1 in inner)
    p.append(f'<path d="{d}" class="wall" fill-rule="evenodd"/>')
    # lavar
    lav = [(T, 695, 1150, "Överlav +1150"), (695, 1185, 750, "Underlav +750")]
    for y0, y1, h, lab in lav:
        p.append(rect(T, Y(y1), XP - 47.5 - T, y1 - y0, "bench"))
        for k in range(1, 6):
            yy = y0 + (y1 - y0) * k / 6
            p.append(line(T, Y(yy), XP - 47.5, Y(yy), "ln slat"))
        p.append(text((T + XP) / 2 - 40, Y((y0 + y1) / 2) + 30, lab, "t lab2", 85))
    # kamin
    kx0, kx1, ky0, ky1 = 195, 595, 1450, 1900
    p.append(rect(kx0, Y(ky1), kx1 - kx0, ky1 - ky0, "stove"))
    p.append(line(kx0, Y(ky1), kx1, Y(ky0), "ln thin") + line(kx0, Y(ky0), kx1, Y(ky1), "ln thin"))
    p.append(f'<circle cx="{(kx0 + kx1) / 2}" cy="{Y((ky0 + ky1) / 2)}" r="75" class="flue"/>')
    p.append(text((kx0 + kx1) / 2, Y(ky0) + 130, "Kamin", "t lab2", 85))
    # öppningar långväggar
    def window_plan(x0, x1, yo, yi):
        return (rect(x0, min(Y(yo), Y(yi)), x1 - x0, T, "paper")
                + line(x0, Y(yo), x1, Y(yo), "ln thin") + line(x0, Y(yi), x1, Y(yi), "ln thin")
                + line(x0, Y((yo + yi) / 2), x1, Y((yo + yi) / 2), "glassl")
                + line(x0, Y(yo), x0, Y(yi), "ln") + line(x1, Y(yo), x1, Y(yi), "ln"))

    for oid, x0, x1, sill, _ in FRONT_OPEN:
        if sill is not None:
            p.append(window_plan(x0, x1, B, B - T))
        else:  # balkongdörr utåt, gångjärn höger
            w = x1 - x0
            p.append(rect(x0, 0, w, T, "paper") + line(x0, 0, x0, T, "ln") + line(x1, 0, x1, T, "ln"))
            p.append(line(x1, 0, x1, -w, "leaf"))
            p.append(f'<path d="M{x0},0 A{w},{w} 0 0,1 {x1},{-w}" class="swing"/>')
            p.append(line(x0, T / 2, x1, T / 2, "glassl"))
        p.append(tag((x0 + x1) / 2, -300 if sill is not None else -300, oid) if False else "")
    for oid, x0, x1, sill, _ in BACK_OPEN:
        w = x1 - x0
        p.append(rect(x0, B - T, w, T, "paper") + line(x0, B - T, x0, B, "ln") + line(x1, B - T, x1, B, "ln"))
        p.append(line(x1, B, x1, B + w, "leaf"))
        p.append(f'<path d="M{x0},{B} A{w},{w} 0 0,0 {x1},{B + w}" class="swing"/>')
    # bastudörr
    _, y0, y1, _, _ = SD
    w = y1 - y0
    p.append(rect(XP - 47.5, Y(y1), T, w, "paper") + line(XP - 47.5, Y(y1), XP + 47.5, Y(y1), "ln")
             + line(XP - 47.5, Y(y0), XP + 47.5, Y(y0), "ln"))
    p.append(line(XP + 47.5, Y(y0), XP + 47.5 + w, Y(y0), "leaf glassleaf"))
    p.append(f'<path d="M{XP + 47.5},{Y(y1)} A{w},{w} 0 0,1 {XP + 47.5 + w},{Y(y0)}" class="swing"/>')
    # rumsnamn
    p.append(text(1030, Y(1880), "BASTU", "t room", 150))
    p.append(text(1030, Y(1880) + 150, f"{fmt(G['in_len_s'] * G['in_w'] / 1e6, 1)} m²", "t lab2", 95))
    p.append(text(4000, Y(1350), "RELAX / FÖRRUM", "t room", 150))
    p.append(text(4000, Y(1350) + 150, f"{fmt(G['in_len_r'] * G['in_w'] / 1e6, 1)} m²", "t lab2", 95))
    # taggar
    for oid, x0, x1, sill, _ in FRONT_OPEN:
        p.append(tag((x0 + x1) / 2, -1130 if False else 470, oid) if False else "")
    tags = [("F1", 1255, 330), ("F2", 3455, 330), ("D2", 4995, 330 + 0), ("D1", 5105, B - 330), ("D3", XP + 470, Y(1755))]
    for s, x, yy in tags:
        p.append(tag(x, yy, s))
    # mått fram (överkant)
    fx = [0] + [v for o in FRONT_OPEN for v in (o[1], o[2])] + [L]
    p.append(dim_h(fx, -1150, ext_from=-40))
    p.append(dim_h([0, L], -1500, ext_from=-40))
    bx = [0, XP, BACK_OPEN[0][1], BACK_OPEN[0][2], L]
    p.append(dim_h(bx, B + 1250, ext_from=B + 40))
    p.append(dim_h([0, L], B + 1600, ext_from=B + 40))
    p.append(dim_v([0, B], -450, ext_from=-40))
    p.append(dim_v([Y(B - T), Y(y1), Y(y0), Y(T)], L + 450, size=85))
    p.append(text(L + 700, B / 2, "D3 i mellanvägg (mätt från baksidan)", "t lab2", 80, rot=-90))
    p.append(text(-80, -1720 - 80, "FRAMSIDA – fönstersida", "t side", 105, "start"))
    p.append(text(-80, B + 1900, "BAKSIDA – entré", "t side", 105, "start"))
    # snitt-markering A–A
    sx = 1000
    p.append(line(sx, -700, sx, -250, "cut") + line(sx, B + 250, sx, B + 700, "cut"))
    p.append(text(sx, -760, "A", "t cutt", 120) + text(sx, B + 840, "A", "t cutt", 120))
    # norrpil/skala
    plan_svg = svg((-900, -2000, L + 1900, B + 4100), "".join(p), label="Planritning bastustuga")

    # ================= FASADER =================
    def facade(title, u_of_x, openings, back=False):
        f = []
        base = 208
        top_wall = FLOOR + (HB if back else HF)
        z = lambda v: -v
        # mark
        f.append(line(-700, 0, L + 700, 0, "ground"))
        f.append(rect(-700, 0, L + 1400, 90, "groundfill"))
        for px in G["PLINTS_X"]:
            u = u_of_x(px)
            f.append(rect(u - 100, z(base), 200, base, "plint"))
        if back:
            fb = FLOOR + zr(-OVH_B)
            ft = fb + roof_th
            f.append(rect(0, z(fb), L, fb - base, "clad"))
            f.append(rect(-22, z(ridge), L + 44, ridge - ft, "roofplane"))
            f.append(rect(-22, z(ft), L + 44, ft - fb, "fascia"))
        else:
            fb = FLOOR + zr(B + OVH_F)
            f.append(rect(0, z(top_wall), L, top_wall - base, "clad"))
            f.append(rect(-22, z(ridge), L + 44, ridge - fb, "fascia"))
            f.append(poly([(0, z(top_wall)), (L, z(top_wall)), (L + 22, z(fb)), (-22, z(fb))], "soffit"))
        # panellinjer
        zz = base + 132
        lim = (FLOOR + zr(-OVH_B)) if back else top_wall
        while zz < lim:
            f.append(line(0, z(zz), L, z(zz), "board"))
            zz += 132
        f.append(line(0, z(FLOOR - 22), L, z(FLOOR - 22), "ln thin"))
        for oid, x0, x1, sill, name in openings:
            u0, u1 = sorted((u_of_x(x0), u_of_x(x1)))
            s = FLOOR + (sill or 0)
            h = FLOOR + HEAD
            f.append(rect(u0 - 60, z(h + 60), u1 - u0 + 120, h - s + 120 if sill else h - s + 60, "trim"))
            f.append(rect(u0, z(h), u1 - u0, h - s, "frame"))
            if sill is None:
                f.append(rect(u0 + 70, z(h - 70), u1 - u0 - 140, h - s - 70 - (450 if oid == "D2" else 0),
                              "glass" if oid == "D2" else "doorleaf"))
                if oid == "D1":
                    f.append(rect(u0 + 70 + (u1 - u0 - 140) * 0.15, z(h - 300), (u1 - u0 - 140) * 0.7, 900, "glass"))
                    f.append(f'<circle cx="{u0 + 150}" cy="{z(FLOOR + 1050)}" r="22" class="knob"/>')
                else:
                    f.append(f'<circle cx="{u0 + 110 if u_of_x(x1) > u_of_x(x0) else u1 - 110}" cy="{z(FLOOR + 1050)}" r="22" class="knob"/>')
            else:
                f.append(rect(u0 + 70, z(h - 70), u1 - u0 - 140, h - s - 140, "glass"))
            f.append(tag((u0 + u1) / 2, z(h + 280), oid))
        # skorsten (bastukamin)
        cu = u_of_x(395)
        roof_at = FLOOR + zr(1675) + roof_th
        f.append(rect(cu - 75, z(4300), 150, 4300 - roof_at, "chim"))
        f.append(rect(cu - 110, z(4300), 220, 60, "chimcap"))
        # nivåer
        lx = L + 350
        f.append(level(lx, z(0), "±0 mark"))
        f.append(level(lx, z(FLOOR), f"+{fmt(FLOOR)} golv"))
        f.append(level(lx, z(top_wall), f"+{fmt(top_wall)} ök stomme"))
        f.append(level(lx, z(ridge), f"+{fmt(round(ridge, -1))} högsta punkt"))
        f.append(dim_h([0, L], 420, ext_from=10))
        return svg((-800, -4550, L + 2800, 5150), "".join(f), label=title)

    front_svg = facade("Fasad framsida", lambda x: L - x, FRONT_OPEN)
    back_svg = facade("Fasad baksida", lambda x: x, BACK_OPEN, back=True)

    # gavel (vänster, bastusidan) sett utifrån: u = 2900 - y
    g = []
    U = lambda y: (B + OVH_F) - y
    z = lambda v: -v
    g.append(line(-700, 0, 3200 + 700, 0, "ground") + rect(-700, 0, 4600, 90, "groundfill"))
    for py in (45, B - 45):
        g.append(rect(U(py) - 100, z(208), 200, 208, "plint"))
    wall = [(U(0), z(208)), (U(B), z(208)), (U(B), z(FLOOR + zr(B))), (U(0), z(FLOOR + zr(0)))]
    g.append(poly(wall, "clad"))
    zz = 208 + 132
    while zz < FLOOR + HF:
        yb = max(0, min(B, (zz - FLOOR - HB) / G["SLOPE"])) if zz > FLOOR + HB else 0
        if zz < FLOOR + zr(B):
            g.append(line(U(yb), z(zz), U(B), z(zz), "board"))
        zz += 132
    rb = [(U(-OVH_B), z(FLOOR + zr(-OVH_B))), (U(B + OVH_F), z(FLOOR + zr(B + OVH_F))),
          (U(B + OVH_F), z(FLOOR + zr(B + OVH_F) + roof_th)), (U(-OVH_B), z(FLOOR + zr(-OVH_B) + roof_th))]
    g.append(poly(rb, "fascia"))
    cu = U(1675)
    roof_at = FLOOR + zr(1675) + roof_th
    g.append(rect(cu - 75, z(4300), 150, 4300 - roof_at, "chim") + rect(cu - 110, z(4300), 220, 60, "chimcap"))
    g.append(line(U(0), z(FLOOR - 22), U(B), z(FLOOR - 22), "ln thin"))
    g.append(dim_h([U(B + OVH_F), U(B), U(0), U(-OVH_B)], 420, ext_from=10))
    g.append(dim_v([z(FLOOR), z(FLOOR + HF)], U(B) - 350, ext_from=U(B) - 10))
    g.append(dim_v([z(FLOOR), z(FLOOR + HB)], U(0) + 350, ext_from=U(0) + 10))
    g.append(text(U(B) + 30, z(FLOOR + HF + 900), "← framsida", "t lab2", 90, "start"))
    g.append(text(U(0) - 30, z(FLOOR + HF + 900), "baksida →", "t lab2", 90, "end"))
    g.append(text(U(1250), z(ridge + 250), f"taklutning {fmt(ANGLE, 1)}°", "t lab2", 90))
    lx = 3200 + 350
    g.append(level(lx, z(0), "±0 mark") + level(lx, z(FLOOR), f"+{FLOOR} golv")
             + level(lx, z(ridge), f"+{fmt(round(ridge, -1))}"))
    gable_svg = svg((-800, -4550, 3200 + 2400, 5150), "".join(g), minw=520, label="Gavel")

    # ================= SEKTION A–A =================
    s = []
    U = lambda y: y + OVH_B
    s.append(line(-600, 0, U(B + OVH_F) + 600, 0, "ground") + rect(-600, 0, U(B + OVH_F) + 1200, 90, "groundfill"))
    for py in (45, B - 45):
        s.append(rect(U(py) - 100, z(208), 200, 208, "plint"))
    # bjälklag
    s.append(rect(U(0), z(378), B, 170, "cutwood"))
    s.append(rect(U(0), z(FLOOR), B, 22, "board2"))
    s.append(rect(U(90), z(370), B - 180, 150, "insul"))
    # väggar (snitt)
    s.append(rect(U(0), z(FLOOR + HB), T, HB, "cutwall"))
    fs, fh = FLOOR + FRONT_OPEN[0][3], FLOOR + HEAD
    s.append(rect(U(B - T), z(fs), T, fs - FLOOR, "cutwall"))
    s.append(rect(U(B - T), z(FLOOR + HF), T, FLOOR + HF - fh, "cutwall"))
    s.append(rect(U(B - T), z(fh), T, fh - fs, "paper") + line(U(B - T / 2), z(fh), U(B - T / 2), z(fs), "glassl"))
    s.append(rect(U(-60), z(FLOOR + zr(-OVH_B)), 60, FLOOR + zr(-OVH_B) - 208, "cladcut"))
    s.append(rect(U(B), z(FLOOR + HF), 60, FLOOR + HF - 208, "cladcut"))
    # tak
    rp = [(U(-OVH_B), z(FLOOR + zr(-OVH_B))), (U(B + OVH_F), z(FLOOR + zr(B + OVH_F))),
          (U(B + OVH_F), z(FLOOR + zr(B + OVH_F) + roof_th)), (U(-OVH_B), z(FLOOR + zr(-OVH_B) + roof_th))]
    s.append(poly(rp, "cutwood"))
    ip = [(U(T), z(FLOOR + zr(T) + 10)), (U(B - T), z(FLOOR + zr(B - T) + 10)),
          (U(B - T), z(FLOOR + zr(B - T) + 155)), (U(T), z(FLOOR + zr(T) + 155))]
    s.append(poly(ip, "insul"))
    cp = [(U(T), z(FLOOR + zr(T))), (U(B - T), z(FLOOR + zr(B - T))),
          (U(B - T), z(FLOOR + zr(B - T) - 43)), (U(T), z(FLOOR + zr(T) - 43))]
    s.append(poly(cp, "board2"))
    # lavar
    s.append(rect(U(T), z(FLOOR + 1150), 600, 40, "bench"))
    s.append(rect(U(T + 600), z(FLOOR + 750), 490, 40, "bench"))
    s.append(rect(U(T + 1090), z(FLOOR + 350), 300, 40, "bench"))
    for yy, h in ((T + 40, 1110), (T + 560, 1110), (T + 640, 710), (T + 1050, 710), (T + 1110, 310), (T + 1350, 310)):
        s.append(rect(U(yy), z(FLOOR + h), 40, h, "benchleg"))
    # kamin bakom snittet
    s.append(rect(U(1450), z(FLOOR + 800), 450, 800, "stove"))
    s.append(rect(U(1600), z(4300), 150, 4300 - FLOOR - 800, "chim"))
    s.append(text(U(1675), z(FLOOR + 430), "Kamin", "t lab2", 85))
    # höjdmått
    s.append(dim_v([z(FLOOR), z(FLOOR + 1150)], U(T) + 700 + 0, size=85))
    s.append(dim_v([z(FLOOR + 1150), z(FLOOR + zr(T) - 43)], U(T) + 250, size=85))
    s.append(dim_v([z(FLOOR), z(FLOOR + zr(B - T) - 43)], U(B - T) - 200, size=85))
    s.append(dim_v([z(fs), z(fh)], U(B) + 250, ext_from=U(B) + 70, size=85))
    s.append(dim_v([z(0), z(FLOOR)], U(0) - 350, ext_from=U(0) - 70, size=85))
    s.append(dim_h([U(-OVH_B), U(0), U(B), U(B + OVH_F)], 420, ext_from=10))
    # skikt-etiketter
    lx = U(B + OVH_F) + 250
    labs = [
        (FLOOR + zr(B) + 180, "TAK: ytpapp + underlagspapp, råspont 23,"),
        (FLOOR + zr(B) + 80, "luftspalt 25, 45x170 c/c 600 + mineralull 145,"),
        (FLOOR + zr(B) - 20, "bastufolie, glespanel 28x70, bastupanel"),
        (FLOOR + 1700, "VÄGG: panel 22, läkt 22x45, vindskydd 12,"),
        (FLOOR + 1600, "45x95 c/c 600 + mineralull 95, bastufolie,"),
        (FLOOR + 1500, "läkt 22x45 (luftspalt), bastupanel"),
        (FLOOR + 350, "GOLV: våtrumsmatta, golvspån 22,"),
        (FLOOR + 250, "45x170 c/c 600 + mineralull 170,"),
        (FLOOR + 150, "vindskydd + gnagarnät, plint"),
    ]
    for zz, t in labs:
        s.append(text(lx, z(zz), t, "t lab3", 80, "start"))
    s.append(level(U(0) - 700, z(0), "±0", "end") + level(U(0) - 700, z(FLOOR), f"+{FLOOR}", "end")
             + level(U(0) - 700, z(ridge), f"+{fmt(round(ridge, -1))}", "end"))
    s.append(text(U(0) + 60, z(FLOOR + zr(0) + 700), "baksida", "t lab2", 85, "start"))
    s.append(text(U(B) - 60, z(FLOOR + zr(B) + 1000), "framsida", "t lab2", 85, "end"))
    sect_svg = svg((-1700, -4550, 3200 + 5600, 5150), "".join(s), minw=760, label="Sektion A-A genom bastun")

    # ================= GRUND / BJÄLKLAG =================
    q = []
    q.append(rect(0, 0, L, 90, "cutwood") + rect(0, B - 90, L, 90, "cutwood"))
    for jx in G["JOIST_X"]:
        q.append(rect(jx - 22.5, 90, 45, B - 180, "joist"))
    for px in G["PLINTS_X"]:
        for py in (45, B - 45):
            q.append(f'<circle cx="{px}" cy="{py}" r="100" class="plintc"/>')
    q.append(line(XP, -120, XP, B + 120, "dashed"))
    q.append(text(XP, -180, "mellanvägg", "t lab2", 80))
    q.append(text(300, B / 2, "extra under kamin", "t lab2", 70, rot=-90))
    q.append(dim_h(G["PLINTS_X"], B + 450, ext_from=B + 110, size=85))
    q.append(text(-80, B + 750, "Plintar c/c (2 rader × 5)", "t lab2", 80, "start"))
    q.append(dim_h(sorted(G["JOIST_X"]), -450, ext_from=-10, size=70,
                   labels=None))
    q.append(text(-80, -750, "Golvbjälkar 45x170, avstånd mellan centrum", "t lab2", 80, "start"))
    q.append(dim_v([0, 90, B - 90, B], L + 400, ext_from=L + 20, size=75))
    grund_svg = svg((-700, -1000, L + 1500, B + 2000), "".join(q), label="Grund och bjälklag")

    # ================= VÄGGSTOMMAR =================
    def frame_long(title, H, studs, crips, openings, mirror):
        u = (lambda x: L - x) if mirror else (lambda x: x)
        f = []
        f.append(rect(0, -45, L, 45, "wood"))
        f.append(rect(0, -H, L, 45, "wood") + rect(0, -(H - 45), L, 45, "wood"))
        for c, t in studs:
            uc = u(c)
            if t == "trim":
                f.append(rect(uc - 22.5, -HEAD, 45, HEAD - 45, "wood2"))
            else:
                f.append(rect(uc - 22.5, -(H - 90), 45, H - 135, "wood"))
        for (oid, x0, x1, sill, _), (_, cps) in zip(openings, crips):
            a, b = sorted((u(x0), u(x1)))
            f.append(rect(a - 45, -(HEAD + 145), b - a + 90, 145, "wood3"))
            for c in cps:
                f.append(rect(u(c) - 22.5, -(H - 90), 45, H - 90 - HEAD - 145, "wood2"))
            if sill is not None:
                f.append(rect(a, -sill, b - a, 45, "wood3"))
                for c in cps:
                    f.append(rect(u(c) - 22.5, -(sill - 45), 45, sill - 90, "wood2"))
            f.append(text((a + b) / 2, -(HEAD - 250), f"{oid}", "t tagt2", 120))
            f.append(text((a + b) / 2, -(HEAD - 400), f"{fmt(x1 - x0)}×{fmt(HEAD - (sill or 0))}", "t lab2", 85))
        # koordinatmått (centrum regel)
        for c, t in studs:
            if t == "trim":
                continue
            f.append(text(u(c) + 25, 140, fmt(round(u(c))), "t coord", 70, "end", rot=-90))
        f.append(text(-60, 540, "Mått = regelns centrum från vänster hörn i vyn", "t lab2", 75, "start"))
        f.append(dim_v([-H, 0], -300, ext_from=-10, size=85))
        return svg((-600, -(H + 250), L + 900, H + 900), "".join(f), label=title)

    def frame_sloped(title, studs, door=None, mirror=False):
        # u längs väggen, 0 = vänster i vyn. Gavel C sett utifrån: hög sida (fram) till vänster.
        Y0, Y1 = T, B - T
        u = (lambda y: Y1 - y) if mirror else (lambda y: y - Y0)
        W = Y1 - Y0
        f = []
        f.append(rect(0, -45, W, 45, "wood"))
        top = lambda y: zr(y)
        pl = [(u(Y0), -top(Y0)), (u(Y1), -top(Y1)), (u(Y1), -(top(Y1) - 45 * SEC)), (u(Y0), -(top(Y0) - 45 * SEC))]
        f.append(poly(pl, "wood"))
        for c, t in studs:
            ya, yb = c - 22.5, c + 22.5
            if t == "trim":
                f.append(rect(min(u(ya), u(yb)), -door[3], 45, door[3] - 45, "wood2"))
                continue
            pts = [(u(ya), -45), (u(yb), -45), (u(yb), -(top(yb) - 45 * SEC)), (u(ya), -(top(ya) - 45 * SEC))]
            f.append(poly(pts, "wood"))
            f.append(text(u(c) + 25, 140, fmt(round(c)), "t coord", 70, "end", rot=-90))
        f.append(text(-60, 540, "Mått = regelns centrum från baksidans utsida", "t lab2", 75, "start"))
        if door:
            _, y0, y1, h, _ = door
            a, b = sorted((u(y0), u(y1)))
            f.append(rect(a - 45, -(h + 95), b - a + 90, 95, "wood3"))
            for c in [c for c in G["Y_GRID"] if y0 < c < y1]:
                pts = [(u(c - 22.5), -(h + 95)), (u(c + 22.5), -(h + 95)),
                       (u(c + 22.5), -(top(c + 22.5) - 45 * SEC)), (u(c - 22.5), -(top(c - 22.5) - 45 * SEC))]
                f.append(poly(pts, "wood2"))
            f.append(text((a + b) / 2, -(h - 250), "D3", "t tagt2", 120))
            f.append(text((a + b) / 2, -(h - 400), f"{fmt(y1 - y0)}×{fmt(h)}", "t lab2", 85))
        f.append(dim_v([-top(Y1 if not mirror else Y1), 0], -300 if mirror else W + 300, ext_from=-10 if mirror else W + 10, size=85))
        return svg((-600, -(HF + 250), W + 1200, HF + 900), "".join(f), minw=420, label=title)

    fr_front = frame_long("Stomme framsida", HF, G["front_studs"], G["front_crip"], FRONT_OPEN, True)
    fr_back = frame_long("Stomme baksida", HB, G["back_studs"], G["back_crip"], BACK_OPEN, False)
    fr_gable = frame_sloped("Stomme gavel", G["gable_studs"], mirror=True)
    fr_part = frame_sloped("Stomme mellanvägg", G["part_studs"], door=SD)

    # ================= TABELLER =================
    groups = {}
    for gname, part, dim, ln, n, note in G["pieces"]:
        groups.setdefault(gname, []).append((part, dim, ln, n, note))
    cut_html = []
    for gname, rows in groups.items():
        cut_html.append(f'<tr class="grp"><th colspan="5">{escape(gname)}</th></tr>')
        for part, dim, ln, n, note in rows:
            cut_html.append(f"<tr><td>{escape(part)}</td><td class='num'>{escape(dim)}</td>"
                            f"<td class='num'>{fmt(ln)}</td><td class='num'>{n}</td><td class='note'>{escape(note)}</td></tr>")
    buy_html = []
    for dim, (cnt, total, waste, n) in G["purchase"].items():
        lens = ", ".join(f"{c} × {fmt(s / 1000, 1)} m" for s, c in cnt.items())
        buy_html.append(f"<tr><td class='num'>{escape(dim)}</td><td>{lens}</td><td class='num'>{fmt(total / 1000, 1)}</td>"
                        f"<td class='num'>{fmt(waste / 1000, 1)}</td><td class='num'>{n}</td></tr>")
    mat_html = []
    for gname, m, qn, unit, note in G["sheets"]:
        mat_html.append(f"<tr><td>{escape(gname)}</td><td>{escape(m)}</td><td class='num'>{fmt(qn)}</td>"
                        f"<td>{escape(unit)}</td><td class='note'>{escape(note)}</td></tr>")
    op_rows = []
    for oid, x0, x1, sill, name in FRONT_OPEN + BACK_OPEN:
        wall = "A fram" if (oid, x0) in [(o[0], o[1]) for o in FRONT_OPEN] else "B bak"
        op_rows.append((oid, name, wall, f"{fmt(x1 - x0)} × {fmt(HEAD - (sill or 0))}", fmt(sill or 0), f"x {fmt(x0)}–{fmt(x1)}"))
    op_rows.append((SD[0], SD[4], "E mellanvägg", f"{fmt(SD[2] - SD[1])} × {fmt(SD[3])}", "0", f"y {fmt(SD[1])}–{fmt(SD[2])} från baksidan"))
    op_rows.sort()
    op_html = "".join(f"<tr><td class='num'><b>{a}</b></td><td>{escape(b)}</td><td>{c}</td><td class='num'>{d}</td>"
                      f"<td class='num'>{e}</td><td class='num'>{f_}</td></tr>" for a, b, c, d, e, f_ in op_rows)

    ctx = dict(
        plan=plan_svg, front=front_svg, back=back_svg, gable=gable_svg, sect=sect_svg, grund=grund_svg,
        fr_front=fr_front, fr_back=fr_back, fr_gable=fr_gable, fr_part=fr_part,
        cut="".join(cut_html), buy="".join(buy_html), mat="".join(mat_html), ops=op_html,
        ridge=fmt(round(ridge, -1)), angle=fmt(ANGLE, 1), rafter=fmt(G["rafter_len"]),
        sauna=fmt(G["in_len_s"] * G["in_w"] / 1e6, 1), relax=fmt(G["in_len_r"] * G["in_w"] / 1e6, 1),
        ch_b=fmt(zr(T) - 43), ch_f=fmt(zr(B - T) - 43), roof=fmt(G["roof_area"], 1), facade=fmt(G["facade_net"], 1),
    )
    tpl = (G["Path"](G["__file__"]).with_name("template.html")).read_text(encoding="utf-8")
    for k, v in ctx.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    return tpl
