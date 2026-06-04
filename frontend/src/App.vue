<script setup lang="ts">
import { ref } from 'vue'
import { Download } from '@element-plus/icons-vue'
import UploadArea from './components/UploadArea.vue'
import AnalysisCards from './components/AnalysisCards.vue'
import KlineChart from './components/KlineChart.vue'
import {
  generateKline,
  exportExcel,
  downloadBlob,
  type GenerateKlineResponse,
} from './api/index'

const result = ref<GenerateKlineResponse | null>(null)
const loading = ref(false)
const error = ref('')

async function handleAnalyze(file: File) {
  loading.value = true
  error.value = ''
  try {
    result.value = await generateKline(file)
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e?.message || '分析失败，请重试'
  } finally {
    loading.value = false
  }
}

async function handleExport() {
  if (!result.value) return
  try {
    const blob = await exportExcel(result.value)
    downloadBlob(blob, 'love_kline.xlsx')
  } catch (e: any) {
    error.value = '导出失败，请重试'
  }
}
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo">
        <span class="logo-icon">♥</span>
        <h1>Love Kline</h1>
      </div>
      <p class="subtitle">关系 K 线分析</p>
    </header>

    <main class="app-main">
      <UploadArea
        :loading="loading"
        @analyze="handleAnalyze"
      />

      <div v-if="error" class="error-banner">
        {{ error }}
      </div>

      <template v-if="result">
        <AnalysisCards
          :messages="result.messages"
          :index="result.index"
          :kline="result.kline"
        />

        <div class="export-bar">
          <el-button
            type="primary"
            :icon="Download"
            size="large"
            @click="handleExport"
          >
            导出 Excel
          </el-button>
        </div>

        <KlineChart
          :kline="result.kline"
          :index="result.index"
        />
      </template>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  padding-bottom: 60px;
}

.app-header {
  text-align: center;
  padding: 48px 20px 32px;
  background: linear-gradient(180deg, #1a1a2e 0%, var(--bg-primary) 100%);
  border-bottom: 1px solid var(--border);
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.logo-icon {
  font-size: 32px;
  color: var(--accent);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.logo h1 {
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, var(--text-primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin-top: 8px;
  font-size: 14px;
  color: var(--text-secondary);
  letter-spacing: 2px;
}

.app-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
}

.error-banner {
  margin: 16px 0;
  padding: 12px 20px;
  background: rgba(239, 83, 80, 0.15);
  border: 1px solid rgba(239, 83, 80, 0.3);
  border-radius: var(--radius);
  color: var(--red);
  font-size: 14px;
}

.export-bar {
  display: flex;
  justify-content: flex-end;
  margin: 24px 0;
}
</style>
