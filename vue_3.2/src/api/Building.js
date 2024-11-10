import request from './request.js'

export const getBuilding = (params) => {
  return request({
    url: '/buildings',
    method: 'GET',
    params
  })
}

export const addBuilding = (data) => {
  return request({
    url: '/buildings',
    method: 'POST',
    data
  })
}

export const editBuilding = (data) => {
  return request({
    url: '/buildings',
    method: 'PUT',
    data
  })
}

export const delBuilding = (id) => {
  return request({
    url: '/buildings',
    method: 'DELETE',
    data: {
      id: id
    }
  })
}
