# Guia de Migração - Correções e Melhorias MiroFish

> Use este documento para aplicar as correções no projeto original.
> Cada seção tem: arquivo, problema, e o código exato para corrigir.
> Pode ser usado como prompt para o Claude em outro projeto.

---

## Prompt para o Claude no projeto original

Cole este prompt no Claude Code dentro do projeto original:

```
Preciso aplicar as seguintes correções e melhorias no MiroFish.
Leia o arquivo MIGRATION-GUIDE.md e aplique cada correção na ordem.
Não altere lógica existente além do descrito.
```

---

## 1. CRÍTICO: Funções ausentes no config.py

**Arquivo:** `backend/app/config.py`
**Problema:** `_get_bool_env` e `_get_cors_origins` são referenciadas mas não existem.

**Adicionar ANTES da classe Config:**
```python
import secrets  # adicionar ao topo junto com os outros imports

def _get_bool_env(key, default=False):
    """Get a boolean value from environment variable."""
    val = os.environ.get(key, '')
    if not val:
        return default
    return val.lower() in ('true', '1', 'yes')


def _get_cors_origins():
    """Get CORS origins from environment or return defaults."""
    origins = os.environ.get('CORS_ORIGINS', '')
    if origins:
        return [o.strip() for o in origins.split(',')]
    return ['http://localhost:3000', 'http://localhost:5173']
```

---

## 2. CRÍTICO: Import circular no build_graph.py

**Arquivo:** `backend/app/tools/build_graph.py`
**Problema:** Import circular impede o backend de iniciar.

**Remover** esta linha do topo do arquivo:
```python
from ..services.graph_builder import GraphBuilderService
```

**Adicionar** o import dentro da função `run_build()`, logo antes de `builder = GraphBuilderService()`:
```python
from ..services.graph_builder import GraphBuilderService
builder = GraphBuilderService()
```

---

## 3. CRÍTICO: Claude CLI falha com prompts longos

**Arquivo:** `backend/app/utils/llm_client.py`
**Problema:** Prompt passado como argumento de linha de comando estoura limite do OS.

**Substituir:**
```python
result = subprocess.run(
    ["claude", "-p", "--output-format", "json", prompt],
    capture_output=True, text=True, timeout=120,
    cwd="/tmp"
)
```

**Por:**
```python
result = subprocess.run(
    ["claude", "-p", "--output-format", "json"],
    input=prompt,
    capture_output=True, text=True, timeout=120,
    cwd="/tmp"
)
```

---

## 4. IMPORTANTE: oasis_profile_generator não suporta claude-cli

**Arquivo:** `backend/app/services/oasis_profile_generator.py`

### 4a. Substituir import
**Remover:**
```python
from openai import OpenAI
```
**Adicionar:**
```python
from ..utils.llm_client import LLMClient
```

### 4b. Substituir __init__
**Remover:**
```python
self.api_key = api_key or Config.LLM_API_KEY
self.base_url = base_url or Config.LLM_BASE_URL
self.model_name = model_name or Config.LLM_MODEL_NAME

if not self.api_key:
    raise ValueError("LLM_API_KEY is not configured")

self.client = OpenAI(
    api_key=self.api_key,
    base_url=self.base_url
)
```
**Adicionar:**
```python
self.llm = LLMClient(api_key=api_key, base_url=base_url, model=model_name)
```

### 4c. Substituir chamada LLM em `_generate_profile_with_llm`
**Remover** o bloco `self.client.chat.completions.create(...)` e parsing de `response.choices[0]`.
**Substituir por:**
```python
content = self.llm.chat(
    messages=[
        {"role": "system", "content": self._get_system_prompt(is_individual)},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7 - (attempt * 0.1),
    response_format={"type": "json_object"},
)
```
E remover o bloco de `finish_reason` / `_fix_truncated_json` (o LLMClient já limpa o output).

---

## 5. IMPORTANTE: simulation_config_generator não suporta claude-cli

**Arquivo:** `backend/app/services/simulation_config_generator.py`

### 5a. Substituir import
**Remover:**
```python
from openai import OpenAI
```
**Adicionar:**
```python
from ..utils.llm_client import LLMClient
```

### 5b. Substituir __init__
**Remover:**
```python
self.api_key = api_key or Config.LLM_API_KEY
self.base_url = base_url or Config.LLM_BASE_URL
self.model_name = model_name or Config.LLM_MODEL_NAME

if not self.api_key:
    raise ValueError("LLM_API_KEY is not configured")

self.client = OpenAI(
    api_key=self.api_key,
    base_url=self.base_url
)
```
**Adicionar:**
```python
self.llm = LLMClient(api_key=api_key, base_url=base_url, model=model_name)
```

### 5c. Substituir chamada LLM em `_call_llm_with_retry`
**Remover** o bloco `self.client.chat.completions.create(...)` e parsing de `response.choices[0]`.
**Substituir por:**
```python
content = self.llm.chat(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7 - (attempt * 0.1),
    response_format={"type": "json_object"},
)
```

### 5d. Corrigir referências a self.model_name e self.base_url
**Substituir:**
```python
llm_model=self.model_name,
llm_base_url=self.base_url,
```
**Por:**
```python
llm_model=self.llm.model,
llm_base_url=self.llm.base_url,
```

---

## 6. MELHORIA: Parar/Retomar builds de grafo

### 6a. Registro global de builds ativos
**Arquivo:** `backend/app/services/graph_builder.py`
**Adicionar** antes da classe `GraphBuilderService`:
```python
_active_builds = {}  # task_id -> {"stop": False}

def request_stop(task_id: str):
    if task_id in _active_builds:
        _active_builds[task_id]["stop"] = True
        return True
    return False
```

### 6b. Suporte a stop no entity_extractor
**Arquivo:** `backend/app/services/entity_extractor.py`
**Adicionar** parâmetros ao `extract_batch`:
- `stop_check=None` — callable que retorna True para parar
- `start_from=0` — chunk index para retomar
- `prior_entities=None` — entidades já extraídas
- `prior_relationships=None` — relacionamentos já extraídos

No loop, antes de processar cada chunk:
```python
if stop_check and stop_check():
    return {"entities": ..., "relationships": ..., "last_chunk_index": i, "stopped": True}
```

### 6c. Novos endpoints
**Arquivo:** `backend/app/api/graph.py`
- `PUT /api/graph/project/<id>` — atualizar nome
- `POST /api/graph/project/<id>/stop` — parar build, salvar progresso
- `POST /api/graph/project/<id>/resume` — retomar de onde parou

---

## 7. MELHORIA: Frontend - Projetos na home

**Arquivo:** `frontend/src/views/Home.vue`
- Lista de projetos existentes com cards clicáveis
- Campo "Nome do Projeto" na criação
- Botões: ✎ editar, ◼ parar, ▶ continuar, ↻ refazer, ✕ excluir
- Status com bolinha colorida animada

**Arquivo:** `frontend/src/store/pendingUpload.js`
- Adicionado campo `projectName`

**Arquivo:** `frontend/src/views/MainView.vue`
- Envio de `project_name` no FormData

---

## 8. Configuração de LLMs por etapa

O MiroFish usa LLMs em 6 etapas diferentes. Cada uma pode usar um provider diferente:

| # | Etapa | Arquivo principal | Recomendado |
|---|-------|-------------------|-------------|
| 1 | Ontologia/Grafo | `entity_extractor.py` → `llm_client.py` | Claude ou modelo 70B+ |
| 2 | Personas | `oasis_profile_generator.py` → `llm_client.py` | Claude ou modelo 70B+ |
| 3 | Config simulação | `simulation_config_generator.py` → `llm_client.py` | Claude ou modelo 70B+ |
| 4 | Simulação OASIS | `scripts/run_parallel_simulation.py` | API OpenAI-compatible (Ollama, OpenRouter) |
| 5 | Relatório | `llm_client.py` | Claude ou modelo analítico |
| 6 | Chat/Interação | `llm_client.py` | Modelo conversacional |

### Exemplo de `.env` híbrido (Claude + Ollama)
```bash
# Provider principal (etapas 1-3, 5-6)
LLM_PROVIDER=claude-cli

# API para simulação OASIS (etapa 4)
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:32b
```

### TODO futuro
- Criar painel no frontend para configurar LLM por etapa
- Presets: "Qualidade máxima", "Econômico", "100% Local"
- Permitir selecionar modelo Ollama no dropdown

---

## Ordem de aplicação recomendada

1. Correções 1-3 (críticas — backend não inicia sem elas)
2. Correções 4-5 (importante — suporte a claude-cli)
3. Correção 5d (bug após migração)
4. Melhorias 6-7 (funcionalidades novas)
5. Configuração 8 (LLMs por etapa)
