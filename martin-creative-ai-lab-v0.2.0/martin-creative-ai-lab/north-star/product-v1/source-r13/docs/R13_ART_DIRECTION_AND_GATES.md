# MMORPG Maker AI — North Star PRODUCT V1 / R13

**Data:** 15/11/2026  
**Estado:** `ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO`  
**Continuidade:** R06 jogo integral → deltas R07/R08/R10/R11/R12 → delta R13 em cópia isolada. Mesmo C++20/C17 ABI5 e mesmo draft PR #3.

## Resultado verificável

A tentativa de criar novas imagens por ImageGen nesta operação falhou, e não foi repetida. Portanto, **nenhum sprite novo, nenhuma pintura corrigida de casa/forja/botica, nenhum rig e nenhuma arte canônica foram produzidos**. As 12 vistas da arquitetura R11 continuam intactas, com a situação de direitos/coerência visual pendente.

Houve avanço de **direção de arte de combate diretamente no jogo**: o novo módulo `site/r13_stagecraft.js`, inteiramente observacional, cria para cada confronto C++ uma composição específica:

- **B01 / Vigia das Ruínas:** círculo de guarda fraturado, gravuras de metal e faíscas âmbar; silhueta original R06 ampliada.
- **B02 / Sussurro do Brejo:** filamentos espectrais e partículas violetas, contorno iluminado; o mesmo sprite histórico de laboratório, não uma nova criatura desenhada.
- **B03 / Árvore Guardiã:** seis raízes pintadas proceduralmente sob a base, motes e brilho verde; identidade narrativa histórica separada de Rave Masters não canonizada em North Star.

O novo foco da câmera se desloca em **30% no sentido da posição do chefe devolvida pelo C++** apenas quando o laboratório gráfico R13 está ativo. O enquadramento mais próximo, o aumento das silhuetas e as placas de nomes melhoram a leitura dos confrontos nas capturas comparativas. A posição, o dano, o alcance, a ordem de turnos, a prioridade, as quests e os kits **não** são calculados no JavaScript. Todas as células de perigo seguem exclusivamente `nsw_wasm_boss_threatens` do C++.

## Comparação honesta

Reexecutados o próprio `site/world.js`, WASM ABI5, Canvas Skia CPU e fixtures de confrontos verdadeiramente aceitos. A diferença frente ao R12 nas cenas de cada boss, acima de RGB L1 médio >18, foi de aproximadamente **21,15–21,25%** (B01), **21,60–21,62%** (B02), **25,80–25,95%** (B03), em grande parte pelo **reenquadramento da câmera**. Não é medida de aprovação artística. As **quatro vistas sem chefe** diferem do R12 em ~0,148% pela faixa de aviso do laboratório, portanto **não houve melhoria das fachadas**. O cliente padrão, com a flag desligada, mantém 4/4 frames de fallback idênticos aos R12.

Os 6 frames R13 dos 3 chefes são amostras de apresentação (2 tempos cada), **não** sprites novos ou animação skeletal. A comparação `MMAI_R13_R12_BOSS_COMPARISON.jpg` coloca a captura real anterior à esquerda e a nova à direita.

## Regressões e rastreabilidade

- `python3 tools/verify_r12.py` executado na cópia R13 antes do fechamento de identificação R13: **251 unittest Python**, **44 + 67 checks Node**, consumidor **C17 ABI5 real**, **121** ações atuais pareadas C++/WASM, regressões **R04=121 / R03=121 / R02=116 / R01=100**, journal SQLite de **121 eventos**.
- `node tests/test_r13_stagecraft.mjs`: **26 checagens PASS**, inclusive sem chamadas que executem ações autoritativas.
- `node tests/render_r13_fourview_skia.mjs`: quatro vistas reais sem chefe; `node tests/render_r13_boss_stage_skia.mjs`: seis frames dos 3 chefes reais; a revisão e a posição C++ permaneceram invariantes durante renderização.
- `python3 tools/verify_r13.py`: auditoria incremental de integridade e diferenças visuais PASS, incluindo 18 arquivos intocados (C++/WASM, SQLite e 12 pinturas R11).
- Testes de Windows comum, Chromium/GPU, performance em hardware real, opening final, MMORPG online, autoria dos personagens e quality gate humano: **NOT_RUN/NOT_APPROVED**.

## Reproduzir

1. Extrair R06 em pasta isolada; aplicar fontes R07, R08, R10, R11, R12 na ordem. Manter as imagens R11 em `site/assets/world/` e os frames históricos R12 para comparação.
2. Aplicar o delta textual R13 `source-r13/` nessa mesma cópia do produto. **Não** aplicar diretamente sobre os históricos do Drive/HUB.
3. Ativar apenas no executor de laboratório `globalThis.NSR13ArtLab=true` e carregar `r13_stagecraft.js` antes de `world.js`. Sem a flag, o cliente de jogo permanece anterior.
4. Executar `node tests/test_r13_stagecraft.mjs`, `node tests/render_r13_boss_stage_skia.mjs` e `node tests/render_r13_fourview_skia.mjs`. Configurar `MMAI_R12_BASELINE_PATH` para uma cópia **não modificada** do R12 e executar `python3 tools/verify_r13.py`. Requer `skia-canvas`, Node 22+, Python 3.11+, Pillow, NumPy e toolchain de C++/C17, além do ambiente já preparado pelos incrementos anteriores.

## Gates preservados

`PRODUCT_NO_GO`; `ART_REVIEW_PENDING`; 0/12 pinturas R11 aprovadas; B01/B02/B03 experimentais, sem identidades autorais fechadas; sem sprites originais e sem rigs R13; 21 kits de pesquisa sem homologação; opening permanece animatic; Windows/Chromium não rodados. R51/R60/R61, INT-C01-001, C30 STOP_DOCUMENTARY_PENDING_OWNER, RP e Arena HOLD, e gates dos owners C/E/B/D continuam intactos. Nada na `main`, Makers, MER, VEA, C02 ou lore independente foi alterado.
