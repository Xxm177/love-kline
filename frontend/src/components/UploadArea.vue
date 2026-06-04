<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'

defineProps<{ loading: boolean }>()
const emit = defineEmits<{ analyze: [file: File] }>()

const fileList = ref<any[]>([])

function handleChange(_file: any, files: any) {
  fileList.value = files
}

function handleAnalyze() {
  const file = fileList.value[0]?.raw
  if (file) emit('analyze', file)
}
</script>

<template>
  <div class="upload-section">
    <el-upload
      v-model:file-list="fileList"
      drag
      :auto-upload="false"
      :limit="1"
      accept=".txt"
      :on-change="handleChange"
    >
      <div class="upload-content">
        <el-icon class="upload-icon"><UploadFilled /></el-icon>
        <p class="upload-title">拖拽聊天记录文件到此处</p>
        <p class="upload-hint">支持 .txt 格式，每条消息格式：YYYY-MM-DD HH:MM 发送者：内容</p>
      </div>
    </el-upload>

    <el-button
      type="primary"
      size="large"
      :loading="loading"
      :disabled="fileList.length === 0"
      class="analyze-btn"
      @click="handleAnalyze"
    >
      {{ loading ? '正在分析中...' : '开始分析' }}
    </el-button>
  </div>
</template>

<style scoped>
.upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.upload-content {
  padding: 32px 20px;
}

.upload-icon {
  font-size: 48px;
  color: var(--accent);
  margin-bottom: 16px;
}

.upload-title {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 13px;
  color: var(--text-secondary);
}

.analyze-btn {
  min-width: 200px;
  height: 48px;
  font-size: 16px;
}
</style>
