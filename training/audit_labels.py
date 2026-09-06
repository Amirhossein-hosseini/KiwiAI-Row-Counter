from pathlib import Path
import argparse
p=argparse.ArgumentParser(); p.add_argument('dataset'); a=p.parse_args()
root=Path(a.dataset); images={p.stem for p in (root/'images').glob('*') if p.suffix.lower() in {'.jpg','.jpeg','.png'}}; labels=list((root/'labels').glob('*.txt')); errors=[]
for label in labels:
    if label.stem not in images: errors.append(f'no image for {label.name}')
    for n,line in enumerate(label.read_text(encoding='utf-8').splitlines(),1):
        try:
            v=line.split(); assert len(v)==5 and int(v[0]) in (0,1); assert all(0<=float(x)<=1 for x in v[1:])
        except Exception: errors.append(f'{label.name}:{n}')
print(f'images={len(images)} labels={len(labels)} errors={len(errors)}')
if errors: print('\n'.join(errors[:20])); raise SystemExit(1)
