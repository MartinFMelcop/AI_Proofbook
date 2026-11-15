# R07 — Auditoria do renderizador real (Skia CPU)

## Metodologia

Mesmo projeto `site/world.js`, mesmo snapshot C++ ABI5, mesma sequência inicial de ações e mesmas dimensões de 1200×760. Renderizados ângulos 0°/90°/180°/270° e cenas de bosses B01/B02/B03. Comparação com os PNGs históricos R06 do mesmo pacote. O novo JavaScript de atmosfera não possui funções para alterar owner, WASM, journal ou missões.

| Ângulo | R06 fonte | R07 novo | Delta de pixels significativos |
|---|---|---|---:|
| 0° | `artifacts/R06_GAME_VIEW_0.png` | `artifacts/R07_GAME_VIEW_0.png` | 0,0933% |
| 90° | `artifacts/R06_GAME_VIEW_1.png` | `artifacts/R07_GAME_VIEW_1.png` | 0,1050% |
| 180° | `artifacts/R06_GAME_VIEW_2.png` | `artifacts/R07_GAME_VIEW_2.png` | 0,1003% |
| 270° | `artifacts/R06_GAME_VIEW_3.png` | `artifacts/R07_GAME_VIEW_3.png` | 0,2226% |

Critério numérico: média absoluta RGB dos 3 canais superior a 18 por pixel. Os percentuais não avaliam aparência, gosto, densidade, continuidade de personagem, correção de lado nem qualidade de animação. **Não comprova melhoria visual substancial**.

## Defeitos ainda reconhecidos

- Casas/forja/boticário permanecem billboards R04 mostrando a mesma perspectiva, independentemente da orientação do mundo. Quatro ilustrações distintas por construção **não produzidas**.
- Fachadas rígidas do R05 haviam sido tecnicamente orientáveis, mas artisticamente reprovadas; não foram reintroduzidas.
- Movimento de NPCs e bosses R06 são deformações de sprites, não ciclos 2.5D de rig/arte final.
- Áreas de perigo dos bosses vêm de C++ ABI5; silhouettes e identidade definitiva ainda não foram aprovadas.
- Tela-título e opening: animatic de 18 segundos, sem nível final de anime/cinema; não foi modificado aqui.
- Iluminação e sombra R07 são observacionais e ilustrativas; falta validação de custo no GPU, acessibilidade e oclusão em hardware Windows.

**Gate** `ART_BLOCKED / PRODUCT_NO_GO`. Não solicitar teste autoral, não publicar como RPG final, não homologar classes/chefes/quest/Rave Masters por inferência.
