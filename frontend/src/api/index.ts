import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 300_000,
})

export interface ScoredMessage {
  time: string
  sender: string
  message: string
  score: number
  dimension: string
  reason: string
}

export interface IndexPoint {
  time: string
  index: number
}

export interface KlineBar {
  date: string
  open: number
  high: number
  low: number
  close: number
}

export interface GenerateKlineResponse {
  messages: ScoredMessage[]
  index: IndexPoint[]
  kline: KlineBar[]
}

export async function generateKline(file: File): Promise<GenerateKlineResponse> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<GenerateKlineResponse>('/generate-kline', form)
  return data
}

export interface TaskStatus {
  task_id: string
  status: 'pending' | 'processing' | 'done' | 'error' | 'not_found'
  progress: { current: number; total: number }
  result: GenerateKlineResponse | null
  error: string | null
}

export async function generateKlineAsync(file: File): Promise<{ task_id: string }> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<{ task_id: string }>('/generate-kline-async', form)
  return data
}

export async function getTaskStatus(taskId: string): Promise<TaskStatus> {
  const { data } = await api.get<TaskStatus>(`/task/${taskId}`)
  return data
}

export async function exportExcel(
  payload: GenerateKlineResponse
): Promise<Blob> {
  const { data } = await api.post('/export', payload, {
    responseType: 'blob',
  })
  return data
}

export function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
