import request from './request.js'

export const getMoveinstudents = (params) => {
  return request({
    url: '/move_in_records',
    method: 'GET',
    params
  })
}

export const addMoveinstudents = (data) => {
  return request({
    url: '/move_in_records',
    method: 'POST',
    data
  })
}

export const editMoveinstudents = (data) => {
  return request({
    url: '/move_in_records/',
    method: 'PUT',
    data
  })
}

export const delMoveinstudents = (id) => {
  return request({
    url: '/move_in_records/',
    method: 'DELETE',
    data: {
      id: id
    }
  })
}
