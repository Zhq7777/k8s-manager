<template>
  <div class="pod-list">
    <h1>Pod管理</h1>
    
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input v-model="namespace" placeholder="输入namespace" clearable></el-input>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="loadPods">查询</el-button>
          <el-button @click="refreshPods">刷新</el-button>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="content-card">
      <el-table :data="pods" stripe v-loading="loading">
        <el-table-column prop="name" label="名称" width="200"></el-table-column>
        <el-table-column prop="namespace" label="Namespace" width="150"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ready" label="就绪"></el-table-column>
        <el-table-column prop="restarts" label="重启"></el-table-column>
        <el-table-column prop="age" label="年龄"></el-table-column>
        <el-table-column prop="ip" label="IP"></el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewPod(row)">详情</el-button>
            <el-button type="danger" size="small" @click="deletePod(row)">删除</el-button>
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
import { podAPI } from '../api/pod'

const router = useRouter()
const pods = ref([])
const namespace = ref('default')
const loading = ref(false)

const loadPods = async () => {
  loading.value = true
  try {
    const response = await podAPI.listPods(namespace.value)
    pods.value = response.data || []
  } catch (error) {
    ElMessage.error('加载Pod失败')
  } finally {
    loading.value = false
  }
}

const refreshPods = () => {
  loadPods()
}

const viewPod = (row: any) => {
  router.push({ name: 'PodDetail', params: { name: row.name }, query: { namespace: row.namespace } })
}

const deletePod = (row: any) => {
  ElMessageBox.confirm(`确定删除Pod ${row.name}?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    podAPI.deletePod(row.name, row.namespace).then(() => {
      ElMessage.success('删除成功')
      loadPods()
    })
  }).catch(() => {})
}

const getStatusType = (status: string) => {
  if (status === 'Running') return 'success'
  if (status === 'Pending') return 'warning'
  return 'danger'
}

onMounted(() => {
  loadPods()
})
</script>

<style scoped>
.pod-list {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.content-card {
  margin-top: 20px;
}
</style>
