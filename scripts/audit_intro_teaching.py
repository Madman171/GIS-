"""Independent exact-arithmetic and exhaustive-path checks for authored examples.

The data below are transcribed from the teaching cases, not parsed from an answer
or produced by the teaching renderer. Fractions avoid rounding hiding an error.
"""
from fractions import Fraction as F
import argparse
import heapq
import json
from pathlib import Path


def paths(edges, start='S', target='T', visited=()):
    if start == target:
        return [([start], F(0))]
    found = []
    for a, b, cost in edges:
        if a == start and b not in visited + (start,):
            for tail, total in paths(edges, b, target, visited + (start,)):
                found.append(([start] + tail, F(cost) + total))
    return found


def settle(edges):
    distance = {'S': F(0)}
    done = []
    queue = [(F(0), 'S')]
    while queue:
        cost, node = heapq.heappop(queue)
        if node in done:
            continue
        done.append(node)
        for a, b, weight in edges:
            if a == node and cost + weight < distance.get(b, float('inf')):
                distance[b] = cost + weight
                heapq.heappush(queue, (distance[b], b))
    return done, distance


def audit():
    checks = []

    def equal(name, actual, expected):
        assert actual == expected, (name, actual, expected)
        checks.append({'case': name, 'result': str(actual), 'status': 'pass'})

    equal('T02 main squared length, m2', 300**2 + 400**2, 500**2)
    equal('T02 self-check squared length, m2', (610-10)**2 + (820-20)**2, 1000**2)
    equal('T02 self-check total, km', F(1000, 1000) + F('0.5'), F('1.5'))
    base = [('S', 'A', 3), ('A', 'T', 3), ('S', 'B', 2), ('B', 'T', 5)]
    equal('T07/T09 enumerate every candidate', paths(base), [(['S','A','T'], F(6)), (['S','B','T'], F(7))])
    equal('T07 mixed units, km', F(600,1000) + F('0.9') + F(500,1000), F(2))
    equal('T07 self-check, km', F('0.7') + F(800,1000), F('1.5'))
    equal('T07 self-check preferred distance', F('1.5') < F('1.6'), True)
    equal('T08 main travel, min', F('1.8') / 36 * 60, F(3))
    equal('T08 main with one wait, min', F(3) + F('0.4'), F('3.4'))
    equal('T08 two equal-length segments, min', F(1,20)*60 + F(1,40)*60, F('4.5'))
    equal('T08 incorrect arithmetic-mean shortcut, min', F(2,30)*60, F(4))
    equal('T08 route via A, min', F(6,30)*60, F(12))
    equal('T08 route via B, min', F(7,70)*60, F(6))
    equal('T08 self-check single, min', F(2,30)*60, F(4))
    equal('T08 self-check multi-segment with wait, min', F('0.6')/18*60 + F('1.4')/42*60 + F('0.8'), F('4.8'))
    order, distances = settle(base)
    equal('T09 independent priority-queue settlement order', order, ['S','B','A','T'])
    equal('T09 independently settled terminal cost', distances['T'], F(6))
    equal('T09 relaxation improvement', min(8,4+2), 6)
    equal('T09 relaxation retaining old cost', min(8,4+7), 8)
    equal('T09 self-check 2 all paths', paths([('S','A',2),('A','T',3),('S','B',1),('B','T',6)]), [(['S','A','T'],F(5)),(['S','B','T'],F(7))])
    equal('T09 self-check 3 all equal optima', paths([('S','A',2),('A','T',3),('S','B',3),('B','T',2)]), [(['S','A','T'],F(5)),(['S','B','T'],F(5))])
    equal('T10 teaching height boundary', [F(h) <= F('2.6') for h in ['2.5','2.6','2.7']], [True,True,False])
    equal('T10 main off-peak/peak choices', [min({'A':4,'B':6},key={'A':4,'B':6}.get),min({'A':9,'B':7},key={'A':9,'B':7}.get)], ['A','B'])
    equal('T10 self-check off-peak/peak choices', [3 < 5, 10 > 6], [True,True])
    closures = [('S','A',1),('S','B',4),('B','T',2)]
    equal('T10 closed A-T, enumerate remaining paths', paths(closures), [(['S','B','T'], F(6))])
    equal('T10 both terminal edges closed, no invented route', paths(closures[:-1]), [])
    equal('T05 directed cycle allows detour only', paths([('P','Q',1),('Q','R',1),('R','P',1)], 'Q', 'P'), [(['Q','R','P'], F(2))])
    equal('T05 self-check deleted final edge', paths([('X','Y',1),('Y','Z',1)], 'Y', 'X'), [])
    equal('T04 correctly built ramp route', paths([('A','B',1),('B','R',1),('R','D',1),('D','C',1)], 'A','C'), [(['A','B','R','D','C'], F(4))])
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    checks = audit()
    if args.output:
        dest = Path(args.output)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps({'method': 'exact Fraction arithmetic; exhaustive simple paths; independent heap-based settlement', 'checks': checks}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS: {} independent arithmetic, boundary and path checks.'.format(len(checks)))
