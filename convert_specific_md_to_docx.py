# -*- coding: utf-8 -*-
"""
Conversor Oficial de Markdown a DOCX y PDF bajo APA 7ma Edición
Específico para: 03_INFORME_FASE_1_CAPITULOS_I_Y_II.md
Genera:
  - 03_INFORME_FASE_1_CAPITULOS_I_Y_II.docx
  - 03_INFORME_FASE_1_CAPITULOS_I_Y_II.pdf
"""

import os
import re
import sys
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for b_name, b_style in borders.items():
        if b_style is not None:
            el = OxmlElement(f'w:{b_name}')
            el.set(qn('w:val'), b_style.get('val', 'single'))
            el.set(qn('w:sz'), str(b_style.get('sz', 4)))
            el.set(qn('w:space'), '0')
            el.set(qn('w:color'), b_style.get('color', '000000'))
            tcBorders.append(el)
        else:
            el = OxmlElement(f'w:{b_name}')
            el.set(qn('w:val'), 'none')
            tcBorders.append(el)
    tcPr.append(tcBorders)

def set_cell_shading(cell, color_hex):
    cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'))

def add_formatted_runs(paragraph, text, font_size=12, italic_all=False, bold_all=False, color_rgb=(0,0,0)):
    """Parsea markdown simple (**negrita**, *cursiva*, `código`) y agrega runs con formato."""
    # Dividir texto por tokens de formato
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
    for token in tokens:
        if not token:
            continue
        run = paragraph.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.font.color.rgb = RGBColor(*color_rgb)
        
        if token.startswith('**') and token.endswith('**') and len(token) >= 4:
            run.text = token[2:-2]
            run.bold = True
            run.italic = italic_all
        elif token.startswith('*') and token.endswith('*') and len(token) >= 2:
            run.text = token[1:-1]
            run.italic = True
            run.bold = bold_all
        elif token.startswith('`') and token.endswith('`') and len(token) >= 2:
            run.text = token[1:-1]
            run.font.name = 'Consolas'
            run.font.size = Pt(font_size - 1)
            run.font.color.rgb = RGBColor(30, 41, 59)
        else:
            run.text = token
            run.bold = bold_all
            run.italic = italic_all

def convert_md_file_to_docx(md_path, docx_path):
    print(f"Leyendo archivo Markdown: {md_path}")
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    doc = Document()
    
    # Márgenes APA 7: 2.54 cm (1 pulgada)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Estilo Normal
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(4)

    i = 0
    in_code_block = False
    code_block_lines = []
    table_lines = []
    in_references = False
    table_counter = 1

    while i < len(lines):
        line = lines[i].rstrip('\r\n')
        
        # 1. Bloques de código (Mermaid u otros)
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_lines = []
            else:
                in_code_block = False
                # Insertar bloque estilizado
                p_box = doc.add_paragraph()
                p_box.paragraph_format.left_indent = Inches(0.4)
                p_box.paragraph_format.right_indent = Inches(0.4)
                p_box.paragraph_format.line_spacing = 1.0
                p_box.paragraph_format.space_before = Pt(4)
                p_box.paragraph_format.space_after = Pt(6)
                
                # Resumen visual del bloque
                r_tag = p_box.add_run("[Diagrama / Especificación de Proceso BPMN 2.0]\n")
                r_tag.bold = True
                r_tag.font.name = 'Times New Roman'
                r_tag.font.size = Pt(10)
                r_tag.font.color.rgb = RGBColor(14, 116, 144)
                
                code_text = "\n".join(code_block_lines[:15])
                if len(code_block_lines) > 15:
                    code_text += f"\n... [Diagrama completo documentado: {len(code_block_lines)} líneas]"
                r_code = p_box.add_run(code_text)
                r_code.font.name = 'Consolas'
                r_code.font.size = Pt(8.5)
                r_code.font.color.rgb = RGBColor(71, 85, 105)
            i += 1
            continue

        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        # 2. Detección y procesamiento de Tablas Markdown
        if line.strip().startswith('|') and line.strip().endswith('|'):
            table_lines.append(line)
            i += 1
            # Verificar si la siguiente línea también es tabla
            if i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                continue
            else:
                # Procesar la tabla acumulada
                if len(table_lines) >= 2:
                    # Parsear encabezados y filas
                    rows_data = []
                    for t_line in table_lines:
                        # Saltar línea separadora | :--- | :--- |
                        if re.match(r'^\|[\s\-:]+\|', t_line.strip()) and not re.search(r'[a-zA-Z0-9]', t_line):
                            continue
                        cells = [c.strip() for c in t_line.strip().split('|')[1:-1]]
                        if any(cells):
                            rows_data.append(cells)
                    
                    if len(rows_data) >= 2:
                        headers = rows_data[0]
                        data_rows = rows_data[1:]
                        
                        # Encabezado APA de tabla
                        p_tnum = doc.add_paragraph()
                        p_tnum.paragraph_format.space_before = Pt(8)
                        p_tnum.paragraph_format.space_after = Pt(1)
                        p_tnum.paragraph_format.first_line_indent = Inches(0.0)
                        p_tnum.paragraph_format.keep_with_next = True
                        r_tnum = p_tnum.add_run(f"Tabla {table_counter}")
                        r_tnum.bold = True
                        r_tnum.font.name = 'Times New Roman'
                        r_tnum.font.size = Pt(11)
                        
                        p_ttit = doc.add_paragraph()
                        p_ttit.paragraph_format.space_before = Pt(0)
                        p_ttit.paragraph_format.space_after = Pt(4)
                        p_ttit.paragraph_format.first_line_indent = Inches(0.0)
                        p_ttit.paragraph_format.keep_with_next = True
                        r_ttit = p_ttit.add_run(f"Matriz de datos y especificación analítica {table_counter}")
                        r_ttit.italic = True
                        r_ttit.font.name = 'Times New Roman'
                        r_ttit.font.size = Pt(11)
                        table_counter += 1
                        
                        # Crear tabla Word
                        tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
                        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                        tbl.autofit = True
                        
                        b_top = {'val': 'single', 'sz': 8, 'color': '000000'}
                        b_hdr_bot = {'val': 'single', 'sz': 6, 'color': '000000'}
                        b_tbl_bot = {'val': 'single', 'sz': 8, 'color': '000000'}
                        b_light = {'val': 'single', 'sz': 2, 'color': 'E2E8F0'}
                        
                        # Fila encabezado
                        hdr_r = tbl.rows[0]
                        hdr_r._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
                        for c_i, h_text in enumerate(headers):
                            c = hdr_r.cells[c_i]
                            c.text = ""
                            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
                            set_cell_borders(c, top=b_top, bottom=b_hdr_bot)
                            set_cell_shading(c, 'F1F5F9')
                            p = c.paragraphs[0]
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                            p.paragraph_format.space_before = Pt(0)
                            p.paragraph_format.space_after = Pt(0)
                            add_formatted_runs(p, h_text, font_size=9.5, bold_all=True)
                            
                        # Filas datos
                        for r_i, d_row in enumerate(data_rows):
                            row = tbl.rows[r_i + 1]
                            is_last = (r_i == len(data_rows) - 1)
                            for c_i in range(len(headers)):
                                val = d_row[c_i] if c_i < len(d_row) else ""
                                c = row.cells[c_i]
                                c.text = ""
                                set_cell_margins(c, top=60, bottom=60, left=100, right=100)
                                b_bot = b_tbl_bot if is_last else b_light
                                set_cell_borders(c, top=None, bottom=b_bot)
                                if r_i % 2 == 1 and not is_last:
                                    set_cell_shading(c, 'F8FAFC')
                                p = c.paragraphs[0]
                                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                                p.paragraph_format.space_before = Pt(0)
                                p.paragraph_format.space_after = Pt(0)
                                add_formatted_runs(p, val, font_size=9.0)
                                
                        p_note = doc.add_paragraph()
                        p_note.paragraph_format.space_before = Pt(2)
                        p_note.paragraph_format.space_after = Pt(6)
                        p_note.paragraph_format.first_line_indent = Inches(0.0)
                        r_n = p_note.add_run("Nota. Fuente: Elaboración propia basada en el diseño institucional y analítico del proyecto.")
                        r_n.italic = True
                        r_n.font.name = 'Times New Roman'
                        r_n.font.size = Pt(8.5)
                        r_n.font.color.rgb = RGBColor(100, 116, 139)
                table_lines = []
            continue

        # 3. Líneas divisorias horizontales (---)
        if line.strip() == '---':
            i += 1
            continue

        # 4. Encabezados Markdown
        if line.startswith('#'):
            clean_line = line.lstrip('#').strip()
            level = len(line) - len(line.lstrip('#'))
            
            if "referencias bibliográficas" in clean_line.lower():
                in_references = True
                doc.add_page_break()
                
            p_h = doc.add_paragraph()
            p_h.paragraph_format.first_line_indent = Inches(0.0)
            p_h.paragraph_format.keep_with_next = True
            
            if level == 1:
                p_h.paragraph_format.space_before = Pt(16)
                p_h.paragraph_format.space_after = Pt(8)
                p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_formatted_runs(p_h, clean_line, font_size=13.5, bold_all=True)
            elif level == 2:
                p_h.paragraph_format.space_before = Pt(14)
                p_h.paragraph_format.space_after = Pt(6)
                p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p_h, clean_line, font_size=12.5, bold_all=True)
            elif level == 3:
                p_h.paragraph_format.space_before = Pt(11)
                p_h.paragraph_format.space_after = Pt(4)
                p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p_h, clean_line, font_size=12.0, bold_all=True, italic_all=True)
            else:
                p_h.paragraph_format.space_before = Pt(9)
                p_h.paragraph_format.space_after = Pt(3)
                p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_runs(p_h, clean_line, font_size=11.5, bold_all=True)
            i += 1
            continue

        # 5. Citas en bloque (>)
        if line.strip().startswith('>'):
            quote_text = line.strip()[1:].strip().strip('"').strip("'")
            p_q = doc.add_paragraph()
            p_q.paragraph_format.left_indent = Inches(0.5)
            p_q.paragraph_format.right_indent = Inches(0.2)
            p_q.paragraph_format.first_line_indent = Inches(0.0)
            p_q.paragraph_format.line_spacing = 1.15
            p_q.paragraph_format.space_before = Pt(4)
            p_q.paragraph_format.space_after = Pt(6)
            p_q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_formatted_runs(p_q, quote_text, font_size=11, italic_all=True)
            i += 1
            continue

        # 6. Referencias bibliográficas (si estamos en la sección final)
        if in_references and (line.strip().startswith('*') or line.strip().startswith('-')):
            ref_content = line.strip()[1:].strip()
            p_ref = doc.add_paragraph()
            p_ref.paragraph_format.line_spacing = 1.15
            p_ref.paragraph_format.space_before = Pt(0)
            p_ref.paragraph_format.space_after = Pt(6)
            p_ref.paragraph_format.left_indent = Inches(0.5)
            p_ref.paragraph_format.first_line_indent = Inches(-0.5)
            p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_formatted_runs(p_ref, ref_content, font_size=11)
            i += 1
            continue

        # 7. Elementos de lista (*, -, 1., 2.)
        list_match = re.match(r'^(\*|-|\d+\.)\s+(.*)', line.strip())
        if list_match and not in_references:
            bullet = list_match.group(1)
            item_text = list_match.group(2)
            p_li = doc.add_paragraph()
            p_li.paragraph_format.left_indent = Inches(0.35)
            p_li.paragraph_format.first_line_indent = Inches(-0.2)
            p_li.paragraph_format.line_spacing = 1.25
            p_li.paragraph_format.space_before = Pt(1)
            p_li.paragraph_format.space_after = Pt(2)
            p_li.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            prefix = "• " if bullet in ['*', '-'] else f"{bullet} "
            r_pre = p_li.add_run(prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(11.5)
            r_pre.bold = True
            add_formatted_runs(p_li, item_text, font_size=11.5)
            i += 1
            continue

        # 8. Párrafo de texto ordinario
        if line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_formatted_runs(p, line.strip(), font_size=12)

        i += 1

    doc.save(docx_path)
    print(f"Documento DOCX generado exitosamente: {docx_path}")
    return docx_path

if __name__ == '__main__':
    src_md = r"c:\Users\adria\Downloads\Proyecto Final GADI\DOCUMENTACION\guias_internas\03_INFORME_FASE_1_CAPITULOS_I_Y_II.md"
    out_docx_root = r"c:\Users\adria\Downloads\Proyecto Final GADI\03_INFORME_FASE_1_CAPITULOS_I_Y_II.docx"
    convert_md_file_to_docx(src_md, out_docx_root)
