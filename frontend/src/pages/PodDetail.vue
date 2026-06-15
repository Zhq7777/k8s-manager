<template>
  <div class="pod-detail">
    <el-button @click="goBack" style="margin-bottom: 20px">返回</el-button>
    <el-card v-if="pod">
      <template #header>
        <div class="card-header">
          <span>{{ pod.metadata.name }}</span>
        </div>
      </template>
      
      <el-tabs>
        <el-tab-pane label="基础信息">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="名称">{{ pod.metadata.name }}</el-descriptions-item>
            <el-descriptions-item label="Namespace">{{ pod.metadata.namespace }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(pod.status.phase)">{{ pod.status.phase }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="Node">{{ pod.node || 'N/A' }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ pod.created_at }}</el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>
        <el-tab-pane label="容器">
          <el-table :data="pod.containers" stripe>
            <el-table-column prop="name" label="容器名"></el-table-column>
            <el-table-column prop="image" label="镜像"></el-table-column>
            <el-table-column prop="state" label="状态"></el-table-column>
            <el-table-column prop="ready" label="就绪" type="boolean"></el-table-column>
            <el-table-column prop="restarts" label="重启"></el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { podAPI } from '../api/pod'

const route = useRoute()
const router = useRouter()
const pod = ref(null)

const loadPod = async () => {
  try {
    const namespace = route.query.namespace || 'default'
    const response = await podAPI.getPod(route.params.name as string, namespace as string)
    pod.value = response.data
  } catch (error) {
    ElMessage.error('加载Pod失败')
  }
}

const goBack = () => {
  router.back()
}

const getStatusType = (status: string) => {
  if (status === 'Running') return 'success'
  if (status === 'Pending') return 'warning'
  return 'danger'
}

onMounted(() => {
  loadPod()
})
</script>

<style scoped>
.pod-detail {
  padding: 20px;
}
</style>
