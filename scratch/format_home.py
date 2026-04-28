"""
Cleans and properly indents templates/core/home.html.
- Uses a simple indent-tracking approach (no external parser needed for script blocks).
- Django template tags ({% ... %}, {{ ... }}) are preserved verbatim.
- <script> and <style> block contents are preserved verbatim (no re-indentation inside them).
"""
import re

INPUT  = "templates/core/home.html"
OUTPUT = "templates/core/home.html"
INDENT = "    "  # 4 spaces

# Tags that should NOT increase indent for their children
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "param", "source", "track", "wbr"
}

# Tags whose inner content we do NOT re-indent (preserve as-is)
RAW_TAGS = {"script", "style"}

def get_tag_name(tag_str):
    """Extract lowercase tag name from an opening/closing tag string."""
    m = re.match(r'</?([a-zA-Z][a-zA-Z0-9\-]*)', tag_str)
    return m.group(1).lower() if m else None

def is_open_tag(s):
    return bool(re.match(r'<[a-zA-Z][^/][^>]*[^/]>|<[a-zA-Z]>', s.strip()))

def is_close_tag(s):
    return bool(re.match(r'</[a-zA-Z]', s.strip()))

def is_self_closing(s):
    return s.strip().endswith('/>') or get_tag_name(s) in VOID_TAGS

with open(INPUT, "r", encoding="utf-8") as f:
    raw = f.read()

# Normalize line endings and strip trailing whitespace per line
lines = [l.rstrip() for l in raw.replace('\r\n', '\n').splitlines()]

output_lines = []
depth = 0
in_raw_block = False   # inside <script> or <style>
raw_block_tag = None

for line in lines:
    stripped = line.strip()

    # Empty lines: keep one blank line for readability, skip extras
    if not stripped:
        if output_lines and output_lines[-1] != "":
            output_lines.append("")
        continue

    # ── Handle raw blocks (script / style) ──────────────────────────────
    if in_raw_block:
        # Check if this line closes the raw block
        close_match = re.search(r'</' + raw_block_tag + r'\s*>', stripped, re.IGNORECASE)
        if close_match:
            in_raw_block = False
            raw_block_tag = None
            depth -= 1
            output_lines.append(INDENT * depth + stripped)
        else:
            # Preserve raw content with current depth + 1
            output_lines.append(INDENT * (depth) + stripped)
        continue

    # Check if entering a raw block
    raw_open = re.match(r'<(script|style)[\s>]', stripped, re.IGNORECASE)
    if raw_open:
        tag = raw_open.group(1).lower()
        output_lines.append(INDENT * depth + stripped)
        # If the opening tag itself closes on the same line (e.g. <script></script>), skip
        if re.search(r'</' + tag + r'\s*>', stripped, re.IGNORECASE):
            pass  # inline, don't enter raw mode
        else:
            depth += 1
            in_raw_block = True
            raw_block_tag = tag
        continue

    # ── Django template tags: treat as inline, no indent change ─────────
    if stripped.startswith('{%') or stripped.startswith('{{'):
        output_lines.append(INDENT * depth + stripped)
        continue

    # ── HTML comment ─────────────────────────────────────────────────────
    if stripped.startswith('<!--'):
        output_lines.append(INDENT * depth + stripped)
        continue

    # ── Closing tag ──────────────────────────────────────────────────────
    if stripped.startswith('</'):
        tag = get_tag_name(stripped)
        if tag and tag not in VOID_TAGS:
            depth = max(0, depth - 1)
        output_lines.append(INDENT * depth + stripped)
        continue

    # ── Opening tag (possibly with content on same line) ─────────────────
    # Find all tags on this line
    # For simplicity, write the line at current depth, then adjust depth
    output_lines.append(INDENT * depth + stripped)

    # Count opens and closes on this line to adjust depth
    open_tags  = re.findall(r'<([a-zA-Z][a-zA-Z0-9\-]*)(?:\s[^>]*)?>(?!.*</\1)', stripped)
    close_tags = re.findall(r'</([a-zA-Z][a-zA-Z0-9\-]*)>', stripped)
    self_close = re.findall(r'<[a-zA-Z][^>]*/>', stripped)

    net = 0
    for t in open_tags:
        tl = t.lower()
        if tl not in VOID_TAGS:
            # Check it's not immediately closed on the same line
            if not re.search(r'<' + t + r'[^>]*>.*</' + t + r'>', stripped):
                net += 1
    for t in close_tags:
        tl = t.lower()
        if tl not in VOID_TAGS:
            net -= 1

    depth = max(0, depth + net)

# Write output
result = "\n".join(output_lines).strip() + "\n"

with open(OUTPUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(result)

print(f"Done! Wrote {len(result.splitlines())} lines to {OUTPUT}")
