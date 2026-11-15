# MMORPG Maker AI — Virgo Diamond: The North Star · PRODUCT V1 / R01

**One composed preproduction work package — NOT a finished RPG, not an author-approved test candidate.** `ART_REVIEW_PENDING / PRODUCT_NO_GO`.

### Composed flow

Studio logo → original 18-second opening animatic → animated Press to Start → main menu/options → 21 historical class profiles (one or two selected) → genuine 24×20 navigable isometric experiment → NPC interactions, stateful herb gathering and remedy craft → three spatial encounters with telegraphed opponent turns → experimental epilogue.

**Original owner:** `core/world.cpp` C++20 with a C17 ABI; compiled to `site/product.wasm`. The old `core/product.cpp` is built separately for regression tests only. No new Unity/C# development. The 4 quarter-turn camera transformations are a graphics consumer and **never alter world state**. `site/app.js` cannot grant quests or combat outcomes; it forwards validated commands and replays a journal through WASM.

### Rebuild and regression (verified on Linux, NOT Windows)

```bash
sh tools/build.sh
python3 -m unittest discover -s tests -p 'test_*.py' -q
python3 tests/generate_world_trace.py
node tests/test_world_wasm.mjs
node tests/test_world_ui.mjs
node tests/test_wasm.mjs # archival product.cpp regression only
python3 tools/spatial_journal_sqlite.py verify artifacts/world_lab_fixture.sqlite
```

The HTML client requires a trusted, local HTTP server for `product.wasm`; its user-facing Windows viability is **not verified** and the author should **not** be asked to test this unfinished slice. Do **not** circumvent Windows Smart App Control, browser administrative restrictions, or security policies.

### Status boundaries

- `60/60 Python PASS`, native-versus-WASM 100-action parity PASS, Canvas/DOM simulation PASS, SQLite provenance integrity PASS.
- **Not** visually approved. Opening is a motion comic, not final animation. Character art in four views is generated concept art with a removed white background, not a finished rig or spritesheet. Three bosses are mechanics fixtures; their designs and AI are not approved.
- Not 21 class kits, not the MMO, not native Windows, not Steam, not multiplayer. Browser rendering on Windows: `NOT_RUN`. Chromium test in this executor remains `BLOCKED_BY_ADMINISTRATOR`.
- Camera RCT2-style quarter-turns are now applied to terrain, player, NPCs and props. Occlusion/readability/animation under human supervision remains open.

For exact file/provenance/evidence and gate details see `docs/PRODUCT_V1_DELIVERABLE.md`, `docs/R01_SPATIAL_DELTA.md` and `artifacts/R01_TEST_REPORT.json`.

**Historical authorship preserved:** The 21 profiles and separate Rave Masters GDD are only source references. No class, region, NPC, boss, skill, profession or imported narrative is automatically canon for North Star. No Makers, MER, VEA, original C02, independent works or GitHub main were modified in the isolated build.

## R02 — incremento do MESMO entregável, não nova demo

A revisão R02 mantém integralmente splash, opening animatic original, tela-título, menus, criador e prólogo do R01, mas troca o cliente para a **ABI2** (`core/world_r02.cpp`, `site/product.wasm`) preservando todos os owners anteriores para regressão. A classe primária ou secundária agora pode acionar um dos **21 modos de laboratório**, cada qual com efeitos condicionais, sem insinuar 21 kits canônicos. Mineração → fundição → melhoria de ferramenta, conversas NPC por proximidade e padrões diferenciados de três encounters compõem as expansões da mesma jornada. O save localStorage recebe `version=3` (recusa migração muda de R01); Python/SQLite transacional é **apenas laboratório**, independente do save real.

`site/world.js` aplica quatro projeções de câmera, sprite sheet conceitual 4×4, nove materiais raster procedimentais e visualização do estado limitado dos beings. Quatro frames reais do renderizador em Skia headless foram produzidos como *artefatos internos* e revelaram problemas artísticos ainda relevantes. O código C++/WASM foi testado, mas **não existe aprovação estética, animação final, build Windows nem experiência MMORPG homologada**.

### Reproduzir R02 no ambiente de desenvolvimento

```bash
python3 tools/build_r02_hero_assets.py
python3 tools/build_r02_materials.py
python3 tools/build_r02_class_catalog.py
python3 tools/verify_r02.py
```

Pré-requisitos observados no executor Linux: `g++`, `clang++ --target=wasm32`, `cc` C17, Node 22, Python 3, Pillow, ffprobe e skia-canvas para frames. **Nenhuma configuração de Smart App Control, PowerShell ou assinatura deve ser contornada.**

Proveniência, demonstrações de negativo, distinção entre 21 modos versus 21 kits e limites estão em `docs/R02_COMPOSED_DELTA.md` e `artifacts/R02_TEST_REPORT.json`. O único lugar de continuidade do source é a revisão R02 completa, não testes enviados avulsos. `PRODUCT_NO_GO / ART_REVIEW_PENDING`.

## R03 — mesma entrega composta, novo conjunto de fontes (15/11/2026)

**Estado: `PRODUCT_NO_GO / ART_REVIEW_PENDING`.** O site agora usa **ABI3 `core/world_r03.cpp` / `site/product.wasm`**, sem apagar ABI1/ABI2. C++/C17 aplica, com recibos revisados, duas técnicas e uma passiva experimental para cada uma das 21 fichas; em classe dupla, a segunda contribui com um efeito mais fraco na abertura do combate. **Não** representam 21 kits aprovados, armas canônicas nem habilidades homologadas. Os NPCs recebem quatro sprites ilustrados de orientação (`npc_1..4_0..3.webp`), animação ambiente limitada e memória curta de contato no estado do owner; não são beings aprovados ou uma IA social autônoma.

Novos materiais de solo (45 variantes de 9 tipos) reduzem a grade rígida; quatro screenshots Skia verdadeiros do renderizador atual estão em `artifacts/R03_SKIA_VIEW_0..3.png`. A vila **ainda não está bonita o suficiente** para a revisão autoral: poucos edifícios, chefes sem arte in-game e pouca expressividade. A opening original de 18s continua animatic; nenhum vídeo novo foi homologado. Não solicite que o autor jogue o R03.

**Execução comprovada neste Linux:** `132/132` testes Python, 121 intenções C++↔WASM evento a evento; regressões WASM R02 116/R01 100; consumidor C17; SQLite 121 eventos e contraprovas; quatro vistas Skia. Windows e navegador real NOT_RUN; ART_REVIEW_PENDING. Detalhes de origem e bloqueios em `docs/R03_COMPOSED_DELTA.md`, visuais em `docs/R03_VISUAL_AUDIT.md`, políticas de being em `docs/R03_BEINGS_BOUNDARIES.json` e `artifacts/R03_TEST_REPORT.json`.

```bash
sh tools/build.sh
python3 tests/generate_world_trace_r03.py
python3 tools/verify_r03.py
```

A atualização do jogo foi isolada em `MMAI_PRODUCT_V1_R03_WORK`. R02, PR #3, Drive e `main` somente recebem operações aditivas, autorizadas e auditadas. Não há upgrade automático de save de R02 para R03; a nova chave de `localStorage` e `version=4` recusam migração implícita.

## R04 — incremento aditivo, laboratório de arte + perigo autoritativo

O **mesmo** fluxo Produto V1 usa agora `core/world_r04.cpp` (ABI4 C17 / WASM32), mantendo ABI1–3 compilados separadamente para regressão. O canvas real usa nove assets conceituais adicionais de vila, ponte e flora (recibos de origem+SHA), e três estudos de chefe in-game com oclusão parcial. A área de perigo desenhada agora usa a função **pura do owner C++** `nsw_wasm_boss_threatens` (também utilizada no cálculo de dano), preservando câmera de quatro quartos de volta sem escrever no estado. Os 21 kits de pesquisa originais e beings limitados do R03 continuam, mas não são canônicos/aprovados.

Evidência Linux reproduzida: **167 casos Python**, C17 ↔ C++20 ABI4, **121 intents nativos ↔ wasm** com paridade de ameaças e estado, **121/116/100** eventos de regressão R03/R02/R01, SQLite 121 eventos, quatro renderizações Skia + três renderizações de chefes e comparação de pixels R03→R04. Veja `docs/R04_COMPOSED_DELTA.md`, `docs/R04_VISUAL_AUDIT.md`, `artifacts/R04_TEST_REPORT.json` e screenshots reais (não promocionais).

**PRODUCT_NO_GO / ART_REVIEW_PENDING.** Não pedir teste ao autor; Windows/browser, classes canônicas, qualidade de animação/chefes, abertura final e autoridade multiplayer permanecem não homologados. Save de laboratório usa chave própria e version5 sem migração silenciosa dos históricos.
