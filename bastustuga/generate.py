#!/usr/bin/env python3
"""Genererar ritning + kaplista för bastustuga 2,5 x 6,0 m (bastustuga.html).

Alla mått i mm. Koordinater:
  x = längs byggnaden, 0 = vänster gavel (bastusidan) sett när man står vid baksidan.
  y = tvärs byggnaden, 0 = baksidans yttre stomliv (entré), 2500 = framsidans (fönstersidan).
  z = höjd över färdigt golv (golvspånskivans ök) om inget annat anges.
"""
import math
from collections import defaultdict
from pathlib import Path

# ---------- Grundmått ----------
L, B = 6000, 2500          # stommens yttermått
T = 95                     # regeldjup ytterväggar/mellanvägg
XP = 2000                  # mellanväggens centrum (bastu 2,0 m inkl. halva mellanväggen)
FLOOR = 400                # golv ök över mark (ca)
HB, HF = 2400, 2700        # stomhöjd bak (entré) resp. fram (fönster), från golv till ök hammarband
SLOPE = (HF - HB) / (B - T)            # takbalkens underkant: z(0)=HB, z(2405)=HF
SEC = math.sqrt(1 + SLOPE ** 2)
ANGLE = math.degrees(math.atan(SLOPE))
ANG_S = f"{ANGLE:.1f}".replace(".", ",")
RAFTER = 170               # takbalk 45x170
ROOF_TOP = 23 + 5          # råspont + papp
OVH_F, OVH_B = 400, 300    # takutsprång fram / bak (horisontellt)
HEAD = 2110                # överkant karmöppningar (dörrar + fönster), samma linje
KERF = 5

def zr(y):  # takbalkens underkant vid y
    return HB + SLOPE * y

# Öppningar i långväggar: (id, x0, x1, bröstning (None = dörr), namn)
FRONT_OPEN = [
    ("F1", 650, 1860, 1100, "Bastufönster 12x10, fast, härdat isolerglas"),
    ("F2", 2550, 4360, 600, "Relaxfönster 18x15"),
    ("D2", 4540, 5450, None, "Balkongdörr 9x21, glasad"),
]
BACK_OPEN = [
    ("D1", 4600, 5610, None, "Ytterdörr 10x21"),
]
# Bastudörr i mellanväggen (y-led)
SAUNA_DOOR = ("D3", 1350, 2160, 1910, "Bastudörr glas 8x19 (utåtgående)")

pieces = []  # (grupp, del, dim, längd, antal, kommentar)

def add(group, part, dim, length, n, note=""):
    pieces.append((group, part, dim, int(round(length)), n, note))

# ---------- Långväggar ----------
def long_wall(name, H, openings):
    full = H - 45 - 90
    studs = []   # (center, typ)
    zones = []
    for (oid, x0, x1, sill, _) in openings:
        zones.append((x0 - 90, x1 + 90))
        studs += [(x0 - 67.5, "king"), (x0 - 22.5, "trim"), (x1 + 22.5, "trim"), (x1 + 67.5, "king")]
    grid = [22.5] + [600 * k for k in range(1, 10)] + [L - 22.5]
    cripple_pos = defaultdict(list)
    for c in grid:
        hit = [o for o, z in zip(openings, zones) if z[0] < c < z[1]]
        if hit:
            o = hit[0]
            if o[1] < c < o[2]:
                cripple_pos[o[0]].append(c)
            continue
        studs.append((c, "std"))
    for c in [67.5, L - 67.5, XP - 70, XP + 70]:     # hörn- och mellanväggsreglar
        if all(abs(c - s) >= 45 for s, _ in studs) and not any(z[0] < c < z[1] for z in zones):
            studs.append((c, "extra"))
    studs.sort()
    g = f"Vägg {name}"
    add(g, "Syll", "45x95", L, 1, "Kapas bort i dörröppning efter resning")
    add(g, "Hammarband (dubbelt)", "45x95", L, 2, "")
    n_full = sum(1 for _, t in studs if t in ("std", "king", "extra"))
    add(g, "Regel, hel höjd", "45x95", full, n_full, "inkl. hörn-, anslutnings- och sidoreglar")
    trims = sum(1 for _, t in studs if t == "trim")
    add(g, "Bärregel vid öppning", "45x95", HEAD - 45, trims, "står på syll, bär överliggare")
    crip = []
    for (oid, x0, x1, sill, _) in openings:
        w = x1 - x0
        cp = cripple_pos[oid] or [(x0 + x1) / 2]
        add(g, f"Överliggare {oid}", "45x145", w + 90, 2, "på högkant, spikas ihop")
        add(g, f"Kortling över {oid}", "45x95", H - 90 - (HEAD + 145), len(cp), "")
        if sill is not None:
            add(g, f"Bröstningsregel {oid}", "45x95", w, 1, "liggande")
            add(g, f"Kortling under {oid}", "45x95", sill - 90, len(cp), "")
        crip.append((oid, cp))
    return studs, crip

back_studs, back_crip = long_wall("B – baksida (entré)", HB, BACK_OPEN)
front_studs, front_crip = long_wall("A – framsida (fönster)", HF, FRONT_OPEN)

# ---------- Gavlar och mellanvägg (snedkapade) ----------
Y_GRID = [T + 22.5, 600, 1200, 1800, B - T - 22.5]
TOP_SLOPED = (B - 2 * T) * SEC

def sloped_len(yc):
    return zr(yc + 22.5) - 45 - 45 * SEC   # långsida

def gable(name, n_walls=1, door=None):
    g = f"Vägg {name}"
    add(g, "Syll", "45x95", B - 2 * T, n_walls, "")
    add(g, "Hammarband, snett", "45x95", TOP_SLOPED, n_walls, f"ändar snedkapas {ANG_S}°")
    studs = []
    for yc in Y_GRID:
        if door and door[1] - 90 < yc < door[2] + 90:
            continue
        studs.append((yc, "std"))
    if door:
        _, y0, y1, h, _ = door
        studs += [(y0 - 67.5, "king"), (y0 - 22.5, "trim"), (y1 + 22.5, "trim"), (y1 + 67.5, "king")]
    studs.sort()
    for yc, t in studs:
        if t == "trim":
            continue
        add(g, "Regel, snedkapad", "45x95", math.ceil(sloped_len(yc)), n_walls,
            f"läge {yc:.0f} från baksidans utsida; långsida, snedkapas {ANG_S}°")
    if door:
        _, y0, y1, h, _ = door
        add(g, "Bärregel vid dörr", "45x95", h - 45, 2, "")
        add(g, "Överliggare D3", "45x95", y1 - y0 + 90, 2, "på högkant (icke bärande vägg)")
        cps = [c for c in Y_GRID if y0 < c < y1] or [(y0 + y1) / 2]
        for c in cps:
            add(g, "Kortling över D3", "45x95", math.ceil(zr(c + 22.5) - 45 * SEC - (h + 95)), 1,
                "långsida, snedkapas")
    return studs

gable_studs = gable("C/D – gavlar (2 st lika)", n_walls=2)
part_studs = gable("E – mellanvägg bastu/relax", door=SAUNA_DOOR)

# ---------- Bjälklag ----------
JOIST_X = [22.5] + [600 * k for k in range(1, 10)] + [L - 22.5] + [XP, 300]
JOIST_X.sort()
JOIST_LEN = B - 2 * 90
add("Bjälklag", "Kantbalk (dubbel, 2 per långsida)", "45x170", L, 4, "spikas/skruvas ihop parvis")
add("Bjälklag", "Golvbjälke", "45x170", JOIST_LEN, len(JOIST_X),
    "c/c 600 + extra under mellanvägg och kamin, i balkskor")
PLINTS_X = [150, 1500, 3000, 4500, 5850]
add("Bjälklag", "Nätläkt under isolering", "22x45", L, 6, "håller vindskydd/nät under bjälkar")

# ---------- Tak ----------
RAFTER_X = sorted([22.5] + [600 * k for k in range(1, 10)] + [L - 22.5] + [XP])
rafter_len = (B + OVH_F + OVH_B) * SEC
add("Tak", "Takbalk", "45x170", math.ceil(rafter_len), len(RAFTER_X),
    f"lutning {ANG_S}°, mått längs balk, lodkapas i ändar")
add("Tak", "Takfotsbräda fram/bak", "22x145", L + 2 * 22, 2, "")
add("Tak", "Vindskiva gavel", "22x145", math.ceil(rafter_len), 2, "")
ceil_rows = math.ceil((B - 2 * T) * SEC / 400) + 1
add("Tak", "Glespanel innertak c/c 400", "28x70", L, ceil_rows, "kapas per rum (bastu 1858 / relax 3858)")

# ---------- Lavar ----------
SAUNA_IN = XP - 47.5 - T      # invändig längd i bastun (x)
add("Lavar", "Lavbräda överlav", "28x90 asp/al", SAUNA_IN - 10, 6, "10 mm springa")
add("Lavar", "Lavbräda underlav", "28x90 asp/al", SAUNA_IN - 10, 5, "")
add("Lavar", "Lavbräda fotpall (lös)", "28x90 asp/al", 900, 4, "")
add("Lavar", "Lavstomme (ramverk, ben, reglar)", "45x70", 3000, 6, "kapas på plats, ca 18 lpm")

# ---------- Ytor ----------
def opening_area(ops, door_h=HEAD):
    a = 0
    for (_, x0, x1, sill, _) in ops:
        a += (x1 - x0) * (HEAD - (sill or 0))
    return a / 1e6

rim = 22 + 170
gross_back = L * (HB + rim) / 1e6
gross_front = L * (HF + rim) / 1e6
gross_gable = (B + 2 * 22) * ((HB + HF) / 2 + rim) / 1e6
facade_net = gross_back + gross_front + 2 * gross_gable - opening_area(BACK_OPEN) - opening_area(FRONT_OPEN)
roof_area = L * rafter_len / 1e6

in_len_s, in_len_r = SAUNA_IN, L - T - (XP + 47.5)
in_w = B - 2 * T
avg_h = (HB + HF) / 2
f1 = FRONT_OPEN[0]; f2 = FRONT_OPEN[1]; d2 = FRONT_OPEN[2]; d1 = BACK_OPEN[0]
a = lambda o: (o[2] - o[1]) * (HEAD - (o[3] or 0)) / 1e6
d3a = (SAUNA_DOOR[2] - SAUNA_DOOR[1]) * SAUNA_DOOR[3] / 1e6
sauna_wall = (in_len_s * HB + in_len_s * HF + in_w * avg_h * 2) / 1e6 - a(f1) - d3a
relax_wall = (in_len_r * HB + in_len_r * HF + in_w * avg_h * 2) / 1e6 - a(f2) - a(d2) - a(d1) - d3a
sauna_ceil = in_len_s * in_w * SEC / 1e6
relax_ceil = in_len_r * in_w * SEC / 1e6
outer_wall_net = (L * HB + L * HF + 2 * in_w * avg_h) / 1e6 - a(f1) - a(f2) - a(d1) - a(d2)
part_net = in_w * avg_h / 1e6 - d3a
floor_area = L * B / 1e6

PANEL_COVER = 0.132   # m, ytterpanel 22x145 (kontrollera täckbredd)
RASPONT_COVER = 0.085
INNER_COVER = 0.085   # m, innerpanel ca 12,5-15x95

sheets = []  # (grupp, material, mängd, enhet, kommentar)
def sh(g, m, q, u, note=""):
    sheets.append((g, m, q, u, note))

sh("Grund", "Betongplint (t.ex. gjuten i rör Ø200 till tjälfritt djup, eller plintsten)", 10, "st",
   "2 rader × 5, c/c 1500 under kantbalkar")
sh("Grund", "Justerbart plintbeslag", 10, "st", "")
sh("Grund", "Balksko 45x170", 2 * len(JOIST_X), "st", "")
sh("Bjälklag", "Mineralull 170 mm (golv)", math.ceil(floor_area * 1.05), "m²", "")
sh("Bjälklag", "Vindskydd under bjälklag (vindskyddsskiva/duk + gnagarnät)", math.ceil(floor_area * 1.1), "m²", "")
sh("Bjälklag", "Golvspånskiva 22 mm, P5, 600x2400", math.ceil(floor_area / 1.44 * 1.1), "st", "")
sh("Bjälklag", "Bastugolv: våtrumsmatta med uppvik 100 mm + lös trätrall", math.ceil(in_len_s * in_w / 1e6 * 1.2), "m²", "alt. klinker på tätskikt")
sh("Väggar", "Mineralull 95 mm (ytterväggar + mellanvägg)", math.ceil((outer_wall_net + part_net) * 1.08), "m²", "")
sh("Väggar", "Vindskyddsskiva 12 mm (t.ex. asfaboard) 1200x2700", math.ceil((gross_back + gross_front + 2 * gross_gable) / 3.24 * 1.1), "st", "hela ytan, öppningar skärs ur")
sh("Väggar", "Diagonalstag, spikband 20x1 (vindstag)", 4 * 2 * 3.5, "m", "kryss i varje vägg")
sh("Fasad", "Luftläkt 22x45, stående c/c 600", math.ceil((2 * L + 2 * B) / 600 * 2.9 * 1.15), "lpm", "")
sh("Fasad", "Ytterpanel liggande 22x145 (täckbredd ca 132)", math.ceil(facade_net / PANEL_COVER * 1.15), "lpm",
   f"netto {facade_net:.1f} m² + 15 % spill")
sh("Fasad", "Hörnbrädor + foder runt öppningar 22x95", math.ceil((4 * 2 * 2.9 + sum(2 * (o[2] - o[1]) / 1000 + 2 * (HEAD - (o[3] or 0)) / 1000 for o in FRONT_OPEN + BACK_OPEN)) * 1.1), "lpm", "")
sh("Bastu (insida)", "Bastufolie aluminium", math.ceil((sauna_wall + sauna_ceil) * 1.15), "m²", "ångspärr, tejpas i skarvar")
sh("Bastu (insida)", "Spikläkt 22x45 bakom panel (luftspalt)", math.ceil((sauna_wall + sauna_ceil) / 0.6 * 1.1), "lpm", "")
sh("Bastu (insida)", "Bastupanel (asp/al/gran) ca 12,5–15x95", math.ceil((sauna_wall + sauna_ceil) / INNER_COVER * 1.15), "lpm",
   f"netto {sauna_wall + sauna_ceil:.1f} m² vägg+tak")
sh("Relax (insida)", "PE-folie 0,2 mm (ångspärr)", math.ceil((relax_wall + relax_ceil + in_len_r * in_w / 1e6) * 1.15), "m²", "vägg, tak och golv")
sh("Relax (insida)", "Innerpanel ca 12,5–15x95", math.ceil((relax_wall + relax_ceil) / INNER_COVER * 1.15), "lpm",
   f"netto {relax_wall + relax_ceil:.1f} m² vägg+tak")
sh("Tak", "Mineralull 145 mm (25 mm ventilerad luftspalt ovan)", math.ceil((sauna_ceil + relax_ceil) * 1.08), "m²", "")
sh("Tak", "Råspont 23x95 (täckbredd ca 85)", math.ceil(roof_area / RASPONT_COVER * 1.1), "lpm", f"takyta {roof_area:.1f} m²")
sh("Tak", "Underlagspapp + ytpapp (tvålagssystem)", math.ceil(roof_area * 1.15), "m² av vardera", "kontrollera min.lutning för vald produkt")
sh("Tak", "Takfotsplåt/droppbleck + vindskiveplåt", math.ceil((2 * L + 2 * rafter_len) / 1000), "lpm", "")

# ---------- Inköpsförslag (FFD mot standardlängder) ----------
STOCK = {
    "45x95": [2400, 2700, 3000, 3600, 4200, 4800, 5400, 6000],
    "45x145": [3000, 3600, 4200, 4800, 5400],
    "45x170": [2400, 3000, 3300, 3600, 4200, 4800, 5400, 6000],
    "22x145": [3600, 4200, 4800, 5400, 6000, 6300],
    "22x45": [6000],
    "28x70": [6000],
    "45x70": [3000],
    "28x90 asp/al": [1800, 2100, 2400],
}
def buy(dim):
    cuts = []
    for p in pieces:
        if p[2] == dim:
            cuts += [p[3]] * p[4]
    cuts.sort(reverse=True)
    bars = []  # [stock, rest]
    for c in cuts:
        for b in bars:
            if b[1] >= c + KERF:
                b[1] -= c + KERF
                break
        else:
            s = min([s for s in STOCK[dim] if s >= c], default=None)
            if s is None:
                raise SystemExit(f"{dim}: bit {c} längre än standardlängd")
            bars.append([s, s - c - KERF])
    cnt = defaultdict(int)
    for s, _ in bars:
        cnt[s] += 1
    waste = sum(r for _, r in bars)
    total = sum(s for s, _ in bars)
    return dict(sorted(cnt.items())), total, waste, len(cuts)

purchase = {d: buy(d) for d in STOCK}

# ---------- Kontrollutskrift ----------
def report():
    print(f"Lutning {ANGLE:.2f}°  sekant {SEC:.5f}")
    ridge = FLOOR + zr(B + OVH_F) + RAFTER * SEC + ROOF_TOP
    low = FLOOR + zr(-OVH_B)
    print(f"Nockhöjd (framkant takutsprång) över mark: {ridge:.0f} mm; takfot bak uk: {low:.0f}")
    print(f"Bastu invändigt {in_len_s:.0f} x {in_w} = {in_len_s * in_w / 1e6:.2f} m²")
    print(f"Relax invändigt {in_len_r:.0f} x {in_w} = {in_len_r * in_w / 1e6:.2f} m²")
    print(f"Takbalk {rafter_len:.0f}")
    print(f"Invändig takhöjd bastu vid bakvägg: {zr(T) - 28 - 15:.0f}, vid framvägg: {zr(B - T) - 28 - 15:.0f}")
    print(f"Fasad netto {facade_net:.2f} m², tak {roof_area:.2f} m²")
    for p in pieces:
        print(p)
    for d, (c, t, w, n) in purchase.items():
        print(d, c, f"{t/1000:.1f} m köpt, spill {w/1000:.1f} m, {n} bitar")

GEOM = dict(ridge=FLOOR + zr(B + OVH_F) + RAFTER * SEC + ROOF_TOP)

if __name__ == "__main__":
    report()
    from render import render
    html = render(globals())
    out = Path(__file__).with_name("bastustuga.html")
    out.write_text(html, encoding="utf-8")
    print("skrev", out, len(html), "tecken")
