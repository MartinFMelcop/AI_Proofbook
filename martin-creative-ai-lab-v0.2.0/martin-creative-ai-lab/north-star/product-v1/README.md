# MMORPG Maker AI · North Star PRODUCT V1 — composite preproduction

**Author's direction (2026-11-15):** own engine (C++20/C17/Python+AI/SQL; Assembly only if benchmarked). No new Unity/C#-specific production. Historical Unity/C#/VEA/Workbench preserved. Four 90° camera views are a product requirement, distinct from VEA four-view asset production.

**This workstream is `INTERNAL_PREPRODUCTION / ART_REVIEW_PENDING / PRODUCT_NO_GO`**, not a deliverable ready for the author's RPG quality review. Do not distribute another technical test as a North Star game.

## One composed, versioned work package

- **Drive technical/source ZIP:** https://drive.google.com/file/d/1fsbHm8vHKnTD7nj8M-Ua8NbQWbLb8uz0/view
- 17,935,594 bytes; local SHA-256: `27a194e6e76d6bd3be44586f968919a519774313544a9388a853c3c568be10f5` (no remote byte-for-byte readback).
- **Drive master progress + gates:** https://docs.google.com/document/d/1HwKtQ3WLnCFEKMtjUN4cwYi0uRMQickM6SJHZNJkZPU/edit
- The archive contains 33 files: native C++20 core, C17 ABI header, wasm32 compilation, Python and Node tests, an original logo concept, an 18-second original motion-comic animatic and instrumental score, title/menu/creator/prologue interface, asset sources and status manifests.
- Native logic: 33 Python structure/C++ tests and Node WASM/camera suites PASS in Linux. Chromium UI `ERR_BLOCKED_BY_ADMINISTRATOR`; Windows and final game render NOT_RUN.

## Product flow / noncanonical sources

Studio splash → opening animatic → press-to-start title → main/options menu → character identity and up to two of 21 historic R01–R21 class profiles → opening adventure stages → three *mechanical fixture encounters* → epilogue.

21 profiles are a design direction, not 21 implemented class kits. Rogue A and Rogue B are separate research profiles with a shared legacy ROGUE key; their independence is unproven.

Rave Masters v0.2 (separate historical work): https://drive.google.com/file/d/1Q3LwmkiD-p2gvw65756ZLk1bkNmJc32Z/view. Its initial road/guard/dog/7-house village/Rose disappearance/forest/fairies/Guardian Tree minichefe are REFERENCES, not automatically North Star canon. It does **not** specify three North Star bosses. B01 `Vigia das Ruínas` and B02 `Sussurro do Brejo` are proposals; B03 `Árvore Guardiã` is a Rave Masters legacy source, NOT a canonized North Star boss.

## Exit gates before author's acceptance

1. Original brand and opening: author art approval, actual audiovisual animation/mix and publication rights.
2. Native rendered 2.5D world with camera orbit in 4 quarter-turns, readable occlusion/collisions and real NPC beings.
3. Real class kits for 1–2 choices, professions/skills, spatial exploration, quests and 3 authored bosses with real combat behavior and counterplay.
4. Complete persistence/authority, Windows under non-admin standard user, accessibility, reproducible tests and human review.
5. C/E/B/D owner acknowledgements and independent canon gates, preserving R51/R60/R61/INT-C01-001 OPEN, RP-R03-P03/RP-G02-A03 PENDING, C30 STOP_DOCUMENTARY_PENDING_OWNER, Arena S1 HOLD, C05-P01–P07 OPEN, F5/VEA decisions and 737 critiques.

This change is additive and reviewable. Existing baselines, Makers, MER, VEA, Unity and independent works are unchanged.


## R01 — World-owned spatial slice, no product promotion (2026-11-15)

**One composed revision of the same V1**, not a disconnected demo:
- New source ZIP (full, standalone snapshot) https://drive.google.com/file/d/19U1f3Yr7xhfResYMdrEtDAduJA6yscaV/view (22,111,513 bytes; SHA-256 local `cfce150ea5cd021c0fcd9ae30e2502f5ecec262117cbeeb86ab402338fefe553`; Google Drive size/parent readback only, remote binary hash not verified).
- R00 remains preserved at Drive ID `1fsbHm8vHKnTD7nj8M-Ua8NbQWbLb8uz0`; R01 supplements it and becomes the active laboratory source. No historical overwrite.
- World owner: `core/world.cpp`, one C++20-to-wasm32 executable rule set with a C ABI. The previous `core/product.cpp` is built separately only for legacy regression.
- Reality of play: a 24x20 grid rendered isometrically, native tile collisions, river/bridge, WASD/click movement, four actual orthographic quarter-turn projections, deterministic basic NPC routes, guard/leader/herbs/crafting, and three distinct mechanical encounters with telegraphs/guard/retreat, in one title/menu/creator/opening product flow.
- Evidence: 60 Python tests PASS; **100 native C++ intentions replayed in real WASM with matching state after each action**, 4 rotations + input observed under simulated Canvas/DOM, local hash-chained SQLite journal of 100 actions verified, 18-second H.264/AAC animatic unchanged. Browser rendering, Windows, art quality and player UX remain NOT_RUN/NOT_APPROVED.
- The 21 historical classes are selectable **but 21 class kits are not implemented**; skills are noncanonical laboratory techniques. B01/B02 are proposals; B03 is a separate Rave Masters legacy minichefe. No canonical boss, region or class power has been introduced.
- Art direction: extra 4-facing character sheet plus 6 prop sources, all derivations and source hashes in the package; 4-view object self-orientation, rigs, animations, performance and artistic acceptance are **pending**.
- Python/SQLite handles a reproducible **laboratory journal only**, not account persistence or browser save infrastructure. No multiplayer authority proven.
- Technical details in `docs/R01_SPATIAL_DELTA.md` and `artifacts/R01_TEST_REPORT.json` inside the R01 ZIP; this PR remains **DRAFT / PRODUCT_NO_GO**.

Next source-consumer work: four-facing coherent in-game architecture and animation with artistic gates; real 1–2-class kit binding; beings with personality-specific behavior; richer authored three-boss encounters; Windows standard-user build and human art/play review. No extra author-facing test ZIP until composite quality warrants it.


## R02 — Class research modes, bounded beings, materials and real Canvas render (2026-11-15)

**Same composite PRODUCT V1, new isolated revision, still `DRAFT / ART_REVIEW_PENDING / PRODUCT_NO_GO`.**

- R02 complete source package on Drive: https://drive.google.com/file/d/1I81NOh4eI83g-gYGJkGZtOyIbjzTeDVL/view, 29,080,893 bytes, 124 files. Local ZIP SHA-256 `ec71760455d19fedc78639fee42f859a33841d0bc199bc469929e2b4ef804fa8` (archive member CRC and SHA256 verified locally; remote readback confirmed size/folder only, not binary digest). Historic R00 and R01 remain unmodified.
- C++20 `core/world_r02.cpp`/C17 `world_r02.h` new **ABI 2** (old `world.cpp` ABI1 unchanged). Native `libns_world_r02.so` and new `site/product.wasm` use ONE experimental world authority; source and artifacts live in the R02 ZIP, not yet mirrored as executable source in GitHub. All 21 profiles R01–R21 can use **differentiated RESEARCH/LAB_ONLY** ability modes selected primary or secondary, including conditional costs and effects; **NOT 21 approved class kits**.
- New optional mining → smelting → tool upgrade loop with measurable attack changes, bounded C++ being behavioral modes (idle/patrol/attentive/working/concerned/alert; no true RPG AI), three distinct boss-fixture telegraphs, phase/patterns and counterplay. Two bosses proposed; the Tree belongs to a separate Rave Masters GDD historical source and is not canon North Star.
- Four 90° camera projections rendered by **actual** `site/world.js` Canvas code under Skia CPU. 16 concept pose frames and nine deterministic material tiles. Four Skia PNG artifacts in ZIP are **not browser captures**. On internal inspection the scene still has repeated grid textures and geometric NPCs: **art gate stays pending**.
- Technical evidence: **101 Python unittest PASS**, C17 executable linked to C++20 ABI2 PASS, **116 native intents** with field-by-field WASM parity incl being behavior, 100 archived R01 actions parity, 4 distinct Skia renders, SQLite 116-event verified hash-chain/replay, 6 preserved R01 source/asset SHA256 matches. Opening is unchanged 18s motion-comic, not a finished anime-quality video.
- Lab SQLite ledger is NOT authoritative online account/save. Client localStorage journal is version 3 ABI2, fails closed on incompatible R01 save (does not overwrite old key). Windows, real browser, art approval and multiplayer are NOT_RUN / NOT_APPROVED.
- Reproducibility details: `docs/R02_COMPOSED_DELTA.md`, `artifacts/R02_TEST_REPORT.json`, `docs/R02_CLASS_RESEARCH_BINDINGS.json` inside R02 ZIP.

Next gate **ART / authored gameplay quality**: player and beings consistent across 4 camera views, production animation/visual world, specialized 21 kits with author adjudication, three authored boss identities/patterns, opening and normal-user Windows build. Do not issue another fragmented user-test executable or promote any technical pass to `PRODUCT_GO`.


### Source mirror on the same draft PR

After the full R02 source ZIP was uploaded to Drive and its local integrity verified, **49 UTF-8 sources** (C/C++, Python, JavaScript, CSS, HTML, tests, documentation) were additionally committed under [source-r02](source-r02/) on this branch. Sample readback of 7 actual files matched the source bundle exactly. All large source art, animation, compiled binaries and rendered evidence remain in the single ZIP on Drive; no binary duplication or main-branch merge. The transient 228 KB JSON bridge used for this push was deleted from Drive after verification. This supersedes the earlier note saying the source was not mirrored to GitHub.


## R03 — Real renderer improvement, illustrated NPCs, two-action research kits (2026-11-15)

**One complete R03 increment, still `PRODUCT_NO_GO / ART_REVIEW_PENDING`; NOT a game release or author test.**

- **Drive R03 full source, artwork, tests and evidence:** https://drive.google.com/file/d/1gV0_gPI9P_7sQ7UWZt4lnKSAF0CYJklB/view — 37,147,998 bytes, 223 ZIP members, local SHA-256 `6f99e378ee19b2cef319e04aef4c427b48ab27d19af9699ed4ea73f7755a3ce8`, internal CRC and individual SHA-256 verified locally. Drive metadata readback matched size and parent; remote byte-for-byte hash NOT computed.
- **GitHub R03 source:** [source-r03/](source-r03/) contains **77 actual UTF-8 source/test/contract files** (C++20/ABI C17, JavaScript, Python+SQLite, UI, docs). Sample of 11 critical files had exact content readback vs temporary transport; that bridge file was deleted. Assets, binaries, video, SQLite and 4 Skia frames remain in the R03 ZIP only. R01/R02 source folders and their Drive archives preserved.
- **Gameplay owner** `core/world_r03.cpp` ABI3; new R03-only localStorage key and version4 fail closed on old saves. Signature+utility+bounded passive for 21 research profiles, including a reduced passive for the secondary class. **Not approved real 21 class kits**, no canon skill IDs, no independent Rogue A/B proven.
- **Art renderer** actual `site/world.js` executed on Skia CPU with four 1200×760 camera views. The NPC cones are replaced by 4 illustrated archetypes × 4 orientations with original-source/alpha receipts. Nine terrain materials now have 5 variants each (45 total) and less black grid; torches have light gradients. **Still below visual acceptance:** the map remains sparse, other props lack true four-sided art, NPCs lack rich animation, and bosses remain illustrated by mechanical placeholders.
- **Bounded beings and bosses:** near-only causal talk-mask and last-talk tick, no cross-session mind-reading; B01/B02/B03 have distinct laboratory attack patterns incl phase corrosive SP loss and root pressure, with both natural play and explicitly *synthetic* phase tests. B03 is still an independent Rave Masters historical miniboss reference, not North Star canon.
- **Executed verification:** 132 Python unit tests, 121 R03 C++20→WASM parity steps, R02 116 and R01 100 archived WASM steps, C17 executable, 121-event SQLite causal journal and negative checks, 4 real Skia Canvas renders, 10 historical R02 source SHA matches, 16+45 art images decoded. **Windows/browser normal user, final opening, human art, network MMO and three actual author-approved bosses NOT_RUN/NOT_APPROVED.**
- Details and source anchors: `source-r03/docs/R03_COMPOSED_DELTA.md`, `source-r03/docs/R03_VISUAL_AUDIT.md`, `source-r03/artifacts/R03_TEST_REPORT.json`.

Continue on the **same** V1 package and PR; do not open fragmented author-facing demos. Next gate is the qualitative jump: detailed architecture/vegetation, richer NPC/hero motion in all four views, boss creature art and counterplay, 21 class kits with canon owners/balance, cinematic-quality opening and standard-user Windows build. Historical blocks and independent work remain unchanged; main is untouched.


## R04 — arquitetura de vila in-game, chefe ilustrado e telegraph único do owner (15/11/2026)

**DRAFT / ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO**. Isto não é um lançamento nem convite para teste autoral.

- **Pacote integral R04 no Drive:** https://drive.google.com/file/d/1tU1Tk6g7JshWv5IGlUdLx7-gTf0f-zif/view — 55.322.074 bytes, 279 arquivos, SHA-256 local `89eb4a57c1c6dfb912c7c1a9d8afc2ac8bc272f8710cab5a3cc93efcc54e9656`. Verificados localmente CRC e hash de cada arquivo; Drive confirmou tamanho e pasta, **não** hash por redownload remoto. R00–R03 preservados.
- **102 arquivos textuais R04 publicados nesta mesma branch:** [source-r04/](source-r04/). Conjunto contém C++20/ABI C17, Python+SQLite, Canvas JS, testes Node/Python, documentação e recibos; **12 arquivos críticos** comparados exatamente à fonte. Assets/binaries/video/frames apenas no ZIP Drive.
- **Gameplay:** `core/world_r04.cpp` é o único owner do cliente, ABI4. A nova máscara de perigo `nsw_boss_threatens` é a mesma função pura usada pelo dano de chefe; `site/world.js` somente consulta a saída WASM e desenha no tile isométrico. Revisões de gameplay não mudam ao girar a câmera/desenhar.
- **Arte in-game (conceitos não aprovados):** nove props com arquitetura, forja, boticário, ponte, fonte e flora; B01 derivado de quatro sprites de guarda, B02 espírito procedural, B03 variação diferenciada de árvore. Camadas com oclusão mitigada no combate. Props são billboards, **não são malhas e não possuem quatro fachadas autênticas**. Falta mundo completo, animação convincente, personagens e chefões finais.
- **Evidência executada:** 167 Python tests PASS; consumidor C17 ↔ C++20 PASS; **121 intents R04** pareados com WASM e **4 amostras de ameaça por evento**, regressões R03 121/R02 116/R01 100, journal SQLite R04 121 eventos e contraprovas, **4 Skia imagens reais** + **3 Skia imagens reais de chefes**. Na vista equivalente, 17,82% dos pixels tiveram L1 RGB médio >18 vs R03; **mudança não é prova de beleza**. Browser/Windows NOT_RUN.
- **Classes / beings / lore / opening:** 21 kits ainda hipóteses de pesquisa (assinatura+auxiliar+passiva); beings com estados limitados; B01/B02 candidatos e B03 referência separada de Rave Masters — nenhum canonizado. Opening continua animatic 18s. Owner ACKs e todos bloqueios históricos preservados.

Leia [R04_COMPOSED_DELTA](source-r04/docs/R04_COMPOSED_DELTA.md), [R04_VISUAL_AUDIT](source-r04/docs/R04_VISUAL_AUDIT.md) e [R04_TEST_REPORT](source-r04/artifacts/R04_TEST_REPORT.json). Nenhuma alteração em main, Unity/C#, Makers, MER, VEA ou cânone; só documentação/filiais de trabalho. O próximo avanço R05 deve mirar coerência de fachadas e colisões, animação real de beings/chefes, design autoral de classes e chefes, opening final e Windows sob usuário comum, sem enviar testes fragmentados ao autor.


## R05 — quatro fachadas técnicas, direção nativa dos beings e bloqueio artístico (15/11/2026)

**Mesmo produto V1: PRODUCT_NO_GO / ART_REVIEW_PENDING.** Não promover o estudo geométrico como produto acabado.

- [Drive R05 completo, 317 arquivos](https://drive.google.com/file/d/1nbRdNSH8vOQiWFfMEm5ZLDLi-v08wFmd/view) — 71.105.665 bytes; SHA-256 local e7e194033c018e602fce0e5c2b0304a03390ccbd779d5e574506b2235cf04c3c. CRC/sha individuais verificados localmente; metadados do Drive confirmaram pasta/tamanho, hash remoto binário NÃO realizado. R00–R04 originais mantidos.
- [source-r05/](source-r05/) contém **27 arquivos de delta efetivo**, preservando [source-r04/](source-r04/) como base histórica; nove arquivos críticos coincidiram exatamente em readback no GitHub. Não duplicamos os 279 arquivos R04 no PR.
- **Owner C++20 ABI5**: novas consultas PURAS de footprint/âncoras das três construções (todas as células já bloqueadas como tile=9 no R04) e orientação observável de quatro NPCs a partir de suas rotas existentes. Colisões, quests, boss telegraph, kits e progresso inalterados. C17 executado, WASM com ABI5; save local R05/version6 não interpreta journals anteriores.
- **Renderizador real:** quatro vistas do mesmo site/world.js em Skia CPU, com rumo do ator baseado no movimento aceito, não na câmera; NPCs usam rumo do owner e interpolação visual. **O estudo de arquitetura de 4 fachadas e 2 águas passou nos testes geométricos, mas ficou PIOR visualmente que as ilustrações R04. Foi REJEITADO para o jogo e não substituiu as casas na cena padrão.** Capturas internas R05_GAME_VIEW_0..3.png (arte ilustrada), R05_GEOMETRY_VIEW_0..3.png (modelo reprovado), R05_BOSS_1..3.png (telegraphs) no ZIP.
- **QA:** 197 testes Python; 121 ações nativas pareadas com WASM R05, mais regressões independentes R04 121/R03 121/R02 116/R01 100 em WASM; C17; SQLite 121 eventos/replay/negativos; 441 criações válidas (21 monoclasse, 420 duplas). Nenhuma classe, kit, chefe, NPC ou lore foi canonizado.
- **Resultado artístico:** imagem padrão R05 difere apenas 0,24%–1,30% dos pixels relevantes R04; geometria muda 5,88%–7,88% mas perde acabamento. Alteração de pixel não prova qualidade. **Não alcançamos o salto visual solicitado.** A geração de novas artes falhou; material promocional não foi usado como screenshot de gameplay. Quatro fachadas ilustradas, gait/rig, chefes finais, opening, Windows e MMO continuam pendentes.

Fontes: [R05_COMPOSED_DELTA](source-r05/docs/R05_COMPOSED_DELTA.md), [R05_VISUAL_AUDIT](source-r05/docs/R05_VISUAL_AUDIT.md), [R05_TEST_REPORT](source-r05/artifacts/R05_TEST_REPORT.json). R05 é revisão de integridade/autoridade com **NO-GO artístico explícito**. Próxima frente deve produzir fachadas e animação próprias multivista antes de ampliar o catálogo.


## R06 — ciclos derivados, B02 espectral de laboratório e quatro vistas (15/11/2026)

**Mesmo produto composto, sem autorização de teste autoral: PRODUCT_NO_GO / ART_REVIEW_PENDING.**

- Pacote integral R06 Drive: https://drive.google.com/file/d/1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT/view (92.955.749 bytes; 429 arquivos; SHA256 local cc94c5da05ffd446943aa8cbb30420ce20a7bba894ce206607e68920aade6008). CRC e SHA de todos os membros verificados localmente; Drive confirmou nome/tamanho/pasta, não redownload binário. R00–R05 preservados.
- Delta textual R06 nesta mesma branch: [source-r06/](source-r06/), 18 arquivos de renderização JavaScript, geração reprodutível Python, contratos/testes/relatórios. 8/8 arquivos críticos tiveram readback exato. Fontes anteriores R04/R05 intactas.
- Um único owner C++20/C17 permanece core/world_r05.cpp ABI5, sem alterar regras ou versão de save. **205 testes Python PASS**; C17 real PASS; 121 intenções C++↔WASM; regressões R04=121, R03=121, R02=116, R01=100; SQLite 121 eventos e replay/negativos.
- **Motion studies no renderizador real:** 48 quadros derivados de NPC (4 seres ×4 direções ×3 deformações), 18 de bosses e 16 estudos de B02 derivados de arte de NPC #4. Quatro vistas +3 bosses +4 momentos da mesma vista executados via Canvas Skia CPU; GIF temporal no pacote. Deformações observacionais, **não rigs ou arte final**.
- **Não houve avanço estético substancial da cena estática:** R05→R06 registrou 0,004–0,011% de pixels alterados nas vistas equivalentes; quadros consecutivos 0,535–0,816%; boss B02 0,969%. Variação de pixels NÃO é nota estética. Nenhum boss foi canonizado.
- **BLOQUEIO REAL:** a geração de fachadas ilustradas four-facing falhou; preservados os billboards R04 e rejeitada novamente a geometria feia R05. Nenhuma abertura cinematográfica final ou build Windows/browser. ART_REVIEW_PENDING / PRODUCT_NO_GO.

Detalhes: [R06_COMPOSED_DELTA](source-r06/docs/R06_COMPOSED_DELTA.md), [R06_VISUAL_AUDIT](source-r06/docs/R06_VISUAL_AUDIT.md), [R06_TEST_REPORT](source-r06/artifacts/R06_TEST_REPORT.json). Próximo R07 deve priorizar arte original das quatro fachadas e animações convincentes, antes de solicitar teste humano do RPG.


## R07 — renderizador observacional + gate de arte 4-fachadas (15/11/2026)

**ART_BLOCKED_FACADES / PRODUCT_NO_GO. NÃO há ZIP integral R07.** A folha de 12 pinturas originais (3 edifícios ×4 orientações) não foi produzida: a ferramenta de geração de arte falhou e não foi repetida. A qualidade ainda não justifica outro pacote de 100 MB; o último completo continua sendo [R06 no Drive](https://drive.google.com/file/d/1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT/view).

- [source-r07/](source-r07/) contém 17 arquivos de delta real: iluminação, sombras e fumaça ligadas à projeção do mundo, seleção fail-closed de fachadas, contrato JSON, validação física SHA/alpha/dimensões, 3 renderizadores Skia de teste e QA. **12/12** arquivos críticos relidos com igualdade exata.
- **Prova:** 215 testes Python, 44 asserções Node sobre autorização/direção/repetição/hashes, consumidor C17 ABI5, 121 ações C++ ↔ WASM, regressões R04=121/R03=121/R02=116/R01=100 e SQLite 121 eventos, 4 imagens de mundo +3 chefes +4 temporais produzidas pelo Canvas real em Skia CPU. Nenhuma autoridade JS para combate ou NPC.
- **Evidência artística negativa:** R06→R07 só 0,0933% / 0,1050% / 0,1003% / 0,2226% dos pixels modificados acima do limiar por vista. Não comprova salto visual. Edifícios continuam com a mesma pintura R04 em todos os ângulos; geometria R05 reprovada não voltou. Nenhuma classe, boss, lore ou rig foi canonizado.
- **Política de promoção:** quatro arquivos físicos *distintos por construção*, hash distinto confirmado do arquivo real, transparência, mesma âncora, fonte/direitos, quatro vistas renderizadas e AUTHOR_ART_APPROVED explícito. Até lá, **R04_FALLBACK**. O validador não concede aprovação por conta própria.

Arquivos de prova: [R07_COMPOSED_DELTA](source-r07/docs/R07_COMPOSED_DELTA.md), [R07_VISUAL_AUDIT](source-r07/docs/R07_VISUAL_AUDIT.md), [R07_TEST_REPORT](source-r07/artifacts/R07_TEST_REPORT.json).

**Não solicite teste humano, não faça merge, não apresente mockup como gameplay.** Próximo incremento deve gerar/obter arte original de 12 vistas e chefes autorais coerentes, integrar no renderer e comprovar qualidade comparando as quatro vistas; sem isso, manter NO-GO e não ocupar mais espaço na biblioteca.


## R08 — importador de atlas 3×4 e rejeição de cópias; arte ainda bloqueada (15/11/2026)

**ART_BLOCKED_FACADES / PRODUCT_NO_GO. Sem novas pinturas e sem ZIP integral.** A geração de imagem falhou nesta operação e não foi repetida. A folha R04 tem uma única vista por construção; a pasta VEA de recuperação foi listada (17 filhos diretos, sobretudo arquivos de código/interop), sem atlas de 12 vistas identificado. O conteúdo interno dos ZIPs VEA não foi exaurido, então a busca não prova inexistência global.

- [Delta R08 real (7 arquivos)](source-r08/), na mesma branch e PR rascunho #3, **7/7 arquivos relidos com correspondência exata**. tools/import_fourview_atlas_r08.py só aceita folha pintada RGBA de **3 linhas ×4 colunas** e recorta 12 vistas sem espelhamentos, inventar pixels ou sobrescrever arquivos. Emite ART_CANDIDATE_UNREVIEWED, com direitos e aprovação em aberto. tools/fourview_inspector_r08.py detecta suspeita de versões apenas espelhadas, giradas ou recoloridas apesar de hashes diferentes, inconsistências de âncora, transparência, SHA e origem. Heurística não prova originalidade nem concede autorização artística.
- **234 testes Python** (215 históricos+19 novos), 44 checagens Node, C17 ABI5, 121 ações C++/WASM com paridade, regressões independentes R04 121 / R03 121 / R02 116 / R01 100 e SQLite 121 ações/replay. O mesmo Canvas real do site/world.js foi renderizado em Skia CPU. **7 screenshots reais** (4 vistas+3 chefes) são **idênticos pixel a pixel ao R07**. Dez fontes/assets históricos foram comparados por SHA-256: iguais.
- **0/12 fachadas ilustradas prontas.** Nenhuma mudança visual foi integrada ao gameplay, nenhuma nova animação ou arte autoral de boss, nenhuma homologação de 21 kits. A validação perceptual pode ter falsos positivos/negativos; somente inspeção humana em quatro ângulos e confirmação de direitos podem encaminhar a arte ao autor.
- Último pacote integral continua [R06 no Drive](https://drive.google.com/file/d/1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT/view). Para aplicar a pesquisa R08, usar uma **cópia R06** + source-r07 + source-r08; não fazer merge nem distribuir jogo prematuro. R07/08 são deltas de código; a main está intacta.
- Evidência: [R08_ART_INTAKE_AND_AUDIT](source-r08/docs/R08_ART_INTAKE_AND_AUDIT.md), [R08_TEST_REPORT](source-r08/artifacts/R08_TEST_REPORT.json), [verify_r08](source-r08/tools/verify_r08.py).

O próximo gate deve focar **criar ou recuperar artes originais de quatro perspectivas** e inspecionar o resultado dentro do renderizador, antes de abrir nova frente de código ou gerar outro pacote integral.


## R10 — 12 pinturas originais candidatas em quatro vistas, integradas à prévia real (15/11/2026)

**Avanço artístico material, mas ainda não aprovado pelo autor nem PRODUCT_GO.** Três novas folhas 2x2 ilustradas para casa, forja e botica foram geradas nesta conversa, totalizando 12 perspectivas pintadas; recortadas em atlas 3x4 e 12 arquivos WEBP RGBA 640x640 com hashes distintos. Nenhuma perspectiva foi criada por rotação, espelhamento ou recoloração da mesma fachada.

- Arte candidata e evidências no Drive: https://drive.google.com/file/d/1UFkYT8YdRMvawM1PNDZ0cRlluUDPz47W/view — 25.204.151 bytes, 32 arquivos, SHA-256 local 9c13d78fc4afe14ed3fb3d75b24c58b43e5834e44a1c2bd9eb40ca66e632f853. CRC e SHA-256 de cada entrada conferidos localmente; Drive readback por tamanho/pasta, não hash de redownload. Não é ZIP integral de jogo.
- [source-r10/](source-r10/) contém 10 arquivos textuais reais, 10/10 verificados por leitura posterior. site/world.js possui flag de **prévia interna** NSR10ArtPreview, desativada por padrão, e sempre marca a imagem como ART CANDIDATE - NOT APPROVED. Sem esta flag, a cena reproduz exatamente os 4 screenshots anteriores, e o gate oficial NSFacadeR07 continua intacto.
- Renderização real do próprio site/world.js em Skia CPU: quatro quadros de 1200x760 nos ângulos 0/90/180/270. Diferença em pixels por vista versus R07: 4,7041 / 5,5599 / 4,8991 / 5,7510% no limiar RGB médio >18. Mudança não é nota artística. Câmera não mudou posição/revisão do C++.
- Testes: 240 Python unittest PASS; 44 Node checks, ABI5 C17 recompilada e executada, 121 ações C++/WASM, regressões R04 121/R03 121/R02 116/R01 100, journal SQLite 121 eventos, owner e WASM preservados por SHA256.
- O inspetor R08 registra 12 arquivos físicos distintos e âncoras consistentes, porém **BLOCKED para aprovação** por direitos/proveniência, escala e inspeção humana. Fachadas, personagens, bosses, kits e opening final não homologados. Zero das 12 pinturas com AUTHOR_ART_APPROVED.

Reproduzir somente em cópia isolada de R06 + deltas R07/R08/R10 + assets do pacote candidato; nunca sobrescrever histórico nem fazer merge antes da aprovação. Ver [R10_ART_AND_INTEGRATION](source-r10/docs/R10_ART_AND_INTEGRATION.md) e [R10_QA](source-r10/artifacts/R10_ART_QA_REPORT.json).


## R11 — revisão artística real e prévia 4 vistas (15/11/2026)

**Três folhas refinadas, 12 candidatas, ZERO aprovações.** O R11 parte de três novas folhas geradas na conversa para cottage, forge e apothecary. Cada uma contém quatro perspectivas pintadas. São tratadas como imagem-fonte, nunca como screenshot do jogo.

- **Drive:** https://drive.google.com/file/d/1hz4YoQdZGq2H4nNBZlrC8vXMGrj6KOTp/view — `MMAI_PRODUCT_V1_R11_ART_CANDIDATE_DELTA.zip`, **37.221.947 bytes / 46 arquivos**, SHA-256 local `d4191a85bb57c4c0b081a2745792646a101d91d008a036dff68187e834e96820`. CRC e SHA256 de cada membro PASS localmente; tamanho/pasta confirmados no Drive, **hash remoto binário NÃO conferido**. **Não é duplicação integral do jogo**.
- **Fonte revisável:** [source-r11/](source-r11/), oito arquivos textuais (site/world.js, preparação das imagens, verificador QA, runners Skia, manifesto SHA e auditoria); **8/8 readback exato** contra o delta. O ZIP armazena as três fontes PNG, as doze novas imagens de fachada PNG+WebP, atlas e renderizações.
- **Arte técnica:** preparação alfa dos respingos vermelhos e fundos, pivô de solo comum por edifício, quatro perspectivas distintas sem rotação/espelhamento da mesma vista; 12 WEBP RGBA de 640×640, hashes únicos. Os edifícios da prévia são apresentados com escala ilustrativa maior e luz/sombra já existentes. A consistência de porta, chaminé, banca e dimensões entre vistas ainda exige revisão artística; **nenhum rig, malha 3D ou contrato de direitos foi homologado**.
- **Jogo efetivo:** `site/world.js` com flag **exclusivamente interna** `NSR11ArtPreview=true`, OFF por padrão e explicitamente legendada `R11 ART CANDIDATE · NOT APPROVED`. A via normal mantém o R07 AUTHOR_ART_APPROVED gate e fallback original: **4/4 renderizações idênticas pixel a pixel ao R10** quando desligada. A câmera gira 0°, 90°, 180°, 270° sem alterar revisão ou coordenadas no C++.
- **Evidências executadas:** 240 Python unittest PASS; 44 verificações Node de contrato; C17 ABI5 executável real PASS; C++20↔WASM **121** eventos, regressões históricas R04=121/R03=121/R02=116/R01=100; SQLite R05 121 eventos; **4 capturas Skia reais** do próprio renderizador com imagens R11. Comparação R10→R11: **5,6367%, 6,2005%, 5,4107%, 5,9292%** de pixels modificados acima do limiar RGB L1 médio>18 por ângulo. **Diferença de pixels NÃO equivale a ganho estético ou aprovação.**
- **Gates preservados:** arte/copyright/escalas/arquitetura pendentes de revisão humana do autor; 21 kits e três bosses não canônicos; opening, being rigs, Windows, browser, MMO e roteiros finais ainda insuficientes. `PRODUCT_NO_GO / ART_REVIEW_PENDING`; nenhum merge na `main`, alteração em Makers/MER/VEA/cânone ou convite ao autor para testar a build.

Leia [R11_ART_INTEGRATION_AND_GATES](source-r11/docs/R11_ART_INTEGRATION_AND_GATES.md) e [R11_TEST_REPORT](source-r11/artifacts/R11_TEST_REPORT.json). R06 integral, deltas R07/R08/R10 e todas as fontes históricas são preservados.


## R12 — anchor de silhueta e animação visual na câmera real (15/11/2026)

**PRODUCT_NO_GO / ART_REVIEW_PENDING. Novas pinturas: ZERO; 12 pinturas R11 candidatas intactas.** A nova geração de imagens falhou e não foi repetida. Portanto, incoerências pintadas de porta, chaminé e telhado NÃO foram solucionadas; apenas aspectos técnicos de escala, âncora de solo e iluminação foram alterados em modo interno.

- Drive R12 delta/evidências, sem cópia integral: https://drive.google.com/file/d/1J_39TF4-IMsvZJE1o2fqyPoDtHBeLFwq/view — 27.176.073 bytes, 37 arquivos; SHA-256 local c613c99a2abe2821d941bac0f80d4dd945a090a13cf6550533274f854bd61803; CRC e SHA dos 37 membros PASS local, Drive readback de tamanho e pasta, hash remoto binário não refeito. Base R06 e artes R10/R11 preservadas.
- Fonte R12: [source-r12/](source-r12/) contém 15 arquivos de código/teste/contratos, 15/15 verificados por leitura posterior. site/r12_asset_anchors.js, site/r12_finishing.js, site/world.js, medição física das 12 silhuetas RGBA, testes C++/Canvas e QA. A flag NSR12VisualLab=true é laboratório opt-in; OFF, quatro telas pixel a pixel idênticas ao fallback R11. Nenhuma pintura final foi promovida para o cliente normal.
- O que o jogo real renderiza: site/world.js em Skia CPU alinha as 12 perspectivas pelos pixels pintados, normaliza dimensão aparente por edifício e posiciona sombras de contato/luz local. Beings e 3 boss-fixtures têm *timing* visual de inclinação/bob e brilho de antecipação, observando boss_intent e boss_pattern da ABI5, sem alterar regras/dano/alvo, sem rigs. As células vermelhas de ataque continuam usando somente o predicado C++ nsw_wasm_boss_threatens.
- QA executada: 251 Python PASS, 44 Node herdadas+67 Node próprias; consumidor C17 ABI5 compilado e executado; C++20/WASM R05 121 ações e regressões R04=121/R03=121/R02=116/R01=100; SQLite 121 eventos. 18 quadros Skia reais: 4 vistas +4 fallback +6 de três boss (dois tempos) +4 temporais de beings. Quatro fallback idênticos ao R11. Delta visual R11→R12 7,6294 / 8,4766 / 7,2896 / 7,8478% de pixels acima do limiar RGB>18. Mudança não é aprovação estética.
- Gates: cinema final, rig/direção de arte, direitos, consistência quatro fachadas, 21 kits e boss identidades canônicos, Windows/Chromium/GPU e multiplayer ainda ausentes/não verificados. Não propor teste autoral nem merge.

Reprodução: extrair R06 numa cópia, aplicar R07/R08/R10/R11 e por último R12; rodar python3 tools/verify_r12.py. Fontes: [R12 visual audit](source-r12/docs/R12_VISUAL_AND_ENGINEERING_AUDIT.md) e [R12 test report](source-r12/artifacts/R12_TEST_REPORT.json).


## R13 — direção visual de três bosses no Canvas real (15/11/2026)

**ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO.** Geração de nova arte falhou uma vez (não repetida): R13 **não** criou fachadas refeitas, sprites inéditos ou rigs. As 12 pinturas R11, C++20 ABI5, WASM e SQLite continuam idênticos por SHA.

- **R13 delta compacto de 8.040.234 bytes (19 membros):** https://drive.google.com/file/d/119YYYpy2cwlgx0IS7l_8zNkoHJ_YIMWo/view — SHA-256 local 559df77c0a4c18837aecbefbb90360e90a42be5a41110a07c6f4e8a2202ff229; CRC e hash de cada entrada verificados localmente, metadados tamanho/pasta lidos no Drive, **redownload/hash remoto binário NOT_RUN**. Sem ZIP integral duplicado.
- **Código:** [source-r13/](source-r13/) nove arquivos de delta, 9/9 conferidos exatamente em readback. site/r13_stagecraft.js desenha três linguagens gráficas visuais (B01 metal/âmbar; B02 espectro/violeta; B03 raízes/verde), placa nominal de combate e foco visual deslocado 30% em direção ao boss **somente com NSR13ArtLab=true**. São sprites R06 apenas ampliados e ornamentos em Canvas, não novos personagens. Nenhum valor de hitbox, dano, posição ou quest é criado no JavaScript; as células de perigo ainda são C++ nsw_wasm_boss_threatens.
- **Teste executado:** 251 Python unittest do R12 em cópia R13, 44+67 verificações Node herdadas, 26 Node novos da arte pura, ABI5 C17 executada, 121 ações atuais C++↔WASM e 458 ações históricas R04=121/R03=121/R02=116/R01=100; journal 121 eventos. Quatro cenas sem chefe e seis frames de três confrontos renderizados pelo próprio site/world.js em Skia CPU, não em Windows. Revisão e coordenadas autoritativas permaneceram constantes ao desenhar.
- **Comparação visual:** versus R12, 21,15%–25,95% dos pixels de cada cena de boss foram alterados sobretudo por reenquadramento, escala e ornamentos; **não** é medida de beleza. Quatro vistas sem chefe alteraram somente 0,148% (etiqueta de prévia), logo **arquitetura não foi corrigida**. OFF, 4/4 frames do cliente padrão continuam idênticos aos R12. Sem arte nova, sem aceite artístico, sem release.
- **Bloqueios:** fachadas 4 vistas ainda incoerentes/sem ACK; novos rigs e autoria de três chefes pendentes; 21 kits de pesquisa não homologados; opening final, Windows/Chromium/GPU e MMO não aprovados. Main, Makers, MER, VEA, C02 e obras independentes preservados.

Detalhes: [R13_ART_DIRECTION_AND_GATES](source-r13/docs/R13_ART_DIRECTION_AND_GATES.md) e [R13_TEST_REPORT](source-r13/artifacts/R13_TEST_REPORT.json). Prioridade seguinte: ARTE ORIGINAL e animação por partes autorais, não novos ornamentos sobre imagens antigas.
