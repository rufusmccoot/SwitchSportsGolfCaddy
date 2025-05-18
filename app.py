from flask import Flask, render_template
import os
import yaml

app = Flask(__name__)

# Define the 18 holes with their image paths and labels
holes = [
    # Resort 1-9 (holes 1-9)
    {'id': i+1, 'img': f'holes/R{i+1}.png', 'label': f'Resort {i+1}'} for i in range(9)
] + [
    # Classic 10-18 (holes 10-18)
    {'id': i+10, 'img': f'holes/C{i+10}.png', 'label': f'Classic {i+10}'} for i in range(9)
]

# Note file mapping: {hole_id: note_file}
hole_code_map = {}
for h in holes:
    if h['label'].startswith('Resort'):
        num = int(h['label'].split()[-1])
        hole_code_map[h['id']] = f'R{num}'
    elif h['label'].startswith('Classic'):
        num = int(h['label'].split()[-1])
        hole_code_map[h['id']] = f'C{num}'

# Load all hole notes from YAML
NOTES_PATH = os.path.join(app.static_folder, 'notes', 'all_holes.yaml')
if os.path.exists(NOTES_PATH):
    with open(NOTES_PATH, 'r', encoding='utf-8') as f:
        all_notes = yaml.safe_load(f)
else:
    all_notes = {'holes': {}}

@app.route('/')
def index():
    return render_template('index.html', holes=holes)

@app.route('/hole/<int:hole_number>')
def hole_detail(hole_number):
    hole = next((h for h in holes if h['id'] == hole_number), None)
    if not hole:
        return 'Hole not found', 404
    hole_code = hole_code_map.get(hole_number)
    sections = []
    if hole_code and all_notes and 'holes' in all_notes and hole_code in all_notes['holes']:
        sections = all_notes['holes'][hole_code].get('sections', [])
    return render_template('hole.html', hole=hole, sections=sections)

if __name__ == '__main__':
    app.run(port=8585, debug=True, host='0.0.0.0')
