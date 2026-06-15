<template>
  <div class="deployment-list">
    <h1>Deployment管理</h1>
    
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input v-model="namespace" placeholder="输入namespace" clearable></el-input>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="loadDeployments">查询</el-button>
          <el-button @click="refreshDeployments">刷新</el-button>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="content-card">
      <el-table :data="deployments" stripe v-loading="loading">
        <el-table-column prop="name" label="名称" width="200"></el-table-column>
        <el-table-column prop="namespace" label="Namespace" width="150"></el-table-column>
        <el-table-column prop="ready" label="就绪"></el-table-column>
        <el-table-column prop="up_to_date" label="最新"></el-table-column>
        <el-table-column prop="available" label="可用"></el-table-column>
        <el-table-column prop="image" label="镜像"></el-table-column>
        <el-table-column prop="age" label="年龄"></el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDeployment(row)">详情</el-button>
            <el-button type="danger" size="small" @click="deleteDeployment(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { deploymentAPI } from '../api/deployment'

const router = useRouter()
const deployments = ref([])
const namespace = ref('default')
const loading = ref(false)

const loadDeployments = async () => {
  loading.value = true
  try {
    const response = await deploymentAPI.listDeployments(namespace.value)
    deployments.value = response.data || []
  } catch (error) {
    ElMessage.error('加载Deployment失败')
  } finally {
    loading.value = false
  }
}

const refreshDeployments = () => {
  loadDeployments()
}

const viewDeployment = (row: any) => {
  router.push({ name: 'DeploymentDetail', params: { name: row.name }, query: { namespace: row.namespace } })
}

const deleteDeployment = (row: any) => {
  ElMessageBox.confirm(`确定删除Deployment ${row.name}?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    deploymentAPI.deleteDeployment(row.name, row.namespace).then(() => {
      ElMessage.success('删除成功')
      loadDeployments()
    })
  }).catch(() => {})
}

onMounted(() => {
  loadDeployments()
})
</script>

<style scoped>
.deployment-list {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.content-card {
  margin-top: 20px;
}
</style>
