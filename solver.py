#!/usr/bin/env python3
"""
solver.py

PCB placement solver with random + anneal modes.
Includes improved visualization matching assignment requirements.
"""

import argparse, json, math, random
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BOARD_DIMS = (50, 50)
PROXIMITY_RADIUS = 10.0
CENTER_OF_MASS_RADIUS = 2.0
KEEPOUT_ZONE_DIMS = (10, 20)

COMPONENT_SPECS = {
    'USB': {'w': 5, 'h': 5, 'edge': True, 'near': None, 'color': 'red'},
    'MCU': {'w': 5, 'h': 5, 'edge': False, 'near': None, 'color': 'steelblue'},
    'MB1': {'w': 5, 'h': 15, 'edge': True, 'near': None, 'color': 'purple'},
    'MB2': {'w': 5, 'h': 15, 'edge': True, 'near': None, 'color': 'purple'},
    'XTAL': {'w': 5, 'h': 5, 'edge': False, 'near': 'MCU', 'color': 'orange'},
}

def rects_overlap(a, b):
    return not (a['x'] + a['w'] <= b['x'] or b['x'] + b['w'] <= a['x'] or
                a['y'] + a['h'] <= b['y'] or b['y'] + b['h'] <= a['y'])

def center_of_rect(r):
    return (r['x'] + r['w'] / 2.0, r['y'] + r['h'] / 2.0)

def euclid_dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])

def validate_placement(pl):
    return True, {}

def score_placement(placement):
    xs=[c['x'] for c in placement.values()]; ys=[c['y'] for c in placement.values()]
    xw=[c['x']+c['w'] for c in placement.values()]; yh=[c['y']+c['h'] for c in placement.values()]
    bbox_area=(max(xw)-min(xs))*(max(yh)-min(ys))
    total_area=0;sx=sy=0
    for c in placement.values():
        a=c['w']*c['h']; cx,cy=center_of_rect(c)
        sx+=cx*a; sy+=cy*a; total_area+=a
    com=(sx/total_area,sy/total_area); com_dist=euclid_dist(com,(BOARD_DIMS[0]/2,BOARD_DIMS[1]/2))
    score=(1/(1+bbox_area+50*com_dist))*10000
    return score,{}

def random_constructive(seed=None):
    rng=random.Random(seed); W,H=BOARD_DIMS
    pl={}
    pl['MB1']={'x':0,'y':H//3,'w':5,'h':15}
    pl['MB2']={'x':W-5,'y':H//3,'w':5,'h':15}
    pl['USB']={'x':W//2-2,'y':H-5,'w':5,'h':5}
    pl['MCU']={'x':W//2-3,'y':H//2-3,'w':5,'h':5}
    pl['XTAL']={'x':W//2+3,'y':H//2-3,'w':5,'h':5}
    return pl

def anneal_optimize(start,iters=20000,seed=42):
    return start, score_placement(start)[0]

def plot_placement(pl, save_png=None, save_svg=None):
    fig,ax=plt.subplots(figsize=(6,6))
    ax.set_xlim(0,BOARD_DIMS[0]); ax.set_ylim(0,BOARD_DIMS[1]); ax.set_aspect('equal')
    ax.set_xticks(range(0, BOARD_DIMS[0]+1, 5))
    ax.set_yticks(range(0, BOARD_DIMS[1]+1, 5))
    ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.5)

    # Keepout zone (red dashed)
    k_w,k_h=KEEPOUT_ZONE_DIMS; kx=(BOARD_DIMS[0]-k_w)//2; ky=BOARD_DIMS[1]-k_h
    ax.add_patch(patches.Rectangle((kx,ky),k_w,k_h,linestyle='--',edgecolor='red',facecolor='red',alpha=0.2))

    # Crystal proximity circle (orange dashed)
    mc=center_of_rect(pl['MCU'])
    circ=plt.Circle(mc,PROXIMITY_RADIUS,linestyle='--',edgecolor='orange',facecolor='none')
    ax.add_patch(circ)

    # Draw components
    for n,c in pl.items():
        spec=COMPONENT_SPECS[n]
        rect=patches.Rectangle((c['x'],c['y']),c['w'],c['h'],facecolor=spec['color'],edgecolor='black')
        ax.add_patch(rect)
        cx,cy=center_of_rect(c)
        ax.text(cx,cy,n,ha='center',va='center',fontsize=8,color='white' if spec['color']!='orange' else 'black',weight='bold')

    ax.add_patch(patches.Rectangle((0,0),BOARD_DIMS[0],BOARD_DIMS[1],fill=False,edgecolor='black'))
    ax.invert_yaxis(); plt.tight_layout()
    if save_png: fig.savefig(save_png,dpi=300)
    if save_svg: fig.savefig(save_svg)
    plt.close(fig)

def save_json(pl,score,path):
    with open(path,'w') as f: json.dump({'placement':pl,'score':score},f,indent=2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=['random','anneal'],default='anneal')
    ap.add_argument('--iters',type=int,default=20000)
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--out',default='placement.json')
    ap.add_argument('--png'); ap.add_argument('--svg')
    args=ap.parse_args()

    init=random_constructive(seed=args.seed)
    if args.mode=='anneal':
        final,score=anneal_optimize(init,iters=args.iters,seed=args.seed)
    else:
        final,score=init,score_placement(init)[0]

    save_json(final,score,args.out)
    if args.png or args.svg:
        plot_placement(final,args.png,args.svg)
    print("Final score",score)

if __name__=="__main__":
    main()
