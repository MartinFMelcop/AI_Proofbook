# MMORPG Maker AI — PRODUCT V1 R11 | Multivista ilustrada — laboratório

**Status:** `ART_CANDIDATE_NOT_APPROVED / PRODUCT_NO_GO`. Não é release, build ou solicitação de teste autoral.

## Continuidade concreta

Base imutável: pacote integral R06, depois deltas R07/R08/R10 no mesmo PR #3. R11 acrescenta três novas folhas 2×2 produzidas na conversa: casa, forja e botica. Cada folha contém quatro representações pintadas da mesma construção. O consumidor real continua `site/world.js` e o owner permanece `core/world_r05.cpp` (ABI5 C++20 com interface C17/WASM). Não houve qualquer alteração de RF/RNF/HU, classes, NPC owner, quest, colisão, regras dos chefes ou cânone.

Preparação reproduzível: `tools/prepare_r11_refined_sheets.py` separa cada quadrante sem espelhar ou rotacionar; remove respingos de fundo próximos das silhuetas, suaviza exclusivamente a borda e reposiciona os 12 desenhos em células RGBA 640×640 com um único pivô de chão. Preserva folhas-fonte e gera manifesto SHA-256. Exporta WebP lossless para `site/assets/world/r11_{cottage,forge,apothecary}_{0..3}.webp`.

O código de prévia `NSR11ArtPreview=true` é **opt-in interno**, desligado por padrão, e só seleciona a imagem R11 correspondente à rotação da câmera. O caminho normal mantém o gate de aprovação R07 e os billboards ilustrados da geração antiga. A prévia indica no próprio Canvas `R11 ART CANDIDATE · NOT APPROVED`. A escala ilustrativa de 209/216/206 pixels para cottage/forge/apothecary foi ajustada **somente para a prévia**; não modifica footprints, colisores ou arte do cliente padrão.

## Observações visuais reais, sem homologação

Os quatro quadros R11 foram produzidos pelo *Canvas verdadeiro* em Node/Skia, a 1200×760 pixels, em 0°, 90°, 180°, 270°. Em cada orientação aparecem três fachadas distintas; essa prova confirma consumo, **não** consistência geométrica 3D. A comparação R10→R11 excede 5% de pixels modificados em todas as vistas, uma métrica de mudança, não beleza. Os quatro quadros de fallback permanecem idênticos pixel a pixel ao R10.

Questões artísticas ainda abertas, percebidas na inspeção humana interna: (1) escadas, bancas, portas e acessórios variam com a vista e precisam de reconciliação arquitetônica por construção; (2) a percepção de escala com NPCs e chão precisa de direção de arte; (3) folhas geradas exigem checagem de direitos/proveniência independente; (4) sombra e base são billboards observacionais, não malhas 3D; (5) os beings e chefões não têm rigs/animações finais.

## Evidência técnica

`tools/verify_r11.py` reexecutou 240 testes Python, 44 asserções de fachadas Node, o consumidor C17 ABI5 e cinco sequências C++/WASM (R05=121, R04=121, R03=121, R02=116, R01=100) além do journal SQLite R05 de 121 eventos. A revisão do owner e seis arquivos históricos continuam SHA-256 idênticos à baseline R10. Todos os WebP R11 estão em formato RGBA 640×640 e têm hashes distintos; a prévia foi renderizada com 4 quadros Skia. Ver `artifacts/R11_TEST_REPORT.json`.

## Decisão / gate

- `ART_REVIEW_PENDING`: 12 imagens candidatas preparadas, **0/12 aprovadas**.
- `PRODUCT_NO_GO`: não distribuir para avaliação autoral como RPG completo.
- Sem novo ZIP integral do jogo; somente pacote de arte/fonte/evidências R11.
- Não altera main, Makers, MER, VEA, C02, decisões anteriores ou a obra separada Rave Masters.
- Necessário: revisão de fachadas, escala e âncoras, direitos, animação de seres/chefes, abertura e gameplay completo antes do aceite.
