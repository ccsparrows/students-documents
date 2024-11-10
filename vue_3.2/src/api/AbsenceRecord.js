import request from './request.js'

export const getAbsenceRecord = (params) => {
  return request({
    url: '/absence_records/',
    method: 'GET',
    params
  })
}
export const addAbsenceRecord = (data) => {
  return request({
    url: '/absence_records',
    method: 'POST',
    data
  })
}

export const editAbsenceRecord = (data) => {
  return request({
    url: '/absence_records/',
    method: 'PUT',
    data
  })
}

export const delAbsenceRecord = (id) => {
  return request({
    url: '/absence_records/',
    method: 'DELETE',
    data: {
      id: id
    }
  })
}
