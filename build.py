#!/usr/bin/env python3
"""Vibe Gifts static site generator. Usage: python3 build.py  (no packages needed)
Reads data/products.csv (+ data/reviews.json) and writes every page. Edit the CSV, rerun, upload."""
import csv, json, os, html, re
from urllib.parse import quote
R = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://vibegifts.pk'; WA = '923016596803'; EMAIL = 'contactvibegifts@gmail.com'; WA_SHOW = '+92 301 6596803'
SOC = {'Instagram': 'https://www.instagram.com/vibe_gifts_official', 'TikTok': 'https://www.tiktok.com/@vibe_gifts_official',
       'Facebook': 'https://www.facebook.com/profile.php?id=61594945888257'}
HI = "Hi Vibe Gifts! 👋 I'd like to know more about your gifts."
_IC = {
 'box': '<path d="M21 8l-9-5-9 5v8l9 5 9-5V8z"/><path d="M3.3 7.6L12 12l8.7-4.4M12 12v9"/>',
 'palette': '<path d="M12 3a9 9 0 100 18c1.3 0 2-1 1.6-2.1-.4-1.1.3-2.4 1.6-2.4H17a4 4 0 004-4c0-5.1-4-9.5-9-9.5z"/><circle cx="7.5" cy="11" r="1.1" fill="currentColor" stroke="none"/><circle cx="10" cy="7" r="1.1" fill="currentColor" stroke="none"/><circle cx="15" cy="7.5" r="1.1" fill="currentColor" stroke="none"/>',
 'ribbon': '<path d="M12 12C9 6 3 7 4.5 10.5 6 13.5 11 13 12 12zM12 12c3-6 9-5 7.5-1.5C18 13.5 13 13 12 12z"/><path d="M12 12l-3 9M12 12l3 9"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 'basket': '<path d="M3 9h18l-1.8 11H4.8L3 9z"/><path d="M8 9l4-6 4 6M9 13v4M15 13v4"/>',
 'gift': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v9h14v-9M12 8v13"/><path d="M12 8C10 8 7.5 7 7.5 5a2 2 0 013.5-1.3C11.7 4.5 12 8 12 8zM12 8c2 0 4.5-1 4.5-3a2 2 0 00-3.5-1.3C12.3 4.5 12 8 12 8z"/>',
 'flame': '<path d="M12 2.5c1 3.5 5 5.5 5 10a5 5 0 01-10 0c0-2 1-3.2 2-4.2.2 1.5 1 2.2 2 2.2-.5-2.7-.5-5.5 1-8z"/>',
 'truck': '<path d="M2 6h12v10H2zM14 9.5h4l3 3.5v3h-7"/><circle cx="6.5" cy="18" r="2"/><circle cx="17.5" cy="18" r="2"/>',
 'card': '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 10h19M6.5 15h4"/>',
 'pencil': '<path d="M4 20l1-4.5L16.5 4a2 2 0 013 3L8 18.5 4 20zM14.5 6l3.5 3.5"/>',
 'camera': '<path d="M3 8h3.5L8.5 5h7l2 3H21v12H3z"/><circle cx="12" cy="13.5" r="3.5"/>',
 'shield': '<path d="M12 2.5l8 3v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10v-6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 'sparkle': '<path d="M11 3l1.9 5.1L18 10l-5.1 1.9L11 17l-1.9-5.1L4 10l5.1-1.9L11 3z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8L19 15z"/>',
 'heart': '<path d="M12 20.5S3.5 15.5 3.5 9.5a4.5 4.5 0 018.5-2 4.5 4.5 0 018.5 2c0 6-8.5 11-8.5 11z"/>',
 'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
 'star': '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.4l-5.6 2.9 1.1-6.2L3 9.7l6.2-.9L12 3z"/>',
 'crown': '<path d="M3 18h18l-1.5-10-4.5 4-3-6-3 6-4.5-4L3 18zM5 21h14"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 'instagram': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>',
 'facebook': '<path d="M15 3h-2.5A4.5 4.5 0 008 7.5V10H5v4h3v7h4v-7h3l1-4h-4V7.5c0-.3.2-.5.5-.5H15V3z"/>',
 'tiktok': '<path d="M14 3v11.5a3.5 3.5 0 11-3.5-3.5"/><path d="M14 3c.3 2.5 2 4.5 5 4.8"/>',
 'whatsapp': '<path d="M3 21l1.7-5A8.5 8.5 0 1112 20.5a8.5 8.5 0 01-4-1L3 21z"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.5-2-1-1 .8c-1-.4-2-1.4-2.4-2.4l.8-1-1-2L9 8.5z"/>'}
SPRITE = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">' + ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in _IC.items()) + '</svg>'
def I(n, c='ic'): return f'<svg class="{c}" aria-hidden="true"><use href="#i-{n}"/></svg>'
HEADJS = "<script>document.documentElement.className='js';try{var q=new URLSearchParams(location.search).get('for'),m={her:'her',girl:'her',him:'him',boy:'him',any:'any'},l=m[q]||localStorage.getItem('look');if(m[q])localStorage.setItem('look',m[q]);if(l)document.documentElement.setAttribute('data-look',l)}catch(e){}</script>"
STYLEBTN = '<button class="sty" type="button">' + I('palette') + '<span>Style: <b>Surprise me</b></span></button>'
PICKER = f"""<div class="pk" id="pk" role="dialog" aria-modal="true" aria-labelledby="pkt" hidden><div class="pk-b"><button class="pk-x" type="button" aria-label="Close">&times;</button>
<h2 id="pkt">Who are we gifting for today?</h2><p>Bas ek click, aur website aapki pasand ki.</p>
<div class="pk-g"><button class="pk-o" data-look="her" type="button"><i class="sw">{I('heart')}</i><b>For Her</b><span class="d">Rose and gold</span></button><button class="pk-o" data-look="him" type="button"><i class="sw">{I('crown')}</i><b>For Him</b><span class="d">Royal blue, black and gold</span></button><button class="pk-o" data-look="any" type="button"><i class="sw">{I('star')}</i><b>Surprise me</b><span class="d">Classic ivory and gold</span></button></div>
<small>You can change this anytime from the menu: <b>Style</b>.</small></div></div>"""
PRIV = ('<section class="sec"><div class="in"><div class="priv rv-a"><span class="shd">' + I('shield') + '</span><h2>Your privacy is 100% safe with us</h2>'
        '<p>Our customers are the heart of Vibe Gifts. Your name, number, address, photos and designs are used only to make and deliver your order. We never sell or share them with anyone, except the courier who needs your address to deliver your gift. Your photos are never posted anywhere without your permission.</p>'
        '<ul class="pl"><li>' + I('check') + 'Never sold or shared</li><li>' + I('check') + 'Used only for your order</li><li>' + I('check') + 'Never posted without your permission</li></ul>'
        '<a class="btn ghost" href="/privacy-policy/">Read our privacy policy</a></div></div></section>\n')
CATS = ['Mugs', 'Lockets', 'Apparel', 'Bottles', 'Others', 'Pencils']
STORY = '''<section class="story dk" id="story"><div class="stage"><div class="ctr"><p class="eye">How your gift is made</p><h2>From a print to your doorstep</h2></div>
<svg viewBox="0 0 800 400" role="img" aria-label="A gift is printed, framed, wrapped, tied with a ribbon, tagged and delivered by truck">
<line id="road" x1="0" y1="362" x2="800" y2="362" stroke="#8C6A2E" stroke-width="3" stroke-dasharray="22 16"/>
<g class="k"><g id="fr"><rect x="330" y="110" width="140" height="160" rx="4" fill="#fff" stroke="#B08D57" stroke-width="10"/><rect x="346" y="126" width="108" height="128" fill="#F4EEDF"/></g></g>
<g id="pp"><rect x="110" y="175" width="100" height="120" rx="3" fill="#fff"/><path d="M160 208c-14-14-34 4-18 22l18 17 18-17c16-18-4-36-18-22z" fill="#B08D57"/><rect x="128" y="258" width="64" height="5" rx="2" fill="#2B2B2B" opacity=".6"/><rect x="138" y="270" width="44" height="5" rx="2" fill="#B08D57"/></g>
<g id="pr"><rect x="40" y="170" width="240" height="140" rx="14" fill="#3B3025"/><rect x="60" y="170" width="200" height="12" rx="4" fill="#0f0c08"/><rect x="60" y="282" width="200" height="8" rx="4" fill="#B08D57"/><circle cx="256" cy="222" r="6" fill="#B08D57"/><text x="150" y="244" fill="#B08D57" font-size="15" text-anchor="middle" font-family="Georgia,serif">VibeGifts</text></g>
<g class="k"><g id="wr"><rect x="318" y="98" width="164" height="184" rx="8" fill="#E9DFC8"/><g fill="#B08D57" opacity=".45"><circle cx="345" cy="126" r="3.5"/><circle cx="385" cy="244" r="3.5"/><circle cx="455" cy="130" r="3.5"/><circle cx="440" cy="250" r="3.5"/><circle cx="346" cy="215" r="3.5"/><circle cx="458" cy="215" r="3.5"/></g></g></g>
<g class="k"><rect id="rv" x="392" y="98" width="16" height="184" fill="#8C6A2E"/><rect id="rh" x="318" y="182" width="164" height="16" fill="#8C6A2E"/><g id="bw"><path d="M400 190c-32-42-64-20-44 3 14 14 44 0 44-3zM400 190c32-42 64-20 44 3-14 14-44 0-44-3z" fill="#B08D57" stroke="#8C6A2E" stroke-width="3"/><circle cx="400" cy="190" r="9" fill="#8C6A2E"/></g></g>
<g class="k"><g id="tg"><path d="M404 194c22 16 38 22 50 34" stroke="#8C6A2E" stroke-width="2" fill="none"/><rect x="430" y="226" width="68" height="42" rx="4" fill="#fff" stroke="#B08D57" stroke-width="2"/><text x="464" y="244" font-size="10" text-anchor="middle" fill="#2B2B2B" font-family="Georgia,serif" font-weight="700">Vibe Gifts</text><text x="464" y="258" font-size="8" text-anchor="middle" fill="#8C6A2E">made for you</text></g></g>
<g id="tk"><rect x="0" y="296" width="170" height="44" rx="4" fill="#8C6A2E"/><text x="85" y="324" text-anchor="middle" fill="#FBF8F1" font-size="14" font-family="Georgia,serif">vibegifts.pk</text><path d="M176 340v-60h38l30 30v30z" fill="#B08D57"/><path d="M186 288h24l20 20h-44z" fill="#FBF8F1" opacity=".85"/><circle cx="45" cy="342" r="18" fill="#1E1912"/><circle cx="210" cy="342" r="18" fill="#1E1912"/><circle cx="45" cy="342" r="7" fill="#B08D57"/><circle cx="210" cy="342" r="7" fill="#B08D57"/></g></svg>
<div class="cap"><span class="num"></span><h3></h3><p></p></div><div class="dots"><i></i><i></i><i></i><i></i><i></i><i></i></div><button class="rp" type="button" hidden>Replay</button></div></section>'''
MQ = ('<span>Every order is customized, so payment is 50% advance + 50% Cash on Delivery ' + I('box') + '</span>') * 3

e = html.escape
def wa(msg): return f'https://wa.me/{WA}?text=' + quote(msg)
def rs(n): return f'Rs. {int(n):,}'
def w(path, s):
    p = os.path.join(R, path); os.makedirs(os.path.dirname(p) or R, exist_ok=True); open(p, 'w', encoding='utf-8').write(s)

def load():
    out = []
    for r in csv.DictReader(open(os.path.join(R, 'data/products.csv'), encoding='utf-8')):
        if r['status'] != 'active': continue
        r['price'] = int(r['price']); r['compare_price'] = int(r['compare_price'] or 0)
        r['imgs'] = r['images'].split(';'); r['bul'] = [re.sub(r'^[^A-Za-z0-9\u0600-\u06FF(]+', '', x) for x in r['description'].split('|') if x]; r['for'] = r.get('for') or 'both'
        r['g'] = []
        for g in filter(None, r['options'].split(';')):
            n, _, rest = g.partition('='); o = []
            for x in rest.split('|'):
                f = (x.split(':') + ['', ''])[:3]; o.append(dict(l=f[0], p=int(f[1]) if f[1] else None, i=int(f[2]) - 1 if f[2] else None))
            r['g'].append(dict(n=n, o=o))
        pr = [o['p'] for g in r['g'] for o in g['o'] if o['p']]
        dp = r['price']
        for g in r['g']:
            if g['o'][0]['p']: dp = g['o'][0]['p']
        r['low'] = dp; r['varies'] = False
        r['url'] = f"/product/{r['slug']}/"; r['sort'] = int(r['sort']); out.append(r)
    return sorted(out, key=lambda x: x['sort'])
P = load(); BY = {c: [p for p in P if p['category'] == c] for c in CATS}
def csl(c): return c.lower()

def pct(p): return round(100 - p['low'] * 100 / p['compare_price']) if p['compare_price'] > p['low'] else 0
def price_html(p):
    s = f'<b>{rs(p["low"])}</b>'
    if pct(p): s = f'<s>{rs(p["compare_price"])}</s> ' + s + f' <span class="off">{pct(p)}% OFF</span>'
    return f'<p class="pr">{s}</p>'
def order_link(p):
    m = f"Hi Vibe Gifts! 👋 I'd like to order:\n🎁 Product: {p['title']}\n"; pr = p['price']
    for g in p['g']:
        o = g['o'][0]; m += f"🎨 {g['n']}: {o['l']}\n"; pr = o['p'] or pr
    return wa(m + f"💰 Price: {rs(pr)}\n🔗 {SITE}{p['url']}\n\nName / design / photo to print: ")
def card(p, hid=False):
    off = ''
    return (f'<article class="card" data-price="{p["low"]}" data-slug="{p["slug"]}"{" hidden" if hid else ""}>{off}<a href="{p["url"]}"><img src="/images/{p["imgs"][0]}" alt="{e(p["title"])}" width="600" height="600" loading="lazy"></a>'
            f'<div class="cb"><h3><a href="{p["url"]}">{e(p["title"])}</a></h3>{price_html(p)}<div class="btns"><a class="btn ghost" href="{p["url"]}">View</a>'
            f'<a class="btn" href="{order_link(p)}" target="_blank" rel="noopener">Order on WhatsApp</a></div></div></article>')

LOGO = ('<svg viewBox="0 0 40 40" width="32" height="32" aria-hidden="true"><rect x="6" y="17" width="28" height="19" rx="2" style="fill:var(--gd)"/>'
        '<rect x="4" y="12" width="32" height="7" rx="2" style="fill:var(--gold)"/><rect x="18" y="12" width="4" height="24" style="fill:var(--bg)"/>'
        '<path d="M20 12C14 3 6 8 11 12M20 12c6-9 14-4 9 0" fill="none" style="stroke:var(--ink)" stroke-width="2.2" stroke-linecap="round"/></svg>')
WAICON = '<svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true"><path fill="#fff" d="M16 4C9.4 4 4 9.2 4 15.6c0 2.3.7 4.4 1.9 6.2L4 28l6.400-1.800a12 12 0 0 0 5.600 1.400c6.600 0 12-5.200 12-11.600S22.600 4 16 4z"/><path fill="#25D366" d="M12.200 10.400c-.6 0-1.400.8-1.100 2.200.6 2.700 3.500 5.600 6.900 6.500 1.200.3 2.100-.5 2.100-1.100l-.1-1.300-2.100-1-1 1.100c-1.400-.5-2.600-1.700-3.100-3.100l1.100-1z"/></svg>'

def page(path, title, desc, body, img=None, ld=''):
    url = SITE + path; img = SITE + '/images/' + (img or 'logo.svg')
    nav = ''.join(f'<a href="{h}">{t}</a>' for h, t in [('/', 'Home'), ('/shop/', 'Shop'), ('/about/', 'About'), ('/faq/', 'FAQ'), ('/contact/', 'Contact')])
    nav += STYLEBTN
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOC.items())
    hi = wa(HI); bc = ' class="home"' if path == '/' else ''
    s = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{img}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/images/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500&display=swap"><link rel="stylesheet" href="/css/style.css">{HEADJS}{ld}</head><body{bc}>{SPRITE}
<div class="top"><div class="tr">{MQ}{MQ}</div></div>
<header class="hd"><a class="logo" href="/" aria-label="Vibe Gifts home">{LOGO}<span class="lg">Vibe<em>Gifts</em></span></a><button class="mb" aria-label="Menu" aria-expanded="false">{I("menu")}</button><nav>{nav}</nav><a class="btn hbtn" href="{hi}" target="_blank" rel="noopener">Order on WhatsApp</a></header>
<main>{body}</main>
<footer class="ft"><div class="in"><div><a class="logo" href="/">{LOGO}<span class="lg">Vibe<em>Gifts</em></span></a><p>Personalized gifts, made with love in Pakistan.</p><p class="pv">{I("lock")} Your privacy is 100% safe with us</p></div>
<div><h4>Explore</h4><a href="/shop/">Shop</a><a href="/about/">About</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a></div>
<div><h4>Policies</h4><a href="/payment-policy/">Payment &amp; Delivery</a><a href="/return-policy/">Return Policy</a><a href="/privacy-policy/">Privacy Policy</a></div>
<div><h4>Contact</h4><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{hi}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a><div class="soc">{soc}</div></div></div>
<p class="cp">© 2026 Vibe Gifts. All rights reserved.</p></footer>
{PICKER}<a class="fwa" href="{hi}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WAICON}</a><script src="/js/app.js" defer></script></body></html>'''
    w(path.strip('/') + '/index.html' if path != '/404.html' and path != '/' else ('404.html' if path == '/404.html' else 'index.html'), s)

def grid(ps): return '<div class="grid">' + ''.join(card(p) for p in ps) + '</div>'
SORT = '<label class="sort">Sort <select id="sort"><option value="">Featured</option><option value="a">Price: low to high</option><option value="d">Price: high to low</option></select></label>'
def chips(cur): return '<nav class="chips">' + ''.join(f'<a href="{h}"{" class=on" if c == cur else ""}>{c}</a>' for h, c in [('/shop/', 'All')] + [(f'/{csl(c)}/', c) for c in CATS if BY[c]]) + '</nav>'

# ---------- Home ----------
feat = [p for c in CATS for p in BY[c] if p['featured'] == '1']
tiles = ''.join(f'<a class="tile" href="/{csl(c)}/"><img src="/images/{BY[c][0]["imgs"][0]}" alt="{c}" width="400" height="400" loading="lazy"><span>{c}</span></a>' for c in CATS if BY[c])
hero_p = next((p for p in P if p['slug'] == 'custom-image-thermal-magic-locket'), P[0])
revs = json.load(open(os.path.join(R, 'data/reviews.json'), encoding='utf-8'))
rv = ''
if revs:
    rv = '<section class="sec alt"><div class="in"><h2>Customer Reviews</h2><div class="rvs">' + ''.join(
        f'<div class="rv"><p class="st">{"★" * int(r["rating"])}{"☆" * (5 - int(r["rating"]))}</p><p>{e(r["text"])}</p><p><b>{e(r["name"])}</b> · {e(r.get("product", ""))}</p>'
        + ''.join(f'<img src="/images/{i}" alt="Customer photo" loading="lazy">' for i in r.get("images", [])) + '</div>' for r in revs) + '</div></div></section>'
ham = wa("Hi Vibe Gifts! 👋 I'd like to ask about a custom gift hamper.")
BYS = {q['slug']: q for q in P}
def rk(l): return [q for q in P if l == 'any' or q['for'] in (l, 'both')]
FANS = {'any': ['custom-image-printed-full-black-mug-premium', 'custom-image-thermal-magic-locket', 'customized-frame'], 'her': ['customized-frame', 'custom-image-thermal-magic-locket', 'heart-shaped-custom-name-locket'], 'him': ['custom-image-printed-full-black-mug-premium', 'custom-name-steel-bracelet', 'customized-hoodie']}
LK = {}
for l, h, st in [('any', 'made just for them', 'Featured Gifts'), ('her', 'made just for her', 'Featured for Her'), ('him', 'made just for him', 'Featured for Him')]:
    r = rk(l); sl = ([q for q in r if q['featured'] == '1'] + [q for q in r if q['featured'] != '1'])[:8] if l == 'any' else r[:8]
    LK[l] = dict(h=h, st=st, sh=[q['slug'] for q in r[:5]], sl=[q['slug'] for q in sl], fan=[[BYS[x]['imgs'][0], BYS[x]['title']] for x in FANS[l]])
fan = ''.join(f'<img src="/images/{im}" alt="{e(al)}" width="300" height="300" style="--r:{rot}deg">' for (im, al), rot in zip(LK['any']['fan'], (-7, 0, 7)))
ANYSL = LK['any']['sl']
SLIDER = ''.join(card(BYS[x], x not in ANYSL) for x in ANYSL + [q['slug'] for q in P if q['slug'] not in ANYSL])
LKJ = '<script type="application/json" id="looks">' + json.dumps(LK, ensure_ascii=False) + '</script>'
perks = ''.join(f'<div class="pf rv-a" style="--d:{i * .08}s"><i>{I(ic)}</i><b>{t}</b><span>{d}</span></div>' for i, (ic, t, d) in enumerate([('palette', 'Made for you', 'Your name, photo or design'), ('ribbon', 'Nafees gift wrapping', 'On every order'), ('clock', 'Ready in 24-36 hours', 'After design approval'), ('basket', 'Gift hampers', 'Custom hampers available')]))
SHSL = []
for l in ('any', 'her', 'him'):
    for x in LK[l]['sh']:
        if x not in SHSL: SHSL.append(x)
ANYSH = LK['any']['sh']
SHOW = ('<section class="show dk" id="show"><div class="stg"><div class="sh-t"><p class="eye">Premium picks</p><h2>Gifts they will remember</h2></div>'
        + ''.join(f'<div class="bgl" data-slug="{x}" style="background-image:url(/images/{BYS[x]["imgs"][0]})"{"" if x in ANYSH else " hidden"}></div>' for x in SHSL)
        + ''.join(f'<article class="pc" data-slug="{x}"{"" if x in ANYSH else " hidden"}><a class="pi" href="{BYS[x]["url"]}"><img src="/images/{BYS[x]["imgs"][0]}" alt="{e(BYS[x]["title"])}" width="600" height="600" loading="lazy"></a><div class="meta"><h3>{e(BYS[x]["title"])}</h3>{price_html(BYS[x])}<div class="btns c"><a class="btn ghost" href="{BYS[x]["url"]}">View</a><a class="btn" href="{order_link(BYS[x])}" target="_blank" rel="noopener">Order on WhatsApp</a></div></div></article>' for x in SHSL)
        + f'<div class="sctl"><button class="sbp" type="button" aria-label="Previous product">&lsaquo;</button><span class="sdt"></span><button class="sbn" type="button" aria-label="Next product">&rsaquo;</button></div><div class="cnt"><span id="sc">1</span> / <span id="sn">{len(ANYSH)}</span></div></div></section>')
mx = max(pct(p) for p in P)
home = f'''<section class="hero dk"><div class="in"><p class="eye">Customized gifts · Pakistan</p><h1>Gifts that speak, <em class="look-h">made just for them</em></h1>
<p>Personalized mugs, lockets, frames and more, beautifully wrapped and delivered to your door.</p><p class="pill">{I("flame")} Up to {mx}% OFF on selected gifts</p><div class="btns c"><a class="btn" href="/shop/">Shop Now</a>
<a class="btn ghost" href="{wa(HI)}" target="_blank" rel="noopener">Order on WhatsApp</a></div><div class="fan">{fan}</div></div></section>
<section class="sec"><div class="in"><div class="perks">{perks}</div></div></section>
<section class="sec"><div class="in"><h2 class="ctr">Shop by Category</h2><div class="tiles">{tiles}</div></div></section>
<section class="sec alt"><div class="in"><div class="sh"><h2 class="sl-t">Featured Gifts</h2><div class="ar"><button id="pv" aria-label="Previous">‹</button><button id="nx" aria-label="Next">›</button></div></div>
<div class="slider" id="sl">{SLIDER}</div></div></section>
{SHOW}
<section class="band lt"><div class="in"><h2>Custom gift hampers also available {I("gift")}</h2><p>Beautiful gift wrapping and hampers made to your occasion. Tell us what you have in mind.</p><a class="btn" href="{ham}" target="_blank" rel="noopener">Ask on WhatsApp</a></div></section>
{rv}{STORY}
<section class="band dk"><div class="in"><h2>Ready to make someone smile?</h2><p>Send us your idea on WhatsApp and we will take it from there.</p><a class="btn" href="{wa(HI)}" target="_blank" rel="noopener">Chat on WhatsApp</a><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></section>{LKJ}'''
page('/', 'Vibe Gifts | Personalized Gifts in Pakistan', 'Custom name mugs, photo lockets, pens, bottles and more. Order personalized gifts in Pakistan on WhatsApp. Gift wrapping and hampers available.', home, hero_p['imgs'][0],
     '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Vibe Gifts", "url": SITE, "email": EMAIL, "sameAs": list(SOC.values())}) + '</script>')

# ---------- Shop & categories ----------
page('/shop/', 'Shop Personalized Gifts | Vibe Gifts', 'Browse all customized gifts: mugs, lockets, pencils, bottles and more. Order on WhatsApp.', f'<section class="sec"><div class="in"><h1>Shop All Gifts</h1>{chips("All")}{SORT}{grid(P)}</div></section>')
INTRO = {'Mugs': 'custom photo and name mugs', 'Lockets': 'personalized lockets', 'Pencils': 'custom name pens', 'Bottles': 'custom name bottles', 'Others': 'bracelets, caps, frames and mobile covers', 'Apparel': 'custom hoodies and winter shawls'}
for c in CATS:
    if BY[c]: page(f'/{csl(c)}/', f'{c} | Personalized Gifts in Pakistan | Vibe Gifts', f'Shop {INTRO[c]} in Pakistan. Customized with your name or photo. Order on WhatsApp.', f'<section class="sec"><div class="in"><h1>{c}</h1>{chips(c)}{SORT}{grid(BY[c])}</div></section>', BY[c][0]['imgs'][0])

# ---------- Products ----------
for p in P:
    th = ''.join(f'<button class="th" data-i="{i}"><img src="/images/{m}" alt="{e(p["title"])} view {i + 1}" width="120" height="120" loading="lazy"></button>' for i, m in enumerate(p['imgs']))
    ob = ''.join(f'<p class="ol">{e(g["n"])}</p><div class="ops" data-g="{gi}">' + ''.join(f'<button class="op{" on" if i == 0 else ""}" data-i="{i}">{e(o["l"])}</button>' for i, o in enumerate(g['o'])) + '</div>' for gi, g in enumerate(p['g']))
    if p['g']: ob += '<p class="hint" hidden>' + I('camera') + ' A photo for this option is coming soon. We share the real photo on WhatsApp.</p>'
    rel = ([x for x in BY[p['category']] if x is not p] + [x for x in P if x['category'] != p['category']])[:4]
    data = json.dumps(dict(t=p['title'], g=p['g'], p=p['price'], c=p['compare_price'], u=SITE + p['url'], i=p['imgs'], wa=WA), ensure_ascii=False)
    deal = f'<div class="deal" id="pp"><div class="dl"><b class="now">{rs(p["low"])}</b>' + (f'<s class="was">{rs(p["compare_price"])}</s><span class="off big">{pct(p)}% OFF</span></div><p class="save">You save {rs(p["compare_price"] - p["low"])} on this gift</p>' if pct(p) else '</div>') + '</div>'
    body = f'''<section class="sec"><div class="in pd"><div class="gal"><img id="mi" src="/images/{p['imgs'][0]}" alt="{e(p['title'])}" width="900" height="900"><div class="ths">{th}</div></div>
<div class="info"><p class="eye"><a href="/{csl(p['category'])}/">{p['category']}</a></p><h1>{e(p['title'])}</h1>{deal}{ob}
<ul class="bl">{''.join(f'<li>{e(b)}</li>' for b in p['bul'])}</ul>
<p class="note">{I("pencil")} Send the name / design / photo on WhatsApp. Production starts only after your design is approved.</p>
<a class="btn big" id="wb" href="{order_link(p)}" target="_blank" rel="noopener">Order on WhatsApp</a>
<ul class="strip"><li>{I("card")} 50% advance + 50% Cash on Delivery</li><li>{I("clock")} Ready within 24-36 hours of design approval</li><li>{I("truck")} Delivery in 3-5 business days. Charges vary by city</li><li>{I("gift")} Gift packing charged separately</li></ul>
<p class="small">Images are for reference. The real photo of your finished product is shared on WhatsApp before dispatch.</p></div></div>
<div class="in"><h2>You may also like</h2>{grid(rel)}</div></section><script type="application/json" id="pd">{data}</script>'''
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p['title'], "image": [SITE + '/images/' + i for i in p['imgs']], "description": p['bul'][0] if p['bul'] else p['title'], "brand": {"@type": "Brand", "name": "Vibe Gifts"}, "offers": {"@type": "Offer", "priceCurrency": "PKR", "price": str(p['low']), "availability": "https://schema.org/InStock", "url": SITE + p['url']}}, ensure_ascii=False) + '</script>'
    d = re.sub(r'^\W+', '', p['bul'][0]) if p['bul'] else p['title']
    page(p['url'], f"{p['title']} | Vibe Gifts", f"{p['title']} from {rs(p['low'])}. {d}. Customized in Pakistan, order on WhatsApp.", body, p['imgs'][0], ld)

# ---------- Static pages ----------
def simple(path, t, d, h, inner): page(path, f'{t} | Vibe Gifts', d, f'<section class="sec"><div class="in txt"><h1>{h}</h1>{inner}</div></section>')
VALS = ''.join(f'<span>{t}</span>' for t in ['Nafees gift wrapping ✦ ', 'Custom gift hampers ✦ ', 'Made just for you ✦ ', 'Ready in 24-36 hours ✦ ', 'Gifts that speak ✦ ']) * 2
about = f'''<section class="dk ab"><span class="fl f1">{I("gift")}</span><span class="fl f2">{I("sparkle")}</span><span class="fl f3">{I("heart")}</span><span class="fl f4">{I("ribbon")}</span><div class="in ctr"><p class="eye">Our story</p><h1>About <em>Vibe Gifts</em></h1><p>Gifts made for one person, wrapped like they matter.</p></div></section>
<div class="vals"><div class="tr">{VALS}{VALS}</div></div>
<section class="sec"><div class="in ctr"><h2>The people behind Vibe Gifts</h2><div class="team"><article class="tm rv-a"><button class="tb" aria-expanded="false"><span class="ph"><img src="/images/team-fahad.webp" alt="Fahad Mehmood, CEO of Vibe Gifts" width="240" height="240" loading="lazy"></span><b>Fahad Mehmood</b><em class="rl">CEO</em><span class="mr">Tap to read more</span></button><div class="bio"><div><p>Fahad leads Vibe Gifts. He has 2+ years of experience in graphic designing and brings that design eye to everything we make, from the way your gift looks to the way this website feels. He is also a student at PGC Ellahabad, and Vibe Gifts is his way of turning creativity into gifts people keep.</p></div></div></article><article class="tm rv-a" style="--d:.12s"><button class="tb" aria-expanded="false"><span class="ph"><img src="/images/team-noman.webp" alt="Noman Sajid, Sales Manager of Vibe Gifts" width="240" height="240" loading="lazy"></span><b>Noman Sajid</b><em class="rl">Sales Manager</em><span class="mr">Tap to read more</span></button><div class="bio"><div><p>Noman looks after sales and our customers. With 2+ years of experience in sales, he helps you pick the right gift, confirms your order details and keeps you updated until your gift reaches your door.</p></div></div></article></div></div></section>
{PRIV}<section class="sec alt"><div class="in txt"><h2 class="ctr">Our story</h2><p>A gift means more when it is made for one person. Vibe Gifts began with a simple idea: turn your names, photos and memories into gifts people keep for years. From name mugs and photo lockets to bottles, frames and bracelets, every piece is customized to your design.</p></div>
<div class="in"><div class="fc"><div class="rv-a"><i>{I("ribbon")}</i><h3>Nafees gift wrapping</h3><p>Every order is wrapped with care, so the gift feels special from the moment it is opened.</p></div><div class="rv-a" style="--d:.1s"><i>{I("heart")}</i><h3>A good customized experience</h3><p>From your first WhatsApp message to delivery at your door, we look after the details.</p></div><div class="rv-a" style="--d:.2s"><i>{I("basket")}</i><h3>Custom gift hampers</h3><p>Looking for something bigger? Custom gift hampers are also available, built around your occasion and budget.</p></div><div class="rv-a" style="--d:.3s"><i>{I("gift")}</i><h3>Custom gifts for everyone</h3><p>Birthdays, anniversaries, corporate gifts or just because. Tell us the idea and we make it yours.</p></div></div></div></section>
<section class="sec"><div class="in"><h2 class="ctr">How it works</h2><div class="steps"><div class="rv-a"><b>Choose your gift</b><p>Pick a product and tap Order on WhatsApp.</p></div><div class="rv-a" style="--d:.1s"><b>Send your details</b><p>Share the name, design or photo to print.</p></div><div class="rv-a" style="--d:.2s"><b>Approve the design</b><p>We send it for your approval first.</p></div><div class="rv-a" style="--d:.3s"><b>We make and deliver</b><p>Ready within 24-36 hours of approval, delivered in 3-5 business days.</p></div></div></div></section>
<section class="band dk"><div class="in"><h2>Let us make your next gift</h2><a class="btn" href="{wa(HI)}" target="_blank" rel="noopener">Chat on WhatsApp</a></div></section>'''
page('/about/', 'About Us | Vibe Gifts', 'Meet the team behind Vibe Gifts: customized gifts, nafees gift wrapping and custom gift hampers in Pakistan.', about)
FAQ = [('How do I order?', 'Open any product and tap “Order on WhatsApp”. A message with the product and link is ready for you. Send your name, design or photo there.'),
       ('How does payment work?', 'Every order is customized, so payment is 50% advance and 50% Cash on Delivery. Account details are shared on WhatsApp only.'),
       ('Why is an advance needed?', 'Customized items cannot be resold, so the advance covers the materials and work for your order.'),
       ('How is my design approved?', 'We send you the design on WhatsApp. Production starts only after you approve it.'),
       ('How long does it take?', 'Your order is ready within 24-36 hours of design approval. Delivery usually takes 3-5 business days.'),
       ('What are the delivery charges?', 'Delivery charges vary from place to place. We confirm the exact amount on WhatsApp before you pay.'),
       ('Is packing included?', 'Gift packing is charged separately. We share the amount on WhatsApp.'),
       ('Can I cancel my order?', 'The advance is non-refundable once your order is confirmed, because the item is made just for you.'),
       ('What if my item is damaged or wrong?', 'Contact us within 24 hours of delivery with an unboxing video and we will make it right.'),
       ('Will the colour match the photos?', 'A slight difference is possible due to lighting and screens. We share a real photo of your finished item before dispatch.'),
       ('Can I change my order?', 'Yes, before the design is approved. After that production begins.'),
       ('Do you make gift hampers?', 'Yes, custom gift hampers are available. Message us on WhatsApp with your occasion and budget.'),
       ('Is my information safe?', 'Yes. We use your name, number, address and photos only to make and deliver your order. We never sell or share them, except with the courier who needs your address. Your photos are never posted without your permission.')]
simple('/faq/', 'FAQ', 'Answers about ordering, payment, delivery, customization and returns at Vibe Gifts.', 'Frequently Asked Questions', ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ))
def gcard(cls, icon, name, handle, url, ext=True):
    return f'<a class="gl {cls} rv-a" href="{url}"{" target=_blank rel=noopener" if ext else ""}><i class="gi">{I(icon)}</i><span class="gt"><b>{name}</b><span>{handle}</span></span><span class="go">{I("arrow")}</span></a>'
CT = ('<section class="ct dk"><span class="orb o1"></span><span class="orb o2"></span><span class="orb o3"></span><div class="in"><div class="ctr cth"><p class="eye">Get in touch</p><h1>Contact <em>Us</em></h1><p>The fastest way to reach us is WhatsApp. Follow us to see our latest gifts.</p></div>'
      '<div class="ctg"><div class="ctl">' + gcard('wa', 'whatsapp', 'WhatsApp', WA_SHOW, wa(HI)) + gcard('ml', 'mail', 'Email', EMAIL, 'mailto:' + EMAIL, False)
      + gcard('tk', 'tiktok', 'TikTok', '@vibe_gifts_official', SOC['TikTok']) + gcard('ig', 'instagram', 'Instagram', '@vibe_gifts_official', SOC['Instagram']) + gcard('fb', 'facebook', 'Facebook', 'Vibe Gifts', SOC['Facebook']) + '</div>'
      '<aside class="gl qrc rv-a"><img src="/images/qr-instagram.webp" alt="Instagram QR code for vibe_gifts_official" width="180" height="207" loading="lazy"><b>Scan to follow us</b><span>@vibe_gifts_official on Instagram</span></aside></div></div></section>')
page('/contact/', 'Contact | Vibe Gifts', 'Contact Vibe Gifts on WhatsApp, email, Instagram, TikTok or Facebook.', CT)
simple('/payment-policy/', 'Payment & Delivery Policy', 'Payment, production time and delivery details for Vibe Gifts orders.', 'Payment &amp; Delivery Policy', '''<p><b>Payment.</b> Every order is customized, so we take 50% advance and 50% Cash on Delivery. Account details are shared only on WhatsApp.</p><p><b>Design approval.</b> Production starts after you approve the final design.</p>
<p><b>Production.</b> Orders are ready within 24-36 hours of design approval.</p><p><b>Delivery.</b> Delivery usually takes 3-5 business days. Delivery charges vary from place to place and are confirmed on WhatsApp.</p><p><b>Packing.</b> Gift packing is charged separately.</p>''')
simple('/return-policy/', 'Return Policy', 'Return and complaint policy for customized gifts at Vibe Gifts.', 'Return Policy', '''<p>Customized items are made specially for you, so we do not accept returns or exchanges.</p><p>If your item arrives damaged or incorrect, contact us within 24 hours of delivery on WhatsApp with a clear unboxing video.</p><p>The advance payment is non-refundable once an order is confirmed.</p>''')
simple('/privacy-policy/', 'Privacy Policy', 'How Vibe Gifts handles your information.', 'Privacy Policy', f'''<p>We collect only what is needed to make and deliver your order: your name, phone number, delivery address and any photo or text you send us on WhatsApp.</p><p>We use it only to complete your order and do not sell it. Customer reviews and photos are shown on the site only with your permission.</p>
<p>This site may use analytics and advertising cookies from Google, Meta and TikTok to measure visits and ads. You can block cookies in your browser.</p><p>Your style choice (Her, Him or Surprise me) is saved only in your own browser.</p><p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')
w('404.html', open(os.path.join(R, 'index.html'), encoding='utf-8').read().split('<main>')[0] + '<main><section class="sec"><div class="in ctr"><h1>Page not found</h1><p>The page you are looking for is not here.</p><a class="btn" href="/shop/">Browse the shop</a></div></section></main>' + open(os.path.join(R, 'index.html'), encoding='utf-8').read().split('</main>')[1])
urls = ['/', '/shop/'] + [f'/{csl(c)}/' for c in CATS if BY[c]] + [p['url'] for p in P] + ['/about/', '/faq/', '/contact/', '/payment-policy/', '/return-policy/', '/privacy-policy/']
w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{u}</loc></url>' for u in urls) + '</urlset>')
w('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print(f'Built {len(P)} products, {len(urls)} pages')
