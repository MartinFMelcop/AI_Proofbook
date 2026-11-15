# North Star PRODUCT V1 — R05 · execução composta, sem aprovação de arte

**15/11/2026 | ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO**

## Fontes e precedência

Este trabalho é uma cópia aditiva **do pacote R04 efetivamente compilado e testado** (`Drive 1tU1Tk6g7JshWv5IGlUdLx7-gTf0f-zif`; SHA-256 `89eb4a57c1c6dfb912c7c1a9d8afc2ac8bc272f8710cab5a3cc93efcc54e9656`). Preserva todas as revisões R00–R04. Autoridade documental do produto: Drive `1HwKtQ3WLnCFEKMtjUN4cwYi0uRMQickM6SJHZNJkZPU` e draft PR #3 no HUB. Fichas R01–R21: Combat Philosophies Drive `1hd8QM4x5aKP3gh6LnaedpbauHzMpFFZJM47N0-kBKY8`. Rave Masters Drive `1Q3LwmkiD-p2gvw65756ZLk1bkNmJc32Z` é obra independente.

Decisão autoral C: priorizar C++20/C17/Python+IA/SQL, sem novos trabalhos específicos Unity/C#. As quatro orientações de câmera permanecem requisito autoral com quartos de volta de 90°; não são quatro mundos distintos. Nenhum owner C/E/B/D respondeu ou autorizou transformação do cânone por esta operação.

## Contribuição de engenharia R05

**ABI5:** `core/world_r05.cpp` e `core/world_r05.h` foram derivados exclusivamente de R04 e compilados em biblioteca Linux e WASM. O estado de gameplay, regras de quest/boss/kit e as trajetórias anteriores não foram alterados. Foram acrescentadas **consultas puras**, sem revisão/ação:

- `nsw_structure_at(x,y)` mapeia as três construções existentes para IDs 1–3 apenas nas células `nsw_tile==9` já bloqueadas (casa 10×7–9; forja 17×8–9; boticário 20×10–11).
- `nsw_structure_x/y(id)` fornece pontos de ancoragem únicos consumidos pelo cliente — sem um segundo mapeamento autoritativo de edifícios no JS.
- `nsw_being_facing(id,tick)` infere direções observáveis das rotas existentes. Um NPC parado recebe orientação estável, não uma ação fictícia. O cliente traduz esse rumo para a orientação da câmera, com interpolação apenas visual, partículas emocionais discretas quando o C++ realmente indica atenção/preocupação/alerta e nenhuma mutação de `world_tick`.
- O avatar passa a conservar a direção da última movimentação aceita pelo núcleo. Rotacionar a câmera não reescreve a direção do mundo.
- Save R05 é isolado em `localStorage` versão 6; R04 versão 5 preservada, sem migração presumida.

**Fachadas:** `site/architecture_r05.js` implementa volumes de 4 paredes/2 águas de telhado projetados por `NSCamera4`. A prova gera quatro orientações geometricamente distintas e se ancora nas células que o C++ já bloqueava. Entretanto, o protótipo procedural teve desempenho visual **pior** que os edifícios ilustrados R04. Decisão de qualidade R05: **não promovê-lo à cena padrão**; conservar os sprites ricos R04 enquanto a geometria é consumida somente em verificação interna (`NSArchitecturePreviewMode`). Não declarar quatro fachadas desenhadas, modelagem final ou ART_PASS. A tentativa de geração de novas artes falhou tecnicamente e não foi repetida nesta operação.

**Chefes e kits:** todas as regras de chefes, telegraphs e 21 kits de laboratório são as mesmas verificadas no owner R04. Reexecutar as ações com ABI5 comprova regressão, **não valida três chefes canônicos ou 21 kits balanceados**. Foram aceitas 21 opções monoclasse e 420 pares ordenados de duas classes. Duplicatas e IDs fora do intervalo são recusados. Nenhum ID de habilidade canônica foi inventado.

## Execução comprovada localmente (Linux)

- 197 Python unittest PASS; consumidor C17 compilado e executado com libns_world_r05.so.
- 121 ações R05 na biblioteca nativa C++20 e em WebAssembly com recibos e campos equivalentes; nova observação de direção validada em cada evento.
- Regressão independente WASM R04=121, R03=121, R02=116, R01=100 ações.
- Journal SQLite separado, versão 5: 121 eventos e hashes encadeados/replay; recusa de reabrir fixture para criação; negativas de UID, adulteração e revisão herdadas da suíte.
- 4 renders de cena do mesmo `site/world.js` usando Skia Canvas CPU, 4 renders internos de volumes e 3 renders de boss com risco C++ e sem modificar o estado.
- 9 fontes R04 conferidas por SHA256 idêntico, incluindo C++, sprites R04 e opening de 18 segundos.
- Comparação com R04: 0,24%–1,30% de pixels significativamente modificados na cena preservada; a geometria experimental difere 5,88%–7,88% dos pixels. **Isso é alteração de imagem, não melhora ou métrica estética.**

## NO-GO e próximos gates

O R05 **não alcançou um salto artístico suficiente**. Casas R04 ainda são billboards nas quatro perspectivas na cena padrão; volumes 4 faces são planos sem materiais ricos. Faltam locomoção autoral completa em quatro ângulos, fachadas pintadas em cada orientação, densidade de cidade e interiores, biome blending, personagem e três chefes com arte final, combate e habilidades autorais, opening cinematográfica final e build Windows para usuário comum. Browser real e servidor MMORPG também não foram executados.

Nada de canonizar B01/B02, Árvore Guardiã, 21 kits, regiões, classes ou NPCs; Rogue A/B com independência estrutural não aprovada. R51/R60/R61/INT-C01-001 OPEN; RP-R03-P03/RP-G02-A03 PENDING; C30 STOP_DOCUMENTARY_PENDING_OWNER; Arena S1 HOLD; C05-P01–P07 OPEN. Nenhuma alteração em Makers, MER, VEA, Unity, obras independentes ou `main`.

Fontes/testes: `tools/verify_r05.py`, `artifacts/R05_TEST_REPORT.json`, `tests/test_world_r05.py`, `tests/test_r05_class_contract.py`, `tests/test_world_r05_wasm.mjs`, `tests/test_architecture_r05.mjs`, `site/architecture_r05.js`, `artifacts/R05_GAME_VIEW_0..3.png` e `R05_GEOMETRY_VIEW_0..3.png`, `artifacts/R05_BOSS_1..3.png`.
