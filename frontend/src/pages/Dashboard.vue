<template>
  <div class="dashboard">
    <h1>仪表板</h1>
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-number">-</div>
          <div class="stat-label">集群</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-number">{{ podCount }}</div>
          <div class="stat-label">Pod</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-number">{{ deploymentCount }}</div>
          <div class="stat-label">Deployment</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-number">-</div>
          <div class="stat-label">Service</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { podAPI } from '../api/pod'
import { deploymentAPI } from '../api/deployment'

const podCount = ref(0)
const deploymentCount = ref(0)

const loadStats = async () => {
  try {
    const podsRes = await podAPI.listPods()
    podCount.value = podsRes.data?.length || 0
    
    const deploymentsRes = await deploymentAPI.listDeployments()
    deploymentCount.value = deploymentsRes.data?.length || 0
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stat-card {
  text-align: center;
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  margin-top: 10px;
  color: #606266;
  font-size: 14px;
}
</style>
