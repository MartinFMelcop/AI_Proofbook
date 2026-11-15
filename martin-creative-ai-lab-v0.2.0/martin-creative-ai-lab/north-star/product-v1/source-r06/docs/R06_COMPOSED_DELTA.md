# MMAI North Star · PRODUCT V1 / R06 — movimento ilustrado e leitura de chefes

**Estado:** `ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO`  
**Escopo:** incremento aditivo do mesmo V1; a direção autoral C mantém C++20/C17 + Python/IA + SQLite, sem novos trabalhos Unity/C#.

## Dependência e autoridade

Base *exata*: R05 no Drive `1nbRdNSH8vOQiWFfMEm5ZLDLi-v08wFmd` (71.105.665 bytes; SHA256 informado em R05 `e7e194033c018e602fce0e5c2b0304a03390ccbd779d5e574506b2235cf04c3c`). O C++ owner em `core/world_r05.cpp` **NÃO mudou**. A interface do cliente permanece ABI5 (`site/product.wasm` é reconstruído do mesmo código), sem ABI6, novas regras, expansão de canon ou migração silenciosa de save. As fontes/arte R00–R05 estão preservadas.

## Incrementos efetivos

1. **Quadros de movimento derivado:** `tools/build_r06_cycles.py` gerou 48 quadros NPC (quatro personagens × quatro orientações × três deformações adicionais), mais 18 quadros derivados de chefes R04. **Não são rigs, keyframes autorais nem uma animação aprovada.** O renderizador observa movimento/interpolação e só alterna o quadro quando houve mudança de posição na rota observável. O jogador mantém a animação 4×4 anterior.
2. **Silhueta de laboratório do B02:** `tools/build_r06_wraith.py` derivou 16 variantes visuais espectrais de sprite da herbalista R03 (quatro orientações × quatro fases), com recibos de fonte SHA256. A dependência de arte é transparente; a identidade do chefe permanece proposta, NÃO canonizada. A imagem de laboratório B02 foi efetivamente consumida por `site/world.js` em três renderizações de chefe.
3. **Ambiência observacional:** `site/ambience_r06.js` adiciona gradações de luz quente e partículas discretas. O módulo só consome Canvas, tempo e projeção. Não simula inteligência de seres, não decide dano/colisão nem modifica revisão de world state.
4. **Contratos de apresentação:** `site/index.html` carrega a ambiência antes do renderizador; `site/world.js` pré-carrega quadros derivados. Ausência de assets novos não invalida o gameplay porque as imagens originais permanecem como fallback.

## Observações e resultados comprovados

| Prova executada | Evidência | Estado |
|---|---|---|
| Python unittest | 205 casos após incremento (197 históricos + 8 novos) | PASS |
| Consumidor C17 → C++20 ABI5 | programa compilado e executado em Linux | PASS |
| C++ ↔ WebAssembly | 121 intenções R05 pareadas no WASM; owner intacto | PASS |
| Regressões WASM | R04 121, R03 121, R02 116, R01 100 ações | PASS |
| SQLite de laboratório | journal R05 121 eventos, replay e recusa de overwrite | PASS |
| Skia CPU executando `site/world.js` | 4 vistas, 3 encontros de chefe, 4 tempos consecutivos do cenário | PASS técnico |
| Integridade de originais | 10 fontes e assets R05 confrontados com hashes do manifesto | MATCH |
| Qualidade visual | fachada inédita NÃO criada; R05 permaneceu base | ART_REVIEW_PENDING |
| Windows/browser padrão | não executado | NOT_RUN |

**Métricas não são qualidade:** em vista estática equivalente R05→R06 mudou aproximadamente **0,004%–0,011%** dos pixels ao limiar RGB-L1 médio >18. Entre os quadros temporais 0 e 1–3 da mesma cena, **0,535%–0,816%** mudaram. O combate B02 modificou **0,969%** da imagem. Isso prova uma diferença, não que a arte seja satisfatória.

## Falha real de produção artística

A ferramenta de geração das novas imagens falhou durante R06; nenhuma nova arte pintada de fachadas quatro-vistas foi produzida. A antiga prova de geometria R05, reprovada artisticamente, continua isolada — NÃO promovida à cena principal. A arquitetura ilustrada R04 permanece a melhor opção disponível, mas usa *billboards* com a mesma pintura vista das quatro orientações. **Gate de fachadas quatro-vistas continua aberto.**

Os bosses ainda usam estudos derivados, não silhuetas autorais finais. Não houve nova opening cinematográfica ou 21 kits reais/canônicos. A jogabilidade prossegue como pré-produção, sem prova de multiplayer ou executável Windows. B01/B02 são propostas; a Árvore Guardiã B03 é referência da obra independente Rave Masters e não foi canonizada para North Star.

## Continuidade

R07 deve priorizar **assets efetivos e verificáveis de quatro fachadas, ciclos desenhados para cada orientação e chefes com identidade original**. Exigir imagens do *próprio* renderizador antes/depois e provas de C++ e replay; rejeitar variações de sprite que reduzam a qualidade. Não apresentar build a usuário final enquanto `PRODUCT_NO_GO`.

**Gates históricos preservados:** R51/R60/R61/INT-C01-001 OPEN; RP-R03-P03 / RP-G02-A03 PENDING; C30 STOP_DOCUMENTARY_PENDING_OWNER; Arena S1 HOLD, C05-P01–P07 OPEN, VEA e direitos e ACKs C/E/B/D pendentes.
