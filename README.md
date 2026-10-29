# Hip-Hop & Cinematic Scenes Ultimate
Biblioteca assistida com **52 prompts originais completos em inglês** para cenas hip-hop, urbanas, cyberpunk, carros, retratos, silhuetas e surrealismo cinematográfico.

## Uso
- “Me dê a cena 17” → Midnight Call, texto integral.
- “Quero opções com carro e luz vermelha” → correspondências por tema e características.
- “Somente o prompt Crimson Smoke” → original inglês sem metadados.
- “Adapte a cena 4 com minha personagem” → preencher campo e identificar adaptação.
- “Troque só vermelho para azul” → texto inteiro atualizado; original não muda.
Tradução só por pedido. Não converter automaticamente 3D/Unreal/surreal em foto realista. Não executar geração ao apenas consultar.

## Conteúdo e lacunas
57 entradas de origem: 52 preenchidas e 5 vazias. Numeração 1–53 sem cena 47. Preservados números, descrições e todos os blocos textuais, com hashes por prompt. [Lacunas](docs/KNOWN_GAPS.md), [cobertura](docs/CONTENT_COVERAGE.md), [fonte integral](docs/SOURCE_PACK.md).
[SKILL.md](.agents/skills/hip-hop-cinematic-scenes-ultimate/SKILL.md) tem núcleo/índice. Os textos integrais estão nas referências e catálogo JSON da mesma pasta; manter a pasta inteira. Temas são classificação editorial, não informação adicionada aos originais.

## Instalação e requisitos
Copiar `.agents/skills/hip-hop-cinematic-scenes-ultimate` para o projeto alvo. Host deve reconhecer Skills ou carregar SKILL.md explicitamente. Modelo de linguagem basta para consulta; visão só para analisar referências reais, e gerador externo para executar imagens. Sem conta/API ou credencial obrigatória. [Instalação e atualização](docs/INSTALLATION.md).
Busca opcional, Python padrão:
```bash
python .agents/skills/hip-hop-cinematic-scenes-ultimate/scripts/search_catalog.py 'carro vermelho'
python .agents/skills/hip-hop-cinematic-scenes-ultimate/scripts/search_catalog.py 17 --original
```
Busca lexical, sem motor vetorial ou integração de gerador. Nomes de câmera, marcas e renderizadores não comprovam setup técnico.

## Testes
```bash
python -m pip install -r tests/requirements.txt
python tests/validate_catalog.py
python -m unittest discover -s tests -p 'test_*.py'
```
Verifica fonte, hashes, 52 textos, cinco lacunas, cena ausente, links e recuperação. Não mede qualidade visual ou comportamento do host. [Aceitação](tests/acceptance-tests.md) e [resultados](tests/RESULTS.md). GitHub Actions configurado.

MIT para contribuições originais; conteúdo da origem mantém direitos dos titulares. [NOTICE](NOTICE.md), [CHANGELOG](CHANGELOG.md). Sem alegação de endosso ou acesso a instruções privadas.
