import request from './request.js'

export const StudentsList = () => {
  return request({
    url: '/students',
    method: 'GET'
  })
}
