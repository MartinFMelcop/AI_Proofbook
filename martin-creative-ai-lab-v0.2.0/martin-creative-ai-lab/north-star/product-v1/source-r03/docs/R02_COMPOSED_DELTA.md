# NORTH STAR — PRODUCT V1 / R02 — Implementação composta

**15/11/2026 · `INTERNAL_PREPRODUCTION` · `PRODUCT_NO_GO` · `ART_REVIEW_PENDING`**

A revisão R02 prolonga o mesmo produto: splash da empresa → opening motion-comic original de 18s → Press to Start → menus → criador com 21 perfis R01–R21 (até duas classes) → mundo isométrico com câmera de 4 quadrantes → exploração, NPCs, ervas e ofícios → 3 encontros experimentais. Não é uma build aprovada para teste autoral; nenhum componente isolado representa o MMORPG.

## 1. Execução comprovada

- `core/world_r02.cpp` + `.h`: **ABI C17 versão 2**, núcleo C++20, sessões independentes, legalidade de movimentação, herança do mapa de 24×20, colisões e progressão R01, com três formas de melhoria mecânica:
  - **21 modos de técnica de laboratório** endereçados pelos IDs de perfis históricos R01–R21, com custos e consequências diferentes e escolhas primária/secundária por intenção `type=8,value=0|1`. Baseados nos princípios conceptuais da fonte, **não equivalem a 21 kits completos nem skills canônicas**.
  - **Profissões experimentais**: mineração perto do nó (8) → fundição perto da bancada (9) → upgrade de ferramenta até grau 2, com materiais e XP. A melhoria tem efeito observável no ataque básico. Não importa receitas Maker nem modifica bancos oficiais.
  - **Beings de laboratório**: quatro agentes com `repouso/patrulha/atenção/trabalho/preocupação/alerta`, estados limitados por localização, fase e rotina; interação autoritativa apenas em proximidade. Não possuem memória pessoal, conversação rica, comportamento aprovado ou IA generativa implantada.
  - **Três confrontos** com telegraph, defesa, deslocamento, janela de recuperação, alcance e políticas distintas: Vigia das Ruínas (golpe/feint), Sussurro do Brejo (zona e desgaste de SP), Árvore Guardiã (raio/raízes por fase). Todos **não canônicos**; B03 é uma fonte histórica de *Adventures Unleashed: Rave Masters*, não o chefe aprovado de North Star.
- `site/product.wasm`: um único `world_r02.cpp` como autoridade do cliente; `core/world.cpp`, `core/product.cpp` e seus artefatos R01 permanecem intactos e compilados **somente para regressão**, sem duplicação de owner no jogo.
- `site/world.js`: quatro projeções de 90° que não mudam gameplay; pré-carregamento de 16 poses de um personagem e nove materiais tile; apresentação de NPCs e kits. O renderer continua **Canvas isométrico 2D**, NÃO motor gráfico próprio final GPU/3D, nem qualidade artística homologada. Occlusão de objeto usa transparência visual sem afetar visibilidade de gameplay.
- `site/classes_r02.js`, `docs/R02_CLASS_RESEARCH_BINDINGS.json`: 21 perfis/cores/princípios com fonte por Drive ID. A pesquisa de Rogue A/B continua estruturalmente não homologada. Informações exibidas como propostas de teste.
- `tools/world_r02_ledger.py`: ponte Python/SQLite de laboratório com recibos por UID, gravação transacional, replay determinístico em C++, hashes encadeados, isolamento por sessão e recusa de adulteração. **NÃO é o save persistente do cliente** (navegador mantém journal localStorage de versão 3 separado), nem banco de servidor ou MER.

## 2. Evidências efetivamente executadas

`python3 tools/verify_r02.py` em executor Linux:

- **101/101 casos `unittest` Python PASS**, incorporando regressões R00/R01, 21 modos com subtestes, C++ spatial/quest/profissões e cenários negativos do journal; contagem de casos não mede maturidade das 21 classes.
- `cc -std=c17 -Wall -Wextra -Werror` compila cliente C17 e invoca biblioteca nativa C++20 ABI2 (PASS).
- Trace R01 preservado: 100 ações/estado nativo e WASM histórico PASS.
- Trace **R02: 116 ações** reais incluem grupo mono/dual, mineração, fundição, melhoria de ferramenta, ervas, banco, boss1/2/3 e epílogo; cada estado foi confrontado campo a campo com WebAssembly, além de comportamentos NPC por ação. PASS.
- **4 frames reais de Canvas em Skia headless** a 0°,90°,180°,270°, via `site/world.js`, com pixels distintos. **Não é Chromium nem prova de FPS/performance/render final**.
- Banco SQLite de laboratório: 116 eventos consecutivos, hash encadeado e `integrity_check=ok`; testes negativos de adulteração/UID/atomicidade. PASS.
- 16 imagens WEBP de pose, 9 materiais WEBP; decodificação e dimensões verificadas. A qualidade de sprites, animação, quatro perspectivas e scene dressing NÃO foi aprovada.
- Opening H.264/AAC = 18 segundos, arquivo legado preservado exatamente por SHA-256. A opening final de qualidade anime ainda NÃO existe.
- Compatibilidade Windows e navegador real **NOT_RUN**, devido a ausência de executor apropriado e bloqueio administrativo prévio; nenhuma política de segurança foi contornada.

`artifacts/R02_TEST_REPORT.json` contém status testados e SHA-256 das principais fontes. `artifacts/R02_SKIA_VIEW_*.png` são evidências internas de lookdev e não capturas de navegador nem imagens de divulgação.

## 3. Fontes e autoridade — sem canonização indevida

- MMAI C02, Drive `103SZI0xfvsaJxb15FXpsJs7BpltzQCmfkP-UUCsqVas`, e MASTER `1-VSJGFCjpv2jKHG_v1JsubtAKhVL_uSDzHxhTHosZws`: dark fantasy 2.5D e direção autoral, não implementação pronta.
- Combat Philosophies, Drive `1hd8QM4x5aKP3gh6LnaedpbauHzMpFFZJM47N0-kBKY8`: princípio pesquisado e paleta histórica dos 21 perfis; `A2-IDENTIDADE_QUANTIDADE=C`, Rogue A/B independência estrutural não comprovada; gates A3/A4 ainda separados.
- Rave Masters `1Q3LwmkiD-p2gvw65756ZLk1bkNmJc32Z`: estrada, guarda/cão, sete casas, Rose, ervas, fadas e Árvore Guardiã na **obra de referência**. **Não** descreve três chefes North Star nem transfere cânone.
- Direção autoral C: novos trabalhos na engine própria C++20/C17/Python+IA/SQL, sem Unity/C# novo. NS-CAM-4VIEW-001: quatro orientações; inclinação e oclusão final aguardam QA.
- F5 `1O3CFRjHQBZV84DDZQa5gsXsnrl3aBJkslf6T5hzQ0LY`, F6 `1EhTn82WnDNI2QTKnY2XVNYWISc2laQp_B6Ny9AeLmYM` e VEA preservados.

## 4. Gates objetivos antes de pedir teste autoral

1. **ART:** cenário coerente, sete casas como proposta de conteúdo e não cópia, pisos/ambiente de alta qualidade, personagens e beings com expressão, animação verdadeira, sombras, iluminação e consistência *nas quatro vistas*. **Os renders atuais ainda têm tiles repetitivos e NPCs geométricos: ART_REVIEW_PENDING.**
2. **OPENING:** videoclipe artístico/anime com duração, ritmo, composição, música/mix e direitos aprovados; animatic de 18s NÃO atende.
3. **CLASSES:** kits reais das 21 classes e regras mono/dual adjudicadas, sem transformar automaticamente os 21 modos experimentais em cânone; diferenciabilidade de Rogue A/B e 63 cores ainda não fechadas.
4. **BEINGS:** NPC com identidade, rotinas legíveis, percepção autorizada, memória e consequências sem vida artificial excessiva; comportamentos atuais são apenas estados pequenos e determinísticos.
5. **BOSSES:** três chefões do universo **North Star** aprovados e arte/rig/telegraphs/balanceamento/contrajogo testados; B01/B02 propostos, B03 legado separado.
6. **ENGINE:** cliente nativo Windows de usuário padrão, renderizador/asset importer próprio, saves reais, acessibilidade, desempenho, segurança, distribuição e multiplayer futuramente.
7. **OWNERS:** C/E/B/D ACK identificável e precedência, direitos, R51/R60/R61/INT-C01-001 OPEN, RP-R03-P03/RP-G02-A03 PENDING, C30 `STOP_DOCUMENTARY_PENDING_OWNER`, Arena S1 HOLD, C05-P01…P07 OPEN, VEA e F5 condicionantes.

A aprovação de engenharia é insuficiente para `AUTHOR_ART_APPROVED` ou `PRODUCT_GO`. Esta revisão não foi solicitada para teste ao autor.
