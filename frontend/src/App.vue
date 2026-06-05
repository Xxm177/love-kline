<script setup lang="ts">
import { ref, computed } from 'vue'
import { Download } from '@element-plus/icons-vue'
import UploadArea from './components/UploadArea.vue'
import AnalysisCards from './components/AnalysisCards.vue'
import KlineChart from './components/KlineChart.vue'
import {
  generateKline,
  exportExcel,
  downloadBlob,
  type GenerateKlineResponse,
  type ScoredMessage,
} from './api/index'

const result = ref<GenerateKlineResponse | null>(null)
const loading = ref(false)
const error = ref('')
const showMessages = ref(false)
const sortKey = ref<keyof ScoredMessage>('time')
const sortAsc = ref(true)

const sortedMessages = computed(() => {
  if (!result.value) return []
  const msgs = [...result.value.messages]
  msgs.sort((a, b) => {
    const va = a[sortKey.value]
    const vb = b[sortKey.value]
    if (typeof va === 'number' && typeof vb === 'number') {
      return sortAsc.value ? va - vb : vb - va
    }
    const cmp = String(va).localeCompare(String(vb))
    return sortAsc.value ? cmp : -cmp
  })
  return msgs
})

function toggleSort(key: keyof ScoredMessage) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = true
  }
}

function scoreColor(s: number) {
  if (s > 0) return 'var(--green)'
  if (s < 0) return 'var(--red)'
  return 'var(--gold)'
}

async function handleAnalyze(file: File) {
  loading.value = true
  error.value = ''
  showMessages.value = false
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
      <UploadArea :loading="loading" @analyze="handleAnalyze" />

      <div v-if="error" class="error-banner">{{ error }}</div>

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

        <!-- Message Detail Table -->
        <div class="message-section">
          <div class="section-header" @click="showMessages = !showMessages">
            <h4>消息评分详情 ({{ result.messages.length }} 条)</h4>
            <span class="toggle-icon">{{ showMessages ? '▾' : '▸' }}</span>
          </div>

          <div v-if="showMessages" class="table-wrap">
            <table class="msg-table">
              <thead>
                <tr>
                  <th @click="toggleSort('time')" class="sortable">
                    时间 {{ sortKey === 'time' ? (sortAsc ? '↑' : '↓') : '' }}
                  </th>
                  <th @click="toggleSort('sender')" class="sortable">
                    发送者 {{ sortKey === 'sender' ? (sortAsc ? '↑' : '↓') : '' }}
                  </th>
                  <th class="msg-col">消息</th>
                  <th @click="toggleSort('score')" class="sortable">
                    评分 {{ sortKey === 'score' ? (sortAsc ? '↑' : '↓') : '' }}
                  </th>
                  <th @click="toggleSort('dimension')" class="sortable">
                    维度 {{ sortKey === 'dimension' ? (sortAsc ? '↑' : '↓') : '' }}
                  </th>
                  <th class="reason-col">原因</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(m, i) in sortedMessages" :key="i">
                  <td class="time-cell">{{ m.time }}</td>
                  <td>{{ m.sender }}</td>
                  <td class="msg-cell">{{ m.message }}</td>
                  <td :style="{ color: scoreColor(m.score), fontWeight: '700' }">
                    {{ m.score > 0 ? '+' : '' }}{{ m.score }}
                  </td>
                  <td>
                    <span v-if="m.dimension" class="dim-tag">{{ m.dimension }}</span>
                  </td>
                  <td class="reason-cell">{{ m.reason }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
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

/* ── Message Table ── */
.message-section {
  margin-top: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid transparent;
}

.section-header:hover { background: rgba(255,255,255,0.02); }
.section-header h4 { font-size: 15px; font-weight: 600; }

.toggle-icon {
  font-size: 18px;
  color: var(--text-secondary);
}

.table-wrap {
  overflow-x: auto;
  max-height: 500px;
  overflow-y: auto;
  border-top: 1px solid var(--border);
}

.msg-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.msg-table thead {
  position: sticky;
  top: 0;
  z-index: 1;
}

.msg-table th {
  background: #1a1a2e;
  color: var(--text-secondary);
  padding: 10px 14px;
  text-align: left;
  font-weight: 600;
  white-space: nowrap;
  border-bottom: 1px solid var(--border);
}

.msg-table th.sortable {
  cursor: pointer;
}
.msg-table th.sortable:hover {
  color: var(--text-primary);
}

.msg-table td {
  padding: 10px 14px;
  border-bottom: 1px solid rgba(48, 54, 61, 0.5);
  vertical-align: middle;
}

.msg-table tbody tr:hover {
  background: rgba(255,255,255,0.03);
}

.time-cell { color: var(--text-secondary); white-space: nowrap; font-size: 12px; }
.msg-cell { max-width: 200px; }
.reason-cell { color: var(--text-secondary); max-width: 260px; font-size: 12px; }

.dim-tag {
  display: inline-block;
  padding: 1px 8px;
  border-radius: 10px;
  background: rgba(233, 69, 96, 0.12);
  color: var(--accent);
  font-size: 12px;
  white-space: nowrap;
}
</style>
