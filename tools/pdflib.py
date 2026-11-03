"""Parse a Code Reviser "COMBINEDTITLE" PDF (lawfilesext.leg.wa.gov/law/RCWPDF/) into RCW sections. Deterministic.

Layout (Courier 12 pt): a section starts with a bold line "RCW <cite>  <Caption>." at the paragraph indent; the
caption may wrap; the text follows in regular type. A new paragraph starts at the indent (x about 88); a wrapped line
starts at the margin (x about 52). The history note "[...]" closes the text; notes after it (until the next section),
chapter headings, tables of sections, italic cross references and the 10 pt page footers are not law text.
"""
import re

PUNCT = {'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '−': '-'}
HEAD = re.compile(r'^RCW\s+(\d+[A-Z]?\.[0-9]+[A-Z]?[.\-][0-9][0-9A-Za-z.\-]*)\s+(.*)$')
HIST = re.compile(r'\s*\[[^\[\]]*\b(c|ex\.s\.|s|sp\.s\.|Initiative|Code|RRS|Rem\.|Laws|Const\.)\b[^\[\]]*\]\s*$')


def norm(s):
    for a, b in PUNCT.items():
        s = s.replace(a, b)
    s = s.replace('\xa0', ' ').replace('\xad', '').replace('​', '').replace('﻿', '')
    s = re.sub(r'(^|\s)\*(?=\d)', r'\1* ', s)   # "RCW *43.43" reads "RCW * 43.43" in the section files
    return re.sub(r'[ \t\r\n]+', ' ', s).strip()


def lines_of(doc):
    """(x0, kind, text, bold_prefix) per text line, footers dropped; kind: bold|italic|normal|small."""
    out = []
    for page in doc:
        for b in page.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                sp = [s for s in ln['spans'] if s['text']]
                if not sp:
                    continue
                size = max(round(s['size']) for s in sp)
                txt = ''.join(s['text'] for s in sp)
                if not txt.strip():
                    continue
                if size <= 10 and all(round(s['size']) <= 10 for s in sp):
                    foot = re.fullmatch(r'\s*(Certified on \d+/\d+/\d{4}|(Combined )?(Chapter|Title) \S+ RCW|Page \d+)\s*', txt)
                    out.append((round(ln['bbox'][0]), 'footer' if foot else 'small', txt, ''))
                    continue
                f0 = sp[0]['font']
                bold = 'Bold' in f0
                ital = 'Italic' in f0
                bp = ''
                for s in sp:
                    if 'Bold' in s['font'] or (bp and not s['text'].strip()):
                        bp += s['text']
                    else:
                        break
                kind = 'bolditalic' if bold and ital else 'bold' if bold else 'italic' if ital else 'normal'
                out.append((round(ln['bbox'][0]), kind, txt, bp))
    return out


def join(a, b):
    if not a:
        return b
    if a.endswith(('-', '—', '–')) and not a.endswith((' -', ' —', ' –')):
        return a + b
    if b.startswith(('—', '–')) or (b.startswith('-') and len(b) > 1 and not b[1].isspace()):
        return a + b
    return a + ' ' + b


MON = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']


def status(cap):
    """('until'|'from'|'expires'|None, 'YYYY-MM-DD' or None) from a caption's "(Effective until June 30, 2029.)"."""
    m = re.search(r'\((Effective until|Effective|Expires|Contingent expiration date|Contingent effective date)[ ,.][^)]*\)', cap, re.I)
    if not m:
        return None, None
    kind = m.group(1).lower()
    d = re.search(r'(' + '|'.join(MON) + r') (\d{1,2}), (\d{4})', m.group(0).lower())
    day = '%s-%02d-%02d' % (d.group(3), MON.index(d.group(1)) + 1, int(d.group(2))) if d else None
    return {'effective until': 'until', 'effective': 'from', 'expires': 'expires',
            'contingent expiration date': 'until', 'contingent effective date': 'contingent'}[kind], day


def in_force(cap, day):
    k, d = status(cap)
    if k in ('until', 'expires'):
        return d is None or d > day
    if k == 'from':
        return d is not None and d <= day
    if k == 'contingent':
        return False
    return True


def sections(doc):
    """[(cite, caption, [paragraph, ...]), ...] in document order."""
    out = []
    cur = None          # [cite, caption_parts, paras, in_caption, closed]
    for x, kind, txt, bp in lines_of(doc):
        if kind == 'footer':
            continue
        t = txt.rstrip()
        if kind == 'small':
            # forms set in 10 pt inside a section: one line each, as in the section files
            if cur and not cur['closed'] and t.strip():
                cur['paras'].append(t.strip())
            continue
        if kind == 'bold' and x >= 80 and HEAD.match(norm(bp or t)):
            if cur:
                out.append(cur)
            m = HEAD.match(norm(bp))
            rest = t[len(bp):] if bp and t.startswith(bp) else ''
            cur = {'cite': m.group(1), 'cap': m.group(2), 'paras': [], 'incap': not rest.strip(), 'closed': False}
            if rest.strip():
                cur['paras'].append(rest.strip())
            continue
        if cur is None:
            continue
        if cur['incap'] and bp:
            # the caption wraps, in bold; "(Effective until <date>.)" or "(Expires <date>.)" may be set in bold italic
            cur['cap'] = join(cur['cap'], norm(bp))
            rest = t[len(bp):].strip() if t.startswith(bp) else ''
            if rest:
                cur['paras'].append(rest)
                cur['incap'] = False
            continue
        if kind in ('bold', 'bolditalic'):
            # chapter heading or note heading: the section's text is over
            cur['closed'] = True
            continue
        if cur['closed']:
            continue
        cur['incap'] = False
        if x >= 80 or not cur['paras']:
            cur['paras'].append(t.strip())
        else:
            cur['paras'][-1] = join(cur['paras'][-1], t.strip())
        if HIST.search(cur['paras'][-1]):
            cur['closed'] = True
    if cur:
        out.append(cur)
    res = []
    for c in out:
        ps = [norm(p) for p in c['paras']]
        if ps:
            ps[-1] = HIST.sub('', ps[-1]).strip()
        ps = [p for p in ps if p]
        res.append((c['cite'], norm(c['cap']), ps))
    return res
