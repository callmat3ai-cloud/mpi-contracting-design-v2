from pathlib import Path
import json, html

R = Path(__file__).parent
O = R / 'site'
B = '/mpi-contracting-design-v2/'
G = json.loads((R / 'source-manifest.json').read_text())
E = html.escape
routes = []

ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
NAV = [('services', 'Services'), ('about', 'About'), ('our-work', 'Our work'),
       ('testimonials', 'Testimonials'), ('contact', 'Contact')]
PHONE = '(714) 777-4103'

INFO = {
    'concrete': ('Structure, restored.',
                 'Structural repair, flatwork and architectural concrete surfaces.',
                 'Sculptural restraint: cast, cut, finished.'),
    'waterproofing': ('Protection, built in.',
                      'Systems for below grade, decks, podiums and the building envelope.',
                      'Where water is stopped, not merely slowed.'),
    'pool': ('A better shared space.',
             'Pool installation, restoration and the outdoor environments around them.',
             'Water held by structure, structure held by detail.'),
    'stucco': ('The finish matters.',
               'Wall assemblies, repairs, flashing and architectural finishes.',
               'The last millimetre of a building is the one people touch.'),
}


IMG = {'concrete': 'slab', 'waterproofing': 'membrane', 'pool': 'coping', 'stucco': 'render'}
PHOTO = {
 'building': ('Exposed concrete building frame under construction', '50% 50%'),
 'concrete': ('Construction worker placing material during floor work', '50% 55%'),
 'slab': ('Worker power-trowelling a freshly placed concrete slab', '52% 65%'),
 'rebar': ('Concrete placement into a footing beside reinforcing bars', '50% 62%'),
 'pool': ('Terraced resort swimming pools and surrounding decks', '50% 55%'),
 'coping': ('Stone pool coping, tiled edge and clear blue water', '60% 58%'),
 'stucco': ('Worker smoothing a pale plaster wall', '45% 42%'),
 'render': ('Worker applying cement render to a masonry wall', '48% 42%'),
 'membrane': ('Gloved worker positioning rolled waterproofing membrane on a flat roof; illustrative material application, not an MPI project or system specification', '50% 56%'),
}
DETAIL = {
 'concrete': {'flat-work':'slab','entry-drives':'slab','custom-finishes':'slab','traffic-coatings':'slab','pt-cable-repairs':'building','structural-repairs':'building','parking-structures':'building','podium-decks':'building','block-walls':'render','drainage-systems':'rebar'},
 'pool': {'common-areas':'pool','new-installations':'pool','aesthetic-upgrades':'pool'},
 'stucco': {'custom-finishes':'stucco','premium-painting':'stucco'},
}



def link(p, t, c=''):
    return f'<a class="{c}" href="{B}{p.strip("/") + "/" if p else ""}">{t}</a>'


def image(n, alt='', cls='', sizes='(max-width:800px) 100vw,60vw', pos=''):
    pos = PHOTO[n][1]
    style = f' style="object-position:{pos}"'
    safe_alt = E(PHOTO[n][0] + ' — illustrative stock, not MPI work or staff')
    iw, ih = {'concrete': (1600, 1067), 'slab': (1600, 1067), 'coping': (1600, 2400), 'membrane': (1600, 2844), 'rebar': (1600, 2133), 'render': (1600, 2400), 'pool': (1600, 1068), 'building': (1067, 1600), 'stucco': (1600, 1067)}[n]
    loading = 'eager' if cls in ('hero-photo', 'division-photo', 'detail-photo') else 'lazy'
    priority = ' fetchpriority="high"' if loading == 'eager' else ''
    sw = 533 if n == 'building' else 800
    return (f'<img class="{cls}" src="{B}assets/{n}-1600.webp" '
            f'srcset="{B}assets/{n}-800.webp {sw}w,{B}assets/{n}-1600.webp {iw}w" sizes="{sizes}" '
            f'width="{iw}" height="{ih}"{style} alt="{safe_alt}" '
            f'loading="{loading}"{priority} decoding="async">')


def header(active=''):
    nav = ''.join(link(x, t, 'is-active' if x == active else '') for x, t in NAV)
    return ('<div class="note-bar"><span>MPI design review</span>'
            '<span>Illustrative stock imagery · Form demo only</span></div>'
            '<a class="skip" href="#main">Skip to content</a>'
            '<header id="top" class="site-head">'
            + link('', '<b>MPI</b><i></i><small>Contracting Services</small>', 'wordmark')
            + '<button class="menu" aria-controls="site-nav" aria-expanded="false">'
              '<span class="menu-label">Menu</span>'
              '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h18M3 16h18"/></svg></button>'
            + f'<nav id="site-nav" aria-label="Main">{nav}'
              '<div class="nav-foot"><span>Office</span>'
              f'<a href="tel:+17147774103">{PHONE}</a>'
              '<a href="' + B + 'contact/">981 W 18th Street, Suite F · Costa Mesa</a>'
              f'<a class="btn drawer-cta" href="{B}contact/">Discuss your project {ARROW}</a></div></nav>'
            + f'<a class="head-cta" href="{B}contact/"><span>Discuss your project</span>{ARROW}</a>'
            + '<div class="progress" aria-hidden="true" data-progress></div>'
            + '</header><div class="scrim" hidden></div>')


def footer():
    return f'''<footer class="site-foot">
<div class="foot-lead">
  {link('', '<b>MPI</b><small>Contracting Services</small>', 'wordmark')}
  <p>Trusted Partners. Built to Last.</p>
</div>
<div class="foot-cols">
  <div><h2>Divisions</h2>{''.join(link('services/' + d, d.title()) for d in G)}</div>
  <div><h2>Company</h2>{''.join(link(x, t) for x, t in NAV)}</div>
  <div><h2>Office</h2><a href="tel:+17147774103">{PHONE}</a>
  <p>981 W 18th Street, Suite F<br>Costa Mesa, CA 92627</p>
  <p>Monday–Friday, 8:00am–4:30pm<br>Saturday–Sunday, closed</p></div>
</div>
<div class="foot-base"><span>MPI Contracting Services · Review preview</span>
{link('photo-credits', 'Imagery &amp; preview notes')}</div>
</footer>'''


def page(path, title, body, active='', ptype=''):
    doc = f'''<!doctype html><html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
{'<link rel="preload" as="image" href="' + B + 'assets/building-1600.webp" imagesrcset="' + B + 'assets/building-800.webp 533w,' + B + 'assets/building-1600.webp 1067w" imagesizes="100vw">' if ptype == 'home' else ''}<meta name="theme-color" content="#1b1a18">
<title>{E(title)} | MPI Contracting Services</title>
<link rel="preload" href="{B}assets/bodoni-moda.ttf" as="font" type="font/ttf" crossorigin>
<link rel="preload" href="{B}assets/archivo.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{B}assets/site.css">
<script defer src="{B}assets/vendor/gsap.min.js"></script>
<script defer src="{B}assets/vendor/ScrollTrigger.min.js"></script>
<script defer src="{B}assets/site.js"></script>
</head><body class="t-{ptype}">{header(active)}<main id="main">{body}</main>{footer()}</body></html>'''
    dest = O / path / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc)
    routes.append({'route': B + path + ('/' if path else ''), 'file': str(dest.relative_to(O)), 'title': title})


# ---------------------------------------------------------------- shared blocks
def hero():
    return f'''<section class="hero">
  <div class="hero-media" data-parallax="12">
    {image('building', 'Illustrative architectural structure under construction, not an MPI project', 'hero-photo', '100vw')}
    <span class="media-credit">Illustrative stock photography · not an MPI project</span>
  </div>
  <div class="hero-panel">
    <canvas class="field" aria-hidden="true" data-field></canvas>
    <div class="hero-grid">
      <h1><span>Trusted Partners.</span><em>Built to Last.</em></h1>
      <div class="hero-aside">
        <p>Specialty contracting for Southern California’s general contractors, developers and property teams. Concrete, waterproofing, pool and stucco, since 1979.</p>
        <div class="hero-actions">
          {link('contact', 'Discuss your project ' + ARROW, 'btn')}
          {link('services', 'See all services ' + ARROW, 'btn ghost')}
        </div>
      </div>
    </div>
    <span class="hero-rule" aria-hidden="true" data-hero-rule></span>
  </div>
</section>'''


def chapters():
    rows = ''
    for d in G:
        rows += (f'<a class="chapter" href="#c-{d}" data-chapter>'
                 f'<span class="chapter-n">{d.title()}</span>'
                 f'<span class="chapter-d">{INFO[d][0]}</span>{ARROW}</a>')
    return f'<nav class="chapters" id="chapters" aria-label="Division chapters">{rows}</nav>'


def heritage():
    return f'''<section class="heritage">
  <p class="stamp"><span>Established</span><strong>1979</strong></p>
  <p class="stamp-copy">Independent specialty contracting.<br>Costa Mesa · Southern California.</p>
  {link('about', 'A partner’s perspective ' + ARROW, 'text-link')}
</section>'''


def stories():
    out = ['<section class="stories" aria-label="Divisions">']
    for i, d in enumerate(G):
        pos = ['center 40%', 'center 62%', 'center 45%', 'center 55%'][i % 4]
        variant = ['story--a', 'story--b', 'story--c', 'story--d'][i % 4]
        out.append(f'''<article class="story {variant}" id="c-{d}">
  <div class="story-media" data-parallax="8">{image(IMG[d], INFO[d][2], 'story-photo', '100vw', pos)}</div>
  <div class="story-panel reveal">
    <h2>{d.title()}</h2>
    <p class="story-lede">{INFO[d][0]}</p>
    <p>{INFO[d][1]}</p>
    {link('services/' + d, 'Explore the division ' + ARROW, 'text-link')}
  </div>
</article>''')
    out.append('</section>')
    return ''.join(out)


CLIENTS = ['General contractors', 'School districts', 'Municipalities', 'Commercial properties',
           'Apartments', 'Homeowner associations', 'Highrise clients', 'Hospitals',
           'California utility companies']


def editorial():
    items = ''.join(f'<li>{c}</li>' for c in CLIENTS)
    return f'''<section class="editorial">
  <h2>Built for the people<br><em>who build.</em></h2>
  <div class="editorial-body">
    <p>We work closely with our clients to understand their priorities, provide sound technical recommendations, and deliver practical, cost effective solutions to address their property’s specific needs.</p>
    {link('about', 'The MPI difference ' + ARROW, 'text-link')}
  </div>
  <ul class="clients" aria-label="Types of clients MPI works with">{items}</ul>
</section>'''


def materials():
    caps = [('slab', 'Method / Concrete finishing'), ('render', 'Material / Wall render'),
            ('membrane', 'Material / Waterproofing membrane'), ('coping', 'Detail / Pool coping')]
    figs = ''.join(f'<figure class="material">{image(n, "", "material-img", "(max-width:800px) 78vw,32vw")}'
                   f'<figcaption>{c}</figcaption></figure>' for n, c in caps)
    return f'''<section class="materials">
  <div class="mat-head">
    <h2>The details<br>make the difference.</h2>
    <div><p>Materials, methods and the small decisions that survive weather, time and use. Detail crops of illustrative stock photography.</p>
    <div class="mat-ctrl"><button type="button" data-gal="-1" aria-label="Previous images"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12H5M11 6l-6 6 6 6"/></svg></button>
    <button type="button" data-gal="1" aria-label="Next images"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg></button></div></div>
  </div>
  <div class="material-rail" data-rail>{figs}</div>
</section>'''


def technical():
    return f'''<section class="technical-band">
  <svg class="field-draw" viewBox="0 0 600 600" aria-hidden="true" data-draw>
    <g fill="none" stroke="currentColor" stroke-width="1">
      <circle cx="300" cy="300" r="70"/><circle cx="300" cy="300" r="140"/>
      <circle cx="300" cy="300" r="210"/><circle cx="300" cy="300" r="280"/>
      <path d="M20 300h560M300 20v560"/><path d="M90 510 510 90"/>
    </g>
  </svg>
  <div class="tech-copy">
    <h2>One subcontractor.<br>Four divisions.</h2>
    <p>From post tension cable repairs and structural concrete restoration to waterproofing systems and architectural finishes, explore the methods and materials behind each division.</p>
    {link('services', 'Find your project scope ' + ARROW, 'text-link')}
  </div>
  <ol class="principles">
    <li><span>Recommendations</span><p>Sound technical advice, stated plainly, before the schedule decides for you.</p></li>
    <li><span>Coordination</span><p>One subcontractor across four divisions, from structure to finish.</p></li>
    <li><span>Delivery</span><p>Practical, cost effective solutions shaped around each property’s conditions.</p></li>
  </ol>
</section>'''


def cta():
    return f'''<section class="cta">
  <div>
    <h2>Your next scope.<br><em>Let’s talk it through.</em></h2>
    <p>Concrete, waterproofing, pool and stucco services for Southern California projects.</p>
  </div>
  <div class="cta-actions">
    {link('contact', 'Discuss your project ' + ARROW, 'btn light')}
    <a href="tel:+17147774103" class="cta-phone">{PHONE}</a>
  </div>
</section>'''


def masthead(title, copy, extra=''):
    return f'''<section class="masthead">
  <div class="mast-inner"><h1>{title}</h1><div class="mast-aside"><p>{copy}</p>{extra}</div></div>
</section>'''


def cta_band_light():
    return f'''<section class="cta-band">
  <h2>Bring your next scope<br>into focus.</h2>
  <div>{link('contact', 'Start a conversation ' + ARROW, 'text-link')}</div>
</section>'''


# ---------------------------------------------------------------- home
page('', 'Trusted Partners. Built to Last.',
     hero() + chapters() + heritage() + stories() + editorial() + materials() + technical() + cta(),
     ptype='home')

# ---------------------------------------------------------------- services index
service_rows = ''
for d, v in INFO.items():
    rows = ''.join(link('services/' + d + '/' + s['slug'],
                        f'<span>{E(s["title"])}</span>' + ARROW) for s in G[d])
    service_rows += (f'<section class="index-group reveal" id="d-{d}"><div class="index-head">'
                     f'<h2>{d.title()}</h2><p>{v[1]}</p>'
                     + link('services/' + d, 'Division overview ' + ARROW, 'text-link')
                     + f'</div><div class="index-list">{rows}</div></section>')
page('services', 'Project Services',
     masthead('Project<br><em>services.</em>',
              'A technical directory for estimators, general contractors, developers and property teams. Forty-three scopes across four divisions.')
     + '<nav class="jump" aria-label="Divisions">'
     + ''.join(f'<a href="#d-{d}"><span>{d.title()}</span><em>{len(G[d])}</em></a>' for d in G)
     + '</nav>'
     + f'<div class="index">{service_rows}</div>' + cta_band_light(),
     active='services', ptype='index')

# ---------------------------------------------------------------- divisions + 43 services
for d, v in INFO.items():
    rows = ''.join(link('services/' + d + '/' + s['slug'], f'<span>{E(s["title"])}</span>' + ARROW)
                   for s in G[d])
    page('services/' + d, d.title() + ' Division',
         f'''<section class="division-mast">
  {image(IMG[d], INFO[d][2], 'division-photo', '100vw')}
  <div class="division-mast-inner"><h1>{d.title()}</h1>
  <p class="division-lede">{v[0]}</p></div>
</section>
<section class="division-body">
  <div class="division-intro reveal"><p>{v[1]}</p>{link('contact', 'Discuss your scope ' + ARROW, 'btn')}</div>
  <div class="index-list wide">{rows}</div>
</section>''' + cta_band_light(), active='services', ptype='division')

    for j, s in enumerate(G[d]):
        rel = G[d][(j + 1) % len(G[d])]
        body = f'''<div class="detail-mast">
  {image(DETAIL.get(d, {}).get(s['slug'], IMG[d]), '', 'detail-photo', '100vw')}
  <div class="detail-mast-inner">
    <div class="crumbs">{link('services', 'Services')}<span>/</span>{link('services/' + d, d.title())}</div>
    <h1>{E(s['title'])}</h1>
    <div class="detail-mast-actions">{link('contact', 'Discuss this scope ' + ARROW, 'btn')}
    <p class="detail-caption">{d.title()} division · Illustrative stock imagery, not MPI project photography</p></div>
  </div>
</div>
<div class="detail-body">
  <article class="reading-panel reveal">
    <h2>Scope &amp; application</h2>
    <p class="description">{E(s['description'])}</p>
    <p class="panel-note">Bring your project location, existing conditions and anticipated schedule to the conversation.</p>
  </article>
  <aside class="detail-aside">
    <h2>Project considerations</h2>
    <p>Bring your project location, existing conditions, drawings or specifications, and anticipated schedule to the conversation.</p>
    <a class="text-link" href="tel:+17147774103">{PHONE}{ARROW}</a>
    <p class="small">{d.title()} division<br>Southern California</p>
  </aside>
</div>
<section class="related">
  <h2>Continue</h2>
  <div>{link('services/' + d + '/' + rel['slug'], '<span>' + E(rel['title']) + '</span>' + ARROW, 'related-link')}
  {link('services/' + d, 'All ' + d + ' services ' + ARROW, 'text-link')}</div>
</section>'''
        page('services/' + d + '/' + s['slug'], s['title'], body, active='services', ptype='service')

# ---------------------------------------------------------------- about
page('about', 'About MPI',
     masthead('A partner’s<br><em>perspective.</em>',
              'MPI has contributed to our clients’ success and provided specialized construction solutions since 1979.')
     + f'''<section class="about-lead">
  <div class="about-media" data-parallax="8">{image('slab', 'Illustrative concrete work, not an MPI project', 'about-photo', '(max-width:800px) 100vw,48vw')}</div>
  <div class="about-copy reveal">
    <h2>The MPI difference</h2>
    <p>Beyond technical expertise, we ensure our client’s definition of a successful project is fully realized — not just in the finished project but throughout the construction process.</p>
    <p>We work closely with our clients to understand their priorities, provide sound technical recommendations, and deliver practical, cost effective solutions to address their property’s specific needs.</p>
  </div>
</section>
<section class="about-clients">
  <h2>Construction partners<br>across Southern California.</h2>
  <ul>{''.join(f'<li>{c}</li>' for c in CLIENTS)}</ul>
</section>
<section class="about-facts">
  <div><strong>1979</strong><p class="meta">Established</p></div>
  <div><strong>Four</strong><p class="meta">Divisions</p></div>
  <div><strong>Costa Mesa</strong><p class="meta">California</p></div>
  <p class="about-note">Specialized construction solutions for general contractors, developers and property teams across Southern California.</p>
</section>''' + cta_band_light(),
     active='about', ptype='about')

# ---------------------------------------------------------------- our work
page('our-work', 'Our Work',
     masthead('The work,<br><em>in focus.</em>',
              'Materials, methods and possibilities across our four divisions.')
     + f'''<p class="disclosure wrap">Capability imagery only — not MPI completed projects. Approved project photography and case studies are pending, so no projects are presented here.</p>
<section class="gallery">{''.join(f'<figure class="gal-item reveal"><div class="gal-media">{image(IMG[d], INFO[d][2], "", "(max-width:800px) 100vw,60vw")}</div><figcaption><h2>{d.title()}</h2><p>{INFO[d][1]}</p>{link("services/" + d, "Explore capabilities " + ARROW, "text-link")}</figcaption></figure>' for d in G)}</section>'''
     + cta_band_light(), active='our-work', ptype='work')

# ---------------------------------------------------------------- testimonials
page('testimonials', 'Testimonials',
     f'''<section class="voices">
  <div class="voices-copy">
    <h1>Good work starts with<br><em>good partnerships.</em></h1>
    <p>Client testimonials will be published here once they are approved. Nothing has been written in their place — no quotes, names, ratings or logos.</p>
    <div class="voices-actions">{link('our-work', 'Explore our work ' + ARROW, 'btn')}{link('about', 'Meet MPI ' + ARROW, 'text-link')}</div>
  </div>
  <figure class="voices-media" data-parallax="8">{image('building', 'Illustrative structural construction, not an MPI project', 'voices-photo', '(max-width:800px) 100vw,46vw')}<figcaption>Illustrative stock photography · not an MPI project</figcaption></figure>
</section>''' + cta_band_light(), active='testimonials', ptype='voices')

# ---------------------------------------------------------------- contact
FIELDS = [('name', 'Name', 'text'), ('company', 'Company', 'text'), ('email', 'Email', 'email'),
          ('phone', 'Phone (optional)', 'tel'), ('location', 'Project location', 'text')]
form = ('<form id="estimate" novalidate><h2>Outline<br><em>your project.</em></h2>'
        '<p class="disclosure">Demo only. Use fictional details. Nothing is sent or saved. '
        'All fields required unless marked optional.</p><div class="form-grid">'
        + ''.join(f'<label>{lbl}<input id="{k}" type="{t}" autocomplete="off" '
                  f'{"required" if k != "phone" else ""}></label>' for k, lbl, t in FIELDS)
        + '<label>Division<select id="division" required><option value="">Select a division</option>'
        + ''.join(f'<option>{d.title()}</option>' for d in G)
        + '</select></label><label class="full">Project description'
          '<textarea id="description" rows="4" required></textarea></label></div>'
          f'<button type="button" id="demo" class="btn" disabled>Check demo request {ARROW}</button>'
          '<p id="form-status" role="status"></p>'
          '<noscript>No submission is available. Enable JavaScript to test the form.</noscript></form>')
page('contact', 'Contact',
     f'''<section class="contact">
  <div class="contact-info">
    <h1>Let’s discuss<br><em>your project.</em></h1>
    <p>Concrete, waterproofing, pool and stucco services for your next scope.</p>
    <a class="contact-number" href="tel:+17147774103">{PHONE}</a>
    <dl class="contact-details">
      <div><dt>Office</dt><dd>981 W 18th Street, Suite F<br>Costa Mesa, CA 92627</dd></div>
      <div><dt>Hours</dt><dd>Monday–Friday, 8:00am–4:30pm<br>Saturday–Sunday, closed</dd></div>
      <div><dt>Divisions</dt><dd>{', '.join(d.title() for d in G)}</dd></div>
    </dl>
  </div>
  {form}
</section>''', active='contact', ptype='contact')

# ---------------------------------------------------------------- credits
credits = json.loads((R / 'asset-sources.json').read_text())
page('photo-credits', 'Imagery & Preview Notes',
     masthead('About this<br><em>preview.</em>',
              'An isolated design review, not a production website.')
     + f'''<section class="reading-page">
  <h2>Illustrative photography</h2>
  <p>All photographs are licensed stock images, not MPI projects, staff or clients. No endorsement is implied.</p>
  <ul class="credits">{''.join(f'<li><a href="{c["source"]}">{E(c["name"])} — Pexels</a> ({", ".join(c["files"])})</li>' for c in credits)}</ul>
  <p><a href="https://www.pexels.com/license/">Pexels license and use terms</a></p>
  <p>Images are resized, compressed and responsively cropped. Waterproofing imagery shows a stock flat-roof membrane application to illustrate the material only; it does not depict MPI work, an MPI installation method, or the specific assembly described on a service page. Service images provide division context, not documentation of the individual scope.</p>
  <h2>Assets and functionality</h2>
  <p>The text wordmark is a temporary stand-in for approved logo artwork. Approved project images and client testimonials are pending. Display and text faces are self-hosted: Bodoni Moda and Archivo, both under the SIL Open Font License.</p>
  <p>The form demonstrates local validation only. No information is submitted, saved or transmitted. No analytics or tracking are installed, and no third-party requests are made at runtime. All pages are noindex.</p>
  <h2>Motion</h2>
  <p>Scroll reveals, image parallax and the hero field are progressive enhancements. They are disabled entirely under <em>prefers-reduced-motion</em>, and every page reads completely with JavaScript switched off.</p>
  <h2>Production review</h2>
  <p>Business credentials, final claims and production hosting isolation require confirmation before launch. This is a preview deployment only.</p>
</section>''', ptype='notes')

(O / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(O / '.nojekyll').touch()
(R / 'routes.json').write_text(json.dumps(routes, indent=2))
print(len(routes), 'pages;', sum(map(len, G.values())), 'services')
