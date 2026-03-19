<template>
  <div class="home-container">
    <!-- Top Navigation Bar -->
    <nav class="navbar">
      <div class="nav-brand">MIROFISH</div>
      <div class="nav-links">
        <a href="https://github.com/666ghj/MiroFish" target="_blank" class="github-link">
          Visite nossa página no Github <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- Top Half: Hero Area -->
      <section class=”hero-section”>
        <div class=”hero-left”>
          <div class=”tag-row”>
            <span class=”orange-tag”>Um Motor de Inteligência de Enxame Simples e Universal</span>
            <span class=”version-text”>/ v0.1-Preview</span>
          </div>

          <h1 class=”main-title”>
            Envie Qualquer Relatório<br>
            <span class=”gradient-text”>Preveja o Futuro Instantaneamente</span>
          </h1>

          <div class=”hero-desc”>
            <p>
              Mesmo com apenas um único texto, o <span class=”highlight-bold”>MiroFish</span> consegue extrair sementes da realidade e gerar automaticamente um mundo paralelo composto por até <span class=”highlight-orange”>milhões de Agentes</span>. Injete variáveis com uma visão onisciente e encontre <span class=”highlight-code”>”ótimos locais”</span> em ambientes dinâmicos por meio de interações complexas de enxame.
            </p>
            <p class=”slogan-text”>
              Deixe o futuro ensaiar entre Agentes, deixe as decisões prevalecerem após incontáveis tentativas<span class=”blinking-cursor”>_</span>
            </p>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <!-- Logo Area -->
          <div class="logo-container">
            <img src="../assets/logo/MiroFish_logo_left.jpeg" alt="MiroFish Logo" class="hero-logo" />
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- Bottom Half: Dual Panel Layout -->
      <section class="dashboard-section">
        <!-- Left Panel: Status & Steps -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> Status do Sistema
          </div>

          <h2 class="section-title">Pronto</h2>
          <p class="section-desc">
            Motor de previsão em espera. Envie múltiplos arquivos de dados não estruturados para inicializar a sequência de simulação.
          </p>

          <!-- Data Metric Cards -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">Baixo Custo</div>
              <div class="metric-label">Média de $5 por simulação padrão</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">Alta Disponibilidade</div>
              <div class="metric-label">Até milhões de simulações com Agentes</div>
            </div>
          </div>

          <!-- Simulation Workflow Steps -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> Sequência do Fluxo
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">Construção do Grafo</div>
                  <div class="step-desc">Extração de sementes da realidade & injeção de memória individual/coletiva & construção do GraphRAG</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">Configuração do Ambiente</div>
                  <div class="step-desc">Extração de entidades e relações & geração de personas & configuração do ambiente e injeção de parâmetros de simulação via Agente</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">Iniciar Simulação</div>
                  <div class="step-desc">Simulação paralela em duas plataformas & análise automática de requisitos de previsão & atualizações dinâmicas de memória temporal</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">Geração de Relatório</div>
                  <div class="step-desc">O ReportAgent possui um conjunto rico de ferramentas para interação profunda com o ambiente pós-simulação</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">Interação Profunda</div>
                  <div class="step-desc">Converse com qualquer indivíduo no mundo simulado & interaja com o ReportAgent</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel: Interactive Console -->
        <div class="right-panel">
          <div class="console-box">
            <!-- Upload Area -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">01 / Sementes da Realidade</span>
                <span class="console-meta">Formatos suportados: PDF, MD, TXT</span>
              </div>
              
              <div 
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">Arraste e solte arquivos para enviar</div>
                  <div class="upload-hint">ou clique para navegar no sistema de arquivos</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Project Name -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ Nome do Projeto</span>
              </div>
              <input
                v-model="formData.projectName"
                class="name-input"
                placeholder="Ex: Análise de Opinião Pública"
                :disabled="loading"
              />
            </div>

            <!-- Divider -->
            <div class="console-divider">
              <span>Parâmetros de Entrada</span>
            </div>

            <!-- Input Area -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ 02 / Prompt de Simulação</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  placeholder="// Insira requisitos de simulação ou previsão em linguagem natural (ex.: Se uma universidade anunciar a reversão de uma ação disciplinar, quais tendências de opinião pública surgiriam?)"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">Motor: MiroFish-V1.0</div>
              </div>
            </div>

            <!-- Launch Button -->
            <div class="console-section btn-section">
              <button
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">Iniciar Motor</span>
                <span v-else>Inicializando...</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Projetos Existentes -->
      <section class="projects-section" v-if="projects.length > 0">
        <div class="projects-header">
          <span class="diamond-icon">◇</span> Projetos Existentes
          <button class="refresh-projects-btn" @click="loadProjects" title="Atualizar">↻</button>
        </div>
        <div class="projects-grid">
          <div
            v-for="proj in projects"
            :key="proj.project_id"
            class="project-card"
            @click="openProject(proj)"
          >
            <div class="project-card-header">
              <span class="project-status-dot" :class="proj.status"></span>
              <span v-if="editingProject !== proj.project_id" class="project-name">{{ proj.name || 'Projeto Sem Nome' }}</span>
              <input
                v-else
                v-model="editName"
                class="project-name-input"
                @click.stop
                @keyup.enter="saveProjectName(proj)"
                @keyup.escape="editingProject = null"
                ref="editInput"
              />
            </div>
            <div class="project-card-id">{{ proj.project_id }}</div>
            <div class="project-card-meta">
              <span class="project-card-status">{{ formatStatus(proj.status, proj.error) }}</span>
              <span class="project-card-files">{{ (proj.files || []).length }} arquivo(s)</span>
            </div>
            <div class="project-card-date">{{ formatDate(proj.created_at) }}</div>
            <div class="project-card-actions" @click.stop>
              <button
                v-if="editingProject !== proj.project_id"
                class="action-btn edit-btn"
                @click="startEdit(proj)"
                title="Editar nome"
              >✎</button>
              <button
                v-else
                class="action-btn save-btn"
                @click="saveProjectName(proj)"
                title="Salvar"
              >✓</button>
              <button
                v-if="proj.status === 'graph_building' || proj.status === 'ontology_generating'"
                class="action-btn stop-btn"
                @click="stopProject(proj)"
                title="Parar build"
              >◼</button>
              <button
                v-if="proj.error === 'paused'"
                class="action-btn resume-btn"
                @click="resumeProject(proj)"
                title="Continuar de onde parou"
              >▶</button>
              <button
                v-if="proj.status === 'ontology_generated' || proj.status === 'failed' || proj.error === 'paused'"
                class="action-btn rebuild-btn"
                @click="rebuildProject(proj)"
                title="Refazer do zero"
              >↻</button>
              <button
                class="action-btn delete-btn"
                @click="deleteProject(proj)"
                title="Excluir projeto"
              >✕</button>
            </div>
            <div class="project-card-arrow">→</div>
          </div>
        </div>
      </section>

      <!-- History Database -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()

// Form data
const formData = ref({
  simulationRequirement: '',
  projectName: ''
})

// File list
const files = ref([])

// Projects list
const projects = ref([])

// State
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// Load existing projects
const loadProjects = async () => {
  try {
    const res = await axios.get('/api/graph/project/list')
    if (res.data.success) {
      projects.value = res.data.data.sort((a, b) =>
        new Date(b.created_at) - new Date(a.created_at)
      )
    }
  } catch (e) {
    console.error('Erro ao carregar projetos:', e)
  }
}

const openProject = (proj) => {
  router.push({ name: 'Process', params: { projectId: proj.project_id } })
}

const formatStatus = (status, error) => {
  if (error === 'paused') return 'Pausado'
  const map = {
    'created': 'Criado',
    'ontology_generating': 'Gerando Ontologia',
    'ontology_generated': 'Ontologia Gerada',
    'graph_building': 'Construindo Grafo',
    'graph_completed': 'Grafo Completo',
    'failed': 'Erro',
  }
  return map[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

// Edit project
const editingProject = ref(null)
const editName = ref('')

const startEdit = (proj) => {
  editingProject.value = proj.project_id
  editName.value = proj.name || ''
}

const saveProjectName = async (proj) => {
  try {
    await axios.patch(`/api/graph/project/${proj.project_id}`, { name: editName.value })
    proj.name = editName.value
    editingProject.value = null
  } catch (e) {
    console.error('Erro ao salvar nome:', e)
  }
}

const stopProject = async (proj) => {
  if (!confirm('Tem certeza que deseja parar o build deste projeto?')) return
  try {
    await axios.post(`/api/graph/project/${proj.project_id}/stop`)
    await loadProjects()
  } catch (e) {
    console.error('Erro ao parar projeto:', e)
  }
}

const resumeProject = async (proj) => {
  try {
    await axios.post(`/api/graph/project/${proj.project_id}/resume`)
    await loadProjects()
  } catch (e) {
    console.error('Erro ao retomar projeto:', e)
    alert('Erro ao retomar: ' + (e.response?.data?.error || e.message))
  }
}

const rebuildProject = async (proj) => {
  if (!confirm('Refazer o grafo do zero? Todo o progresso anterior será perdido.')) return
  try {
    await axios.post(`/api/graph/build`, {
      project_id: proj.project_id,
      force: true
    })
    await loadProjects()
  } catch (e) {
    console.error('Erro ao refazer projeto:', e)
    alert('Erro ao refazer: ' + (e.response?.data?.error || e.message))
  }
}

const deleteProject = async (proj) => {
  if (!confirm(`Excluir o projeto "${proj.name || proj.project_id}"? Esta ação não pode ser desfeita.`)) return
  try {
    await axios.delete(`/api/graph/project/${proj.project_id}`)
    projects.value = projects.value.filter(p => p.project_id !== proj.project_id)
  } catch (e) {
    console.error('Erro ao excluir projeto:', e)
  }
}

onMounted(() => {
  loadProjects()
})

// File input ref
const fileInput = ref(null)

// Computed: whether form can be submitted
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

// Trigger file selection
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// Handle file selection
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// Handle drag events
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// Add files
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// Remove file
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// Scroll to bottom
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// Start simulation - navigate immediately, API calls happen on Process page
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return

  // Store pending upload data
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement, formData.value.projectName)

    // Navigate to Process page immediately (use special identifier for new project)
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* Global variables & reset */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  /*
    Use Space Grotesk as main heading font, JetBrains Mono for code/label font
    Make sure these Google Fonts are imported in index.html
  */
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* Top Navigation */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
}

.github-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

/* Main content area */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero area */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 500;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: var(--black);
}

.gradient-text {
  background: linear-gradient(90deg, #000000 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--black);
  font-weight: 700;
}

.highlight-orange {
  color: var(--orange);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--black);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: var(--black);
  letter-spacing: 1px;
  border-left: 3px solid var(--orange);
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: var(--orange);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
}

.hero-logo {
  max-width: 500px; /* Adjust logo size */
  width: 100%;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--orange);
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--orange);
}

/* Dashboard dual panel layout */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* Left panel */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid var(--border);
  padding: 20px 30px;
  min-width: 150px;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
}

/* Simulation workflow steps */
.steps-container {
  border: 1px solid var(--border);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--black);
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* Right interactive console */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid #CCC; /* Outer solid border */
  padding: 8px; /* Inner padding for double-border effect */
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

.upload-zone {
  border: 1px dashed #CCC;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #FAFAFA;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: #F0F0F0;
  border-color: #999;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #AAA;
}

.start-engine-btn {
  width: 100%;
  background: var(--black);
  color: var(--white);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* Clickable state (not disabled) */
.start-engine-btn:not(:disabled) {
  background: var(--black);
  border: 1px solid var(--black);
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E5E5;
}

/* Guide animation: subtle border pulse */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

/* Projects Section */
.projects-section {
  border-top: 1px solid var(--border);
  padding-top: 50px;
  margin-top: 60px;
}

.projects-header {
  font-family: var(--font-mono);
  font-size: 0.9rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 25px;
}

.refresh-projects-btn {
  background: none;
  border: 1px solid var(--border);
  cursor: pointer;
  font-size: 1rem;
  color: #999;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10px;
  transition: all 0.2s;
}

.refresh-projects-btn:hover {
  border-color: var(--orange);
  color: var(--orange);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.project-card {
  border: 1px solid var(--border);
  padding: 20px 24px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.project-card:hover {
  border-color: var(--black);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.project-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.project-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #999;
  flex-shrink: 0;
}

.project-status-dot.graph_completed { background: #22c55e; }
.project-status-dot.graph_building { background: var(--orange); animation: pulse-dot 1.5s infinite; }
.project-status-dot.ontology_generated { background: #3b82f6; }
.project-status-dot.ontology_generating { background: #eab308; animation: pulse-dot 1.5s infinite; }
.project-status-dot.created { background: #999; }
.project-status-dot.failed { background: #ef4444; }

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.project-name {
  font-weight: 600;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-card-id {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #bbb;
  margin-bottom: 12px;
}

.project-card-meta {
  display: flex;
  gap: 16px;
  font-size: 0.8rem;
  margin-bottom: 6px;
}

.project-card-status {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--black);
}

.project-card-files {
  color: #999;
}

.project-card-date {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #bbb;
}

.project-card-actions {
  display: flex;
  gap: 6px;
  margin-top: 10px;
}

.action-btn {
  width: 28px;
  height: 28px;
  border: 1px solid var(--border);
  background: #fff;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: #999;
}

.action-btn:hover { border-color: #999; color: var(--black); }
.stop-btn:hover { border-color: var(--orange); color: var(--orange); }
.resume-btn:hover { border-color: #22c55e; color: #22c55e; }
.rebuild-btn:hover { border-color: #3b82f6; color: #3b82f6; }
.delete-btn:hover { border-color: #ef4444; color: #ef4444; }
.save-btn:hover { border-color: #22c55e; color: #22c55e; }

.project-name-input {
  flex: 1;
  border: 1px solid var(--orange);
  background: #fff;
  padding: 4px 8px;
  font-size: 0.95rem;
  font-weight: 600;
  font-family: inherit;
  outline: none;
}

.name-input {
  width: 100%;
  border: 1px solid #DDD;
  background: #FAFAFA;
  padding: 12px 16px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.name-input:focus {
  border-color: var(--orange);
}

.name-input::placeholder {
  color: #bbb;
}

.project-card-arrow {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 1.2rem;
  color: #ddd;
  transition: all 0.2s;
}

.project-card:hover .project-card-arrow {
  color: var(--orange);
  transform: translateX(3px);
}

/* Responsive layout */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>
