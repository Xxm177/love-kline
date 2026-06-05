<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { KlineBar, IndexPoint } from '../api/index'

const props = defineProps<{
  kline: KlineBar[]
  index: IndexPoint[]
}>()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

function calcMA(data: number[], period: number): (number | null)[] {
  const result: (number | null)[] = []
  for (let i = 0; i < data.length; i++) {
    if (i < period - 1) {
      result.push(null)
    } else {
      let sum = 0
      for (let j = i - period + 1; j <= i; j++) sum += data[j]
      result.push(Number((sum / period).toFixed(1)))
    }
  }
  return result
}

function buildOption(): echarts.EChartsOption {
  const dates = props.kline.map((k) => k.date)
  const ohlc = props.kline.map((k) => [k.open, k.close, k.low, k.high])
  const closes = props.kline.map((k) => k.close)
  const ma5 = calcMA(closes, 5)
  const ma10 = calcMA(closes, 10)

  const indexData = props.index.map((p) => [p.time, p.index])

  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      backgroundColor: '#1c2333',
      borderColor: '#30363d',
      textStyle: { color: '#e6edf3', fontSize: 12 },
    },
    legend: {
      top: 0,
      left: 'center',
      textStyle: { color: '#8b949e', fontSize: 11 },
      itemWidth: 14,
      itemHeight: 8,
      data: ['K线', 'MA5', 'MA10'],
    },
    grid: [
      { left: '3%', right: '3%', top: '8%', height: '52%' },
      { left: '3%', right: '3%', top: '68%', height: '24%' },
    ],
    xAxis: [
      {
        type: 'category',
        data: dates,
        gridIndex: 0,
        axisLine: { lineStyle: { color: '#30363d' } },
        axisLabel: { color: '#8b949e', fontSize: 11 },
        axisTick: { show: false },
      },
      {
        type: 'category',
        data: dates,
        gridIndex: 1,
        axisLine: { lineStyle: { color: '#30363d' } },
        axisLabel: { show: false },
        axisTick: { show: false },
      },
    ],
    yAxis: [
      {
        type: 'value',
        gridIndex: 0,
        scale: true,
        axisLine: { show: false },
        axisLabel: { color: '#8b949e', fontSize: 11 },
        splitLine: { lineStyle: { color: '#1a1a2e' } },
      },
      {
        type: 'value',
        gridIndex: 1,
        axisLine: { show: false },
        axisLabel: { color: '#8b949e', fontSize: 11 },
        splitLine: { lineStyle: { color: '#1a1a2e' } },
      },
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 0,
        end: 100,
      },
      {
        type: 'slider',
        xAxisIndex: [0, 1],
        start: 0,
        end: 100,
        bottom: 0,
        height: 20,
        borderColor: '#30363d',
        backgroundColor: '#161b22',
        fillerColor: 'rgba(233, 69, 96, 0.15)',
        textStyle: { color: '#8b949e' },
      },
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: ohlc,
        itemStyle: {
          color: '#26a69a',
          color0: '#ef5350',
          borderColor: '#26a69a',
          borderColor0: '#ef5350',
        },
        markPoint: {
          label: {
            formatter: (p: any) => Math.round(p.value as number).toString(),
            color: '#e6edf3',
          },
        },
      },
      {
        name: 'MA5',
        type: 'line',
        data: ma5,
        smooth: true,
        symbol: 'none',
        lineStyle: { color: '#f5a623', width: 1.5 },
      },
      {
        name: 'MA10',
        type: 'line',
        data: ma10,
        smooth: true,
        symbol: 'none',
        lineStyle: { color: '#7b68ee', width: 1.5 },
      },
      {
        name: '关系指数',
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: indexData,
        smooth: true,
        symbol: 'none',
        lineStyle: {
          color: '#e94560',
          width: 2,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(233, 69, 96, 0.3)' },
            { offset: 1, color: 'rgba(233, 69, 96, 0.02)' },
          ]),
        },
      },
    ],
  }
}

function initChart() {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value, undefined, { renderer: 'canvas' })
  chart.setOption(buildOption())
}

function handleResize() {
  chart?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

watch(() => props.kline, () => {
  chart?.setOption(buildOption())
})
</script>

<template>
  <div class="chart-wrapper">
    <div class="chart-header">
      <h3>关系 K 线走势图</h3>
      <div class="chart-legend">
        <span class="legend-tag up">阳线</span>
        <span class="legend-tag down">阴线</span>
        <span class="legend-tag ma5">MA5</span>
        <span class="legend-tag ma10">MA10</span>
        <span class="legend-tag index-line">指数</span>
      </div>
    </div>
    <div ref="chartRef" class="chart-canvas" />
  </div>
</template>

<style scoped>
.chart-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
}

.chart-legend {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.legend-tag {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 4px;
}
.legend-tag.up { background: rgba(38, 166, 154, 0.15); color: var(--green); }
.legend-tag.down { background: rgba(239, 83, 80, 0.15); color: var(--red); }
.legend-tag.ma5 { background: rgba(245, 166, 35, 0.15); color: #f5a623; }
.legend-tag.ma10 { background: rgba(123, 104, 238, 0.15); color: #7b68ee; }
.legend-tag.index-line { background: rgba(233, 69, 96, 0.15); color: var(--accent); }

.chart-canvas {
  width: 100%;
  height: 520px;
}
</style>
