#!/usr/bin/env python3
"""Build a client-branded Agentforce Observability guide.

Outputs (choose with --formats, default all):
  html     -> <slug>-guia-agentforce-observability.html  (interactive, self-contained)
  docx     -> "<Client> - Guia Agentforce Observability.docx"
  netlify  -> netlify-<slug>/index.html + netlify-<slug>.zip  (drag to app.netlify.com/drop)

Example:
  python3 build_guide.py --client "Coral Clouds" --logo logo.png --industry retail \
      --contact-name "Alex Rivera" --contact-email alex@salesforce.com --out ./salida
Colors are extracted from the logo unless --accent is given.
"""
import warnings; warnings.filterwarnings("ignore", category=DeprecationWarning)
import argparse, base64, colorsys, datetime, html, io, json, os, re, subprocess, sys, tempfile, unicodedata, zipfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
sys.path.insert(0, HERE)
from industries import get_industry  # noqa: E402

try:
    from PIL import Image
except ImportError:
    sys.exit('Pillow is required: pip install pillow --break-system-packages')

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
DOCS = [
    ['Agentforce Observability Setup and Access', 'Salesforce Help', 'https://help.salesforce.com/s/articleView?id=005237036&language=en_US&type=1'],
    ['Set Up Agentforce Session Tracing', 'Salesforce Help', 'https://help.salesforce.com/s/articleView?language=en_US&id=ai.generative_ai_session_trace_setup.htm&type=5'],
    ['Data Model for Agentforce Session Tracing', 'Salesforce Help', 'https://help.salesforce.com/s/articleView?language=en_US&id=ai.generative_ai_session_trace_data_model.htm&type=5'],
    ['Billing Considerations for Agentforce Session Tracing', 'Salesforce Help', 'https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_usage_types.htm&language=en_US&type=5'],
    ['Release Notes: Observability sin créditos Data 360', 'Salesforce Help', 'https://help.salesforce.com/s/articleView?id=release-notes.rn_einstein_copilot.htm'],
    ['Learn About Agentforce Observability', 'Salesforce Help', 'https://help.salesforce.com/s/articleView?id=005226932&language=en_US&type=1'],
    ['Agent Analytics Data Model', 'Salesforce Help', 'https://help.salesforce.com/s/articleView?id=ai.generative_ai_agent_analytics_data_model.htm&type=5'],
    ['Export Agentforce Session Tracing Data – OTel API', 'Salesforce Developers', 'https://developer.salesforce.com/docs/ai/agentforce/guide/otel-api.html'],
    ['Agent Platform Tracing', 'Salesforce Developers Blog', 'https://developer.salesforce.com/blogs/2026/05/agent-platform-tracing-debug-agentforce-with-trace-trees-soql-and-slack'],
    ['Novedades de Agentforce Observability – julio 2026', 'Salesforce Blog', 'https://www.salesforce.com/blog/agentforce-observability/'],
]

# ---------- color helpers ----------
def hex2rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb2hex(c): return '#%02X%02X%02X' % tuple(max(0, min(255, int(round(v)))) for v in c)

def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def contrast_white(c): return 1.05 / (lum(c) + 0.05)

def mix(c, other, t): return tuple(a * (1 - t) + b * t for a, b in zip(c, other))

def darken_until(c, ratio=3.2):
    """Darken so white text on the color stays readable (buttons, badges)."""
    for _ in range(40):
        if contrast_white(c) >= ratio: return c
        c = mix(c, (0, 0, 0), 0.06)
    return c

def extract_brand_color(img):
    im = img.convert('RGBA'); im.thumbnail((160, 160))
    buckets, members = Counter(), {}
    for r, g, b, a in im.getdata():
        if a < 128: continue
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if v > 0.92 and s < 0.12: continue      # white-ish background
        if s < 0.25 or v < 0.15: continue       # greys / black text
        key = (r // 24, g // 24, b // 24)
        buckets[key] += 1
        members.setdefault(key, []).append((r, g, b))
    if not buckets: return None
    key = buckets.most_common(1)[0][0]
    px = members[key]
    return tuple(sum(p[i] for p in px) / len(px) for i in range(3))

# ---------- logo ----------
def load_logo(path, transparent_bg):
    """Returns (html_data_uri, docx_png_path_or_None, img_for_color_or_None)."""
    ext = os.path.splitext(path)[1].lower()
    raw = open(path, 'rb').read()
    if ext == '.svg':
        uri = 'data:image/svg+xml;base64,' + base64.b64encode(raw).decode()
        png = None
        try:
            import cairosvg
            png_bytes = cairosvg.svg2png(bytestring=raw, output_height=320)
            img = Image.open(io.BytesIO(png_bytes))
        except Exception:
            img = None
        if img is None: return uri, None, None
    else:
        img = Image.open(io.BytesIO(raw)); uri = None
    img = img.convert('RGBA')
    if transparent_bg:
        img.putdata([(r, g, b, 0) if r > 238 and g > 238 and b > 238 else (r, g, b, a) for r, g, b, a in img.getdata()])
    bbox = img.getbbox()
    if bbox: img = img.crop(bbox)
    img.thumbnail((600, 200))
    buf = io.BytesIO(); img.save(buf, 'PNG', optimize=True)
    if uri is None: uri = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False); tmp.write(buf.getvalue()); tmp.close()
    return uri, tmp.name, img

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') or 'cliente'

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', help='JSON file with any of the options below (CLI flags override it)')
    ap.add_argument('--client'); ap.add_argument('--logo')
    ap.add_argument('--accent', help='Brand color hex, e.g. #CC2131 (default: extracted from logo)')
    ap.add_argument('--hero', help='"salesforce" (default navy→blue), "brand" (client colors) or two hex colors "#111111,#333333"')
    ap.add_argument('--industry', help='retail | banca | seguros | telco | generic')
    ap.add_argument('--contact-name'); ap.add_argument('--contact-email')
    ap.add_argument('--version', help='Label shown as "Versión ..." (default: current month and year)')
    ap.add_argument('--out', help='Output folder')
    ap.add_argument('--formats', help='Comma list: html,docx,netlify (default all)')
    ap.add_argument('--transparent-bg', action='store_true', help='Turn the logo white background transparent')
    a = vars(ap.parse_args())
    if a.get('config'):
        cfg = json.load(open(a['config']))
        for k, v in cfg.items():
            k2 = k.replace('-', '_')
            if a.get(k2) in (None, False): a[k2] = v
    if not a.get('client'): sys.exit('--client is required')
    client = a['client'].strip()
    out = os.path.abspath(a.get('out') or '.'); os.makedirs(out, exist_ok=True)
    formats = [f.strip() for f in (a.get('formats') or 'html,docx,netlify').split(',') if f.strip()]
    ind, ind_key = get_industry(a.get('industry'))
    today = datetime.date.today()
    version = a.get('version') or f'{MONTHS[today.month - 1]} {today.year}'

    logo_uri = logo_png = logo_img = None
    if a.get('logo'):
        if not os.path.exists(a['logo']): sys.exit(f'Logo not found: {a["logo"]}')
        logo_uri, logo_png, logo_img = load_logo(a['logo'], a.get('transparent_bg'))

    if a.get('accent'): base = hex2rgb(a['accent']); src = 'manual'
    else:
        base = extract_brand_color(logo_img) if logo_img is not None else None
        src = 'logo'
        if base is None: base = hex2rgb('#0176D3'); src = 'default (no logo color found)'
    accent = darken_until(base)
    accent_dark = mix(accent, (0, 0, 0), 0.25)
    accent_soft = mix(base, (255, 255, 255), 0.88)
    hero = (a.get('hero') or 'salesforce').strip()
    if hero == 'brand': hero1, hero2 = rgb2hex(mix(accent, (0, 0, 0), 0.45)), rgb2hex(accent)
    elif ',' in hero: hero1, hero2 = [rgb2hex(hex2rgb(x)) for x in hero.split(',')[:2]]
    else: hero1, hero2 = '#032D60', '#0176D3'

    cname, cmail = a.get('contact_name'), a.get('contact_email')
    if cname and cmail:
        contact_html = f'Escribinos a {html.escape(cname)} (<a href="mailto:{html.escape(cmail)}">{html.escape(cmail)}</a>) y coordinamos una sesión de acompañamiento con el equipo técnico.'
        contact_text = f'Ante cualquier consulta durante la activación, escribinos a {cname} ({cmail}) y coordinamos una sesión de acompañamiento con el equipo técnico.'
    elif cname or cmail:
        who = cname or cmail
        contact_html = f'Escribinos a {html.escape(who)} y coordinamos una sesión de acompañamiento con el equipo técnico.'
        contact_text = f'Ante cualquier consulta durante la activación, escribinos a {who} y coordinamos una sesión de acompañamiento con el equipo técnico.'
    else:
        contact_html = contact_text = 'Contactá a tu equipo de cuenta de Salesforce y coordinamos una sesión de acompañamiento con el equipo técnico.'

    slug = slugify(client)
    sf_logo = os.path.join(ASSETS, 'salesforce-logo.png')
    sf_uri = 'data:image/png;base64,' + base64.b64encode(open(sf_logo, 'rb').read()).decode()
    results = []

    if 'html' in formats or 'netlify' in formats:
        tpl = open(os.path.join(ASSETS, 'guide.template.html'), encoding='utf-8').read()
        esc = html.escape(client)
        logo_tag = f'<img class="client" src="{logo_uri}" alt="{esc}">' if logo_uri else f'<b style="font-size:20px;color:var(--accent-dark)">{esc}</b>'
        total_ms = max(s[2] + s[3] for s in ind['trace']['steps'])
        data = dict(agent=ind['agent'], intents=ind['intents'], trace=ind['trace'])
        rep = {
            '{{CLIENT}}': esc, '{{LOGO_TAG}}': logo_tag, '{{SF_SRC}}': sf_uri,
            '{{ACCENT}}': rgb2hex(accent), '{{ACCENT_DARK}}': rgb2hex(accent_dark), '{{ACCENT_SOFT}}': rgb2hex(accent_soft),
            '{{HERO1}}': hero1, '{{HERO2}}': hero2, '{{VERSION}}': html.escape(version),
            '{{SENSITIVE}}': html.escape(ind['sensitive']), '{{CHANNELS}}': html.escape(ind['channels']), '{{CH1}}': html.escape(ind['ch1']),
            '{{CONTACT_LINE}}': contact_html, '{{TRACE_TOTAL}}': f'{total_ms / 1000:.2f} s en total'.replace('.', ','),
            '{{DATA_JSON}}': json.dumps(data, ensure_ascii=False),
        }
        page = tpl
        for k, v in rep.items(): page = page.replace(k, v)
        left = re.findall(r'\{\{[A-Z_0-9]+\}\}', page)
        if left: sys.exit(f'Unreplaced placeholders: {set(left)}')
        if 'html' in formats:
            p = os.path.join(out, f'{slug}-guia-agentforce-observability.html')
            open(p, 'w', encoding='utf-8').write(page); results.append(p)
        if 'netlify' in formats:
            d = os.path.join(out, f'netlify-{slug}'); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page)
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z: z.writestr('index.html', page)
            zp = os.path.join(out, f'netlify-{slug}.zip')
            open(zp, 'wb').write(buf.getvalue()); results += [d, zp]

    if 'docx' in formats:
        logo_docx = None
        if logo_png:
            w, h = Image.open(logo_png).size
            H = 42; W = round(w * H / h)
            if W > 200: W, H = 200, round(h * 200 / w)
            logo_docx = dict(path=logo_png, type='png', width=W, height=H)
        rc = dict(client=client, accent_text=rgb2hex(accent), logo_docx=logo_docx, sf_logo=sf_logo, version=version,
                  sensitive=ind['sensitive'], channels=ind['channels'], ch1=ind['ch1'], intents=ind['intents'],
                  contact_text=contact_text, docs=DOCS)
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8'); json.dump(rc, tmp, ensure_ascii=False); tmp.close()
        safe = re.sub(r'[\\/:*?"<>|]+', '', client)
        p = os.path.join(out, f'{safe} - Guia Agentforce Observability.docx')
        tmp_docx = tempfile.NamedTemporaryFile(suffix='.docx', delete=False).name
        r = subprocess.run(['node', os.path.join(HERE, 'build_docx.js'), tmp.name, tmp_docx], capture_output=True, text=True)
        if r.returncode != 0: sys.exit('DOCX build failed:\n' + r.stderr + r.stdout)
        open(p, 'wb').write(open(tmp_docx, 'rb').read()); results.append(p)

    print(json.dumps(dict(client=client, industry=ind_key, accent=rgb2hex(accent), accent_source=src,
                          hero=[hero1, hero2], version=version, outputs=results), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
