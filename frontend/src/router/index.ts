import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../pages/Dashboard.vue')
  },
  {
    path: '/pods',
    name: 'Pods',
    component: () => import('../pages/PodList.vue')
  },
  {
    path: '/pods/:name',
    name: 'PodDetail',
    component: () => import('../pages/PodDetail.vue')
  },
  {
    path: '/deployments',
    name: 'Deployments',
    component: () => import('../pages/DeploymentList.vue')
  },
  {
    path: '/deployments/:name',
    name: 'DeploymentDetail',
    component: () => import('../pages/DeploymentDetail.vue')
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('../pages/ServiceList.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
