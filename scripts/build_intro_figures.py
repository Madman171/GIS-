"""Four original reusable SVG teaching figures. No raster generation service."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'frontend/public/assets/teaching/intro';OUT.mkdir(parents=True,exist_ok=True)
INK='#24343B';BLUE='#658FAA';TEAL='#7EAAA0';RED='#AC645B';BG='#F7F6F1'
def txt(x,y,t,s=27):return '<text x="{}" y="{}" font-size="{}" fill="{}">{}</text>'.format(x,y,s,INK,escape(t))
def path(d,color=BLUE,width=8,arrow=False):return '<path d="{}" fill="none" stroke="{}" stroke-width="{}" stroke-linecap="round" {}/>'.format(d,color,width,'marker-end="url(#a)"' if arrow else '')
def node(x,y,t):return '<circle cx="{}" cy="{}" r="23" fill="{}"/>'.format(x,y,INK)+txt(x-9,y+10,t,28).replace('fill="'+INK+'"','fill="#FFFFFF"')
def save(name,title,desc,body):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="540" viewBox="0 0 1000 540" role="img" aria-labelledby="t d"><title id="t">{}</title><desc id="d">{}</desc><defs><marker id="a" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0 0L4 2L0 4Z" fill="{}"/></marker></defs><style>text{{font-family:"Microsoft YaHei","Noto Sans SC",sans-serif}}</style><rect width="1000" height="540" fill="{}"/>{}{}{}</svg>'.format(escape(title),escape(desc),BLUE,BG,txt(40,54,title,32),txt(40,98,'自拟教学示意；不代表真实道路或实测数据',23),body)
 (OUT/name).write_text(s,encoding='utf-8')
body=txt(70,170,'点：站点位置')+'<circle cx="220" cy="255" r="13" fill="'+BLUE+'"/>'+txt(530,170,'线：道路中心线')+path('M540 290L655 230L800 280',BLUE,10)
body+=txt(70,365,'面：校区边界')+'<path d="M100 400L340 400L300 490L130 480Z" fill="#DCE8E5" stroke="'+TEAL+'" stroke-width="5"/>'+txt(530,365,'栅格：规则像元与取值')
for row in range(3):
 for col in range(4):
  body+='<rect x="{}" y="{}" width="58" height="40" fill="{}" stroke="#FFFFFF" stroke-width="2"/>'.format(555+col*58,395+row*40,['#C8DAE1','#AEC6D0','#92B2C0'][(row+col)%3])
  body+=txt(574+col*58,423+row*40,str(10+row+col),20)
save('data-models.svg','先辨认数据表达，再判断能回答什么问题','公交站用点、道路中心线用线、校区边界用面；栅格按规则行列像元记录值。表达方式取决于任务。',body)
body=path('M210 210H755',arrow=True)+path('M767 230L510 415',arrow=True)+path('M475 415L206 235',arrow=True)
body+=node(180,210,'P')+node(790,210,'Q')+node(490,435,'R')
body+=txt(335,182,'P → Q')+txt(685,345,'Q → R')+txt(195,345,'R → P')+txt(70,510,'从 Q 到 P：可沿 Q→R→P；图中没有直接的 Q→P 边。',25)
save('direction.svg','箭头定义本题允许的方向','仅有P到Q、Q到R、R到P三条有向边。Q到P可绕经R，不能自行补出直接反向边。',body)
body=txt(40,165,'① 真实尽端路')+path('M100 220V355M100 280H260',BLUE,12)+'<circle cx="260" cy="280" r="10" fill="'+INK+'"/>'+txt(40,425,'保留真实结构',26)
body+=txt(355,165,'② 本应相接却留缝')+path('M390 280H480M500 220V355M500 280H620',BLUE,12)+'<circle cx="480" cy="280" r="8" fill="'+RED+'"/>'+txt(355,425,'核实后按规则修正',25)
body+=txt(700,165,'③ 无连接的跨层路')+path('M835 210V360',TEAL,15)+path('M730 280H950',BG,44)+path('M730 280H950',BLUE,15)+path('M792 258H878M792 302H878',BLUE,3)+txt(700,425,'不能凭靠近误接',25)
body+=txt(40,505,'检查标记是线索；处理依据是真实道路、数据规范与适用规则。',25)
save('topology-check.svg','同样有端点，处理方式可能不同','真实尽端路应保留；现场应连通而数据留有缝隙需核实；桥上桥下无转换设施时不能误接。',body)
body=path('M145 267L457 160',arrow=True)+path('M510 160L830 267',arrow=True)+path('M145 290L457 397',arrow=True)+path('M510 397L830 290',arrow=True)
body+=node(120,280,'S')+node(485,150,'A')+node(485,410,'B')+node(860,280,'T')
body+=txt(260,188,'3 km')+txt(655,188,'3 km')+txt(260,395,'2 km')+txt(655,395,'5 km')
body+=txt(65,470,'经 A：3＋3＝6 km；经 B：2＋5＝7 km。',27)+txt(65,515,'给定沿道路长度；线段不按长度比例绘制，四条边均允许使用。',24)
save('distance-network.svg','比较累计成本，不只看第一条边','仅S到A为3千米、A到T为3千米、S到B为2千米、B到T为5千米。均为合法有向边，无额外延误。',body)
print('Built four reusable original intro SVGs.')
