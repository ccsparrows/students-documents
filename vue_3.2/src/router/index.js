import {
  createRouter,
  createWebHashHistory
} from 'vue-router'

const routes = [{
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/index.vue')
  },
  {
    path: '/',
    name: '',
    component: () => import('../layout'),
    redirect: '/MoveInRecord',
    children: [{
        path: 'MoveInRecord',
        name: 'MoveInRecord',
        component: () => import('@/views/MoveInRecord/index.vue')
      },
      {
        path: 'MoveOutRecord',
        name: 'MoveOutRecord',
        component: () => import('@/views/MoveOutRecord/index.vue')
      },
      {
        path: 'AbsenceRecord',
        name: 'AbsenceRecord',
        component: () => import('@/views/AbsenceRecord/index.vue')
      },
      {
        path: 'Building',
        name: 'Building',
        component: () => import('@/views/Building/index.vue')
      },
      {
        path: 'Dormitory',
        name: 'Dormitory',
        component: () => import('@/views/Dormitory/index.vue')
      }

    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
