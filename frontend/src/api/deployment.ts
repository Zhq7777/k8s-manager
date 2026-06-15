import apiClient from './client'

export const deploymentAPI = {
  listDeployments(namespace = 'default') {
    return apiClient.get('/deployments', { params: { namespace } })
  },

  getDeployment(name: string, namespace = 'default') {
    return apiClient.get(`/deployments/${name}`, { params: { namespace } })
  },

  createDeployment(data: any) {
    return apiClient.post('/deployments', data)
  },

  updateDeployment(name: string, data: any, namespace = 'default') {
    return apiClient.patch(`/deployments/${name}`, data, { params: { namespace } })
  },

  deleteDeployment(name: string, namespace = 'default') {
    return apiClient.delete(`/deployments/${name}`, { params: { namespace } })
  },

  scaleDeployment(name: string, replicas: number, namespace = 'default') {
    return apiClient.post(`/deployments/${name}/scale`, {}, { 
      params: { namespace, replicas } 
    })
  }
}
