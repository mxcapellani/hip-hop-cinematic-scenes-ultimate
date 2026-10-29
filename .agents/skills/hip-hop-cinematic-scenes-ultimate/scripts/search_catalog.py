"""Offline lexical search and exact retrieval. No network or generation."""
from pathlib import Path
import argparse,json,re,unicodedata
CATALOG=Path(__file__).resolve().parents[1]/'assets/scene-catalog.json'
def normalize(t):
 t=''.join(c for c in unicodedata.normalize('NFKD',t.lower()) if not unicodedata.combining(c))
 return ' '.join(re.findall(r'[a-z0-9]+',t))
ALIASES={'carros':'carro','cars':'carro','car':'carro','vermelha':'vermelho','vermelhas':'vermelho','red':'vermelho','crimson':'vermelho','scarlet':'vermelho','blue':'azul','green':'verde','golden':'dourado','gold':'dourado','luzes':'luz','lights':'luz','light':'luz','retratos':'retrato','portais':'portal','silhuetas':'silhueta','surrealismo':'surreal','noite':'noturno','night':'noturno'}
STOP={'quero','um','uma','o','a','os','as','de','do','da','com','para','prompt','prompts','me','mostre','por','favor','em','cena','cenas','e'}
def tokens(t):return [ALIASES.get(x,x) for x in normalize(t).split() if x not in STOP]
def search(rows,query):
 n=normalize(query);num=re.fullmatch(r'(?:cena\s*|c\s*)?0*(\d+)',n)
 if num:return [r for r in rows if r['number']==int(num[1])]
 exact=[r for r in rows if normalize(r['title'])==n]
 if exact:return exact
 ts=tokens(query)
 if not ts:return []
 found=[]
 for r in rows:
  hay=set(tokens(r['title']+' '+r['description_pt']+' '+' '.join(r['themes'])+' '+r['prompt_en']))
  if all(t in hay for t in ts):found.append(r)
 return found
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('query');p.add_argument('--original',action='store_true');a=p.parse_args();rows=search(json.loads(CATALOG.read_text()),a.query)
 if a.original:
  if len(rows)!=1:p.error('Use a unique scene number/title; zero or multiple matches')
  print(rows[0]['prompt_en'],end='')
 else:print(json.dumps([{k:r[k] for k in ('id','number','title','themes')} for r in rows],ensure_ascii=False,indent=2))
