#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Al Fikri — SEO Page Generator
==============================
এই স্ক্রিপ্ট articles.json পড়ে প্রতিটা আর্টিকেলের
আলাদা HTML ফাইল ও sitemap.xml তৈরি করে।

ব্যবহার:
    python generate_pages.py
"""

import json
import os
from datetime import datetime

# ============================
# কনফিগারেশন — শুধু এটুকু বদলান
# ============================
SITE_URL = "https://alfikrime.github.io"  # আপনার সাইটের URL
ARTICLES_FILE = "articles.json"           # articles.json এর নাম
OUTPUT_DIR = "posts"                      # আর্টিকেল ফাইলগুলো কোথায় যাবে
AUTHOR = "কাজী ইবনুল হোসেন"
SITE_NAME = "চিন্তার আঙিনা | Al Fikri"
SITE_DESC = "দর্শন, কালাম, বিজ্ঞান, সভ্যতা, মনোবিজ্ঞান ও সাহিত্য।"
# ============================

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Noto+Sans+Bengali:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box}
:root{--ink:#1a1612;--cream:#f5f2ec;--parchment:#ede8de;--border:#d6cfc2;--accent:#5c3d1e;--accent-light:#8b5e2f;--muted:#888070;--white:#fff;--gold:#b8933f}
html,body{margin:0;padding:0;background:#fff;font-family:'Noto Sans Bengali','EB Garamond',Georgia,sans-serif;color:#1c1c1c}
#rpbar{position:fixed;top:0;left:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--gold));width:0%;z-index:9999;transition:width .08s linear;pointer-events:none}
.W{width:100%;max-width:780px;margin:0 auto;padding:0 18px}
header{background:#fff;border-bottom:2px solid var(--ink);padding:14px 0 10px;margin-bottom:32px}
.h-brand{text-align:center;text-decoration:none;display:block}
.h-title{font-family:'Playfair Display',serif;font-weight:700;font-size:clamp(22px,5vw,36px);color:var(--ink);display:block}
.h-tag{font-size:11px;color:var(--muted);letter-spacing:2px;font-style:italic;display:block;margin-top:4px}
.back{display:inline-block;margin-bottom:24px;background:none;border:1px solid var(--border);padding:7px 16px;font-size:12px;cursor:pointer;font-family:sans-serif;color:var(--muted);border-radius:2px;text-decoration:none}
.back:hover{border-color:var(--accent);color:var(--accent)}
.pill{display:inline-block;padding:3px 10px;border-radius:1px;font-size:10px;font-family:sans-serif;letter-spacing:1.5px;text-transform:uppercase;background:var(--parchment);color:var(--accent);border:1px solid var(--border)}
.a-title{font-family:'Playfair Display',serif;font-size:clamp(22px,5vw,36px);font-weight:700;line-height:1.25;margin:14px 0 10px;color:var(--ink)}
.a-meta{display:flex;gap:14px;font-size:13px;color:var(--muted);font-family:sans-serif;flex-wrap:wrap;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid var(--border)}
.body p{font-family:'Noto Sans Bengali','EB Garamond',Georgia,sans-serif;font-size:clamp(18px,2.8vw,22px);line-height:2.1;color:#221e18;margin:0 0 1.1em;text-align:justify;word-break:break-word}
.body .sec-head{font-family:'Playfair Display',serif;font-size:clamp(16px,3vw,20px);font-weight:600;color:var(--ink);margin:2em 0 .5em;border-left:4px solid var(--accent);padding-left:12px}
.body .divider{text-align:center;color:var(--border);letter-spacing:.6em;font-size:13px;margin:1.8em 0}
.body .wager-item{padding:9px 14px 9px 18px;border-left:3px solid var(--border);margin:4px 0;font-size:clamp(15px,2.5vw,17px);color:#333;line-height:1.8}
.body .wager-item.good{border-color:var(--gold);background:rgba(184,147,63,.06)}
.body .wager-item.bad{border-color:#b05020;background:rgba(176,80,32,.05)}
.body p.dropcap::first-letter{font-size:1.6em;font-weight:700;color:var(--accent)}
.refs{background:#fff;border:1px solid var(--border);border-radius:3px;padding:18px 22px;margin-bottom:24px}
.refs h3{font-family:'Playfair Display',serif;font-size:17px;font-weight:600;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--border);color:var(--ink)}
.ref{padding:7px 0;border-bottom:1px solid var(--parchment);font-size:14px;line-height:1.8;color:#444;word-break:break-word}
.ref:last-child{border-bottom:none}
.ref a{color:var(--accent);text-decoration:none}
.tags{margin:28px 0 16px}
.tag{display:inline-block;background:var(--parchment);color:var(--accent);padding:3px 9px;font-size:11px;margin:2px;font-family:sans-serif;border:1px solid var(--border);border-radius:1px}
.sh-label{font-size:11px;color:var(--muted);font-family:sans-serif;letter-spacing:1px;margin-bottom:8px}
.sh-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:40px}
.sh-btn{padding:10px 14px;border:1px solid var(--border);font-size:12px;background:#fff;font-family:sans-serif;cursor:pointer;border-radius:2px}
.sh-btn:hover{background:var(--parchment)}
.cover-img{width:100%;max-height:360px;object-fit:cover;border-radius:4px;margin-bottom:1.2em;box-shadow:0 2px 16px rgba(0,0,0,.12)}
footer{background:var(--ink);color:#999;padding:28px 0 16px;margin-top:40px;text-align:center;font-size:12px;font-family:sans-serif}
footer a{color:#bbb;text-decoration:none}
footer a:hover{color:#fff}
</style>
"""

def escape_html(text):
    if not text:
        return ""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;"))

def render_body(paragraphs):
    """bodyParagraphs থেকে HTML তৈরি করে"""
    html = ""
    for b in paragraphs:
        t = b.get("type", "p")
        text = escape_html(b.get("text", ""))

        if t == "p":
            cls = ' class="dropcap"' if b.get("dropcap") else ""
            html += f'<div class="body"><p{cls}>{text}</p></div>\n'

        elif t == "sec":
            html += f'<div class="body"><div class="sec-head">{text}</div></div>\n'

        elif t == "div":
            html += '<div class="body"><div class="divider">· · ·</div></div>\n'

        elif t == "wager":
            items_html = ""
            for it in b.get("items", []):
                cls = it.get("cls", "")
                it_text = escape_html(it.get("text", ""))
                items_html += f'<div class="wager-item {cls}">{it_text}</div>\n'
            html += f'<div class="body" style="margin:0 0 1.1em">{items_html}</div>\n'

        elif t == "iframe":
            src = escape_html(b.get("src", ""))
            height = b.get("height", 500)
            caption = escape_html(b.get("caption", ""))
            cap_html = f'<div style="font-size:12px;color:var(--muted);text-align:center;margin-top:6px;font-style:italic">{caption}</div>' if caption else ""
            html += f'<div class="body"><iframe src="{src}" height="{height}" width="100%" style="border:none;border-radius:4px" scrolling="no"></iframe>{cap_html}</div>\n'

        elif t == "img":
            src = escape_html(b.get("url", ""))
            caption = escape_html(b.get("caption", ""))
            cap_html = f"<figcaption>{caption}</figcaption>" if caption else ""
            html += f'<div class="body"><figure style="margin:1.5em 0;text-align:center"><img src="{src}" alt="{caption}" style="max-width:100%;border-radius:4px" loading="lazy"/>{cap_html}</figure></div>\n'

        elif t == "html":
            html += f'<div class="body">{b.get("html","")}</div>\n'

    return html


def render_refs(refs):
    if not refs:
        return ""
    items = ""
    for r in refs:
        links_html = ""
        for lk in r.get("links", []):
            links_html += f' <a href="{escape_html(lk["url"])}" target="_blank" rel="noopener">{escape_html(lk["label"])} ↗</a>'
        note_html = f'<span style="display:block;color:var(--muted);font-size:12px;margin-top:3px;font-style:italic">{escape_html(r.get("note",""))}</span>' if r.get("note") else ""
        items += f'<div class="ref"><strong>[{r["num"]}]</strong> {escape_html(r.get("text",""))}{note_html}{links_html}</div>\n'
    return f'<div class="refs"><h3>তথ্যসূত্র</h3>{items}</div>\n'


def generate_article_html(a, all_articles):
    """একটি আর্টিকেলের সম্পূর্ণ HTML তৈরি করে"""

    title = escape_html(a.get("title", ""))
    title_en = escape_html(a.get("titleEn", ""))
    abstract = escape_html(a.get("abstract", ""))
    date = a.get("date", "")
    author = AUTHOR
    art_id = a.get("id", "")
    cat_id = a.get("cat", "")
    tags = a.get("tags", [])
    url = f"{SITE_URL}/posts/{art_id}.html"

    # ক্যাটাগরি নাম
    cat_names = {
        "philosophy": "দর্শন ও কালাম",
        "science": "বিজ্ঞান ও নৈতিকতা",
        "history": "সভ্যতা ও ইতিহাস",
        "psychology": "মনোবিজ্ঞান ও মানবআচরণ",
        "literature": "সাহিত্য ও কবিতা",
    }
    cat_label = cat_names.get(cat_id, cat_id)

    # পরবর্তী আর্টিকেল (একই ক্যাটাগরি)
    same_cat = [x for x in all_articles if x["id"] != art_id and x.get("cat") == cat_id]
    next_art = same_cat[0] if same_cat else None

    tags_html = "".join(f'<span class="tag">#{escape_html(t)}</span>' for t in tags)

    body_html = render_body(a.get("bodyParagraphs", []))
    refs_html = render_refs(a.get("refs", []))

    cover_html = ""
    if a.get("coverImage"):
        ci = a["coverImage"]
        cover_html = f'<img class="cover-img" src="{escape_html(ci.get("url",""))}" alt="{escape_html(ci.get("caption", title))}" loading="lazy"/>\n'

    next_html = ""
    if next_art:
        n_title = escape_html(next_art.get("title", ""))
        n_abs = escape_html(next_art.get("abstract", ""))
        n_href = f"{next_art['id']}.html"
        next_html = f"""
<div style="margin-top:40px;padding-top:28px;border-top:2px solid var(--border)">
  <div style="font-family:sans-serif;font-size:11px;letter-spacing:1.5px;color:var(--muted);text-transform:uppercase;margin-bottom:16px">আরো পড়ুন</div>
  <a href="{n_href}" style="display:block;background:#fff;border:1px solid var(--border);border-radius:4px;padding:16px 18px;text-decoration:none;transition:border-color .2s">
    <div style="font-size:10px;font-family:sans-serif;letter-spacing:1px;color:var(--accent);text-transform:uppercase;margin-bottom:6px">আরো পড়ুন</div>
    <div style="font-family:'Playfair Display',serif;font-size:18px;font-weight:600;color:var(--ink);line-height:1.35;margin-bottom:6px">{n_title}</div>
    <div style="font-size:13px;color:var(--muted);line-height:1.6">{n_abs[:120]}...</div>
    <div style="font-size:13px;color:var(--accent);margin-top:10px">পড়ুন →</div>
  </a>
</div>
"""

    html = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} — {SITE_NAME}</title>
<meta name="description" content="{abstract[:160]}"/>
<meta name="author" content="{author}"/>
<meta name="keywords" content="{', '.join(tags)}"/>
<link rel="canonical" href="{url}"/>

<!-- Open Graph (Facebook, WhatsApp) -->
<meta property="og:type" content="article"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{abstract[:200]}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:site_name" content="{SITE_NAME}"/>
<meta property="og:locale" content="bn_BD"/>
<meta property="article:author" content="{author}"/>

<!-- Twitter Card -->
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{abstract[:200]}"/>

<!-- Structured Data (JSON-LD) -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{abstract[:200]}",
  "author": {{
    "@type": "Person",
    "name": "{author}"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "{SITE_NAME}",
    "url": "{SITE_URL}"
  }},
  "url": "{url}",
  "inLanguage": "bn"
}}
</script>

{CSS}
</head>
<body>
<div id="rpbar"></div>

<header>
  <div class="W">
    <a class="h-brand" href="{SITE_URL}">
      <span class="h-title">চিন্তার আঙিনা</span>
      <span class="h-tag">দর্শন · কালাম · ইতিহাস · মনোবিজ্ঞান · সাহিত্য</span>
    </a>
  </div>
</header>

<div class="W">
  <a class="back" href="{SITE_URL}">← ফিরে যান</a>

  <span class="pill">{cat_label}</span>
  <h1 class="a-title">{title}</h1>
  <div class="a-meta">
    <span>✍ {author}</span>
    <span>◷ {date}</span>
  </div>

  {cover_html}
  {body_html}
  {refs_html}

  <div class="tags">{tags_html}</div>

  <div class="sh-label">শেয়ার করুন</div>
  <div class="sh-row">
    <button class="sh-btn" onclick="navigator.clipboard.writeText(window.location.href);alert('লিংক কপি!')">🔗 কপি</button>
    <button class="sh-btn" onclick="window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(document.title)+'&url='+encodeURIComponent(window.location.href))">𝕏</button>
    <button class="sh-btn" onclick="window.open('https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(window.location.href))">Facebook</button>
    <button class="sh-btn" onclick="window.print()">🖨</button>
  </div>

  {next_html}
</div>

<footer>
  <div>© ২০২৬ {author} &nbsp;·&nbsp; <a href="{SITE_URL}">{SITE_NAME}</a></div>
</footer>

<script>
// রিডিং প্রগ্রেস বার
window.addEventListener('scroll',function(){{
  var el=document.documentElement;
  var pct=el.scrollHeight-el.clientHeight;
  var bar=document.getElementById('rpbar');
  if(bar) bar.style.width=(pct>0?(el.scrollTop/pct*100):0)+'%';
}});
</script>
</body>
</html>
"""
    return html


def generate_sitemap(articles):
    """sitemap.xml তৈরি করে"""
    today = datetime.today().strftime("%Y-%m-%d")
    urls = f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>\n"""

    for a in articles:
        art_url = f"{SITE_URL}/posts/{a['id']}.html"
        urls += f"""  <url>
    <loc>{art_url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""


def main():
    # articles.json পড়া
    if not os.path.exists(ARTICLES_FILE):
        print(f"❌ {ARTICLES_FILE} পাওয়া যায়নি! স্ক্রিপ্টের পাশে রাখুন।")
        return

    with open(ARTICLES_FILE, encoding="utf-8") as f:
        articles = json.load(f)

    print(f"✅ {len(articles)}টি আর্টিকেল পাওয়া গেছে।")

    # posts/ ফোল্ডার তৈরি
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # প্রতিটা আর্টিকেলের HTML তৈরি
    for a in articles:
        art_id = a.get("id")
        if not art_id:
            print(f"⚠️  id নেই, এড়িয়ে গেলাম: {a.get('title','?')}")
            continue

        html = generate_article_html(a, articles)
        filepath = os.path.join(OUTPUT_DIR, f"{art_id}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"   ✍ তৈরি: {filepath}")

    # sitemap.xml তৈরি
    sitemap = generate_sitemap(articles)
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("✅ sitemap.xml তৈরি হয়েছে।")

    print(f"\n🎉 সম্পন্ন! {len(articles)}টি ফাইল '{OUTPUT_DIR}/' ফোল্ডারে তৈরি হয়েছে।")
    print("এখন পুরো ফোল্ডারটা GitHub-এ push করুন।")


if __name__ == "__main__":
    main()
