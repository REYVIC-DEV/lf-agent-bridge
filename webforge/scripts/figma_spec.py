#!/usr/bin/env python3
"""Flatten a figwright `get_node` dump into a layout+type spec.

figwright returns the full node tree; this reduces it to the handful of
properties that actually map onto Tailwind (see .claude/rules/figma-to-tailwind.md)
so a build can be driven off measured values instead of a screenshot.

  python3 webforge/scripts/figma_spec.py <get_node-dump.json> [--out spec.json]
"""
import json, sys, argparse


def dget(v, k, default=None):
    """figwright returns the string "MIXED" where a node has mixed values."""
    if isinstance(v, dict):
        return v.get(k, default)
    return 'MIXED' if isinstance(v, str) else default


def solid(fills):
    for f in fills or []:
        if isinstance(f, dict) and f.get('type') == 'SOLID' and f.get('visible', True):
            c = f['color']
            hexv = '#%02x%02x%02x' % tuple(round(c[k] * 255) for k in 'rgb')
            return hexv if f.get('opacity', 1) == 1 else '%s@%.2f' % (hexv, f['opacity'])
    return None


def spec(n, depth=0, out=None):
    if out is None:
        out = []
    if not isinstance(n, dict):
        return out
    lay = n.get('layout') or {}
    row = {
        'depth': depth, 'id': n.get('id'), 'name': n.get('name'), 'type': n.get('type'),
        'w': round(n.get('width', 0)), 'h': round(n.get('height', 0)),
    }
    if lay.get('mode') and lay['mode'] != 'NONE':
        pad = [lay.get('padding' + s, 0) for s in ('Top', 'Right', 'Bottom', 'Left')]
        row['layout'] = {
            'dir': lay['mode'], 'gap': lay.get('itemSpacing'),
            'pad': pad if len(set(pad)) > 1 else pad[0],
            'justify': lay.get('primaryAxisAlignItems'),
            'align': lay.get('counterAxisAlignItems'),
            'wrap': lay.get('layoutWrap'),
        }
    for k, short in (('layoutSizingHorizontal', 'sizeH'), ('layoutSizingVertical', 'sizeV')):
        if n.get(k):
            row[short] = n[k]
    if n.get('cornerRadius'):
        row['radius'] = n['cornerRadius']
    if solid(n.get('fills')):
        row['fill'] = solid(n['fills'])
    if n.get('strokes'):
        row['stroke'] = {'color': solid(n['strokes']), 'weight': n.get('strokeWeight'),
                         'align': n.get('strokeAlign')}
    if n.get('effects'):
        row['effects'] = [{'type': e.get('type'), 'radius': e.get('radius'),
                           'offset': e.get('offset'), 'color': (
                               '#%02x%02x%02x@%.2f' % (
                                   round(e['color']['r'] * 255), round(e['color']['g'] * 255),
                                   round(e['color']['b'] * 255), e['color'].get('a', 1))
                               if e.get('color') else None)}
                          for e in n['effects'] if isinstance(e, dict) and e.get('visible', True)]
        if not row['effects']:
            del row['effects']
    if n.get('type') == 'TEXT':
        row['text'] = {
            'chars': n.get('characters'), 'size': n.get('fontSize'),
            'family': dget(n.get('fontName'), 'family'),
            'style': dget(n.get('fontName'), 'style'),
            'lh': dget(n.get('lineHeight'), 'value'),
            'lhUnit': dget(n.get('lineHeight'), 'unit'),
            'ls': dget(n.get('letterSpacing'), 'value', 0),
            'align': n.get('textAlignHorizontal'), 'case': n.get('textCase'),
            'decoration': n.get('textDecoration'), 'color': solid(n.get('fills')),
        }
    out.append(row)
    for c in (n.get('children') or []):
        spec(c, depth + 1, out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dump')
    ap.add_argument('--out')
    ap.add_argument('--max-depth', type=int, default=99)
    a = ap.parse_args()
    raw = json.load(open(a.dump))
    node = raw.get('node', raw)
    rows = [r for r in spec(node) if r['depth'] <= a.max_depth]
    if a.out:
        json.dump({'frame': node.get('id'), 'name': node.get('name'),
                   'width': round(node.get('width', 0)), 'height': round(node.get('height', 0)),
                   'nodes': rows}, open(a.out, 'w'), indent=1, ensure_ascii=False)
        print('wrote %s  (%d nodes)' % (a.out, len(rows)))
    else:
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))


if __name__ == '__main__':
    main()
