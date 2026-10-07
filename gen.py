"""프로필 그림(SVG)을 다크/라이트 두 벌로 만든다.  실행: python gen.py"""
from pathlib import Path

OUT = Path(__file__).parent / "assets"
SHARE = "https://claude.ai/artifact/5SkoEZ41K48d7E4Ehmkyiw"

THEMES = {
    "light": dict(bg="#ffffff", border="#d0d7de", text="#1f2328", muted="#59636e",
                  accent="#047857", track="#e4e7eb", on="#ffffff", chip="#ecfdf5"),
    "dark":  dict(bg="#161b22", border="#30363d", text="#f0f6fc", muted="#9198a1",
                  accent="#34d399", track="#30363d", on="#04241a", chip="#0f2a22"),
}

STYLE = """<style>
text{{font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR',sans-serif;fill:{text}}}
.m{{fill:{muted}}} .a{{fill:{accent}}} .mono{{font-family:'JetBrains Mono',Consolas,monospace}}
@keyframes rise{{from{{opacity:0;transform:translateY(6px)}}}}
@keyframes fill{{from{{transform:scaleX(0)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes blip{{0%,100%{{opacity:.2}}40%{{opacity:1}}}}
.r{{animation:rise .8s cubic-bezier(.16,1,.3,1) backwards}}
.xp{{transform-box:fill-box;transform-origin:left;animation:fill 1.6s cubic-bezier(.16,1,.3,1) .4s backwards}}
.sweep{{transform-origin:700px 120px;animation:spin 4s linear infinite}}
.b1{{animation:blip 4s linear infinite}} .b2{{animation:blip 4s linear 2.2s infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>"""


def svg(w, h, t, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">{STYLE.format(**t)}'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            f'{body}</svg>')


def hero(t):
    body = f"""
<rect x="32" y="40" width="64" height="64" rx="12" fill="{t['chip']}" stroke="{t['accent']}"/>
<text x="64" y="82" text-anchor="middle" font-size="28" font-weight="700" class="a mono">W</text>
<g class="r"><text x="120" y="66" font-size="30" font-weight="700">Won-22</text></g>
<g class="r" style="animation-delay:.1s"><text x="120" y="96" font-size="16" font-weight="700" class="a">훈련생 <tspan class="mono">Lv.1</tspan></text></g>
<g class="r" style="animation-delay:.2s"><text x="32" y="148" font-size="15" class="m">보안관제(SOC) 분석가를 목표로 공부하고 있습니다.</text></g>
<text x="32" y="186" font-size="11" class="m mono">EXP</text>
<rect x="64" y="179" width="380" height="8" rx="4" fill="{t['track']}"/>
<rect class="xp" x="64" y="179" width="152" height="8" rx="4" fill="{t['accent']}"/>
<g fill="none" stroke="{t['border']}">
  <circle cx="700" cy="120" r="28"/><circle cx="700" cy="120" r="56"/><circle cx="700" cy="120" r="84"/>
  <path d="M616 120h168M700 36v168"/>
</g>
<g class="sweep">
  <path d="M700 120L784 120A84 84 0 0 0 764.3 66Z" fill="{t['accent']}" fill-opacity=".16"/>
  <path d="M700 120H784" stroke="{t['accent']}" stroke-width="1.5"/>
</g>
<circle class="b1" cx="736" cy="146" r="4" fill="{t['accent']}"/>
<circle class="b2" cx="672" cy="86" r="4" fill="{t['accent']}"/>"""
    return svg(840, 240, t, body, "Won-22, 훈련생 Lv.1. 보안관제(SOC) 분석가를 목표로 공부하고 있습니다.")


def card(t, w, kind, title, desc, meta, cta=None):
    body = f"""
<text x="28" y="40" font-size="12" class="m">{kind}</text>
<text x="28" y="72" font-size="22" font-weight="700">{title}</text>
<text x="28" y="100" font-size="14" class="m">{desc}</text>
<text x="28" y="126" font-size="12" class="a mono">{meta}</text>"""
    if cta:
        body += f"""
<rect x="{w-28-136}" y="54" width="136" height="42" rx="21" fill="{t['accent']}"/>
<text x="{w-28-68}" y="80" text-anchor="middle" font-size="15" font-weight="700" style="fill:{t['on']}">{cta}</text>"""
    return svg(w, 150, t, body, f"{title}: {desc}")


def stats(t):
    x, chips = 28, ""
    for name in ["Python", "Jupyter", "JavaScript", "로그 분석"]:
        cw = 26 + sum(15 if ord(c) > 0x3000 else 8.4 for c in name)
        chips += (f'<rect x="{x}" y="58" width="{cw:.0f}" height="30" rx="15" fill="{t["chip"]}"/>'
                  f'<text x="{x + cw/2:.0f}" y="78" text-anchor="middle" font-size="13">{name}</text>')
        x += cw + 8
    body = f"""
<text x="28" y="40" font-size="12" class="m">보유 스킬</text>{chips}
<rect x="540" y="24" width="272" height="78" rx="12" fill="none" stroke="{t['border']}" stroke-dasharray="4 4"/>
<text x="560" y="52" font-size="12" class="m">다음 목표</text>
<text x="560" y="80" font-size="16" font-weight="700">리눅스·네트워크 기초</text>"""
    return svg(840, 126, t, body, "보유 스킬: Python, Jupyter, JavaScript, 로그 분석. 다음 목표: 리눅스·네트워크 기초")


OUT.mkdir(exist_ok=True)
for name, t in THEMES.items():
    files = {
        "hero": hero(t),
        "quest-socquest": card(t, 840, "메인 퀘스트", "SOC Quest",
                               "학원 파이썬 노트북 36문제를 브라우저에서 바로 풀어 보는 학습 게임",
                               "Python  JavaScript", cta="플레이하기"),
        "quest-toolkit": card(t, 412, "퀘스트", "security-agent-toolkit", "Skt Aleph 학습", "Jupyter Notebook"),
        "quest-aleph": card(t, 412, "퀘스트", "SKT-ALEPH", "프로젝트성 과제", "JavaScript"),
        "stats": stats(t),
    }
    for f, s in files.items():
        (OUT / f"{f}-{name}.svg").write_text(s, encoding="utf-8")
print("ok:", sorted(p.name for p in OUT.iterdir()))
