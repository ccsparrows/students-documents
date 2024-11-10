import request from './request.js'

export const getMoveoutstudents = (params) => {
  return request({
    url: '/move_out_records',
    method: 'GET',
    params
  })
}

export const addMoveoutstudents = (data) => {
  return request({
    url: '/move_out_records/',
    method: 'POST',
    data
  })
}

export const editMoveoutstudents = (data) => {
  return request({
    url: '/move_out_records/',
    method: 'PUT',
    data
  })
}

export const delMoveoutstudents = (id) => {
  return request({
    url: '/move_out_records/',
    method: 'DELETE',
    data: {
      id: id
    }
  })
}
