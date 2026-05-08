import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/views/home.vue')
    },
    {
      path: '/scatter',
      component: () => import('@/views/scatter.vue')
    }
  ]
})

export default router
