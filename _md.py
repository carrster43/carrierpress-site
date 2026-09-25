"""Tiny Markdown subset, enough for author blog posts, no dependencies.

Deliberately small. It supports what a prose post actually needs and nothing
more: headings, paragraphs, bold, italic, links, unordered and ordered lists,
blockquotes, horizontal rules and inline code. Anything it does not recognise
is emitted as an escaped paragraph rather than passed through as raw HTML, so a
post file can never inject markup into the page.
"""
import html, re

def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    # External links open in a new tab. Site-relative ones must NOT: sending a
    # reader to another page of the same site in a new tab is hostile, and it
    # breaks the back button that a journal post reading "start with this one"
    # depends on.
    t = re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    # ⛔ THE SCHEME IS NOT OPEN. Only a path or a fragment, so a post file can
    # never emit javascript: or data: through this. That is the same reason the
    # external branch above is anchored to https?:// rather than to anything
    # that looks like a URL.
    #
    # WHY THIS WAS ADDED. Until it existed a post could not link to this site at
    # all: `[The Willows](/#b-B0HGTD7VBZ)` rendered as literal square brackets on
    # the page. The journal named twelve catalogue titles across four posts and
    # linked none of them, and it was tempting to read that as an oversight by
    # whoever wrote the posts. It was not. The renderer made it impossible.
    t = re.sub(r'\[([^\]]+)\]\((/[^\s)]*|#[^\s)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<em>\1</em>', t)
    return t

def render(md):
    out, i, lines = [], 0, md.replace('\r\n', '\n').split('\n')
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if re.match(r'^(-{3,}|\*{3,})\s*$', ln):
            out.append('<hr class="rule">'); i += 1; continue
        h = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if h:
            lvl = len(h.group(1)) + 1          # h1 is the post title, body starts at h2
            out.append(f'<h{lvl}>{_inline(h.group(2).strip())}</h{lvl}>'); i += 1; continue
        if ln.lstrip().startswith('> '):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith('> '):
                buf.append(lines[i].lstrip()[2:]); i += 1
            out.append('<blockquote><p>' + _inline(' '.join(buf)) + '</p></blockquote>'); continue
        if re.match(r'^\s*[-*]\s+', ln):
            buf = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                buf.append(re.sub(r'^\s*[-*]\s+', '', lines[i])); i += 1
            out.append('<ul>' + ''.join(f'<li>{_inline(b)}</li>' for b in buf) + '</ul>'); continue
        if re.match(r'^\s*\d+\.\s+', ln):
            buf = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                buf.append(re.sub(r'^\s*\d+\.\s+', '', lines[i])); i += 1
            out.append('<ol>' + ''.join(f'<li>{_inline(b)}</li>' for b in buf) + '</ol>'); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|>\s|\s*[-*]\s|\s*\d+\.\s|-{3,}|\*{3,})', lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append('<p>' + _inline(' '.join(buf)) + '</p>')
    return '\n'.join(out)

def front_matter(text):
    """Parse a leading --- block of key: value pairs. Returns (meta, body)."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[3:end].strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, text[end + 4:].lstrip('\n')
