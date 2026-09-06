from pathlib import Path
import random, shutil, argparse
p=argparse.ArgumentParser(); p.add_argument('source'); p.add_argument('output'); p.add_argument('--seed',type=int,default=42); a=p.parse_args()
s=Path(a.source); o=Path(a.output); imgs=[x for x in (s/'images').glob('*') if x.suffix.lower() in {'.jpg','.jpeg','.png'}]; random.Random(a.seed).shuffle(imgs)
for split, items in {'train':imgs[:round(.8*len(imgs))],'val':imgs[round(.8*len(imgs)):round(.9*len(imgs))],'test':imgs[round(.9*len(imgs)): ]}.items():
 for img in items:
  for kind,src in [('images',img),('labels',s/'labels'/(img.stem+'.txt'))]:
   dst=o/kind/split/src.name; dst.parent.mkdir(parents=True,exist_ok=True)
   if src.exists(): shutil.copy2(src,dst)
print(f'Created split for {len(imgs)} images at {o}')
