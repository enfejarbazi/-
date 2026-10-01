#!/usr/bin/env python3
"""Build dependency-free, crawlable Persian HTML. Run: python scripts/build_site.py"""
from pathlib import Path
from html import escape as esc
import json
import re
import sys
sys.path.insert(0, str(Path(__file__).parent))
from content import PAGES, BRANDS, page, section

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://enfejarbazi.github.io"
SITE = "سایت شرط بندی"
DATE = "2026-10-01"
REPO = "https://github.com/enfejarbazi/enfejarbazi.github.io"
HUBS = {"شناخت بازی‌ها":("games","بازی‌ها"),"بررسی نام‌ها":("reviews","بررسی نام‌ها"),"راهنماهای کاربردی":("guides","راهنماها")}

def href(slug):
    return "/" + (slug.strip("/") + "/" if slug else "")

def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content,encoding="utf-8")

def prose(text):
    """Keep address examples readable in an RTL paragraph, without injecting HTML."""
    pattern=r"https?://[A-Za-z0-9./_?=\u0026%+#@:-]+|\b(?:[A-Za-z0-9-]+\.)+(?:com|org|net|test)\b|(?<!\w)/help\b"
    pieces=[]; start=0
    for match in re.finditer(pattern,text):
        pieces.append(esc(text[start:match.start()]))
        pieces.append("<bdi>"+esc(match.group())+"</bdi>")
        start=match.end()
    pieces.append(esc(text[start:]))
    return "".join(pieces)

def head(title, desc, slug, kind="WebPage", image="editorial", noindex=False, crumbs=()):
    url = BASE + href(slug)
    title = title if slug == "" else title + " | " + SITE
    graph = [
        {"@type":"WebSite","@id":BASE+"/#website","name":SITE,"url":BASE+"/","inLanguage":"fa-IR","publisher":{"@id":BASE+"/#organization"}},
        {"@type":"Organization","@id":BASE+"/#organization","name":SITE,"url":BASE+"/","logo":{"@type":"ImageObject","url":BASE+"/assets/images/logo.svg"}},
        {"@type":kind,"@id":url+"#page","url":url,"name":title,"description":desc,"inLanguage":"fa-IR","isPartOf":{"@id":BASE+"/#website"}}
    ]
    if kind == "Article":
        graph[-1].update(headline=title.split(" | ")[0],datePublished=DATE,dateModified=DATE,
          image=[BASE+f"/assets/images/{image}-social.jpg"],
          mainEntityOfPage={"@type":"WebPage","@id":url},
          author={"@type":"Person","@id":BASE+"/author/soroush-amini/#person","name":"سروش امینی","url":BASE+"/author/soroush-amini/"},
          publisher={"@id":BASE+"/#organization"})
    elif kind == "ProfilePage":
        graph[-1].update(mainEntity={"@type":"Person","@id":url+"#person","name":"سروش امینی","url":url})
    if crumbs:
        graph.append({"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":i+1,"name":name,"item":BASE+path} for i,(name,path) in enumerate(crumbs)]})
    schema = json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False).replace("</","<\\/")
    canonical = "" if noindex else f'<link rel="canonical" href="{url}"><link rel="alternate" hreflang="fa-IR" href="{url}">'
    return f"""<!doctype html>
<html lang="fa-IR" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc,quote=True)}">
<meta name="robots" content="{'noindex,follow' if noindex else 'index,follow,max-image-preview:large'}">
<meta name="referrer" content="strict-origin-when-cross-origin">{canonical}
<link rel="preload" href="/assets/fonts/Gandom.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v=20261001-r2"><link rel="icon" href="/assets/images/logo.svg?v=20261001-r2" type="image/svg+xml">
<meta name="theme-color" content="#102e25">
<meta property="og:type" content="{'article' if kind=='Article' else 'website'}">
<meta property="og:locale" content="fa_IR"><meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(desc,quote=True)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/images/{image}-social.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{'تصویرسازی مفهومی با اشیای هندسی' if image=='editorial' else 'تصویرسازی زمین فوتبال خالی'}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title,quote=True)}">
<meta name="twitter:description" content="{esc(desc,quote=True)}"><meta name="twitter:image" content="{BASE}/assets/images/{image}-social.jpg">
<script type="application/ld+json">{schema}</script><script src="/assets/js/site.js?v=20261001-r2" defer></script></head><body>"""

def header(slug):
    links = [("","خانه"),("games","بازی‌ها"),("reviews","بررسی نام‌ها"),("guides","راهنماها"),("about","درباره ما")]
    nav = "".join(f'<a href="{href(s)}"'+ (' aria-current="page"' if s==slug else '')+f'>{name}</a>' for s,name in links)
    return f"""<a class="skip" href="#main">رفتن به محتوای اصلی</a>
<div class="topline">برای خواندن دقیق‌تر، تصمیم آگاهانه‌تر · ویژه بزرگسالان</div>
<header class="site-header"><div class="container header-inner">
<a class="brand" href="/"><img src="/assets/images/logo.svg?v=20261001-r2" width="40" height="40" alt=""><span><strong>{SITE}</strong><small>راهنمای فارسی بازی و سواد دیجیتال</small></span></a>
<nav class="nav-links" aria-label="منوی اصلی">{nav}</nav><a class="search-link" href="/search/">جستجوی مطالب ↗</a>
<details class="mobile-nav"><summary>منو</summary><nav aria-label="منوی موبایل">{nav}<a href="/search/">جستجوی مطالب</a></nav></details>
</div></header>"""

def footer():
    return """<footer class="site-footer"><div class="container"><div class="footer-grid">
<div><h2>اطلاعات روشن.<br>پرسش‌های بهتر.</h2><p>راهنمای فارسی برای شناخت سازوکار بازی‌ها، خواندن دامنه‌ها و بررسی ادعاها. این سایت شرط یا پرداخت ثبت نمی‌کند.</p><span class="badge">۱۸+ · بدون وعده سود</span></div>
<div><h3>مسیرهای مطالعه</h3><a href="/games/">شناخت بازی‌ها</a><a href="/reviews/">بررسی نام‌های تجاری</a><a href="/guides/domain-check/">بررسی دامنه</a><a href="/guides/provably-fair/">راستی‌آزمایی نتیجه</a><a href="/responsible-gaming/">آسیب‌های قمار و کمک</a></div>
<div><h3>درباره این راهنما</h3><a href="/about/">درباره ما</a><a href="/editorial-policy/">سیاست تحریریه</a><a href="/author/soroush-amini/">نویسنده: سروش امینی</a><a href="/contact/">تماس و گزارش خطا</a><a href="/privacy/">حریم خصوصی</a></div>
</div><div class="footer-bottom"><span>© ۲۰۲۶ سایت شرط بندی · محتوای آموزشی</span><span>قمار می‌تواند به زیان مالی منجر شود. <a href="/responsible-gaming/">اطلاعات و مسیر کمک</a></span></div></div></footer></body></html>"""

def picture(image="editorial", cls="", priority=False, caption=False):
    alt = "تصویرسازی مفهومی با گوی روشن، قوس شیشه‌ای سبز و اشیای برنجی" if image=="editorial" else "تصویرسازی یک توپ در زمین فوتبال خالی هنگام غروب"
    sizes = "(max-width:1200px) 100vw, 1200px" if cls == "article-cover" else "(max-width:800px) 100vw, 600px"
    im = f'<img class="{cls}" src="/assets/images/{image}-960.webp" srcset="/assets/images/{image}-640.webp 640w, /assets/images/{image}-960.webp 960w, /assets/images/{image}-1440.webp 1440w" sizes="{sizes}" width="1440" height="960" alt="{alt}" '+('fetchpriority="high" loading="eager"' if priority else 'loading="lazy"')+' decoding="async">'
    return im + ('<figcaption>تصویرسازی اصلی · ساخته‌شده با هوش مصنوعی</figcaption>' if caption else "")

def card(slug, index=0, featured=False, searchable=False):
    p=PAGES.get(slug) or {"title":{"reviews":"بررسی نام‌های تجاری","games":"شناخت بازی‌ها","guides":"راهنماهای کاربردی"}[slug],"category":"مسیر مطالعه","description":"موضوع‌های مرتبط را در یک صفحه پیدا کنید و مسیر مناسب مطالعه را انتخاب کنید."}
    return f'<article class="card {"featured" if featured else ""} {"search-card" if searchable else ""}"><span class="tag">{p["category"]}</span><span class="card-number">{index:02d}</span><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><a href="{href(slug)}">مطالعه راهنما <span aria-hidden="true">←</span></a></article>'

def brands():
    return '<div class="link-grid">' + "".join(f'<a class="brand-card" href="/{s}/"><b>{name}</b><span><bdi>{latin}</bdi> · راهنمای بررسی ←</span></a>' for s,name,latin,*_ in BRANDS) + '</div>'

def related(slugs):
    if not slugs: return ""
    return '<section class="container related"><h2>ادامه این مسیر</h2><div class="card-grid">'+"".join(card(s,i+1) for i,s in enumerate(slugs[:3]))+'</div></section>'

def crumb_list(slug,p):
    items=[("خانه","/")]
    hub=HUBS.get(p["category"])
    if hub and slug!=hub[0]: items.append((hub[1],href(hub[0])))
    items.append((p["title"],href(slug)))
    return items

def breadcrumbs(items):
    return '<nav class="container breadcrumbs" aria-label="مسیر صفحه">' + '<span aria-hidden="true">/</span>'.join(f'<a href="{path}">{esc(name)}</a>' if i<len(items)-1 else f'<span aria-current="page">{esc(name)}</span>' for i,(name,path) in enumerate(items)) + '</nav>'

def article(slug,p):
    crumbs=crumb_list(slug,p)
    output=head(p["title"],p["description"],slug,p["kind"],p["image"],crumbs=crumbs)+header(slug)+breadcrumbs(crumbs)
    readtime=max(2,round((len((p["intro"]+str(p["sections"])).split())+100)/160))
    output+=f'<main id="main" class="container"><header class="article-header"><span class="section-kicker">{p["category"]}</span><h1>{esc(p["title"])}</h1><p class="lead">{esc(p["intro"])}</p><div class="meta"><span>بازبینی: <time datetime="{DATE}">۹ مهر ۱۴۰۵</time></span><span>حدود {readtime} دقیقه مطالعه</span>'
    if p["kind"]=="Article": output+='<a href="/author/soroush-amini/">نویسنده: سروش امینی</a>'
    output+='</div></header>'
    if slug in ["enfejar","football-betting","plinko"]: output+=picture(p["image"],"article-cover",True)
    output+='<div class="article-layout"><article class="article-body"><div class="callout"><strong>آنچه باید بدانید</strong><p>'+esc(p["takeaway"])+'</p></div>'
    for i,s in enumerate(p["sections"]):
        output+=f'<section id="section-{i+1}"><h2>{esc(s["title"])}</h2>'
        output+="".join(f'<p>{prose(text)}</p>' for text in s["paragraphs"])
        if s["bullets"]: output+='<ul>'+"".join(f'<li>{esc(t)}</li>' for t in s["bullets"])+'</ul>'
        if s["table"]:
            cols,rows=s["table"]
            output+='<div class="table-wrap"><table><caption class="visually-hidden">'+esc(s["title"])+'</caption><thead><tr>'+"".join(f'<th scope="col">{esc(c)}</th>' for c in cols)+'</tr></thead><tbody>'+"".join('<tr>'+"".join(f'<td>{esc(c)}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
        output+=s["extra"]+'</section>'
    if p["faq"]: output+='<section id="faq" class="faq"><h2>سوالات متداول</h2>'+''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in p["faq"])+'</section>'
    if p["sources"]: output+='<section id="sources" class="sources"><h2>منابع و مطالعه بیشتر</h2><ul>'+''.join(f'<li><a href="{url}" rel="noopener">{esc(name)}</a></li>' for name,url in p["sources"])+'</ul><p>منابع برای توضیح موضوع ذکر شده‌اند؛ ذکر نام یک خدمت به معنی توصیه استفاده از آن نیست.</p></section>'
    if p["kind"]=="Article": output+='<div class="author-box"><span class="author-avatar" aria-hidden="true">س ا</span><div><a href="/author/soroush-amini/">سروش امینی</a><small>نویسنده راهنماهای فارسی · <a href="/editorial-policy/">روش تهیه محتوا</a></small></div></div>'
    output+='</article><aside class="sidebar"><nav class="toc" aria-label="فهرست مطلب"><h2>در این راهنما</h2>'
    output+=''.join(f'<a href="#section-{i+1}">{esc(s["title"])}</a>' for i,s in enumerate(p["sections"]))
    if p["faq"]:output+='<a href="#faq">سوالات متداول</a>'
    if p["sources"]:output+='<a href="#sources">منابع</a>'
    output+='</nav><div class="side-note">خواندن دقیق‌تر، پیش از هر تصمیم. این راهنما سود، برداشت یا امنیت مالی را تضمین نمی‌کند.<a href="/responsible-gaming/">آسیب‌های قمار و کمک ←</a></div></aside></div></main>'
    return output+related(p["related"])+footer()

def home():
    title="سایت شرط بندی؛ راهنمای بازی‌ها و بررسی دامنه"
    desc="راهنمای فارسی بازی انفجار، پلینکو و شرط‌بندی فوتبال؛ بررسی دامنه و ادعاهای هات بت و سایر نام‌ها با توضیحات روشن و بدون وعده سود."
    out=head(title,desc,"",kind="WebPage")+header("")
    out+='<main id="main"><section class="hero"><div class="container hero-grid"><div><p class="eyebrow">راهنمای فارسی بازی و سواد دیجیتال</p><h1>پیش از کلیک،<br><em>بهتر بدانید.</em></h1><p class="lead">از سازوکار بازی‌ها تا بررسی دامنه و ادعاهای فنی؛ توضیح‌های روشن برای پرسیدن سؤال‌های درست درباره شرط‌بندی آنلاین.</p><div class="actions"><a class="button" href="/guides/">شروع از راهنماها <span aria-hidden="true">←</span></a><a class="button outline" href="/reviews/">بررسی نام‌ها</a></div><p class="hero-note">محتوای آموزشی · ویژه بزرگسالان · بدون وعده برد تضمینی</p></div><figure class="hero-art">'+picture(priority=True,caption=True)+'</figure></div></section>'
    out+='<div class="trust-strip"><div class="container"><span><b>۰۱</b> توضیح روشن مفاهیم</span><span><b>۰۲</b> تفکیک ادعا از مدرک</span><span><b>۰۳</b> منابع قابل مراجعه</span></div></div>'
    out+='<section class="section"><div class="container"><div class="section-head"><div><span class="section-kicker">از اینجا شروع کنید</span><h2>سه راهنما، سه پرسش مهم</h2></div><p>چطور آدرس را بخوانیم؟ نتیجه چگونه ساخته می‌شود؟ چه چیزی واقعاً قابل بررسی است؟</p></div><div class="card-grid">'
    out+=''.join(card(s,i+1,i==0) for i,s in enumerate(["guides/domain-check","guides/provably-fair","guides/algorithm"]))
    out+='</div></div></section>'
    out+='<section class="section tint"><div class="container"><div class="section-head"><div><span class="section-kicker">شناخت، پیش از تصمیم</span><h2>بازی‌ها چگونه کار می‌کنند؟</h2></div><a class="arrow-link" href="/games/">همه راهنماهای بازی ←</a></div><div class="card-grid">'+''.join(card(s,i+1) for i,s in enumerate(["enfejar","plinko","poop"]))+'</div></div></section>'
    out+='<section class="section"><div class="container feature-row"><div><span class="section-kicker">راهنمای ویژه</span><h2>عدد ضریب،<br>تمام داستان نیست.</h2><p>در راهنمای فوتبال، تفاوت ضریب، احتمال ضمنی و قواعد تسویه را بخوانید. یک محاسبه‌گر آموزشی نیز معنای عددها را نشان می‌دهد.</p><a class="button" href="/football-betting/">خواندن راهنمای فوتبال ←</a></div><figure class="feature-image">'+picture("football")+'</figure></div></section>'
    out+='<section class="section tint"><div class="container"><div class="section-head"><div><span class="section-kicker">بررسی نام‌ها</span><h2>به جای شعار، سؤال بپرسید.</h2></div><p>برای هر نام، موضوع‌های مهم بررسی را بخوانید. این صفحه‌ها رتبه‌بندی خدمات یا تأیید دامنه رسمی نیستند.</p></div>'+brands()+'</div></section>'
    out+='<section class="section"><div class="container feature-row"><div><span class="section-kicker">شفافیت محتوا</span><h2>آنچه می‌دانیم،<br>آنچه تأیید نشده.</h2><p>مثال‌های آموزشی، اطلاعات فنی و ادعاهای بدون مدرک باید از هم جدا باشند. روش نگارش و گزارش خطا را ببینید.</p><a class="arrow-link" href="/editorial-policy/">سیاست تحریریه ←</a></div><div class="callout warning"><strong>اگر بازی روی زندگی شما اثر گذاشته</strong><p>برای جبران باخت، پرداخت بیشتری انجام ندهید. اگر توقف دشوار شده، مسیرهای حمایت و منابع معتبر را بررسی کنید.</p><a class="arrow-link" href="/responsible-gaming/">اطلاعات و مسیر کمک ←</a></div></div></section></main>'
    return out+footer()

def collection(slug,title,desc,items):
    crumbs=[("خانه","/"),(title,href(slug))]
    out=head(title,desc,slug,"CollectionPage",crumbs=crumbs)+header(slug)+breadcrumbs(crumbs)
    out+=f'<main id="main" class="container"><header class="article-header"><span class="section-kicker">مسیرهای مطالعه</span><h1>{title}</h1><p class="lead">{desc}</p></header>'
    out+='<div class="card-grid" style="margin-bottom:60px">'+''.join(card(s,i+1) for i,s in enumerate(items))+'</div></main>'
    return out+footer()

def search_page():
    title="جستجوی مطالب"
    desc="در راهنماهای فارسی بازی، دامنه، راستی‌آزمایی و اطلاعات سایت جستجو کنید."
    out=head(title,desc,"search",noindex=True)+header("search")+'<main id="main" class="container"><header class="article-header"><h1>'+title+'</h1><p class="lead">'+desc+'</p></header>'
    out+='<div class="search-box"><label for="site-search">موضوع یا نام مورد نظر</label><input type="search" id="site-search" placeholder="مثلاً: هات بت، دامنه، ضریب" autocomplete="off"></div><p class="search-count" id="search-status" role="status"></p><noscript>جستجوی لحظه‌ای به جاوااسکریپت نیاز دارد. همه مطالب در ادامه فهرست شده‌اند.</noscript><div class="card-grid" style="margin-bottom:60px">'
    out+=''.join(card(s,i+1,searchable=True) for i,s in enumerate(PAGES))+'</div></main>'+footer()
    return out

def build():
    for slug,p in PAGES.items(): write(slug+"/index.html",article(slug,p))
    write("index.html",home())
    hubs=[
      ("games","شناخت بازی‌ها","سازوکار بازی‌های دیجیتال، ضریب و قواعد پرداخت را با مثال‌های روشن بخوانید؛ بدون پیشنهاد شرط یا روش برد تضمینی.",["enfejar","plinko","football-betting","poop"]),
      ("guides","راهنماهای کاربردی","از خواندن آدرس وب تا راستی‌آزمایی نتیجه؛ مفاهیم فنی و پرسش‌هایی که پیش از اعتماد به یک ادعا اهمیت دارند.",["guides/domain-check","guides/provably-fair","guides/algorithm","responsible-gaming"]),
      ("reviews","بررسی نام‌های تجاری","راهنمای پرسیدن سؤال‌های درست درباره دامنه، شرایط حساب و ادعاهای نام‌های تجاری؛ بدون رتبه‌بندی یا تجربه پرداخت تأییدنشده.",[b[0] for b in BRANDS])]
    for slug,title,desc,items in hubs: write(slug+"/index.html",collection(slug,title,desc,items))
    write("search/index.html",search_page())
    write("404.html",head("صفحه پیدا نشد","این آدرس در راهنمای فارسی موجود نیست؛ به خانه یا جستجوی مطالب بروید.","404",noindex=True)+header("404")+'<main id="main" class="container not-found"><span class="big" aria-hidden="true">۴۰۴</span><h1>این صفحه پیدا نشد</h1><p>ممکن است آدرس تغییر کرده باشد یا بخشی از آن اشتباه نوشته شده باشد.</p><div class="actions"><a class="button" href="/">بازگشت به خانه ←</a><a class="button" href="/search/">جستجوی مطالب</a></div></main>'+footer())
    all_slugs=[""]+list(PAGES)+[h[0] for h in hubs]
    write("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{href(s)}</loc><lastmod>{DATE}</lastmod></url>\n' for s in all_slugs)+'</urlset>\n')
    write("robots.txt",f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    write(".nojekyll","")
    print(f"Built {len(PAGES)+6} HTML pages and sitemap with {len(all_slugs)} URLs.")

if __name__=="__main__": build()
