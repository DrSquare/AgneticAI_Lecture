"""Limited Markdown rendering for local notes, using only the standard library."""
from html import escape
import re
from urllib.parse import quote, unquote, urlsplit


def link_target(target, source, root):
    parsed = urlsplit(target.strip().strip('<>'))
    if parsed.scheme in ('https', 'http', 'mailto'):
        return target
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    candidate = (source.parent / unquote(parsed.path)).resolve()
    try:
        relative = candidate.relative_to(root.resolve())
    except ValueError:
        return None
    if candidate.suffix.lower() == '.pptx':
        candidate = candidate.with_suffix('.pdf')
        relative = candidate.relative_to(root.resolve())
    if not candidate.is_file():
        return None
    result = quote(relative.as_posix(), safe='/')
    return result + ('#' + quote(parsed.fragment, safe='=,&-') if parsed.fragment else '')


def inline(text, source, root):
    tokens = []

    def hold(value):
        tokens.append(value)
        return '\x00' + str(len(tokens) - 1) + '\x00'

    text = re.sub(r'`([^`]+)`', lambda m: hold('<code>' + escape(m[1]) + '</code>'), str(text))

    def link(match):
        label = escape(match[1])
        target = link_target(match[2], source, root)
        if target:
            return hold('<a href="' + escape(target, quote=True) + '" target="_blank" rel="noopener noreferrer">' + label + '</a>')
        return hold(label)

    text = re.sub(r'!?\[([^\]]+)\]\(([^\s)]+)\)', link, text)
    text = escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    # Expand twice to handle code spans used as a link label.
    for _ in range(2):
        text = re.sub(r'\x00(\d+)\x00', lambda m: tokens[int(m[1])], text)
    return text


def cells(line):
    return [x.strip() for x in re.split(r'(?<!\\)\|', line.strip().strip('|'))]


def markdown(text, source, root):
    lines, out, i = text.splitlines(), [], 0
    fmt = lambda s: inline(s, source, root)
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]); i += 1
            out.append('<pre><code>' + escape('\n'.join(code)) + '</code></pre>')
        elif match := re.match(r'^(#{1,6})\s+(.+)', line):
            level = min(6, len(match[1]) + 1)
            out.append(f'<h{level}>' + fmt(match[2]) + f'</h{level}>')
        elif re.fullmatch(r'[-*_]{3,}', line):
            out.append('<hr>')
        elif i + 1 < len(lines) and '|' in line and re.fullmatch(r'[\s|:\-]+', lines[i + 1]) and '-' in lines[i + 1]:
            out.append('<div class="table-scroll"><table><thead><tr>' + ''.join('<th scope="col">' + fmt(c) + '</th>' for c in cells(line)) + '</tr></thead><tbody>')
            i += 2
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                out.append('<tr>' + ''.join('<td>' + fmt(c) + '</td>' for c in cells(lines[i])) + '</tr>'); i += 1
            out.append('</tbody></table></div>')
            continue
        elif re.match(r'^([-*+] |\d+\. )', line):
            tag = 'ol' if re.match(r'^\d+\.', line) else 'ul'
            out.append('<' + tag + '>')
            while i < len(lines) and re.match(r'^(?:[-*+] |\d+\. )', lines[i].strip()):
                out.append('<li>' + fmt(re.sub(r'^(?:[-*+] |\d+\. )', '', lines[i].strip())) + '</li>'); i += 1
            out.append('</' + tag + '>')
            continue
        elif line.startswith('>'):
            group = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                group.append(lines[i].strip().lstrip('>').strip()); i += 1
            out.append('<blockquote>' + fmt(' '.join(group)) + '</blockquote>')
            continue
        else:
            group = [line]; i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|>|```|[-*+] |\d+\. |\|)', lines[i].strip()):
                group.append(lines[i].strip()); i += 1
            out.append('<p>' + fmt(' '.join(group)) + '</p>')
            continue
        i += 1
    return '\n'.join(out)


def walkthrough(text, source, root):
    match = re.search(r'## Five.minute walkthrough\s*\n(.*?)(?=\n## |\Z)', text, re.S | re.I)
    steps = []
    if match:
        for line in match[1].splitlines():
            row = cells(line)
            if len(row) >= 3 and re.match(r'^\d+:\d+', row[0]):
                steps.append({'time': row[0], 'action': inline(row[1], source, root), 'point': inline(row[2], source, root), 'label': re.sub(r'[`*]', '', row[1])})
    return steps


def reusable_prompt(text):
    match = re.search(r'## (?:Reusable(?: panel)? prompt|Prompt for a fresh run)\s*\n(.*?)(?=\n## |\Z)', text, re.S | re.I)
    return re.sub(r'^```[^\n]*\n?|^>\s?', '', match[1].strip(), flags=re.M).strip() if match else ''
