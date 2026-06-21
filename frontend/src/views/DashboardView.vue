<template>
  <section class="panel">
    <SectionToolbar eyebrow="Dashboard" title="运营看板">
      <button type="button" class="ghost-button" :disabled="appStore.dashboardLoading" @click="refreshDashboardStats(true)">
        {{ appStore.dashboardLoading ? '刷新中...' : '刷新' }}
      </button>
    </SectionToolbar>

    <div v-if="!appStore.dashboardStats && !appStore.dashboardLoading" class="stats-empty">
      <p>暂无数据，请点击右上角"刷新"按钮加载</p>
      <button v-if="appStore.dashboardError" type="button" class="ghost-button" @click="refreshDashboardStats(true)">
        重试加载
      </button>
    </div>

    <p v-if="appStore.dashboardError && appStore.dashboardStats" class="error">{{ appStore.dashboardError }}（显示的为上次加载的数据）</p>
    <div v-if="appStore.dashboardStats">
      <div class="stats-grid">
        <button type="button" class="stat-card" @click="$emit('navigate', 'workstations')">
          <span>总工位</span>
          <strong>{{ appStore.dashboardStats.total_workstations }}</strong>
        </button>
        <button type="button" class="stat-card" @click="$emit('navigate', 'workstations')">
          <span>可租工位</span>
          <strong>{{ appStore.dashboardStats.available_workstations }}</strong>
        </button>
        <button type="button" class="stat-card" @click="$emit('navigate', 'contracts')">
          <span>履行合同</span>
          <strong>{{ appStore.dashboardStats.active_contracts }}</strong>
        </button>
        <button type="button" class="stat-card" @click="$emit('navigate', 'reminders')">
          <span>30天到期</span>
          <strong>{{ appStore.dashboardStats.expiring_contracts }}</strong>
        </button>
      </div>
      <div class="stats-amounts-wrap" :class="{ 'is-loading': appStore.dashboardLoading, 'is-error': appStore.dashboardError }">
        <div class="stats-grid stats-amounts-group">
          <button type="button" class="stat-card warning" @click="$emit('navigate', 'payments')">
            <span class="stat-card-label">待收金额</span>
            <strong class="stat-card-number">{{ currency(appStore.dashboardStats.unpaid_amount) }}</strong>
          </button>
          <button type="button" class="stat-card success" @click="$emit('navigate', 'payments')">
            <span class="stat-card-label">已收金额</span>
            <strong class="stat-card-number">{{ currency(appStore.dashboardStats.paid_amount) }}</strong>
          </button>
          <button type="button" class="stat-card danger" @click="$emit('navigate', 'reminders')">
            <span class="stat-card-label">逾期金额</span>
            <strong class="stat-card-number">{{ currency(appStore.dashboardStats.overdue_amount) }}</strong>
          </button>
        </div>
        <div v-if="appStore.dashboardLoading" class="stats-amounts-overlay">
          <span class="stats-loading-text">更新中...</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import SectionToolbar from '../components/SectionToolbar.vue'
import { appStore, refreshDashboardStats } from '../utils/store'
import { notify } from '../utils/notify'
import { currency } from '../utils/formatters'

defineEmits(['navigate'])

watch(
  () => appStore.dashboardError,
  (err, prev) => {
    if (err && err !== prev) {
      notify.error(`看板刷新失败：${err}`)
    }
  }
)

onMounted(() => {
  if (!appStore.dashboardStats) {
    refreshDashboardStats()
  }
})
</script>
