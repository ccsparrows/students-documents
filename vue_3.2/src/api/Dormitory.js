import request from './request.js'

export const getDormitory = (params) => {
  return request({
    url: '/dormitories',
    method: 'GET',
    params
  })
}

export const addDormitory = (data) => {
  return request({
    url: '/dormitories',
    method: 'POST',
    data
  })
}

export const editDormitory = (data) => {
  return request({
    url: '/dormitories',
    method: 'PUT',
    data
  })
}

export const delDormitory = (id) => {
  return request({
    url: '/dormitories',
    method: 'DELETE',
    data: {
      id: id
    }
  })
}
