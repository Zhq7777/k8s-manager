<template>
  <div class="deployment-detail">
    <el-button @click="goBack" style="margin-bottom: 20px">返回</el-button>
    <el-card v-if="deployment">
      <template #header>
        <div class="card-header">
          <span>{{ deployment.name }}</span>
        </div>
      </template>
      
      <el-tabs>
        <el-tab-pane label="基础信息">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="名称">{{ deployment.name }}</el-descriptions-item>
            <el-descriptions-item label="Namespace">{{ deployment.namespace }}</el-descriptions-item>
            <el-descriptions-item label="副本数">{{ deployment.replicas }}</el-descriptions-item>
            <el-descriptions-item label="就绪">{{ deployment.status.ready }}/{{ deployment.status.desired }}</el-descriptions-item>
            <el-descriptions-item label="最新">{{ deployment.status.updated }}</el-descriptions-item>
            <el-descriptions-item label="可用">{{ deployment.status.available }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ deployment.created_at }}</el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { deploymentAPI } from '../api/deployment'

const route = useRoute()
const router = useRouter()
const deployment = ref(null)

const loadDeployment = async () => {
  try {
    const namespace = route.query.namespace || 'default'
    const response = await deploymentAPI.getDeployment(route.params.name as string, namespace as string)
    deployment.value = response.data
  } catch (error) {
    ElMessage.error('加载Deployment失败')
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  loadDeployment()
})
</script>

<style scoped>
.deployment-detail {
  padding: 20px;
}
</style>
