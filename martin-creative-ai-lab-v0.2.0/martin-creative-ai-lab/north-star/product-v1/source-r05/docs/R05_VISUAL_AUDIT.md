# R05 — Laudo visual da cena real (Canvas Skia CPU, não apresentação promocional)

## Conclusão editorial

**ART_REVIEW_PENDING / GEOMETRY_STUDY_ART_REJECTED_INTERNAL / PRODUCT_NO_GO**. Foram testados os quatro ângulos por meio de `site/world.js`; esse código é o renderizador do cliente, não a arte de um cartaz. Os NPCs agora têm direção derivada do mundo, mas a arte de marcha continua rudimentar. As fachadas volumétricas experimentais provaram a separação entre geometria/câmera e gameplay, mas aparecem demasiadamente planas e sem qualidade suficiente. A escolha correta foi manter o asset ilustrado anterior, deixando o modelo em modo interno.

## Imagens internas

- `artifacts/R05_GAME_VIEW_0.png` a `R05_GAME_VIEW_3.png`: cena padrão de laboratório, arte ilustrada R04 e atualização de direção de NPC/personagem.
- `artifacts/R05_GEOMETRY_VIEW_0.png` a `_3.png`: teste de quatro fachadas/telhados reais em Canvas, falha de qualidade artística.
- `artifacts/R05_BOSS_1.png` a `_3.png`: três confrontos do núcleo C++ ABI5, telegraph lido do owner e câmera em 0/90/180 graus.

Nenhuma dessas imagens demonstra rodar no navegador Windows ou GPU; a execução foi Skia CPU headless. A qualidade não foi aprovada por artista/autor. Não fornecer build ao autor por conta dessas capturas.

## Corrigir no próximo incremento

Integrar **arte autoral de quatro fachadas verdadeiramente coerentes** ao volume testado; manter células de ocupação do C++ como dado único. Evoluir personagem/NPCs de quatro estudos de orientação para ciclos de movimento e transição genuínos. Estudar rigs/animação, oclusão e z-sorting com transparência e telegraph sem esconder alvo. Criar silhuetas e telegraphs distintos para os 3 chefes que preservem Rave Masters como obra independente. A abertura artística ainda é animatic de 18 s, não opening final.
