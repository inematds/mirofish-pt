/**
 * Temporary storage for pending file uploads and requirements.
 * Used when launching the engine from the homepage - stores data
 * before navigating to Process page where the API call is made.
 */
import { reactive } from 'vue'

const state = reactive({
  files: [],
  simulationRequirement: '',
  projectName: '',
  isPending: false
})

export function setPendingUpload(files, requirement, projectName) {
  state.files = files
  state.simulationRequirement = requirement
  state.projectName = projectName || ''
  state.isPending = true
}

export function getPendingUpload() {
  return {
    files: state.files,
    simulationRequirement: state.simulationRequirement,
    projectName: state.projectName,
    isPending: state.isPending
  }
}

export function clearPendingUpload() {
  state.files = []
  state.simulationRequirement = ''
  state.projectName = ''
  state.isPending = false
}

export default state
