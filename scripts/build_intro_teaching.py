"""Build the reviewed static teaching registry; never change the question bank."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT/'docs/teaching/intro'
DEST = ROOT/'frontend/src/teaching/content.json'
SPECS = [
    ('T01','简明讲解','4–6分钟',['M1-001','M1-002','M1-004','M1-009','M7-010'],['S01','S02','S03','S04','S09','S13']),
    ('T02','重点详讲','8–12分钟',['M3-017','M3-018','M7-010'],['S05','S06','S07','S08','S24','S25','S26']),
    ('T03','重点详讲','6–10分钟',['M1-007','M1-008','M1-009'],['S04','S10','S11','S14','S20']),
    ('T04','重点详讲','8–12分钟',['M1-013','M1-015'],['S10','S11','TEACH-TURNS','TEACH-TOPOLOGY']),
    ('T05','简明讲解','3–5分钟',['M1-011','M1-016','M1-029'],['S13','S15','S20']),
    ('T06','简明讲解','3–5分钟',['M1-014'],['S11','S12','S28']),
    ('T07','简明讲解','4–6分钟',['M1-012','M4-001','M4-002'],['S14','S15']),
    ('T08','重点详讲','6–10分钟',['M4-003'],['S14','S22','CN01']),
    ('T09','重点详讲','8–12分钟',['M4-001','M4-006'],['S19','S27']),
    ('T10','重点详讲','6–10分钟',['M4-019','M4-020','M4-021','M5-005'],['S15','S16','S17']),
]
CHAPTERS={'L01':['T01'],'L02':['T02'],'L03':['T03','T04','T05','T06'],
          'L04':['T07','T08'],'L05':['T09'],'L06':['T10']}


def build():
    bank=json.loads((ROOT/'backend/content/learning-bank.json').read_text(encoding='utf-8'))
    snapshot=json.loads((ROOT/'data/graph-snapshot.json').read_text(encoding='utf-8'))
    nodes={n['businessId']:n['properties']['name'] for n in snapshot['nodes'] if n.get('primaryLabel')=='KnowledgePoint'}
    sources={s['id']:dict(s) for s in bank['sources']}
    sources['TEACH-TURNS']={'id':'TEACH-TURNS','title':'Esri：Turns','url':'https://pro.arcgis.com/en/pro-app/3.6/help/analysis/networks/turns-in-the-network-dataset.htm','version_or_date':'ArcGIS Pro 3.6','section':'开头转向与限制说明；Understanding turns','accessed':'2026-11-05'}
    sources['TEACH-TOPOLOGY']={'id':'TEACH-TOPOLOGY','title':'QGIS：7. Topology','url':'https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/topology.html','version_or_date':'QGIS 3.44','section':'§7.1–7.3','accessed':'2026-11-05'}
    lessons=[];mapping={}
    for lid,level,minutes,ids,source_ids in SPECS:
        md=(DOCS/(lid+'.md')).read_text(encoding='utf-8').strip()
        title=md.splitlines()[0].removeprefix('# ').strip() if hasattr(str,'removeprefix') else md.splitlines()[0][2:].strip()
        for sid in source_ids:
            assert sid in sources
            md=re.sub(r'\['+re.escape(sid)+r'\](?!\()',lambda m:'['+sid+']('+sources[sid]['url']+') ',md)
        for path in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',md):
            assert re.fullmatch(r'/assets/teaching/[A-Za-z0-9/_-]+\.(svg|png|webp)',path)
            assert (ROOT/'frontend/public'/path.lstrip('/')).is_file(),path
        assert not re.search(r'\[(?:S\d\d|CN\d\d)\](?!\()',md),'Unresolved source reference'
        assert all(i in nodes for i in ids)
        lessons.append({'id':lid,'title':title,'level':level,'readingTime':minutes,
                        'knowledgePointIds':ids,'sourceIds':source_ids,
                        'embeddedSources':lid=='T04','markdown':md,
                        'reviewed':'2026-11-05'})
        for kid in ids:mapping.setdefault(kid,[]).append(lid)
    mapping['M1-009']=['T03','T01'];mapping['M7-010']=['T02','T01']
    target={q['main_knowledge_point']['id'] for q in bank['questions']}
    assert set(mapping)==target and len(mapping)==24
    by_id={l['id']:l for l in lessons}
    for ch,lids in CHAPTERS.items():
        covered=set().union(*(set(by_id[l]['knowledgePointIds']) for l in lids))
        assert {q['main_knowledge_point']['id'] for q in bank['questions'] if q['chapter_id']==ch} <= covered
    used={sid for l in lessons for sid in l['sourceIds']}
    return {'version':'1.0.0','scope':'六关入门教学；不代表高阶知识点全部内容','lessons':lessons,
            'chapterLessons':CHAPTERS,'knowledgePointLessons':mapping,
            'knowledgePointNames':{k:nodes[k] for k in mapping},
            'sources':[sources[k] for k in sorted(used)]}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    payload=json.dumps(build(),ensure_ascii=False,indent=2)+'\n'
    if args.check:
        assert DEST.read_text(encoding='utf-8')==payload,'Teaching registry is stale; run scripts/build_intro_teaching.py'
        print('PASS: 10 lessons cover all 24 introductory knowledge points and all six chapter objectives.')
    else:
        DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(payload,encoding='utf-8')
        print('Built frontend teaching registry; question bank unchanged.')
