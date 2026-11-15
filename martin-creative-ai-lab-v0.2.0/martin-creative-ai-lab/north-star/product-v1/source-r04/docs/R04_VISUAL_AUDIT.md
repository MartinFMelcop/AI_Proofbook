# Auditoria comparativa de render R03 → R04 (somente produção)

Os arquivos `R03_SKIA_VIEW_0.png`, `R04_SKIA_VIEW_0.png` e `R04_VISUAL_COMPARISON.png` são evidências do código Canvas executado no runtime Skia CPU, **não capturas do navegador Windows nem imagens promocionais**. Três cenários de chefe `R04_BOSS_1..3.png` foram renderizados depois de reproduzir intenções aceitas do C++ até cada encontro; no R04 a máscara do perigo vem de export puro do C++.

**Melhorias visíveis:** edificações ornamentadas, luz própria em forja e lanternas, praça com fonte, ponte volumétrica, vegetação de silhueta diferenciada, sprites de chefe diferentes dos antigos marcadores inertes. Quatro vistas continuam projetando a geometria sem mudar estado de jogo.

**Defeitos observados sem inventar aprovação:** sprites de casas são billboards sem fachadas traseiras, repetição da mesma árvore em distâncias pequenas, vegetação volumosa pode esconder atores em combate (mitigação parcial por atenuação), cenário fora da vila carece de elementos marcantes, ausência de trajetória/rig de locomoção no jogador e NPCs, escala prop vs personagem desigual, perda de densidade em algumas rotações, atmosfera ainda conceitual, três chefões sem arte definitiva nem animação telegráfica específica, câmera ainda restrita à grade e sem paralaxe robusta. Aumento de diferença em pixels **não é um aval artístico**.

**Status:** ART_REVIEW_PENDING / PRODUCT_NO_GO. Não convidar o autor para testar esta versão.
