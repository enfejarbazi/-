#!/usr/bin/env python3
"""Check built pages, route preservation, metadata, schema, links and assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
BASE="https://enfejarbazi.github.io"
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.ids=[]; self.h1=0; self.title=""; self.in_title=False
        self.schemas=[]; self.schema=None; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if tag=="h1": self.h1+=1
        if a.get("id"): self.ids.append(a["id"])
        if tag=="title": self.in_title=True
        if tag=="script" and a.get("type")=="application/ld+json": self.schema=""
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.schema is not None:self.schema+=data
    def handle_endtag(self,tag):
        if tag=="title":self.in_title=False
        if tag=="script" and self.schema is not None:
            self.schemas.append(json.loads(self.schema)); self.schema=None

def check():
    pages={p:Page(p.read_text()) for p in ROOT.rglob("*.html")}
    assert len(pages)==26, f"Expected 26 HTML pages, got {len(pages)}"
    titles=[]; descriptions=[]; indexed=set()
    errors=[]
    for path,p in pages.items():
        rel=path.relative_to(ROOT).as_posix()
        assert p.h1==1,(rel,"H1 count",p.h1)
        assert len(p.ids)==len(set(p.ids)),(rel,"duplicate IDs")
        assert p.title,(rel,"missing title")
        titles.append(p.title)
        metas={a.get("name"):a.get("content") for t,a in p.tags if t=="meta"}
        assert metas.get("description"),(rel,"missing description")
        descriptions.append(metas["description"])
        assert any(t=="html" and a.get("lang")=="fa-IR" and a.get("dir")=="rtl" for t,a in p.tags),(rel,"language")
        assert len(p.schemas)==1 and p.schemas[0]["@graph"],(rel,"schema")
        for node in p.schemas[0]["@graph"]:
            if node["@type"]=="Article":
                assert node.get("headline") and node.get("author") and node.get("image") and node.get("dateModified"),(rel,"Article fields")
        canonical=[a["href"] for t,a in p.tags if t=="link" and a.get("rel")=="canonical"]
        if "noindex" in metas.get("robots",""):
            assert not canonical,(rel,"noindex canonical")
        else:
            expected=BASE+("/" if rel=="index.html" else "/"+rel[:-10])
            assert canonical==[expected],(rel,canonical,expected)
            indexed.add(expected)
        for tag,a in p.tags:
            if tag=="img": assert "alt" in a and a.get("width") and a.get("height"),(rel,"image dimensions/alt")
            refs=[]
            if tag in ("a","link") and a.get("href"):refs.append(a["href"])
            if tag in ("img","script") and a.get("src"):refs.append(a["src"])
            if tag=="img" and a.get("srcset"):refs += [s.strip().split()[0] for s in a["srcset"].split(",")]
            for ref in refs:
                u=urlsplit(ref)
                if u.scheme or u.netloc: continue
                if not u.path: target=path
                else:
                    target=ROOT/unquote(u.path.lstrip("/")) if u.path.startswith("/") else path.parent/unquote(u.path)
                    if u.path.endswith("/"): target=target/"index.html"
                if not target.exists():errors.append((rel,ref,"missing target"))
                if u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append((rel,ref,"missing fragment"))
    assert not errors,errors
    assert len(titles)==len(set(titles)),"Duplicate titles"
    assert len(descriptions)==len(set(descriptions)),"Duplicate descriptions"
    sitemap=ET.parse(ROOT/"sitemap.xml")
    urls={n.text for n in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    assert urls==indexed,("sitemap mismatch",urls.symmetric_difference(indexed))
    old=["","1xbet","about","author/soroush-amini","bet365","betboro","contact","editorial-policy","enfejar","football-betting","guides/algorithm","guides/domain-check","guides/provably-fair","hotbet","jetbet","plinko","poop","privacy","responsible-gaming","sibbet","yekbet"]
    assert all((ROOT/s/"index.html").exists() for s in old),"Original routes missing"
    assert (ROOT/"assets/fonts/Gandom.woff").read_bytes()[:4]==b"wOFF","Invalid font"
    print(f"PASS: {len(pages)} pages, {len(indexed)} indexable URLs, unique metadata, schema, internal links, fragments, images and original routes.")

if __name__=="__main__":check()
