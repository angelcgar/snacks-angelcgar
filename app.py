#!/usr/bin/env python3

from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf(toc_level=2, optimize=True)

text = """# Test

## subtitulo

### subtitulo

#### subtitulo

Esto es un texto

**negritas**

_italica_

[link](https://google.com)
"""

pdf.add_section(Section(text, paper_size="A4-L"), user_css="h1 {text-align:center}")

# pdf.meta["title"] = "User Guide"
# pdf.meta["author"] = "Vitaly Bogomolov"

pdf.save("guide1.pdf")
