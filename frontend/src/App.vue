<template>
  <div class="app-container">
    <div class="sidebar">
      <div class="logo">
        <h1>K8s Manager</h1>
      </div>
      <el-menu :default-active="activeMenu" :router="true" class="menu">
        <el-menu-item index="/">
          <span>仪表板</span>
        </el-menu-item>
        <el-menu-item index="/pods">
          <span>Pod管理</span>
        </el-menu-item>
        <el-menu-item index="/deployments">
          <span>Deployment管理</span>
        </el-menu-item>
        <el-menu-item index="/services">
          <span>Service管理</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
}

.sidebar {
  width: 200px;
  background-color: #545c64;
  color: white;
  overflow-y: auto;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #444;
}

.logo h1 {
  margin: 0;
  font-size: 18px;
  color: white;
}

.menu {
  border-right: none;
  background-color: #545c64;
}

.menu :deep(.el-menu-item) {
  color: #fff;
}

.menu :deep(.el-menu-item:hover) {
  background-color: #434a52 !important;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
