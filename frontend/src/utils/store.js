import { reactive } from 'vue'
import { fetchDashboardStats } from '../api/dashboard'

export const appStore = reactive({
  dashboardStats: null,
  dashboardLoading: false,
  dashboardError: ''
})

let dashboardRefreshPromise = null

export async function refreshDashboardStats(force = false) {
  if (appStore.dashboardLoading && !force) {
    return dashboardRefreshPromise
  }
  appStore.dashboardLoading = true
  appStore.dashboardError = ''
  dashboardRefreshPromise = (async () => {
    try {
      appStore.dashboardStats = await fetchDashboardStats()
      return appStore.dashboardStats
    } catch (err) {
      appStore.dashboardError = err.message
      throw err
    } finally {
      appStore.dashboardLoading = false
      dashboardRefreshPromise = null
    }
  })()
  return dashboardRefreshPromise
}
