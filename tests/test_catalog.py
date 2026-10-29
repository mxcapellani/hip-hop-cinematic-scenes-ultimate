import unittest,importlib.util,json,tempfile,shutil,subprocess,sys
from pathlib import Path
from validate_catalog import validate,B
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('search',R/B/'scripts/search_catalog.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ROWS=json.loads((R/B/'assets/scene-catalog.json').read_text())
class SearchTests(unittest.TestCase):
 def test_number(self):self.assertEqual(m.search(ROWS,'17')[0]['title'],'Midnight Call')
 def test_id(self):self.assertEqual(m.search(ROWS,'C004')[0]['number'],4)
 def test_phrase_number(self):self.assertEqual(m.search(ROWS,'Cena 17')[0]['number'],17)
 def test_title(self):self.assertEqual(m.search(ROWS,'CRIMSON SMOKE')[0]['number'],8)
 def test_missing47(self):self.assertEqual(m.search(ROWS,'47'),[])
 def test_car_red(self):self.assertTrue({12,27,28}.issubset({x['number'] for x in m.search(ROWS,'carro vermelho')}))
 def test_unknown(self):self.assertEqual(m.search(ROWS,'ornitorrinco astronauta'),[])
 def test_cli_literal(self):
  r=subprocess.run([sys.executable,str(R/B/'scripts/search_catalog.py'),'17','--original'],capture_output=True,text=True,check=True);self.assertEqual(r.stdout,next(x['prompt_en'] for x in ROWS if x['number']==17))
 def test_cli_missing_fails(self):
  r=subprocess.run([sys.executable,str(R/B/'scripts/search_catalog.py'),'47','--original'],capture_output=True,text=True);self.assertNotEqual(r.returncode,0)
class IntegrityTests(unittest.TestCase):
 def setUp(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.r=Path(t.name)/'repo';shutil.copytree(R,self.r)
 def test_valid(self):self.assertEqual(validate(self.r),[])
 def test_modified_prompt(self):
  p=self.r/B/'assets/scene-catalog.json';d=json.loads(p.read_text());d[0]['prompt_en']+='Modified';p.write_text(json.dumps(d));self.assertTrue(validate(self.r))
 def test_lost_gap(self):
  p=self.r/'docs/gaps.json';d=json.loads(p.read_text());d['empty_entries'].pop();p.write_text(json.dumps(d));self.assertTrue(validate(self.r))
 def test_missing_reference(self):
  (self.r/B/'references/original-prompts.md').unlink();self.assertTrue(validate(self.r))
 def test_wrong_name(self):
  p=self.r/B/'SKILL.md';p.write_text(p.read_text().replace('name: hip-hop-cinematic-scenes-ultimate','name: other',1));self.assertTrue(validate(self.r))
 def test_source_changed(self):
  p=self.r/'docs/SOURCE_PACK.md';p.write_text(p.read_text()+'\nAltered');self.assertTrue(validate(self.r))
if __name__=='__main__':unittest.main()
