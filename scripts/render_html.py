#!/usr/bin/env python3
"""
render_html.py — Markdown to self-contained HTML for research reports.
"""
import html as html_mod
import re
import sys

K = dict(
    ink="#141413", body="#3d3d3a", muted="#8a8a9a",
    line="#d4c0a0", line_s="#a08060",
    canvas="#faf9f5", card="#f5efe6", card2="#efe7da",
    dark="#181715", dark2="#1f1e1b",
)
T = {
    "cict": dict(K, a="#3da9ff", b="#cc785c", c="#5b9bff", sd="#141828"),
    "tech": dict(K, a="#5b9bff", b="#cc785c", c="#4f8cff", sd="#141626"),
}
D = "cict"

def slug(u, s):
    b = re.sub(r'[^\w\u4e00-\u9fff]+','-',re.sub(r'<[^>]+','',s)).strip('-').lower() or 's'
    i = 2
    while (r := f'{b}-{i}' if i > 2 else b) in u:
        i += 1; r = f'{b}-{i}'
    u.add(r); return r

def hl(t):
    t = html_mod.escape(t)
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',re.sub(r'\[(S\d+)\]','<a href="#ref-\\1" class="src-ref">[\\1]</a>',t))

def conv(md):
    u, toc, o = set(), [], []
    tr = []
    def ft():
        nonlocal tr
        if tr:
            o.append('<table>' + ''.join(tr) + '</table>'); tr = []
    for s in md.split('\n'):
        s2 = s.rstrip('\n')
        if not s2.strip(): ft(); o.append(''); continue
        if s2.strip() == '---': ft(); o.append('<hr/>'); continue
        m = re.match(r'^(#{1,3})\s+(.+)$', s2)
        if m:
            ft(); lv = len(m.group(1)); rt = m.group(2).strip()
            sid = slug(u, rt)
            toc.append((lv, rt.replace('<','&lt;').replace('>','&gt;'), sid))
            o.append(f'<h{lv} id="{sid}">{hl(rt)}</h{lv}>'); continue
        if s2.strip().startswith('|') and s2.strip().endswith('|'):
            ce = [c.strip() for c in s2.strip().strip('|').split('|')]
            if all(not c or set(c) <= set('-: ') for c in ce): continue
            if tr:
                ro = '<tr>' + ''.join(
                    ('<td id="ref-{c}"' if i==0 and re.match(r'^S\d+$',c) else '<td>')
                    + f'{hl(c)}</td>' for i,c in enumerate(ce)) + '</tr>'
                tr.append(ro)
            else:
                tr.append('<tr>' + ''.join(f'<th>{hl(c)}</th>' for c in ce) + '</tr>')
            continue
        else: ft()
        if re.match(r'^[-*]\s+', s2.strip()): 
            txt = re.sub(r'^[-*]\s+', '', s2.strip())
            o.append(f'<ul><li>{hl(txt)}</li></ul>')
            continue
        o.append(f'<p>{hl(s2.strip())}</p>')
    return toc, '\n'.join(o)

def ct(t):
    lines = []
    for lv, ti, sid in t:
        if lv >= 3:
            extra = ' style="padding-left:14px"'
        else:
            extra = ''
        line = '<a href="#' + sid + '" class="toc-lv' + str(lv) + '"'
        if extra:
            line += ' ' + extra
        line += '>' + ti + '</a>'
        lines.append(line)
    return '\n'.join(lines)

def css(th):
    t = T[th]
    C = []
    # Root variables
    line1 = ':root{'
    line1 += f'--bg:{t["canvas"]};'
    line1 += f'--card:{t["card"]};'
    line1 += f'--sd:{t["sd"]};'
    line1 += f'--bd:{t["line"]};'
    line1 += f'--bds:{t["line_s"]};'
    line1 += f'--a:{t["a"]};'
    line1 += f'--b:{t["b"]};'
    line1 += f'--c:{t["c"]};'
    line1 += '--sh:0 8px 16px rgba(0,0,0,.18)'
    line1 += '}'
    C.append(line1)
    # Reset and body
    C.append('*{box-sizing:border-box}')
    C.append('body{margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:#141413;line-height:1.8;font-size:15px}')
    # Layout
    C.append('.w{display:grid;grid-template-columns:240px minmax(0,1fr);gap:24px;max-width:1360px;margin:0 auto;padding:20px}')
    # Sidebar
    C.append('.bar{position:sticky;top:0;left:0;align-self:start;height:100vh;overflow-y:auto;padding:20px 14px;border-right:1px solid var(--bds);border-radius:0 12px 12px 0;background:var(--card);box-shadow:var(--sh)}')
    C.append('.bar h2{font-size:9px;margin:0 0 10px;text-transform:uppercase;letter-spacing:.14em;color:var(--a);font-weight:700}')
    C.append('.bar a{display:block;color:#8a8a9a;text-decoration:none;padding:4px 0;font-size:11.5px;border-bottom:1px solid rgba(210,190,150,.2);transition:all .15s;border-radius:3px}')
    C.append('.bar a:hover{color:#141413;background:rgba(255,255,255,.7)}')
    C.append('.bar a.toc-lv2{padding-left:10px;font-size:11px}')
    C.append('.bar a.toc-lv3{padding-left:20px;font-size:10.5px;opacity:.85}')
    # Main
    C.append('.main{min-width:0}')
    C.append('.hero{padding:28px 24px;margin-bottom:20px;border-radius:12px;background:linear-gradient(135deg,var(--card2),var(--card));box-shadow:var(--sh)}')
    C.append('.hero h1{font-size:30px;line-height:1.2;margin:0 0 8px;color:#000;font-weight:700}')
    C.append('.hero p{color:#666;margin:0;font-size:12.5px}')
    C.append('.art{padding:20px;margin-bottom:16px;border-radius:10px;background:#fff;box-shadow:var(--sh)}')
    # Headings - force black
    C.append('h1,h2,h3,h4{line-height:1.3;letter-spacing:-.01em;margin-top:12px;color:#000}')
    C.append('h2{font-size:21px;margin:24px 0 10px;padding-top:8px;border-top:1px solid var(--bds);color:#000;font-weight:600}')
    C.append('h3{font-size:16px;margin:18px 0 8px;color:var(--b);font-weight:600}')
    C.append('h4{font-size:14px;color:var(--c);margin:12px 0 6px;font-weight:500}')
    C.append('p{margin:6px 0;color:#000;line-height:1.75}')
    # Strong: warm parchment with dark ink
    C.append('strong{color:#000;background:linear-gradient(135deg,#f5e6c8,#ebd8b6);font-weight:600;padding:2px 7px;border-radius:5px;font-size:.9em;letter-spacing:.01em;box-shadow:0 1px 2px rgba(0,0,0,.06)}')
    C.append('em{font-style:italic;color:#a9583e;border-bottom:1.5px solid #ebd8b6;padding:0 1px}')
    C.append('ul{padding-left:16px;color:#000}')
    C.append('li{margin:2px 0;line-height:1.7}')
    C.append('hr{border:0;border-top:1px solid var(--bds);margin:18px 0}')
    # Table
    C.append('table{width:100%;border-spacing:0;border-collapse:collapse;font-size:12.5px;min-width:600px;border:1px solid var(--line_s);border-radius:8px;overflow:hidden;box-shadow:inset 0 1px 0 rgba(200,180,140,.25)}')
    C.append('th,td{padding:9px 12px;text-align:left;vertical-align:top;border-right:1px solid var(--line_s);border-bottom:1px solid var(--line_s)}')
    C.append('th{background:linear-gradient(135deg,rgba(220,200,160,.25),rgba(230,210,170,.3));font-weight:700;color:#000;white-space:nowrap;border-bottom:2px solid var(--b);letter-spacing:.02em}')
    C.append('td{color:#000}')
    C.append('thead tr:first-child th{border-left:0}')
    C.append('tbody tr:last-child td,tbody tr th:last-child{border-right:0}')
    C.append('tbody tr:nth-child(odd) td{background:rgba(220,200,170,.06)}')
    C.append('tbody tr:hover td{background:rgba(220,200,170,.18)}')
    # Source refs
    C.append('.src-ref{color:#a9583e;text-decoration:none;font-size:.72em;border-bottom:1px dotted var(--b);font-weight:600;padding:0 3px;border-radius:2px;transition:all .15s}')
    C.append('.src-ref:hover{color:#fff;background:var(--b);border-color:var(--b);box-shadow:0 1px 3px rgba(0,0,0,.1)}')
    # Responsive
    C.append('@media(max-width:840px){')
    C.append('  .w{display:block;padding:12px}')
    C.append('  .bar{position:relative;height:auto;border-radius:0;border-bottom:1px solid var(--bds);padding:14px}')
    C.append('  .main{padding:12px}.hero h1{font-size:24px}.art{padding:14px}')
    C.append('  table{font-size:11px}')
    C.append('}')
    return '\n'.join(C) + '\n'

def render(text, theme=None):
    th = theme if theme in T else D
    toc, body = conv(text)
    title = next((t for _, t, _ in toc if t), 'Report')
    toc_html = ct(toc)
    css_str = css(th)
    js = "document.querySelectorAll('a[href^=\"#\"]').forEach(function(a){a.onclick=function(e){e.preventDefault();var t=document.querySelector(a.href);if(t)t.scrollIntoView({behavior:'smooth',block:'start'})}});"
    parts = []
    parts.append('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    parts.append(f'<title>{title}</title>')
    parts.append(f'<style>{css_str}</style>')
    parts.append('</head><body>')
    parts.append('<div class="w">')
    parts.append(f'<aside class="bar"><h2>目录</h2>{toc_html}</aside>')
    parts.append('<main class="main">')
    parts.append(f'<section class="hero"><h1>{title}</h1><p>Market Analysis Report</p></section>')
    parts.append(f'<article class="art" id="content">{body}</article>')
    parts.append('</main>')
    parts.append('</div>')
    parts.append(f'<script>{js}</script>')
    parts.append('</body></html>')
    return '\n'.join(parts)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: render_html.py input.md output.html [--theme cict]'); sys.exit(0)
    t = None
    if '--theme' in sys.argv and sys.argv.index('--theme')+1 < len(sys.argv):
        t = sys.argv[sys.argv.index('--theme')+1]
    open(sys.argv[2],'w',encoding='utf-8').write(render(open(sys.argv[1],encoding='utf-8').read(),t))
    print(f'WROTE {sys.argv[2]}')
