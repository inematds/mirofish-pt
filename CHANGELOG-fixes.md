# MiroFish - Registro de Mudanças e Correções

## Sessão de 19/03/2026

### Correções de Bugs

#### 1. Função `_get_bool_env` ausente no config
- **Arquivo:** `backend/app/config.py`
- **Problema:** Classe `Config` referenciava `_get_bool_env` e `_get_cors_origins` que não existiam. Import de `secrets` também faltava.
- **Correção:** Adicionadas as funções `_get_bool_env()` e `_get_cors_origins()` e o import de `secrets`.

#### 2. Import circular no build_graph
- **Arquivo:** `backend/app/tools/build_graph.py`
- **Problema:** Import circular: `services` → `graph_builder` → `models.task` → `core` → `workbench_session` → `tools` → `build_graph` → `services.graph_builder`
- **Correção:** Movido o import de `GraphBuilderService` de top-level para dentro da função `run_build()` (lazy import).

#### 3. Claude CLI falhando com prompts longos
- **Arquivo:** `backend/app/utils/llm_client.py`
- **Problema:** O prompt era passado como argumento de linha de comando (`subprocess.run(["claude", "-p", "--output-format", "json", prompt])`), que estoura o limite do OS (~128KB) para prompts longos.
- **Correção:** Passagem do prompt via `stdin` usando o parâmetro `input=prompt` do `subprocess.run`.

#### 4. `oasis_profile_generator` não suportava `claude-cli`
- **Arquivo:** `backend/app/services/oasis_profile_generator.py`
- **Problema:** Usava `OpenAI` client diretamente, exigindo `LLM_API_KEY`. Não funcionava com `LLM_PROVIDER=claude-cli`.
- **Correção:** Substituído `OpenAI` client por `LLMClient` que suporta todos os providers (openai, anthropic, claude-cli, codex-cli).

#### 5. `simulation_config_generator` não suportava `claude-cli`
- **Arquivo:** `backend/app/services/simulation_config_generator.py`
- **Problema:** Mesmo problema do item 4 — usava `OpenAI` diretamente.
- **Correção:** Substituído `OpenAI` client por `LLMClient`.

#### 6. Atributo `model_name` ausente após migração
- **Arquivo:** `backend/app/services/simulation_config_generator.py`
- **Problema:** Após migrar para `LLMClient`, o código ainda referenciava `self.model_name` e `self.base_url` que não existiam mais.
- **Correção:** Substituído por `self.llm.model` e `self.llm.base_url`.

#### 7. Simulação OASIS exige API key
- **Arquivo:** `backend/scripts/run_parallel_simulation.py`
- **Problema:** O script usa `camel-ai` que exige `OPENAI_API_KEY` via variável de ambiente. Não funciona com `claude-cli`.
- **Solução:** Configurar `LLM_API_KEY`, `LLM_BASE_URL` e `LLM_MODEL_NAME` no `.env` para um provider OpenAI-compatible (ex: Ollama local).
- **TODO:** Migrar para suportar Claude CLI ou permitir configuração separada por etapa.

---

### Novas Funcionalidades

#### 1. Tradução completa para Português Brasileiro
- **Arquivos:** 16 arquivos Vue em `frontend/src/`
- **Escopo:** 330+ strings traduzidas em views e components (Home, Process, Step1-5, GraphPanel, HistoryDatabase, MainView, SimulationView, etc.)

#### 2. Lista de projetos na página principal
- **Arquivo:** `frontend/src/views/Home.vue`
- **Funcionalidade:** Seção "Projetos Existentes" com cards mostrando nome, status (com bolinha colorida), arquivos e data. Clicável para abrir o projeto.

#### 3. Campo nome do projeto na criação
- **Arquivos:** `frontend/src/views/Home.vue`, `frontend/src/store/pendingUpload.js`, `frontend/src/views/MainView.vue`
- **Funcionalidade:** Campo "Nome do Projeto" no formulário de criação. Enviado como `project_name` na API.

#### 4. Editar nome do projeto
- **Arquivos:** `backend/app/api/graph.py` (endpoint PUT), `frontend/src/views/Home.vue`
- **Funcionalidade:** Botão ✎ nos cards para editar nome inline. Salva via `PATCH /api/graph/project/<id>`.

#### 5. Parar build com salvamento de progresso
- **Arquivos:** `backend/app/api/graph.py`, `backend/app/services/graph_builder.py`, `backend/app/services/entity_extractor.py`
- **Funcionalidade:** Botão ◼ para parar o build. O sistema salva o progresso (chunks processados, entidades e relacionamentos extraídos) em arquivo `_progress.json` para retomada posterior.
- **Mecanismo:** Flag global `_active_builds` no `graph_builder.py`, checada a cada chunk no `entity_extractor.extract_batch()`.

#### 6. Retomar build de onde parou
- **Arquivos:** `backend/app/api/graph.py` (endpoint POST /resume), `backend/app/services/graph_builder.py`, `backend/app/services/entity_extractor.py`
- **Funcionalidade:** Botão ▶ para continuar. Carrega o `_progress.json`, cria nova task e retoma extração do chunk onde parou, reaproveitando entidades já extraídas.

#### 7. Refazer build do zero
- **Arquivo:** `frontend/src/views/Home.vue`
- **Funcionalidade:** Botão ↻ para refazer. Chama `/api/graph/build` com `force: true`.

#### 8. Excluir projeto
- **Arquivo:** `frontend/src/views/Home.vue`
- **Funcionalidade:** Botão ✕ com confirmação. Chama `DELETE /api/graph/project/<id>`.

---

### Configuração de LLMs

#### Arquitetura atual (híbrida)
O MiroFish usa LLMs em várias etapas, e cada uma pode usar um provider diferente:

| Etapa | Arquivo | Provider atual | Observação |
|-------|---------|---------------|------------|
| Ontologia/Grafo | `entity_extractor.py` via `llm_client.py` | claude-cli | Suporta todos os providers |
| Geração de Personas | `oasis_profile_generator.py` via `llm_client.py` | claude-cli | Migrado de OpenAI direto |
| Config de Simulação | `simulation_config_generator.py` via `llm_client.py` | claude-cli | Migrado de OpenAI direto |
| Simulação OASIS | `scripts/run_parallel_simulation.py` | Ollama (qwen2.5:32b) | Usa camel-ai, precisa de API key |
| Relatório | via `llm_client.py` | claude-cli | Suporta todos os providers |
| Chat/Interação | via `llm_client.py` | claude-cli | Suporta todos os providers |

#### Configuração via `.env`
```bash
# Provider principal (ontologia, personas, config, relatório, chat)
LLM_PROVIDER=claude-cli

# API para simulação OASIS (precisa ser OpenAI-compatible)
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:32b
```

#### Providers suportados pelo LLMClient
- `openai` — OpenAI API (gpt-4o, gpt-4o-mini)
- `anthropic` — Anthropic API (claude-sonnet, claude-opus)
- `claude-cli` — Claude Code CLI (usa assinatura do usuário)
- `codex-cli` — Codex CLI
- Qualquer provider OpenAI-compatible via `LLM_BASE_URL` (Ollama, OpenRouter, Together, Groq)

#### TODO: Painel de configuração LLM no frontend
Permitir que o usuário configure o LLM para cada etapa via interface, com presets:
- **Qualidade máxima:** Claude para tudo
- **Econômico:** Claude para etapas 1-3, gpt-4o-mini para simulação
- **100% Local:** Ollama para tudo (qwen2.5:72b para análise, qwen2.5:32b para simulação)

---

### Novos Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| PUT/PATCH | `/api/graph/project/<id>` | Atualizar metadados do projeto (nome) |
| POST | `/api/graph/project/<id>/stop` | Parar build em andamento (salva progresso) |
| POST | `/api/graph/project/<id>/resume` | Retomar build de onde parou |

---

### Repositórios atualizados
- **origin:** `git@github.com:inematds/mirofish.git` (main)
- **mirofish-pt:** `git@github.com:inematds/mirofish-pt.git` (main)
