import re,subprocess,unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent.parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.templates=set();self.assets=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  if tag in ('script','link','img','source'):
   key={'script':'src','link':'href','img':'src','source':'src'}[tag]
   if key in d:self.assets.append(d[key])
class StructureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=(ROOT/'site/index.html').read_text();cls.app=(ROOT/'site/app.js').read_text();cls.world=(ROOT/'site/world.js').read_text();cls.css=(ROOT/'site/style.css').read_text();cls.p=Parser();cls.p.feed(cls.html)
 def test_html_parse(self):self.assertGreater(len(self.p.ids),24)
 def test_screens(self):
  for name in ['splash','opening','title','menu','creator','world','options','credits']:self.assertIn('tpl-'+name,self.p.ids)
 def test_21_profiles(self):
  matches=re.findall(r'\[(\d+),\'([^\']+)\'\]',self.app.split('const CLASSES=[')[1].split('];')[0])
  self.assertEqual(len(matches),21);self.assertEqual(sorted(int(x[0]) for x in matches),list(range(1,22)))
 def test_bosses_distinguished(self):
  for name in ['Vigia das Ruínas','Sussurro do Brejo','Árvore Guardiã']:self.assertIn(name,self.world)
  self.assertIn('não canônico',self.world);self.assertIn('Rave Masters',self.world)
 def test_no_js_gameplay_arithmetic(self):
  self.assertIn('nsw_wasm_apply',self.app);self.assertNotRegex(self.app,r'bossHp\s*-\s*damage')
 def test_source_scripts_exist(self):
  for a in self.p.assets:
   if a.startswith(('http:','https:')):continue
   self.assertTrue((ROOT/'site'/a).is_file(),a)
 def test_assets_exist(self):
  for n in ['brand','title','ensemble','city','presentation']:self.assertTrue((ROOT/'site/assets'/(n+'.webp')).is_file())
 def test_stylesheet(self):self.assertIn('reduced-motion',self.css);self.assertIn('PRESS TO START',self.html)
 def test_camera_contract(self):self.assertIn('const C=root.NSCamera4',self.world)
 def test_no_javascript_silent_fallback(self):self.assertIn('CORE AUSENTE · PROGRESSO BLOQUEADO',self.app)
 def test_video_duration(self):
  path=ROOT/'site/assets/opening_animatic.mp4'
  txt=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)]).decode().strip()
  self.assertAlmostEqual(float(txt),18.,delta=.4)
 def test_js_syntax(self):
  for n in ['app.js','world.js','camera4.js']:subprocess.check_call(['node','--check',str(ROOT/'site'/n)],stdout=subprocess.DEVNULL)
if __name__=='__main__':unittest.main(verbosity=2)
