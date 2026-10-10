import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece márgenes internos (padding) para celdas de tabla en dxa."""
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
    """Establece bordes específicos en una celda."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for border_name, border_style in borders.items():
        if border_style is not None:
            b_el = OxmlElement(f'w:{border_name}')
            b_el.set(qn('w:val'), border_style.get('val', 'single'))
            b_el.set(qn('w:sz'), str(border_style.get('sz', 4)))
            b_el.set(qn('w:space'), '0')
            b_el.set(qn('w:color'), border_style.get('color', '000000'))
            tcBorders.append(b_el)
        else:
            b_el = OxmlElement(f'w:{border_name}')
            b_el.set(qn('w:val'), 'none')
            tcBorders.append(b_el)
    tcPr.append(tcBorders)

def set_cell_shading(cell, color_hex):
    """Aplica sombreado de fondo a una celda."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def create_document():
    doc = Document()
    
    # 1. Configuración de Página APA 7: 2.54 cm en los 4 márgenes
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Encabezado estándar APA 7 (número de página en la esquina superior derecha)
        header = section.header
        header_p = header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        # En APA 7 para estudiantes el running head ya no es obligatorio, solo número de página
        hrun = header_p.add_run()
        hrun.font.name = 'Times New Roman'
        hrun.font.size = Pt(10)
        hrun.font.color.rgb = RGBColor(120, 120, 120)

    # 2. Configuración de Estilo Base Normal
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)
    
    return doc

def add_p_apa(doc, text="", bold_prefix=None, space_after=4, first_indent=True):
    """Párrafo de texto corrido APA 7 con sangría de primera línea."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if first_indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    else:
        p.paragraph_format.first_line_indent = Inches(0.0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        
    if text:
        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(12)
    return p

def add_h1(doc, text):
    """Encabezado Nivel 1 APA 7: Centrado, Negrita, Mayúsculas y Minúsculas."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Inches(0.0)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    return p

def add_h2(doc, text):
    """Encabezado Nivel 2 APA 7: Alineado a la izquierda, Negrita."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Inches(0.0)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def add_h3(doc, text):
    """Encabezado Nivel 3 APA 7: Alineado a la izquierda, Negrita, Cursiva."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.first_line_indent = Inches(0.0)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold = True
    run.italic = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def add_callout_quote(doc, text, source=""):
    """Cita en bloque o definición destacada estilo APA 7."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.right_indent = Inches(0.2)
    p.paragraph_format.first_line_indent = Inches(0.0)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    r = p.add_run(f'"{text}"')
    r.italic = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    
    if source:
        r2 = p.add_run(f" ({source})")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        r2.bold = True
    return p

def add_table_apa(doc, table_num, table_title, headers, rows, col_widths=None):
    """Inserta una tabla con estricto formato APA 7."""
    # Etiqueta de la tabla (Número en negrita)
    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(10)
    p_num.paragraph_format.space_after = Pt(1)
    p_num.paragraph_format.first_line_indent = Inches(0.0)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(f"Tabla {table_num}")
    r_num.bold = True
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(11)
    
    # Título descriptivo en cursiva
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(0)
    p_tit.paragraph_format.space_after = Pt(4)
    p_tit.paragraph_format.first_line_indent = Inches(0.0)
    p_tit.paragraph_format.keep_with_next = True
    r_tit = p_tit.add_run(table_title)
    r_tit.italic = True
    r_tit.font.name = 'Times New Roman'
    r_tit.font.size = Pt(11)
    
    # Creación de la tabla
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    border_top = {'val': 'single', 'sz': 10, 'color': '000000'}
    border_header_bottom = {'val': 'single', 'sz': 8, 'color': '000000'}
    border_table_bottom = {'val': 'single', 'sz': 10, 'color': '000000'}
    border_row_light = {'val': 'single', 'sz': 2, 'color': 'E2E8F0'}
    
    # Fila de Encabezados
    hdr_row = table.rows[0]
    hdr_row._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    for idx, header_text in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.text = header_text
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        set_cell_borders(cell, top=border_top, bottom=border_header_bottom)
        set_cell_shading(cell, 'F1F5F9')
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        for r in p.runs:
            r.bold = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(15, 23, 42)
            
    # Filas de Datos
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        is_last = (r_idx == len(rows) - 1)
        for c_idx, cell_value in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.text = str(cell_value)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            b_bottom = border_table_bottom if is_last else border_row_light
            set_cell_borders(cell, top=None, bottom=b_bottom)
            if r_idx % 2 == 1 and not is_last:
                set_cell_shading(cell, 'F8FAFC')
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
                
    # Anchos de columna si están especificados
    if col_widths and len(col_widths) == len(headers):
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(6)
    p_after.paragraph_format.first_line_indent = Inches(0.0)
    r_nota = p_after.add_run("Nota. Fuente: Elaboración propia basada en el diseño metodológico e institucional del proyecto.")
    r_nota.font.name = 'Times New Roman'
    r_nota.font.size = Pt(9)
    r_nota.italic = True
    r_nota.font.color.rgb = RGBColor(100, 116, 139)

def add_reference_apa(doc, ref_text):
    """Agrega una referencia bibliográfica con sangría francesa (hanging indent)."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(ref_text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    return p

print("Módulo de utilidades de documento APA 7 configurado.")
