# Visuais do R03 — avaliação interna, não aceitação artística

**Comparação:** R02 e R03, mesma câmera, mapa e configuração de renderização `1200×760`; resultado técnico Skia CPU. Membros `artifacts/R03_SKIA_VIEW_0..3.png` gerados pela função de desenho real do cliente `site/world.js`. Não são capturas Windows, nem provas de FPS, GPU ou aprovação de arte.

**Melhorias demonstradas:** quatro NPCs ilustrados diferenciam silhuetas e roupas; cada um possui quatro sprites de orientação; a correspondência gira com o mapa (não muda `world_tick`). Materiais do terreno perdem a grade preta rígida e passam a cinco variações determinísticas por tipo. Iluminação radial aparece junto aos pontos de fogo. Hero preserva o atlas 4×4 prévio; não é um rig.

**Problemas ainda visíveis:** cenário vazio no horizonte, ausência de casas históricas reais, escala irregular de props e personagens, objetos com uma única face em algumas rotações, sem animação de locomoção crível dos NPCs, baixa densidade de vegetação/arquitetura e insuficiência de variações artísticas para uma vila de RPG. Falta VFX e chefes tridimensionais/2.5D; boss é marcador de fixture. O opening animatic 18s não ganhou uma nova produção.

**Critério de aceite que NÃO foi atendido:** V1 exige logo de estúdio, opening cinematográfica excelente, tela título chamativa, menus, identidade e até duas classes com kits reais, prólogo amplo, profissões e 3 chefes autorais; o resultado precisa convencer visualmente durante jogo e nas quatro orientações. Falta `AUTHOR_ART_APPROVED`. Manter `PRODUCT_NO_GO`, sem solicitar teste autoral prematuro.
