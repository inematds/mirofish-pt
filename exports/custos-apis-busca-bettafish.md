# Custos de APIs de Busca — BettaFish e Alternativas

---

## 1. Tavily API — Planos e Precos

### Planos mensais

| Plano | Custo/mes | Creditos/mes | Buscas basicas | Custo por busca |
|-------|-----------|-------------|----------------|-----------------|
| **Free (Researcher)** | $0 | 1.000 | ~1.000 | gratis |
| Pay-As-You-Go | $0 fixo | variavel | ilimitado | $0.008/busca |
| Project | $30 | 4.000 | ~4.000 | $0.0075 |
| Bootstrap | $100 | 15.000 | ~15.000 | $0.0067 |
| Startup | $220 | 38.000 | ~38.000 | $0.0058 |
| Growth | $500 | 100.000 | ~100.000 | $0.005 |
| Enterprise | Custom | Custom | Custom | Custom |
| Student | $0 | Variavel | — | gratis |

**Notas:**
- Creditos NAO acumulam — perdem no fim do mes
- Nao precisa cartao de credito no plano free
- Plano Student disponivel via programa especifico

### Custo por operacao

| Operacao | Creditos | Custo (PAYG) | Custo (Growth) |
|----------|----------|-------------|----------------|
| Busca basica | 1 | $0.008 | $0.005 |
| Busca avancada | 2 | $0.016 | $0.010 |
| Extracao basica (5 URLs) | 1 | $0.0016/URL | $0.001/URL |
| Extracao avancada (5 URLs) | 2 | $0.0032/URL | $0.002/URL |
| Map (10 paginas) | 1 | $0.008 | $0.005 |
| Map com instrucoes (10 pag) | 2 | $0.016 | $0.010 |
| Deep Research (Pro) | 15-250 | $0.12-$2.00 | $0.075-$1.25 |
| Deep Research (Mini) | 4-110 | $0.03-$0.88 | $0.02-$0.55 |
| Extracao falha | 0 | gratis | gratis |

### Rate limits

| Ambiente | Endpoints padrao | Crawl | Research | Quem tem acesso |
|----------|-----------------|-------|----------|-----------------|
| Development | 100 RPM | 100 RPM | 20 RPM | Todos (free incluso) |
| Production | 1.000 RPM | 100 RPM | 20 RPM | Planos pagos + PAYG |
| Enterprise | Custom | Custom | Custom | Negociado |

---

## 2. Alternativas Comparadas

| Provider | Free/mes | Custo 1.000 buscas | Status | Foco |
|----------|----------|---------------------|--------|------|
| **Tavily** | 1.000 buscas | $5-8 | Ativo | IA-native, melhor para agentes |
| **SerpAPI** | 250 buscas | ~$15 | Ativo | SERP tradicional (Google, Bing) |
| **Google Custom Search** | ~3.000/mes | $5 | Morrendo (fecha jan/2027) | SERP Google |
| **Bing Web Search** | — | $35 | Morto (encerrou ago/2025) | — |
| **Bocha AI** | ? (registro) | ? (oculto) | Ativo | Internet chinesa (~10B paginas) |
| **Anspire** | ? (registro) | ? (oculto) | Ativo | Busca multimodal para agentes |

### Detalhes das alternativas

**SerpAPI**
- Free: 250 buscas/mes (sem cartao)
- Planos: $25 (1K), $75 (5K), $150 (15K), $275 (30K)
- Foco: dados de SERP tradicionais (nao IA-curado)
- Creditos nao acumulam

**Google Custom Search API**
- Free: 100 queries/dia (~3.000/mes)
- Pago: $5 por 1.000 queries (max 10K/dia)
- FECHADO para novos clientes — deprecacao total em janeiro 2027
- Alternativa recomendada pelo Google: Vertex AI Search

**Bing Web Search API**
- Totalmente encerrado em agosto 2025
- Substituto "Grounding with Bing": $35/1.000 transacoes (40-133% mais caro)
- So funciona dentro do Azure AI Agents

**Bocha AI**
- Focado no mercado chines
- ~10 bilhoes de paginas web indexadas
- Integra com OpenAI function calling, LangChain, Coze, Dify
- Preco oculto — precisa registrar em open.bochaai.com

**Anspire**
- Busca multimodal para agentes IA (RAG, chatbots)
- Plugin no Dify Marketplace
- Preco oculto — contato em open.anspire.cn

---

## 3. Simulacao de Custos para INEMA + BettaFish

### Por analise BettaFish

| Componente | Buscas | Creditos Tavily | Custo (PAYG) |
|-----------|--------|-----------------|-------------|
| QueryEngine (busca web) | 20-50 | 20-50 | $0.16-$0.40 |
| MediaEngine (busca multimodal) | 10-30 | 10-30 | $0.08-$0.24 |
| InsightEngine (extracoes) | 5-20 URLs | 1-4 | $0.008-$0.032 |
| ReportEngine (verificacao) | 5-10 | 5-10 | $0.04-$0.08 |
| **Total por analise** | **40-110** | **36-94** | **$0.29-$0.75** |

### Cenarios mensais

| Cenario | Analises/dia | Buscas/mes | Plano ideal | Custo Tavily | Custo LLM | Custo VPS | **Total/mes** |
|---------|-------------|-----------|-------------|-------------|-----------|-----------|---------------|
| Teste | 1 | ~150 | **Free** | $0 | ~$15 | $0 (local) | **~$15** |
| Leve | 2 | ~1.000 | **Free** | $0 | ~$30-60 | $0 (local) | **~$30-60** |
| Moderado | 5 | ~3.000 | **Project $30** | $30 | ~$75-150 | ~$20 | **~$125-200** |
| Intenso | 15 | ~10.000 | **Bootstrap $100** | $100 | ~$225-450 | ~$24 | **~$350-575** |
| Producao | 30+ | ~25.000+ | **Startup $220** | $220 | ~$450-900 | ~$30+ | **~$700-1150** |

---

## 4. Interface do BettaFish

### Telas principais

O BettaFish tem **4 interfaces web** rodando simultaneamente:

| Porta | Interface | Funcao |
|-------|-----------|--------|
| **5000** | Flask (principal) | Dashboard central, configuracao, gerenciamento |
| **8501** | Streamlit #1 | QueryEngine — busca e monitoramento de noticias |
| **8502** | Streamlit #2 | InsightEngine — mineracao de dados e analise |
| **8503** | Streamlit #3 | ReportEngine — visualizacao de relatorios |

### Fluxo de uso

```
1. Acesse http://localhost:5000 (dashboard principal)
   ├── Configurar topicos de analise
   ├── Definir plataformas para crawl
   └── Iniciar analise

2. Os 5 agentes rodam em paralelo:
   ├── QueryEngine (porta 8501) → busca web/noticias
   ├── MediaEngine → analisa videos/imagens
   ├── InsightEngine (porta 8502) → minera dados
   ├── ForumEngine → debate entre agentes
   └── ReportEngine (porta 8503) → gera relatorio

3. Resultado:
   ├── Relatorio em PDF/Markdown
   ├── Graficos de sentimento
   ├── Timeline de tendencias
   └── Dados brutos em PostgreSQL
```

### Screenshot do fluxo (descricao)

```
┌─────────────────────────────────────────────────┐
│  BettaFish Dashboard (porta 5000)               │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐             │
│  │ Novo Topico  │  │ Historico    │             │
│  │              │  │              │             │
│  │ "IA no       │  │ - Analise 1  │             │
│  │  Brasil"     │  │ - Analise 2  │             │
│  │              │  │ - Analise 3  │             │
│  │ [Iniciar]    │  │              │             │
│  └──────────────┘  └──────────────┘             │
│                                                  │
│  Status dos Agentes:                             │
│  ● QueryEngine   [rodando]  50 buscas           │
│  ● MediaEngine   [rodando]  12 videos           │
│  ● InsightEngine [rodando]  3.200 registros     │
│  ● ForumEngine   [debatendo] round 3/5          │
│  ● ReportEngine  [aguardando]                    │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 5. Estrutura de Pastas do BettaFish

```
BettaFish/
├── app.py                    # Entry point Flask
├── docker-compose.yml        # Deploy com 2 containers
├── Dockerfile               # Imagem Python 3.11
├── requirements.txt         # ~60+ dependencias
├── .env.example             # Template de configuracao
│
├── agents/                  # 5 agentes especializados
│   ├── query_engine/        # Busca web (Tavily)
│   ├── media_engine/        # Analise multimodal
│   ├── insight_engine/      # Mineracao de dados
│   ├── report_engine/       # Geracao de relatorio
│   └── forum_engine/        # Debate entre agentes
│
├── mindspider/              # Submodulo crawler
│   ├── spiders/             # Crawlers por plataforma
│   │   ├── weibo.py
│   │   ├── xiaohongshu.py
│   │   ├── douyin.py
│   │   ├── bilibili.py
│   │   ├── zhihu.py
│   │   └── ...              # 30+ plataformas
│   └── scheduler.py         # Agendador de crawls
│
├── database/                # Modelos e migracoes
│   ├── models.py            # SQLAlchemy models
│   └── migrations/
│
├── streamlit_apps/          # 3 interfaces Streamlit
│   ├── query_ui.py          # porta 8501
│   ├── insight_ui.py        # porta 8502
│   └── report_ui.py         # porta 8503
│
├── reports/                 # Relatorios gerados
│   └── output/              # PDF, Markdown, graficos
│
└── config/
    └── platforms.yaml        # Configuracao das plataformas
```

---

## 6. Como Rodar Localmente

### Opcao A: Docker (recomendado)

```bash
# 1. Clonar
git clone https://github.com/666ghj/BettaFish.git
cd BettaFish

# 2. Configurar
cp .env.example .env
nano .env  # editar API keys

# 3. Subir
docker compose up -d

# 4. Acessar
# Dashboard: http://localhost:5000
# Query UI:  http://localhost:8501
# Insight:   http://localhost:8502
# Report:    http://localhost:8503
```

### Opcao B: Direto (sem Docker)

```bash
# 1. Clonar
git clone https://github.com/666ghj/BettaFish.git
cd BettaFish

# 2. Ambiente Python
conda create -n bettafish python=3.11
conda activate bettafish
pip install -r requirements.txt

# 3. Instalar Playwright
playwright install chromium

# 4. Instalar dependencias do sistema (PDF)
# Ubuntu:
sudo apt install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf-2.0-0
# macOS:
brew install pango gdk-pixbuf libffi

# 5. Banco de dados
# Instalar PostgreSQL 15 ou MySQL 8
# Criar banco: bettafish
# Configurar no .env

# 6. Configurar .env
cp .env.example .env
nano .env

# 7. Rodar
python app.py
```

### Configuracao minima do .env

```bash
# === Banco de dados ===
DB_DIALECT=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=bettafish
DB_PASSWORD=sua_senha
DB_NAME=bettafish

# === Busca ===
TAVILY_API_KEY=tvly-sua-chave-aqui   # gratis em tavily.com

# === LLM (pode usar o mesmo para todos) ===
# Opcao 1: Ollama local (gratis)
QUERY_ENGINE_API_KEY=ollama
QUERY_ENGINE_BASE_URL=http://localhost:11434/v1
QUERY_ENGINE_MODEL_NAME=qwen2.5:32b

MEDIA_ENGINE_API_KEY=ollama
MEDIA_ENGINE_BASE_URL=http://localhost:11434/v1
MEDIA_ENGINE_MODEL_NAME=qwen2.5:32b

INSIGHT_ENGINE_API_KEY=ollama
INSIGHT_ENGINE_BASE_URL=http://localhost:11434/v1
INSIGHT_ENGINE_MODEL_NAME=qwen2.5:72b-instruct-q3_K_M

REPORT_ENGINE_API_KEY=ollama
REPORT_ENGINE_BASE_URL=http://localhost:11434/v1
REPORT_ENGINE_MODEL_NAME=qwen2.5:32b

FORUM_HOST_API_KEY=ollama
FORUM_HOST_BASE_URL=http://localhost:11434/v1
FORUM_HOST_MODEL_NAME=qwen2.5:14b

# Opcao 2: Groq (gratis, mais rapido)
# QUERY_ENGINE_API_KEY=gsk_sua-chave
# QUERY_ENGINE_BASE_URL=https://api.groq.com/openai/v1
# QUERY_ENGINE_MODEL_NAME=llama-3.3-70b-versatile
# ... repetir para os outros agentes

# === Seguranca ===
FLASK_SECRET_KEY=gere-uma-chave-aleatoria-aqui
```

---

## 7. Custo Zero — Setup Minimo Gratis

E possivel rodar BettaFish com custo ZERO:

| Componente | Opcao gratis |
|------------|-------------|
| LLM | Ollama local (qwen2.5:32b) |
| Busca | Tavily free (1.000/mes) |
| Banco | PostgreSQL local |
| Infra | Sua propria maquina |

**Limitacoes do setup gratis:**
- 1.000 buscas/mes no Tavily (~1-2 analises/dia)
- LLM local mais lento que APIs cloud
- Sem analise multimodal avancada (precisa de modelo com visao)
- Crawler limitado a plataformas que nao bloqueiam

---

## 8. Recomendacao para INEMA

### Fase 1: Teste (custo zero)
- BettaFish local com Docker
- Ollama para LLMs (seus modelos ja instalados)
- Tavily free para busca
- PostgreSQL local
- **Custo: $0/mes**

### Fase 2: Producao leve ($50-80/mes)
- BettaFish em VPS ($20/mes)
- Tavily Project ($30/mes)
- Groq para LLMs (gratis) ou Ollama
- **Custo: ~$50-80/mes**

### Fase 3: Pipeline completo ($150-300/mes)
- BettaFish + MiroFish em VPS ($24/mes)
- Tavily Bootstrap ($100/mes)
- Mix de LLMs: Claude para analise, Groq para simulacao
- **Custo: ~$150-300/mes**

---

*Documento gerado em 20/03/2026*
*Fontes: tavily.com/pricing, docs.tavily.com, serpapi.com, GitHub 666ghj/BettaFish*
