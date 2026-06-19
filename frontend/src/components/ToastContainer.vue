<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div v-for="toast in toasts" :key="toast.id" :class="['toast', `toast-${toast.type}`]">
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { notify } from '../utils/notify'
const { toasts } = notify
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast {
  min-width: 240px;
  max-width: 380px;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  font-size: 14px;
  line-height: 1.5;
  pointer-events: auto;
  animation: shake 0.3s ease-out;
}

.toast-success {
  background: #e7f6ec;
  border: 1px solid #a8d8b8;
  color: #1b6b35;
}

.toast-error {
  background: #fde8e7;
  border: 1px solid #f6b8b3;
  color: #9f1d14;
}

.toast-warning {
  background: #fff4d6;
  border: 1px solid #e8d092;
  color: #7a5200;
}

.toast-info {
  background: #e6f0fa;
  border: 1px solid #a8c8e8;
  color: #1d5f8f;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-4px);
  }
  75% {
    transform: translateX(4px);
  }
}

.toast-enter-active {
  transition: all 0.3s ease-out;
}

.toast-leave-active {
  transition: all 0.25s ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(40px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(40px);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>
