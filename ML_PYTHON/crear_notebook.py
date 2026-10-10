"""Convierte el archivo percent-format en un Jupyter notebook estándar."""
import json
from pathlib import Path

source = Path(__file__).with_name('01_prototipo_analitica_adaptativa.py')
destination = source.with_suffix('.ipynb')
text = source.read_text(encoding='utf-8')
parts = text.split('# %%')
cells = []
for part in parts:
    if not part.strip():
        continue
    lines = part.lstrip('\n').splitlines()
    is_markdown = lines[0].strip() == '[markdown]'
    if is_markdown:
        lines = lines[1:]
        cleaned = []
        for line in lines:
            if line.startswith('# '):
                cleaned.append(line[2:])
            elif line == '#':
                cleaned.append('')
            else:
                cleaned.append(line)
        cells.append({'cell_type': 'markdown', 'metadata': {},
                      'source': '\n'.join(cleaned).strip() + '\n'})
    else:
        code = '\n'.join(lines).strip()
        if code:
            cells.append({'cell_type': 'code', 'execution_count': None,
                          'metadata': {}, 'outputs': [], 'source': code + '\n'})
notebook = {
    'cells': cells,
    'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python',
                                'name': 'python3'},
                 'language_info': {'name': 'python', 'version': '3.13'}},
    'nbformat': 4, 'nbformat_minor': 5
}
destination.write_text(json.dumps(notebook, ensure_ascii=False, indent=1),
                       encoding='utf-8')
print(f'Creado: {destination} ({len(cells)} celdas)')
