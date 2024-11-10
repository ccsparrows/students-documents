import { login as loginApi } from '@/api/login'
import router from '@/router'
import { setTokenTime } from '@/utils/auth'
export default {
  namespaced: true,
  state: () => ({
    token: localStorage.getItem('token') || '',
    siderType: true
  }),
  mutations: {
    setToken(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    changeSiderType(state) {
      state.siderType = !state.siderType
    },
    changLang(state, lang) {
      state.lang = lang
    }
  },
  actions: {
    login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        loginApi(userInfo)
          .then((res) => {
            if (!res) {
              return resolve() // 直接 resolve，避免进入 catch
            }
            // 检查 res.token 是否存在
            if (!res.token) {
              return resolve() // 直接 resolve，避免进入 catch
            }
            if (res && res.token) {
              console.log(res)
              commit('setToken', res.token)
              setTokenTime()
              router.replace('/')
              resolve()
            } else {
              reject('Login failed: No token in response')
              ElMessage.error('Login failed: No token in response')
            }
          })
          .catch((err) => {
            reject(err)
            ElMessage.error(err.message || 'Login failed')
          })
      })
    },
    logout({ commit }) {
      commit('setToken', '')
      localStorage.clear()
      router.replace('/login')
    }
  }
}
