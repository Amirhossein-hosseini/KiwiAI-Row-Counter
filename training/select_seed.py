"""Copy evenly spaced source images into a 300-image annotation seed set."""
from pathlib import Path
import argparse, shutil
p=argparse.ArgumentParser(); p.add_argument('source_images'); p.add_argument('seed_root'); p.add_argument('--count',type=int,default=300); a=p.parse_args()
src=sorted(p for p in Path(a.source_images).rglob('*') if p.suffix.lower() in {'.jpg','.jpeg','.png'})
if len(src)<a.count: raise SystemExit(f'Only {len(src)} images found; need {a.count}.')
chosen=[src[round(i*(len(src)-1)/(a.count-1))] for i in range(a.count)]
out=Path(a.seed_root)/'images'; out.mkdir(parents=True,exist_ok=True)
for n,image in enumerate(chosen,1): shutil.copy2(image,out/f'{n:04d}_{image.name}')
print(f'Copied {len(chosen)} diverse images to {out}')
