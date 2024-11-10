import axios from 'axios'
import {
  ElMessage
} from 'element-plus'
import {
  diffTokenTime
} from '@/utils/auth'
import store from '@/store'
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000
})

service.interceptors.request.use(
  (config) => {
    if (localStorage.getItem('token')) {
      if (diffTokenTime()) {
        store.dispatch('app/logout')
        return Promise.reject(new Error('token 失效了'))
      }
    }
    config.headers.Authorization = localStorage.getItem('token')
    return config
  },
  (error) => {
    return Promise.reject(new Error(error))
  }
)

service.interceptors.response.use(
  (response) => {
    if (response.data.status === 200) {
      //window.location.href = '/';
      console.log("response.data")
      return response.data;
    }
    if (response.data.status === 400 || response.data.status === 401) {
      ElMessage.error(response.data.message);
      return Promise.reject(new Error(response.data.message));
    }
  },
  (error) => {
    if (error.response && error.response.data && error.response.data.message) {
      console.log(error.response.data.message);
      ElMessage.error(error.response.data.message);
      //return Promise.reject(new Error(error.response.data.message));
    } else {
      console.error('Network error:', error);
      ElMessage.error('Network error');
      //return Promise.reject(new Error('Network error'));
    }
  }
);

export default service
