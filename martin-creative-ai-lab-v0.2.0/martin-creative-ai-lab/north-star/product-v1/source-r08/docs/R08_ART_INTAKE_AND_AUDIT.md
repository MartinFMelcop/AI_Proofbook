# MMORPG Maker AI — North Star · PRODUCT V1 / R08

**Data:** 15/11/2026. **Estado:** `ART_BLOCKED_FACADES / PRODUCT_NO_GO`. **Entrega:** delta de fonte na branch do mesmo PR #3, sem novo ZIP integral nem build para o autor.

## A tarefa artística e sua consequência concreta

O objetivo era produzir ou recuperar **12 pinturas distintas**: três construções (casa, forja e boticário) × quatro orientações geográficas correspondentes à câmera estilo RCT2 (90°). A geração de imagem falhou nesta operação. A geração não foi repetida e **0/12 pinturas** estão disponíveis. Inspecionou-se o `art_sources/r04_architecture_sheet.png` original: ele contém somente uma perspectiva ilustrada de cada um dos três edifícios, mais outras seis peças distintas. **Não** pode ser recortado, rodado ou espelhado para simular as perspectivas ausentes.

A pasta de recuperação VEA ID `1YnCuJBiLPUIdZkozt4FC_Gi_K9JoKr3S` foi listada diretamente (17 filhos): códigos, ZIPs de recuperação e interoperabilidade, manifestos. Não havia arquivo de arte de 12 vistas explicitamente identificado entre esses filhos; conteúdos internos dos ZIPs e subpastas NÃO foram inspecionados exaustivamente, então não se pode alegar inexistência global.

## Incremento efetivo R08, não produção de arte

1. `tools/fourview_inspector_r08.py`: inspeção **heurística** dos 12 candidatos, depois da checagem física R07. Busca cópias rotacionadas/espelhadas/recoloridas (similaridade estrutural em oito simetrias), presença de quatro pinturas físicas por construção, dimensões/alpha/hashes, posição da base no canvas, origem e direitos. Detecta *fortes suspeitas* de reutilização; não pode provar autenticidade nem coerência artística. Em caso de suspeita, bloqueia promoção e solicita revisão humana.
2. `tools/import_fourview_atlas_r08.py`: importador **não destrutivo** de uma folha RGBA verdadeira 3 linhas ×4 colunas com transparência, ordem declarada (casa, forja, boticário) × (0°,90°,180°,270°). Recorta 12 sprites WEBP sem rodar nem inventar pixels, cria recibos SHA-256 e um `R08_CANDIDATE_MANIFEST.json` sempre marcado `ART_CANDIDATE_UNREVIEWED`, direitos e ancoragem **não verificados**, sem `AUTHOR_ART_APPROVED`. Exige proveniência e recusa sobrescrever destino. Células vazias, grades incompatíveis e cortes que atravessam bordas são rejeitados.
3. `tests/test_r08_fourview_inspector.py` e `tests/test_r08_fourview_import.py`: 19 contraprovas com arte geométrica de **fixture sintética EXCLUSIVAMENTE para teste de código**, não candidata para o produto. Verificadas cópias sob espelho, recolor e metadados diferentes, ancoragem, hashes falsificados, RGB opaco, formatos e cortes inválidos, licenças pendentes, atlas R04 não autorizado e recusa de sobrescrita.
4. `tools/verify_r08.py` recompila/reroda verificação nativa R07, inclui as 19 novas contraprovas e confere que **7 screenshots reais Skia do jogo e 10 fontes/artefatos históricos R07 permanecem idênticos**. O cliente, animação, regras C++/C17, WASM, arquivos de save e combate não foram modificados pelo R08.

## Evidência executada e limites

- 234 testes Python unittest PASS (215 históricos +19 R08).
- 44 asserções Node de contrato/fallback de quatro vistas PASS.
- Consumidor C17 ABI5 PASS; 121 eventos C++20↔WASM com paridade; regressões R04 121, R03 121, R02 116, R01 100, journal SQLite 121 eventos/replay PASS.
- Quatro vistas e três chefões renderizados pelo `site/world.js` real em Skia CPU + quatro momentos de animação. **Sete screenshots de mundo/chefes R08 coincidiram pixel a pixel com R07**. Portanto **nenhuma melhoria artística de gameplay foi realizada no R08**.
- Windows usuário comum, browser humano, GPU, FPS, rig final, abertura final e multiplayer permanecem NOT_RUN/NOT_APPROVED.

**NENHUM resultado de software concede `AUTHOR_ART_APPROVED`.** A checagem heurística é auxiliar e pode ter falsos positivos/negativos; a revisão humana das fachadas, do estilo, da escala e da leitura nas quatro vistas permanece indispensável. O importador não obtém direitos de uso por si só.

## Continuidade e precedência

O R06 integral de 92.955.749 bytes permanece no Drive ID `1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT`. R07 e R08 são deltas de fonte sobre uma cópia do R06, na mesma branch `mmai/product-v1-composite-20261115` do PR rascunho #3. Não há justificativa para gerar outro ZIP integral e poluir a biblioteca. Manter `PRODUCT_NO_GO`, `ART_BLOCKED_FACADES`, estados históricos/ACKs R51/R60/R61/INT-C01-001, C30, RP-R03-P03/RP-G02-A03, Arena S1 HOLD e C05-P01–P07. Preservados main, C02, Makers/MER/VEA e outras obras, sem canonização de três chefões ou das 21 classes.

**Próximo consumidor necessário:** receber as doze pinturas originais (ou recuperá-las de fonte com proveniência/autorizações demonstráveis), importar como candidato, inspecionar visualmente o resultado na câmera de quatro vistas e só então decidir se um novo pacote integral representa avanço real.
