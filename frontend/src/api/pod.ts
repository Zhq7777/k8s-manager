import apiClient from './client'

export const podAPI = {
  listPods(namespace = 'default') {
    return apiClient.get('/pods', { params: { namespace } })
  },

  getPod(name: string, namespace = 'default') {
    return apiClient.get(`/pods/${name}`, { params: { namespace } })
  },

  getPodLogs(name: string, namespace = 'default', container?: string) {
    return apiClient.get(`/pods/${name}/logs`, { 
      params: { namespace, container } 
    })
  },

  deletePod(name: string, namespace = 'default') {
    return apiClient.delete(`/pods/${name}`, { params: { namespace } })
  }
}
