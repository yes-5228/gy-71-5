<template>
  <section class="panel">
    <SectionToolbar eyebrow="Dashboard" title="运营看板">
      <button type="button" class="ghost-button" :disabled="appStore.dashboardLoading" @click="refreshDashboardStats(true)">
        {{ appStore.dashboardLoading ? '刷新中...' : '刷新' }}
      </button>
    </SectionToolbar>

    <p v-if="appStore.dashboardError" class="error">{{ appStore.dashboardError }}</p>
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
      <div class="stats-grid stats-amounts-group">
        <button type="button" class="stat-card warning" @click="$emit('navigate', 'payments')">
          <span>待收金额</span>
          <strong>{{ currency(appStore.dashboardStats.unpaid_amount) }}</strong>
        </button>
        <button type="button" class="stat-card success" @click="$emit('navigate', 'payments')">
          <span>已收金额</span>
          <strong>{{ currency(appStore.dashboardStats.paid_amount) }}</strong>
        </button>
        <button type="button" class="stat-card danger" @click="$emit('navigate', 'reminders')">
          <span>逾期金额</span>
          <strong>{{ currency(appStore.dashboardStats.overdue_amount) }}</strong>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
import SectionToolbar from '../components/SectionToolbar.vue'
import { appStore, refreshDashboardStats } from '../utils/store'
import { currency } from '../utils/formatters'

defineEmits(['navigate'])

onMounted(() => {
  if (!appStore.dashboardStats) {
    refreshDashboardStats()
  }
})
</script>
