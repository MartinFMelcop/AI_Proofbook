# MMORPG Maker AI — Produto V1 composto (candidato interno)

**Data da decisão:** 15/11/2026. **Estado:** `INTEGRATED_CANDIDATE / ART_REVIEW_PENDING / PRODUCT_NO_GO`. O pacote contém um percurso integrado em preprodução, mas **não deve ser oferecido como jogo homologado ou nova demonstração ao autor** antes de cumprir os gates técnicos, de experiência e de qualidade artística.

## Declaração autoral vinculante

O autor recusou demos pequenas e visuais insatisfatórios. Para teste autoral de RPG, estabeleceu como condições: (1) marca de estúdio MMORPG Maker AI; (2) videoclipe de abertura artística; (3) title screen chamativa com Press to Start; (4) menus; (5) criação com identidade e até 2 entre 21 classes; (6) aventura inicial com exploração, atividades/profissões/skills, quests e três primeiros chefes; (7) **qualidade artística satisfatória de verdade**, não mera ausência de erro, e beings de comportamento característico de RPG. A abertura e o conteúdo devem satisfazer a identidade dark fantasy 2.5D e a política de câmera de quatro orientações `NS-CAM-4VIEW-001`. **Sem aceite humano de D/autor, a arte permanece candidata, mesmo quando o software funciona.**

## Direção técnica vigente

A decisão **C** do autor em 15/11/2026 estabelece engine própria como prioridade, com novos trabalhos Unity/C# interrompidos prospectivamente. Python + IA realizam orquestração, autoria, testes e pipeline; C++20 é núcleo nativo candidato; C17 a ABI; SQL via SQLite para experimentos isolados; PostgreSQL e DuckDB são pesquisas para casos futuros; Assembly somente após benchmark. O legado Unity/C#/Blender/Godot e VEA/Workbench permanece arquivado/inspecionável, não apagado. **M6-D07=A** em F5 escolheu Blender como candidato DCC no escopo do Workbench; isso não obriga uso de Blender no novo motor nem autoriza sua exclusão. A seleção final de biblioteca de renderização e infraestrutura multiplayer continua aberta.

## Fonte do conteúdo

**Combate:** `Combat Philosophies and Other Complements`, Google Doc `1hd8QM4x5aKP3gh6LnaedpbauHzMpFFZJM47N0-kBKY8`; R01 Soldier, R02 Dragon Slayer, R03 Berserker, R04 Rogue A, R05 Rogue B, R06 Knight, R07 Ranger, R08 Warrior, R09 Monk, R10 Battlemage, R11 Dark Mage, R12 Pyromancer, R13 Necromancer, R14 Esper, R15 Alchemist, R16 Cryomancer, R17 Bard, R18 Cleric, R19 Druid, R20 Sentinel, R21 Shaman. São **21 fichas/identidades e 20 chaves históricas**, com Rogue A/B no alias ROGUE. O alvo de 21 classes é direção autoral `A2-IDENTIDADE_QUANTIDADE=C`; **independência e habilidades definitivas permanecem não homologadas**. A seleção no criador é uma interface verificável, não concessão de kit funcional de 21 filosofias.

**Referência de aventura:** `GDD_Rave_Masters_v0_2_ptBR.md`, Drive `1Q3LwmkiD-p2gvw65756ZLk1bkNmJc32Z`, §§11 e 13. O **GDD Rave Masters é obra de origem separada, não conteúdo automaticamente canônico de North Star.** A sequência de referência traz estrada sul/ponte/rio, guarda e cão, líder, sete casas, Rose desaparecida, floresta/fadas/poltergeists, remédio e Árvore Guardiã enlouquecida como minichefe, seguida por nova semente e retorno de Rose. Também sugere backgrounds (10), profissões e criação mono/dual. Não identifica três chefes iniciais de North Star.

**Propostas de três confrontos** (não canonizadas):
- B01 `Vigia das Ruínas` — novo candidato, leitura de intenção e retirada; `PROPOSED_NOT_CANON`.
- B02 `Sussurro do Brejo` — novo candidato, observação/recuperação; `PROPOSED_NOT_CANON`.
- B03 `Árvore Guardiã` — **minichefe da obra Rave Masters**, preservado como referência histórica, `LEGACY_SOURCE_ONLY_NOT_NORTH_STAR_CANON`.

**Precedência:** C02 `103SZI0xfvsaJxb15FXpsJs7BpltzQCmfkP-UUCsqVas` e `1-VSJGFCjpv2jKHG_v1JsubtAKhVL_uSDzHxhTHosZws`; F5 `1O3CFRjHQBZV84DDZQa5gsXsnrl3aBJkslf6T5hzQ0LY`; F6 `1EhTn82WnDNI2QTKnY2XVNYWISc2laQp_B6Ny9AeLmYM`; F4 `1YMoX3AiFaqsw1AeOoHiBbuFqEpiQIHH2WIPn0hZMN3g`. Não editar versões antigas para fingir que já adotavam decisão C ou este capítulo.

## Composição produzida

Fluxo de cena no cliente `site/index.html` + `site/style.css` + `site/app.js`:
`splash (marca de estúdio candidata) → opening (animatic instrumental original de 18 s) → title/Press to Start → menu (Novo/Continuar/Opções/Créditos/Sair) → criação (nome, tratamento, background, uma ou duas fichas R01–R21) → eventos de chegada/ofício e três encounters mecânicos de laboratório → epílogo`.

Regras da fixture em `core/product.h/.cpp` compiladas para `artifacts/libns_product.so` e `site/product.wasm`; ABI C17. Receipts revisionados validam a ordem dos quatro gates, consumos, derrotas/retirada e três encontros determinísticos; **não implementam classes, skills, AI agents, profissões reais, combate North Star homologado, persistência MMO ou rede**. Browser UI apenas encaminha intenções e apresenta resultados. Save local utiliza `localStorage` com replay revalidado pelo mesmo core WASM, não autenticidade adversarial. Câmera com 4 valores implementada como controle de UI, **não é um renderer 2.5D quatro-vistas integrado**.

Os PNGs artísticos e logo são **estudos originais por IA**, com direção de texto observacional e aprovação humana pendente. `site/assets/opening_animatic.mp4`: **animatic de 18 s montado com quatro stills e trilha instrumental original sintetizada**, não opening anime animada final. Qualidade artística não foi avaliada pelo autor; evitar usar material promocional como prova de jogo real.

## Evidência e reprovação explicitamente preservadas

- `python3 -m unittest discover -s tests -p test_core.py`: 21 casos Python/C ABI passaram no Linux.
- `node tests/test_wasm.mjs`: sequência 3 encontros concluída em WebAssembly.
- Core nativo e WebAssembly: build C++20 e clang wasm32 verificadas no executor Linux.
- Arte/video: assets gerados localmente, vídeo H.264/AAC com duração 18 s via ffprobe. Não há aprovação da qualidade.
- Chromium/Playwright: **`net::ERR_BLOCKED_BY_ADMINISTRATOR`** em localhost; renderização interativa **NOT_VERIFIED**.
- Windows nativo, sistema de câmera 2.5D renderizada, interação de mundo, classes/skills, beings satisfatórios, experiência de exploração e 3 batalhas autorais: **NOT_IMPLEMENTED_AS_PROVEN / PRODUCT_NO_GO**.

## Gates necessários para promover a entrega

G0 — canonização separada de regiões/NPCs/chefes, mantendo legacy Rave e tipos de relação explícitos. G1 — asset style bible aprovada, consistência de personagem, cenário, animação e escala de gameplay nas quatro orientações. G2 — opening definitiva com animação original, áudio/mixagem/legibilidade/direitos e revisão do autor. G3 — criação de personagem com kit de 1–2 classes real, sem violar `A2=C` e Rogue gate; gameplay nativo e registros. G4 — cena nativa 2.5D, câmera de quatro vistas, colisões, NPC beings com comportamentos previsíveis, quests/profissões, três chefes com telegraph/contrajogo e QA; não aceitar apenas painéis narrativos. G5 — build Windows em usuário comum, proteção contra bloqueio, logs/diagnóstico, licence/proveniência, testes de regressão e experiência humana. G6 — contratos C/E/B/D e source anchors para resultado, memória, direito/material, apresentação/observação.

**Bloqueios preservados:** R51/R60/R61/INT-C01-001 OPEN, RP-R03-P03 e RP-G02-A03 PENDING, C29/C30 STOP_DOCUMENTARY_PENDING_OWNER e ACK C/E/B não obtidos; Arena S1 HOLD, C05-P01–P07 e Rave contents PENDING_CANON; F5/VEA 737 críticas (45 investigação, 692 pendentes), quatro vistas da fonte V1-D02=B; nenhum Maker, MER, VEA, F0–F6, obra independente ou dado sensível foi modificado por este artefato.

**Publicação:** registro de progresso e código em branch/PR de HUB, documento complementar no Drive, e um ZIP técnico único com manifesto/hash; **não é um release de jogo para aceitação autoral**.

## REV R01 — Native spatial implementation (15/11/2026)

The same composed V1 package now contains `core/world.cpp/.h` (single C++20 owner with C17 ABI for a 24x20 world), `site/world.js` (camera-rotated Canvas isometric projection), player traversal, a real river/bridge collision boundary, world anchors with proximity-checked interactions, deterministic NPC patrols, herb collection and remedy crafting, and three mechanical boss encounters with target telegraph, guard, potion, skill fixture and retreat. All three encounters can be completed through 100 validated, spatially legal native actions; the field-level replay is identical between Linux C++ and WASM. The legacy nsp engine stays isolated in an archival binary; the playable `product.wasm` exports only world owner functions. SQL is used in an independent Python/SQLite hashed fixture journal, not the browser save backend.

**Technical evidence:** 60 Python unittest PASS, 100-action native/WASM parity PASS, Canvas+DOM simulated drawing and camera-rotation regression PASS, 18-second animatic source maintained. **PRODUCT_NO_GO** remains for art quality, game feel, 21 specialized kits, truly expressive beings and boss AI/art, authored quest writing, real browser rendering, Windows build and human quality review. Details: `docs/R01_SPATIAL_DELTA.md`, `artifacts/R01_TEST_REPORT.json`. No new canonical status is inferred from these tests.
