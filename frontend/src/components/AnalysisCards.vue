<script setup lang="ts">
import { computed } from 'vue'
import type { ScoredMessage, IndexPoint, KlineBar } from '../api/index'

const props = defineProps<{
  messages: ScoredMessage[]
  index: IndexPoint[]
  kline: KlineBar[]
}>()

const avgScore = computed(() => {
  if (!props.messages.length) return 0
  const sum = props.messages.reduce((a, m) => a + m.score, 0)
  return (sum / props.messages.length).toFixed(1)
})

const currentIndex = computed(() => {
  if (!props.index.length) return 0
  return props.index[props.index.length - 1].index
})

const scoreClass = computed(() => {
  const v = Number(avgScore.value)
  if (v > 0) return 'positive'
  if (v < 0) return 'negative'
  return 'neutral'
})

const topDimension = computed(() => {
  const count: Record<string, number> = {}
  for (const m of props.messages) {
    if (m.dimension) {
      count[m.dimension] = (count[m.dimension] || 0) + 1
    }
  }
  const sorted = Object.entries(count).sort((a, b) => b[1] - a[1])
  return sorted[0]?.[0] || '—'
})

const posCount = computed(() => props.messages.filter((m) => m.score > 0).length)
const negCount = computed(() => props.messages.filter((m) => m.score < 0).length)
const neuCount = computed(() => props.messages.filter((m) => m.score === 0).length)
</script>

<template>
  <div class="cards-grid">
    <div class="stat-card">
      <div class="stat-label">消息总数</div>
      <div class="stat-value">{{ messages.length }}</div>
    </div>

    <div class="stat-card">
      <div class="stat-label">平均情感分</div>
      <div class="stat-value" :class="scoreClass">{{ avgScore }}</div>
    </div>

    <div class="stat-card">
      <div class="stat-label">当前关系指数</div>
      <div class="stat-value" :class="currentIndex >= 0 ? 'positive' : 'negative'">
        {{ currentIndex }}
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-label">最主要维度</div>
      <div class="stat-value dimension">{{ topDimension }}</div>
    </div>
  </div>

  <div class="breakdown-bar">
    <div class="breakdown-seg positive" :style="{ flex: posCount }" />
    <div class="breakdown-seg neutral" :style="{ flex: neuCount }" />
    <div class="breakdown-seg negative" :style="{ flex: negCount }" />
  </div>

  <div class="breakdown-legend">
    <span class="legend-item">
      <span class="dot positive-dot" /> 积极 {{ posCount }}
    </span>
    <span class="legend-item">
      <span class="dot neutral-dot" /> 中性 {{ neuCount }}
    </span>
    <span class="legend-item">
      <span class="dot negative-dot" /> 负面 {{ negCount }}
    </span>
  </div>
</template>

<style scoped>
.cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 24px 0;
}

@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.stat-value.positive { color: var(--green); }
.stat-value.negative { color: var(--red); }
.stat-value.neutral { color: var(--gold); }
.stat-value.dimension { font-size: 22px; color: var(--text-primary); }

.breakdown-bar {
  display: flex;
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
  margin-top: 4px;
}

.breakdown-seg.positive { background: var(--green); }
.breakdown-seg.neutral { background: var(--gold); }
.breakdown-seg.negative { background: var(--red); }

.breakdown-legend {
  display: flex;
  gap: 20px;
  margin-top: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.positive-dot { background: var(--green); }
.neutral-dot { background: var(--gold); }
.negative-dot { background: var(--red); }
</style>
