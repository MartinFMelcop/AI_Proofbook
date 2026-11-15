# MMORPG Maker AI — North Star PRODUCT V1 / R04

**Status: ENGINEERING_LAB_PASS · ART_REVIEW_PENDING · PRODUCT_NO_GO**  
**Data:** 2026-11-15 · **Escopo:** evolução aditiva do mesmo entregável composto R00–R04.

## Fontes e precedência

- Baseline MMAI C02 no Drive: `103SZI0xfvsaJxb15FXpsJs7BpltzQCmfkP-UUCsqVas`; documento mestre do Produto V1 `1HwKtQ3WLnCFEKMtjUN4cwYi0uRMQickM6SJHZNJkZPU`.
- Combat Philosophies `1hd8QM4x5aKP3gh6LnaedpbauHzMpFFZJM47N0-kBKY8`: 21 perfis R01–R21; nenhum kit homologado e Rogue A/B sem independência aprovada.
- GDD Rave Masters v0.2 `1Q3LwmkiD-p2gvw65756ZLk1bkNmJc32Z`: referência **independente**; Árvore Guardiã é minichefe daquela obra, não chefão canonizado de North Star.
- R03 completo Drive `1gV0_gPI9P_7sQ7UWZt4lnKSAF0CYJklB`; PR draft #3, branch `mmai/product-v1-composite-20261115`.
- Direção autoral C: engine própria C++20 / C17 / Python+IA / SQL, sem novos trabalhos específicos para Unity ou C#.

## Mudanças executadas

1. **Cena gráfica real, não mockup.** O `site/world.js` herdado de R03 agora consome nove novos sprites isolados de arquitetura/vegetação: casas em madeira e pedra, forja, boticário, ponte ornamentada, lampião, fonte, árvore florida, árvore antiga e santuário. Posições visuais declaradas em `PROP_POS`. Assets novos vêm da folha `art_sources/r04_architecture_sheet.png` gerada para este incremento; cortes com transparência, hashes e tamanhos em `docs/R04_ARCHITECTURE_ASSET_RECEIPTS.json`. Props são **billboards da câmera**, não malhas com quatro facetas autênticas; não alegar four-view art pass.
2. **Três adversários visualizados na gameplay real.** B01 recebe um conjunto de quatro variações derivadas da arte de NPC R03, B02 um espectro procedural, B03 árvore com transformação visual distinta da vegetação comum. Recibos em `docs/R04_BOSS_ASSET_RECEIPTS.json` e `docs/R04_GUARDIAN_RECEIPT.json`. Identidades/mecânicas continuam *fixtures* não canônicas, sem rig, animação final ou autoria de encounter aprovada.
3. **Telegraph C++ autoritativo.** `core/world_r04.cpp`/`core/world_r04.h` expõem ABI4, `nsw_boss_threatens` e `nsw_boss_threat_radius`, com equivalentes WebAssembly. A regra de alcance usada pelo cálculo de dano agora é a MESMA consultada para a máscara de perigo desenhada pelo Canvas. Consulta é pura; não incrementa revisão, não desloca player, não concede ataque/quest. Sem duplicar raio de ataque em JavaScript. O visual pinta os tiles em risco mesmo com câmera girada.
4. **Oclusão revisada para combate.** Props de cenário próximos a um chefe em combate são atenuados ou omitidos visualmente; nenhuma colisão ou estado da simulação muda. Novos móveis não são indicadores de colisão; caminhos/colliders permanecem no mapa C++ R03/R04. Este descompasso visual ainda exige correção antes de PRODUCT_GO.
5. **Save versionado.** Somente client local recebe `mmai_ns_product_v1_r04_save` / versão 5, sem importar/alterar saves R01–R03. Journal SQLite C++ ABI4 próprio de laboratório, separado de persistência real de servidor.

## Evidência reproduzível no executor Linux

- `sh tools/build.sh`: C++20 nativo (biblioteca Linux) e WASM32 freestanding. Interface C17 real: `artifacts/c17_abi_r04` PASS.
- `python -m unittest discover -s tests -p 'test_*.py' -q`: **167/167 casos PASS**, incluindo auditoria R04 de retorno puro, dano conforme tile, alcance 1/2, coordenadas inválidas e negativa ABI.
- `python tests/generate_world_trace_r04.py` e `node tests/test_world_r04_wasm.mjs`: **121 intents** nativos vs WebAssembly, valores de estado, NPCs, raio e quatro pontos de ameaça comparados a cada revisão. Replays separados para R03 **121**, R02 **116**, R01 **100** ações sem alteração das fontes históricas.
- `python tools/create_r04_journal_fixture.py`: arquivo novo SQLite gerado somente após preflight `create=True` não sobrescreve existentes. `Ledger.verify` passou com 121 eventos, UID idempotente, detecção de adulteração e isolamento de sessões.
- `node tests/render_world_skia_r04.mjs`: **quatro screenshots 1200×760** com o **site/world.js real**, em Skia CPU; `node tests/render_r04_bosses_skia.mjs`: **três screenshots de encontros realmente ativados por trace C++**; a função de render não modifica estado.
- `artifacts/R04_VISUAL_COMPARISON.png` dispõe a captura verdadeira do R03 ao lado da captura verdadeira R04, ambas obtidas do mesmo renderizador. Diferença por pixel (L1 médio RGB > 18) **17,82%**. Não é métrica de qualidade estética ou autorização de lançamento.
- `artifacts/R04_TEST_REPORT.json` registra os checks e SHA-256 das fontes. Histórico R03 comparado por SHA em seis arquivos relevantes.

## Não implementado / gates intactos

- **ART_REVIEW_PENDING:** pouca densidade na borda externa do mapa, assets 2D de orientação fixa, escala ainda inconsistente, animação apenas interpolação/bobbing, sombra/oclusão limitada, bosses conceito sem rigs/múltiplas animações, ainda não satisfaz a direção de arte definida pelo autor.
- **21 classes:** há pesquisa funcional assinatura+auxiliar+passiva herdada do R03, NÃO kit canônico de 21 classes nem integração definitiva com Maker/skills/equipamentos.
- **Beings:** comportamento contextual limitado herdado do R03, não NPCs plenamente escritos/animados e aprovados; owner de observação por NPC pendente.
- **Abertura audiovisual:** mantém animatic de 18 s, NÃO a opening anime final.
- **Windows standard-user, navegador real, server multiplayer, performance, direitos e arte humana:** NOT_RUN/NOT_APPROVED.
- **Chefões:** B01/B02 propostas, B03 Rave Masters histórico; nenhum chefe/bioma/arma/habilidade foi canonizado por inferência.
- **Bloqueios históricos:** R51/R60/R61/INT-C01-001 OPEN; C30 STOP_DOCUMENTARY_PENDING_OWNER, RP-R03-P03 / RP-G02-A03 PENDING, Arena S1 HOLD, C05-P01–P07 OPEN e ACK owners C/E/B/D preservados. `main` GitHub intocada.

## Próximo incremento R05 recomendado

Aprofundar os **consumidores visuais reais**: movimento em quadros próprios (hero, 4 NPCs, bosses) e oclusão/colisão alinhada ao mundo C++; ampliar a vila e biomas com contratos e AAs de origem; aumentar qualidade dos três encontros sem canonizar identidades; garantir pipeline de vídeo com avaliação artística real; preservar o único pacote integrado e manter NO-GO até gate visual/autoral.
