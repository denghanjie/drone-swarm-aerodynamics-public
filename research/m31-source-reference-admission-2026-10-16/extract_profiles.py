"""Extract visible published graphical polylines; never raw experimental samples."""
import argparse
import hashlib
import json
from pathlib import Path
import pdfplumber

PDF_SHA = '81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c'
LEFT, WIDTH, BOTTOM, HEIGHT = 350.386, 198.42685, 326.591, 99.21342

def extract(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == PDF_SHA
    profiles = []
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[4]
        for index, name, rgb, mass, uh, count in [
            (32, 'Offboard 1', (.85, .325, .098), .572, 6.66, 41),
            (33, 'Offboard 2', (.929, .694, .125), 1.207, 9.66, 31),
        ]:
            curve = page.curves[index]
            assert curve['stroke'] and not curve['fill']
            assert tuple(curve['stroking_color']) == rgb
            assert abs(curve['linewidth'] - .79701) < 1e-9
            raw = curve['pts']
            assert len(raw) == count
            pts = [((x - LEFT) * 3 / WIDTH, (BOTTOM - y) * 1.5 / HEIGHT) for x, y in raw]
            assert abs(pts[0][0]) < 1e-10
            pts[0] = (0., pts[0][1])
            assert all(b[0] > a[0] for a, b in zip(pts, pts[1:]))
            visible = [{'r_over_l': x, 'speed_over_UH': y, 'kind': 'original graphical vertex'} for x, y in pts if 0 <= x <= 3]
            assert len(visible) == 16
            for a, b in zip(pts, pts[1:]):
                if a[0] < 3 < b[0]:
                    value = a[1] + (b[1] - a[1]) * (3 - a[0]) / (b[0] - a[0])
                    visible.append({'r_over_l': 3., 'speed_over_UH': value, 'kind': 'interpolated clip intersection; not a measured vertex'})
                    break
            assert visible[-1]['r_over_l'] == 3
            assert all(0 <= p['speed_over_UH'] <= 1.5 for p in visible)
            profiles.append({'name': name, 'curve_index': index, 'rgb': rgb, 'stroke_width_pt': curve['linewidth'],
                'mass_kg': mass, 'motor_distance_m': .266, 'propeller_diameter_m': .1295, 'tabulated_UH_mps': uh,
                'full_path_vertices': count, 'full_path_sha256': hashlib.sha256(json.dumps(raw, separators=(',', ':')).encode()).hexdigest(),
                'visible_original_vertices': 16, 'knots': visible})
    return {'schema': 'published-profile-extraction-v1', 'source': 'https://arxiv.org/pdf/2403.13321v3', 'source_sha256': PDF_SHA,
        'parser': {'name': 'pdfplumber', 'version': pdfplumber.__version__}, 'page': 5, 'figure': 7,
        'axes': {'left_pt': LEFT, 'width_pt': WIDTH, 'bottom_top_origin_pt': BOTTOM, 'height_pt': HEIGHT,
                 'x': 'r/l', 'y': 'speed magnitude / calculated hover induced speed UH', 'downstream_s_over_l': 3.,
                 'x_domain': [0., 3.], 'y_domain': [0., 1.5]},
        'semantics': 'Displayed binned median polylines; not raw observations, not mean axial velocity. Black fitted curve and dispersion bands excluded.',
        'profiles': profiles}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(extract(args.pdf), indent=2) + '\n')
