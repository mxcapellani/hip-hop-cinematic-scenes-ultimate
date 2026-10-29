from pathlib import Path
import re,json,hashlib,sys,yaml
B=Path('.agents/skills/hip-hop-cinematic-scenes-ultimate')
class Unique(yaml.SafeLoader):pass
def unique(loader,node,deep=False):
 d={}
 for k,v in node.value:
  key=loader.construct_object(k,deep=deep)
  if key in d:raise ValueError('duplicate YAML key')
  d[key]=loader.construct_object(v,deep=deep)
 return d
Unique.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique)
def validate(root):
 root=Path(root);e=[]
 for p in ('README.md','LICENSE','NOTICE.md','docs/SOURCE_PACK.md','docs/gaps.json','docs/catalog-manifest.json',str(B/'SKILL.md'),str(B/'assets/scene-catalog.json')):
  if not (root/p).is_file() or not (root/p).read_text().strip():e.append('missing '+p)
 if e:return e
 t=(root/B/'SKILL.md').read_text()
 try:
  assert t.startswith('---\n');d=yaml.load(t.split('---',2)[1],Loader=Unique);assert set(d)=={'name','description'} and d['name']=='hip-hop-cinematic-scenes-ultimate' and len(d['description'])>60
 except Exception:e.append('invalid metadata')
 try:
  s=(root/'docs/SOURCE_PACK.md').read_text();m=json.loads((root/'docs/catalog-manifest.json').read_text());rows=json.loads((root/B/'assets/scene-catalog.json').read_text());g=json.loads((root/'docs/gaps.json').read_text());originals=re.findall(r'```text\n(.*?)```',s,re.S)
  assert hashlib.sha256(s.encode()).hexdigest()==m['source_sha256']
  assert len(rows)==len(originals)==m['prompt_count']==52
  assert len(re.findall(r'^#### ',s,re.M))==m['entry_count']==57
  assert len(g['empty_entries'])==m['empty_count']==5 and g['missing_scene_numbers']==[47]
  assert [x['number'] for x in rows]==[i for i in range(1,54) if i!=47]
  refs=(root/B/'references/original-prompts.md').read_text()
  for x,orig,entry in zip(rows,originals,m['prompts']):
   assert x['prompt_en']==orig and orig in refs
   assert hashlib.sha256(orig.encode()).hexdigest()==x['prompt_sha256']==entry['prompt_sha256']
   assert x['id']==entry['id']==f"C{x['number']:03d}" and x['title']==entry['title'] and x['id'] in t
   assert x['placeholders']==re.findall(r'\[[^\]\n]+\]',orig)
 except Exception:e.append('source/catalog/hash/gap mismatch')
 for p in root.rglob('*.md'):
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if '://' in link or link.startswith('#'):continue
   target=(p.parent/link.split('#')[0]).resolve()
   if not target.is_relative_to(root.resolve()) or not target.exists():e.append('bad link '+link)
 return e
if __name__=='__main__':
 e=validate(Path(__file__).resolve().parents[1]);print('\n'.join(e) if e else 'PASS: YAML, 52 exact prompts, hashes, 5 gaps, absent scene 47 and links');sys.exit(bool(e))
