"""Build explicit RESEARCH_ONLY class profile presentation data from source-grounded labels.
Source: Drive 1hd8QM4x5aKP3gh6LnaedpbauHzMpFFZJM47N0-kBKY8 (§ research E02/E04, palette § appendices).
No effects or colors are promoted to canon by this fixture.
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
rows=[
(1,'Soldier','Coordenar sob limites de agência','#CD7F32','Comando de abertura','Marca uma oportunidade e prepara guarda limitada.'),
(2,'Dragon Slayer','Interpretar escala e condição','#9B111E','Leitura de escala','Resposta mais forte quando o inimigo altera fase.'),
(3,'Berserker','Pressionar assumindo um custo','#DC143C','Pressão arriscada','Golpe forte que cobra vitalidade do usuário.'),
(4,'Rogue A','Explorar uma abertura verdadeira','#862F88','Brecha calculada','Resposta ganha valor após recuperação do oponente.'),
(5,'Rogue B','Desorientar sem comandar a reação','#996666','Finta defensiva','Provoca uma janela defensiva e restringe uma reação.'),
(6,'Knight','Interpor-se e assumir exposição','#000080','Interposição','Reserva proteção para o próximo contato.'),
(7,'Ranger','Preparar alcance e terreno','#8A9A5B','Geometria de tiro','Técnica muda desempenho conforme distância.'),
(8,'Warrior','Decidir pelo contato e instrumento','#4682B4','Controle de contato','Golpe depende de proximidade real.'),
(9,'Monk','Equilibrar e redirecionar','#E0B59A','Fluxo corporal','Converte foco observado em resposta e defesa.'),
(10,'Battlemage','Integrar instrumento e magia','#9966CC','Convergência','Ataque e proteção na mesma decisão.'),
(11,'Dark Mage','Condicionar adversários com limites','#4C515D','Condição pendente','Prepara marca para outro momento.'),
(12,'Pyromancer','Gerir propagação do calor','#CC5500','Chama residual','Aplica consequência térmica em turnos.'),
(13,'Necromancer','Rastrear agentes e persistência','#301934','Eco condicionado','Mantém um efeito posterior verificável.'),
(14,'Esper','Antecipar sob incerteza','#E6E6FA','Antevisão limitada','Abre tempo de resposta sem conhecimento absoluto.'),
(15,'Alchemist','Preparar reações materiais','#CFB53B','Reagente limitado','Consome preparado para aumentar a potência.'),
(16,'Cryomancer','Segmentar temporariamente o espaço','#AFEEEE','Trava fugaz','Restringe uma reação por duração finita.'),
(17,'Bard','Sincronizar oportunidades coletivas','#DA70D6','Cadência','Recupera ritmo e prepara janela temporária.'),
(18,'Cleric','Priorizar preservação','#FFFFF0','Socorro','Troca impacto por recuperação limitada.'),
(19,'Druid','Adaptar-se ao ambiente existente','#808000','Leitura do terreno','Cura conforme o terreno ou prepara proteção.'),
(20,'Sentinel','Antecipar defesa de um setor','#C0C0C0','Vigília','Protege mais conforme o ataque telegráfico.'),
(21,'Shaman','Ancorar focos espaciais','#0F8F99','Foco ancorado','Prepara marca e eco limitado, sem onisciência.')]
assert [r[0] for r in rows]==list(range(1,22))
arr=[{'id':i,'source_id':f'R{i:02d}','name':name,'research_principle':principle,'research_primary_hex':hex,'lab_mode_name':mode,'lab_effect_description':desc,'status':'RESEARCH_PROFILE_LAB_MECHANIC_NOT_CANON'} for i,name,principle,hex,mode,desc in rows]
content={'schema':'mmai.r02.classes.research-ui.v1','source_drive_id':'1hd8QM4x5aKP3gh6LnaedpbauHzMpFFZJM47N0-kBKY8','source_authority':'research/author-approved 21 design identities; A3/A4 gated','rogue_caveat':'R04 and R05 share the historical legacy ROGUE class key; structural independence not proven','records':arr}
path=ROOT/'docs/R02_CLASS_RESEARCH_BINDINGS.json';path.write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
js='// Research-only reading aid; lab modes are NOT skills approved by the author.\nwindow.NSKitLab='+json.dumps(arr,ensure_ascii=False,separators=(',',':'))+';\n'
(ROOT/'site/classes_r02.js').write_text(js,encoding='utf-8')
print('class profile bindings',len(arr),'sha',hashlib.sha256(path.read_bytes()).hexdigest())
