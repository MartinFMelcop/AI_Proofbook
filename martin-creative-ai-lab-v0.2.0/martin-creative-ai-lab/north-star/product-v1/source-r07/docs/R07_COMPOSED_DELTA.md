# MMORPG Maker AI — North Star PRODUCT V1 / R07

**Data** 15/11/2026 · **Estado** `ART_BLOCKED / PRODUCT_NO_GO` · **Modelo de entrega** delta de código sobre R06, **sem novo ZIP integral**, por orientação expressa de evitar arquivos sem avanço artístico substancial.

## Base e proveniência

- R06 integral original: Drive ID `1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT`, SHA-256 local documentado `cc94c5da05ffd446943aa8cbb30420ce20a7bba894ce206607e68920aade6008`.
- Documento mestre V1: Google Doc `1HwKtQ3WLnCFEKMtjUN4cwYi0uRMQickM6SJHZNJkZPU`.
- HUB: PR draft #3, branch `mmai/product-v1-composite-20261115`.
- Alterações R07 são **somente cliente gráfico / teste / contrato de arte**. Core `world_r05.cpp` ABI5, C17 header, WASM, `opening_animatic.mp4`, assets originais R04 e persistência SQLite são idênticos aos de R06 (ver relatório hashes).

## Alteração efetiva implementada

1. `site/atmosphere_r07.js`: sombras de contato orientadas no mundo, quentes em volta das construções e fumaça de chaminé; câmera muda sua projeção mas não muda a direção geográfica da sombra. Passe discreto de névoa visual. Nenhuma autoridade de jogo, física ou gameplay no JavaScript.
2. `site/facades_r07.js` + `docs/R07_FACADE_ART_GATE.json`: contrato físico/visual para 12 obras distintas (casa/forja/boticário × 0/90/180/270). É obrigatório desenho diferente por fachada, direitos verificados, escala/âncora coerentes e ACK autoral explícito antes de trocar as imagens do R04. O estado atual é **ART_BLOCKED** porque a geração artística falhou nesta operação. Quatro cópias ou espelhamentos da mesma vista NÃO recebem aprovação.
3. `tools/validate_facades_r07.py`: confere nomes, hashes SHA-256 contra os arquivos reais, originalidade binária, dimensões, transparência, integridade e direitos declarados. Um `READY_FOR_HUMAN_VISUAL_REVIEW_ONLY` técnico ainda **NÃO concede autorização artística**.
4. `site/world.js`, `site/index.html`: ligação observacional das sombras e do seletor fail-closed à cena principal, mantendo pintura R04 para os três edifícios. Renderiza as mesmas quatro vistas e as três cenas de chefes. Não altera `core/world_r05.cpp`, regras, classes, quests, combate, NPCs, saves nem cinematic.

## Evidência realmente executada

- 215/215 Python unittest, incluindo 9 novos casos de frontend e 7 contraprovas físicas de assets.
- 44 assertions Node específicas de contrato, 4 vistas de sombra e fallback de arte. Falso `AUTHOR_ART_APPROVED`, arquivo ausente, hash repetido, classe inválida, escala/licença pendente ou arquivos com hash errado são rejeitados.
- C17 compilado/executado; R05 nativo C++20 vs WASM 121 eventos com paridade; R04 121, R03 121, R02 116, R01 100 históricos em suas próprias versões WASM; interface UI com 4 rotações. Journal SQLite R05 121 eventos verificado novamente.
- **Canvas verdadeiro do site/world.js em Skia CPU:** quatro vistas R07, três bosses R07 e quatro quadros temporais R07; não é browser Windows nem GPU real.
- Diferenças estáticas de pixels R06→R07 (L1 RGB médio > 18): 0° 0,0933%; 90° 0,1050%; 180° 0,1003%; 270° 0,2226%. **Não é nota artística.** Mudança visual sutil e fora do objetivo principal de quatro fachadas.

## Decisão e no-go

**Não existe salto visual de qualidade confirmado.** A folha original de quatro fachadas não foi gerada (ferramenta falhou e não foi repetida); não se disfarçou perspectiva repetida como vista nova. O R05 geometry study continua reprovado. Os três chefes continuam figurinos experimentais, classes seguem 21 fichas/441 pareamentos de pesquisa, NPCs não possuem rig aprovado, abertura segue animatic de 18 segundos. Windows, navegador normal, multiplayer e julgamento humano **NOT_RUN**.

Recomendação: NÃO criar nem distribuir outro ZIP integral nesta revisão. Publicar só o código delta na branch PR #3 e um registro aditivo de continuidade no Drive. Próxima etapa deve produzir quatro pinturas consistentes, 3 tipos de edifício, com autorização visual e revisão de assets, antes de qualquer release ou teste do usuário.

## Instruções para quem tem acesso técnico ao projeto

Com R06 íntegro e fontes delta R07 na branch do PR #3, aplicar os novos/alterados arquivos sobre uma **cópia** do R06, sem sobrescrever o arquivo Drive histórico, e executar `python3 tools/verify_r07.py`. Requer ferramentas da fase R06 (`g++`, `clang++ --target=wasm32`, `cc`, Python/Pillow/numpy, Node+skia-canvas). Nunca executar versões alteradas no Drive ou em `main`. Não contornar Smart App Control ou restrições do navegador.
