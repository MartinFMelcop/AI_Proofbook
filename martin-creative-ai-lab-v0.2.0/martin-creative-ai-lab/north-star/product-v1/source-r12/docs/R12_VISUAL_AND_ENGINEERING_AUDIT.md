# MMORPG Maker AI — PRODUCT V1 R12 | integração visual e evidência

**Estado: ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO.** Nenhuma atualização de canonical lore, classe, boss, Maker, MER, VEA ou branch main.

## Origem, reprodução e limites

- Base integral R06 Drive `1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT`; aplique em cópia isolada os deltas R07 e R08, arte R10 Drive `1UFkYT8YdRMvawM1PNDZ0cRlluUDPz47W`, arte R11 Drive `1hz4YoQdZGq2H4nNBZlrC8vXMGrj6KOTp`, e por último estes arquivos R12. Não sobrescrever nenhum pacote de origem.
- O desenho de novas fachadas e rig/arte de bosses não foi produzido: a chamada de imagem falhou e não foi repetida. As **12 pinturas R11 originais foram preservadas bit a bit**. Diferentes portas/telhados/chaminés ainda requerem revisão visual e correção de arte, licença e ACK.
- O código `tools/measure_r12_facade_alignment.py` mede o bbox da silhueta alfa de cada fachada R11 e gera `site/r12_asset_anchors.js` e `art_sources/R12_SILHOUETTE_ALIGNMENT.json`. Isto mede apenas imagem, **não inventa colisão, paredes ou cômodos**. `site/r12_finishing.js` ajusta dimensões aparentes por orientação, contato de solo e reflexos de luz; `site/world.js` consome isso **somente** sob `NSR12VisualLab=true`, desligado por padrão. `site/index.html` carrega os módulos em ordem, sem ativar a flag.
- Personagens e chefs usam sprites históricos com movimento temporal visual limitado (cabeça/corpo como imagem única, inclinação/impulso, bob e diferentes brilhos que observam `boss_intent`/`boss_pattern` do C++). **Não são skeletal rigs nem movimentos pintados finais**. A ameaça real permanece exclusivamente no predicado `nsw_wasm_boss_threatens` consultado pelo renderizador; não há segunda autoridade JS.

## Evidências de execução reais

- Linux CLI: `python3 tools/verify_r12.py` retorna 251 unittest Python PASS; 44 asserts Node R07 + 67 Node R12 PASS; ABI5 C17 compilada/executada PASS; eventos C++20↔WASM R05=121; regressões históricas R04=121, R03=121, R02=116, R01=100; SQLite R05 journal de 121 eventos verificado.
- Skia CPU real, executando `site/world.js` com ABI5 WASM e sprites originais: 4 vistas R12, 4 vistas fallback, 4 quadros temporais de beings e **2 quadros por boss = 6 quadros**. O relatório `artifacts/R12_TEST_REPORT.json` contém medição RGB e hashes, com posições/revisões idênticas após as rotações e frames. Não há execução Windows/Chromium/GPU nem afirmação de qualidade autoral.
- Imagem padrão com a flag OFF **idêntica pixel por pixel** ao fallback anterior nas quatro vistas. Modo R12 interno muda 7,29 a 8,48% dos pixels com limiar RGB>18 versus as imagens R11; mudança visual não prova melhoria estética.

## Gates R12

`ART_REVIEW_PENDING`, 12 fachadas candidatas e zero ART_APPROVED; 21 kits e bosses não canônicos, abertura apenas animatic 18s; rigs e identidades autorais ainda pendentes; direitos, qualidade final e Windows não verificados. `PRODUCT_NO_GO`. É necessário revisar os modelos e silhuetas com cuidado e criar desenhos corrigidos antes da promoção da arte; nenhum teste autoral de build ainda.
