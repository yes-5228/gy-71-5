<template>
  <section class="panel">
    <SectionToolbar eyebrow="Payments" title="费用收缴">
      <select v-model="statusFilter" @change="loadPayments">
        <option value="">全部账单</option>
        <option value="unpaid">待收</option>
        <option value="overdue">逾期</option>
        <option value="paid">已收</option>
      </select>
    </SectionToolbar>

    <form class="form-grid" @submit.prevent="submit">
      <select v-model.number="form.contract_id" required>
        <option value="" disabled>选择合同</option>
        <option v-for="contract in activeContracts" :key="contract.id" :value="contract.id">
          {{ contract.contract_no }} / {{ contract.tenant_name }}
        </option>
      </select>
      <input v-model="form.period" placeholder="账期 2026-06" required />
      <input v-model.number="form.amount" type="number" min="0" placeholder="应收金额" required />
      <input v-model="form.due_date" type="date" required />
      <input v-model="form.note" placeholder="备注" />
      <button type="submit">创建账单</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>合同</th>
            <th>租户</th>
            <th>账期</th>
            <th>金额</th>
            <th>到期日</th>
            <th>状态</th>
            <th>收款</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payment in payments" :key="payment.id">
            <td>{{ payment.contract_no }}</td>
            <td>{{ payment.tenant_name }}</td>
            <td>{{ payment.period }}</td>
            <td>{{ currency(payment.amount) }}</td>
            <td>{{ payment.due_date }}</td>
            <td><StatusBadge :value="payment.status" /></td>
            <td>
              <button
                v-if="payment.status !== 'paid'"
                type="button"
                class="small-button"
                :disabled="pendingIds.has(payment.id)"
                :class="{ 'button-loading': pendingIds.has(payment.id) }"
                @click="pay(payment)"
              >
                {{ pendingIds.has(payment.id) ? '确认中...' : '确认收款' }}
              </button>
              <span v-else>{{ payment.method || '已入账' }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { fetchContracts } from '../api/contracts'
import { createPayment, fetchPayments, markPaymentPaid } from '../api/payments'
import SectionToolbar from '../components/SectionToolbar.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { notify } from '../utils/notify'
import { refreshDashboardStats } from '../utils/store'
import { currency, todayISO } from '../utils/formatters'

const payments = ref([])
const activeContracts = ref([])
const statusFilter = ref('')
const error = ref('')
const pendingIds = reactive(new Set())
const form = reactive({
  contract_id: '',
  period: todayISO().slice(0, 7),
  amount: 0,
  due_date: todayISO(),
  note: ''
})

watch(
  () => form.contract_id,
  (id) => {
    const contract = activeContracts.value.find((item) => item.id === Number(id))
    if (contract) {
      form.amount = Number(contract.monthly_rent)
    }
  }
)

async function loadPayments() {
  error.value = ''
  try {
    payments.value = await fetchPayments(statusFilter.value)
  } catch (err) {
    error.value = err.message
    notify.error(err.message)
  }
}

async function loadContracts() {
  activeContracts.value = await fetchContracts('active')
}

async function load() {
  try {
    await Promise.all([loadPayments(), loadContracts()])
  } catch (err) {
    error.value = err.message
  }
}

async function submit() {
  error.value = ''
  try {
    await createPayment({ ...form, contract_id: Number(form.contract_id) })
    Object.assign(form, { contract_id: '', period: todayISO().slice(0, 7), amount: 0, due_date: todayISO(), note: '' })
    notify.success('账单创建成功')
    try {
      await Promise.all([loadPayments(), refreshDashboardStats(true)])
    } catch (refreshErr) {
      notify.warning('账单创建成功，但看板数据刷新失败，显示的可能是旧数据')
    }
  } catch (err) {
    error.value = err.message
    notify.error(err.message)
  }
}

async function pay(payment) {
  const id = payment.id
  if (pendingIds.has(id)) {
    notify.warning('正在确认收款中，请稍候...')
    return
  }
  if (payment.status === 'paid') {
    notify.warning('该账单已收款，无需重复操作')
    return
  }
  error.value = ''
  pendingIds.add(id)
  try {
    const result = await markPaymentPaid(id, { method: 'bank_transfer', note: '前台确认收款' })
    try {
      await Promise.all([loadPayments(), refreshDashboardStats(true)])
    } catch (refreshErr) {
      notify.warning('收款成功，但看板数据刷新失败，显示的可能是旧数据')
    }
    if (result.already_paid) {
      notify.warning('该账单已收款，状态已更新')
    } else {
      notify.success(`收款成功：${payment.tenant_name} - ${currency(payment.amount)}`)
    }
  } catch (err) {
    error.value = err.message
    notify.error(`收款失败：${err.message}`)
  } finally {
    pendingIds.delete(id)
  }
}

onMounted(load)
</script>

<style scoped>
.button-loading {
  opacity: 0.7;
  cursor: not-allowed !important;
}

.small-button:disabled {
  opacity: 0.6;
  cursor: not-allowed !important;
  background: #f0f0f0;
}
</style>
