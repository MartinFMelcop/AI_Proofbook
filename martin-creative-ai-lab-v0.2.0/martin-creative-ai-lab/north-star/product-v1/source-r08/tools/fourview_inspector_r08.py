#!/usr/bin/env python3
"""R08 independent visual duplication/anchor preflight for *candidate* facade art.

It never grants aesthetic or copyright approval. It only detects some particularly
common bogus four-view deliveries (tints, mirrors, copies with changed metadata).
The source images are required; manifest filenames alone cannot certify anything.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from hashlib import sha256
from PIL import Image, ImageOps, ImageFilter
import numpy as np

from validate_facades_r07 import validate as validate_physical, TARGETS, ASSETS


_R = Image.Resampling.LANCZOS


def _d4(im: Image.Image):
    """The eight plane symmetries, only for detecting art reuse; never for rendering."""
    return [im.rotate(-90 * k, expand=True) for k in range(4)] + [
        ImageOps.mirror(im).rotate(-90 * k, expand=True) for k in range(4)
    ]


def _crop(im: Image.Image):
    im = im.convert('RGBA')
    bbox = im.getchannel('A').point(lambda x: 255 if x >= 20 else 0).getbbox()
    return im.crop(bbox) if bbox else im


def _luma(im: Image.Image):
    """Normalize geometry and shading so color swaps alone cannot masquerade as sides."""
    rgba = _crop(im)
    base = Image.new('RGBA', rgba.size, (95, 98, 101, 255))
    base.alpha_composite(rgba)
    gray = ImageOps.autocontrast(ImageOps.grayscale(base.convert('RGB')))
    gray = gray.resize((64, 64), resample=_R).filter(ImageFilter.GaussianBlur(.65))
    return np.asarray(gray, dtype=np.float32) / 255.0


def _edge(arr: np.ndarray):
    # Frequency/gradient features, invariant to global recoloring/brightness.
    gx = np.abs(np.diff(arr, axis=1, prepend=arr[:, :1]))
    gy = np.abs(np.diff(arr, axis=0, prepend=arr[:1, :]))
    return np.minimum(1, gx + gy)


def _corr(a: np.ndarray, b: np.ndarray):
    aa = a.reshape(-1) - float(a.mean())
    bb = b.reshape(-1) - float(b.mean())
    den = math.sqrt(float(np.dot(aa, aa)) * float(np.dot(bb, bb)))
    return float(np.dot(aa, bb) / den) if den > 1e-8 else (1.0 if np.array_equal(a, b) else 0.0)


def similarity_under_reflections(image_a: Image.Image, image_b: Image.Image):
    """Similarity to the best reflected/rotated *copy*; no images are generated."""
    aa = _luma(image_a)
    ae = _edge(aa)
    best = (-1.0, -1.0, 0)
    for k, candidate in enumerate(_d4(_crop(image_b))):
        bb = _luma(candidate)
        lum, edge = _corr(aa, bb), _corr(ae, _edge(bb))
        if (lum + edge) > (best[0] + best[1]):
            best = (round(lum, 4), round(edge, 4), k)
    return {'luma_similarity': best[0], 'edge_similarity': best[1], 'symmetry': best[2]}


def _anchors(im: Image.Image):
    a = np.asarray(im.convert('RGBA').getchannel('A'))
    points = np.argwhere(a > 18)
    if len(points) < 50:
        return None
    h, w = a.shape
    miny, maxy = float(points[:, 0].min()), float(points[:, 0].max())
    minx, maxx = float(points[:, 1].min()), float(points[:, 1].max())
    return {'bottom_y': maxy / h, 'center_x': (minx + maxx) / (2 * w),
            'footprint_w': (maxx - minx) / w, 'footprint_h': (maxy - miny) / h}


def inspect(manifest: dict, assets: Path = ASSETS):
    assets = Path(assets)
    # Structural checks reused only as a *preflight*, never as actual author ACK.
    preflight = validate_physical({**manifest, 'state': 'AUTHOR_ART_APPROVED'}, assets)
    issues = [x for x in preflight['errors'] if x != 'approval_not_granted']
    image_data = {}
    for building, prefix in TARGETS.items():
        entry = (manifest.get('buildings') or {}).get(building) or {}
        faces = entry.get('faces')
        if not isinstance(faces, list) or len(faces) != 4:
            continue
        sprites = []
        for name in faces:
            if not isinstance(name, str) or '/' in name or '\\' in name or '..' in name:
                sprites = []
                break
            fp = assets / (name + '.webp')
            if not fp.is_file():
                sprites = []
                break
            with Image.open(fp) as src:
                sprites.append(src.convert('RGBA'))
        if len(sprites) != 4:
            continue
        image_data[building] = {}
        for i, im in enumerate(sprites):
            image_data[building][str(i)] = {
                'sha256': sha256((assets / (faces[i] + '.webp')).read_bytes()).hexdigest(),
                'anchor': _anchors(im)
            }
        for i in range(4):
            for j in range(i + 1, 4):
                sim = similarity_under_reflections(sprites[i], sprites[j])
                # Intentional conservative rejection only for very strong indication
                # of one painting transformed into another, not for similar designs.
                if sim['luma_similarity'] >= .965 and sim['edge_similarity'] >= .91:
                    issues.append(f'{building}:{i}_{j}:suspected_recolored_or_rotated_copy')
        anchors = [x.get('anchor') for x in image_data[building].values()]
        if all(anchors):
            bottoms = [a['bottom_y'] for a in anchors]
            centers = [a['center_x'] for a in anchors]
            if max(bottoms) - min(bottoms) > .16:
                issues.append(f'{building}:ground_anchor_inconsistent')
            if max(centers) - min(centers) > .22:
                issues.append(f'{building}:horizontal_anchor_inconsistent')
    # Human-only checkpoints cannot be satisfied by script or by a forged JSON
    # state. Art and rights ultimately need external owner evidence.
    return {
        'schema': 'mmai.facade.r08.perceptual_preflight.v1',
        'status': 'READY_FOR_HUMAN_VISUAL_REVIEW_ONLY' if not issues and len(image_data) == 3 else 'BLOCKED',
        'technical_issues': sorted(set(issues)),
        'buildings_with_four_physical_faces': len(image_data),
        'rendering_approved': False,
        'author_art_approved': False,
        'rights_independently_verified': False,
        'methods_are_not_proof_of_artistic_quality': True,
        'anchor_and_similarity_receipts': image_data
    }


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / 'docs/R07_FACADE_ART_GATE.json').read_text())
    print(json.dumps(inspect(data, root / 'site/assets/world'), ensure_ascii=False, indent=2))
