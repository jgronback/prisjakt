"""Inline-SVG-diagram. Ritas med CSS-variabler så de följer sajtens färger."""

INK = "var(--gunmetal-900)"
MUTED = "var(--mist-600)"
LINE = "var(--mist-300)"
GREEN = "var(--reticle-500)"
GREEN_D = "var(--reticle-700)"
GREEN_L = "var(--reticle-50)"
ORANGE = "var(--blaze-500)"


def _box(x, y, w, h, title, sub, fill="#fff", stroke=LINE):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            f'<text x="{x + w / 2}" y="{y + 30}" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">{title}</text>'
            f'<text x="{x + w / 2}" y="{y + 52}" text-anchor="middle" font-size="12" fill="{MUTED}">{sub}</text>')


def _arrow(x1, y, x2):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="{GREEN_D}" stroke-width="2"/>'
            f'<polygon points="{x2 - 10},{y - 5} {x2},{y} {x2 - 10},{y + 5}" fill="{GREEN_D}"/>')


def pipeline() -> str:
    """Signalkedjan i en värmekamera, från objekt till öga."""
    steps = [
        ("Objekt", "strålar 8–14 µm"),
        ("Germaniumlins", "fokuserar IR"),
        ("Mikrobolometer", "384×288 element"),
        ("Utläsning (ROIC)", "spänning per pixel"),
        ("Bildbehandling", "NUC · AGC · DDE"),
        ("Display", "AMOLED/OLED"),
        ("Öga", "okular + dioptri"),
    ]
    w, gap, h, y = 118, 14, 70, 60
    parts = []
    x = 8
    for i, (t, s) in enumerate(steps):
        fill = GREEN_L if i in (1, 2, 4) else "#fff"
        parts.append(_box(x, y, w, h, t, s, fill=fill))
        if i < len(steps) - 1:
            parts.append(_arrow(x + w, y + h / 2, x + w + gap))
        x += w + gap
    total = x - gap + 8
    parts.append(f'<text x="8" y="28" font-size="13" font-weight="700" fill="{GREEN_D}" letter-spacing=".08em">SIGNALKEDJAN I EN VÄRMEKAMERA</text>')
    parts.append(f'<text x="8" y="165" font-size="12" fill="{MUTED}">Gröna rutor är de steg som avgör bildkvaliteten: optik, sensor och bildbehandling. Displayen avgör hur mycket av den kvaliteten du faktiskt ser.</text>')
    return (f'<svg class="diagram" viewBox="0 0 {total} 180" role="img" aria-label="Diagram över signalkedjan i en värmekamera: objekt, germaniumlins, mikrobolometer, utläsning, bildbehandling, display, öga">'
            + "".join(parts) + "</svg>")


def spectrum() -> str:
    """Schematisk bild av det infraröda spektrumet och de atmosfäriska fönstren."""
    # schematisk, inte logaritmisk skala: segment med etiketter
    segs = [
        ("Synligt ljus", "0,4–0,7 µm", 0, 70, "#F7D154"),
        ("NIR", "0,7–1 µm · mörkerkikare, IR-lampa", 70, 160, "#F2701F"),
        ("SWIR", "1–3 µm", 160, 230, "#C1276B"),
        ("MWIR", "3–5 µm · kylda kameror", 230, 330, "#7A2E8E"),
        ("Absorption (H₂O, CO₂)", "5–8 µm", 330, 420, "#3A0E5C"),
        ("LWIR", "8–14 µm · alla jaktvärmekameror", 420, 640, "#01AE55"),
    ]
    parts = [f'<text x="8" y="26" font-size="13" font-weight="700" fill="{GREEN_D}" letter-spacing=".08em">VAR I SPEKTRUMET EN VÄRMEKAMERA SER</text>']
    y, h = 60, 46
    for name, sub, x1, x2, col in segs:
        parts.append(f'<rect x="{x1 + 8}" y="{y}" width="{x2 - x1}" height="{h}" fill="{col}" opacity="0.9"/>')
        parts.append(f'<text x="{(x1 + x2) / 2 + 8}" y="{y + 28}" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">{name}</text>')
        parts.append(f'<text x="{(x1 + x2) / 2 + 8}" y="{y + h + 18}" text-anchor="middle" font-size="11" fill="{MUTED}">{sub}</text>')
    # toppen för kroppsvärme
    px = 8 + 420 + (9.4 - 8) / 6 * 220
    parts.append(f'<line x1="{px}" y1="{y - 18}" x2="{px}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
    parts.append(f'<text x="{px}" y="{y - 24}" text-anchor="middle" font-size="12" font-weight="700" fill="{INK}">37 °C strålar som mest vid ≈9,4 µm</text>')
    parts.append(f'<text x="8" y="160" font-size="12" fill="{MUTED}">Schematisk skala. Mellan 5 och 8 µm absorberar vattenånga och koldioxid strålningen, därför är 8–14 µm det "fönster" som handhållna värmekameror använder.</text>')
    return (f'<svg class="diagram" viewBox="0 0 660 175" role="img" aria-label="Schematisk bild av spektrumet: synligt ljus, nära infrarött som mörkerkikare använder, och långvågigt infrarött 8 till 14 mikrometer som värmekameror använder">'
            + "".join(parts) + "</svg>")


def bolometer() -> str:
    """Tvärsnitt av ett mikrobolometer-element."""
    parts = [f'<text x="8" y="26" font-size="13" font-weight="700" fill="{GREEN_D}" letter-spacing=".08em">ETT ELEMENT I MIKROBOLOMETERN, I GENOMSKÄRNING</text>']
    # inkommande strålning
    for i, x in enumerate((150, 190, 230, 270)):
        parts.append(f'<line x1="{x}" y1="50" x2="{x}" y2="92" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="4 3"/>')
        parts.append(f'<polygon points="{x - 5},88 {x},98 {x + 5},88" fill="{ORANGE}"/>')
    parts.append(f'<text x="300" y="70" font-size="12" fill="{ORANGE}" font-weight="700">infraröd strålning 8–14 µm</text>')
    # membran
    parts.append(f'<rect x="120" y="100" width="190" height="14" rx="3" fill="{GREEN}"/>')
    parts.append(f'<text x="320" y="112" font-size="12" fill="{INK}" font-weight="700">membran av vanadinoxid eller amorft kisel (absorberar och ändrar resistans)</text>')
    # ben
    parts.append(f'<path d="M120 107 L95 107 L95 150" fill="none" stroke="{GREEN_D}" stroke-width="3"/>')
    parts.append(f'<path d="M310 107 L335 107 L335 150" fill="none" stroke="{GREEN_D}" stroke-width="3"/>')
    parts.append(f'<text x="320" y="140" font-size="12" fill="{MUTED}">smala ben: elektrisk kontakt, men dålig värmeledning</text>')
    # vakuumgap
    parts.append(f'<text x="215" y="138" text-anchor="middle" font-size="11" fill="{MUTED}">vakuumgap ≈ 2 µm</text>')
    # reflektor + substrat
    parts.append(f'<rect x="80" y="150" width="270" height="6" fill="{INK}"/>')
    parts.append(f'<text x="360" y="156" font-size="12" fill="{MUTED}">reflektor (skickar tillbaka strålning som passerat membranet)</text>')
    parts.append(f'<rect x="60" y="156" width="310" height="34" fill="var(--mist-200)"/>')
    parts.append(f'<text x="215" y="178" text-anchor="middle" font-size="12" font-weight="700" fill="{INK}">kiselsubstrat med utläsningskrets (ROIC)</text>')
    parts.append(f'<text x="8" y="215" font-size="12" fill="{MUTED}">Pixelstorlek 12 eller 17 µm. Membranet värms några tusendels grad av strålningen; resistansändringen läses av 50 gånger per sekund.</text>')
    return (f'<svg class="diagram" viewBox="0 0 760 230" role="img" aria-label="Tvärsnitt av ett mikrobolometer-element: ett tunt membran på smala ben över ett vakuumgap och en utläsningskrets">'
            + "".join(parts) + "</svg>")


def fov_compare() -> str:
    """Synfält för 256/384/640 vid samma objektiv, ritat som bildbredd på 100 m."""
    rows = [("256×192", 8.8, "#CAD3D8"), ("384×288", 13.2, "#A7B3B9"), ("640×512", 21.9, "#26C079"), ("1024×768", 35.1, "#01AE55")]
    parts = [f'<text x="8" y="26" font-size="13" font-weight="700" fill="{GREEN_D}" letter-spacing=".08em">BILDBREDD PÅ 100 M, SAMMA 35 MM-OBJEKTIV OCH 12 µm PIXLAR</text>']
    y = 50
    scale = 14  # px per meter
    for name, m, col in rows:
        parts.append(f'<text x="8" y="{y + 18}" font-size="13" font-weight="700" fill="{INK}">{name}</text>')
        parts.append(f'<rect x="100" y="{y}" width="{m * scale}" height="26" rx="5" fill="{col}"/>')
        parts.append(f'<text x="{100 + m * scale + 8}" y="{y + 18}" font-size="13" fill="{INK}">{str(m).replace(".", ",")} m</text>')
        y += 40
    parts.append(f'<text x="8" y="{y + 10}" font-size="12" fill="{MUTED}">Fler pixlar ger bredare bild, inte längre räckvidd. Räckvidden sitter i brännvidd och pixelstorlek.</text>')
    return (f'<svg class="diagram" viewBox="0 0 680 {y + 24}" role="img" aria-label="Stapeldiagram: bildbredd på 100 meter för sensorer med 256, 384, 640 och 1024 pixlar vid samma objektiv">'
            + "".join(parts) + "</svg>")
