import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TimeMachine from '@/views/TimeMachine.vue'
import AiCurator from '@/views/AiCurator.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/time-machine',
      name: 'time-machine',
      component: TimeMachine,
    },
    {
      path: '/ai-curator',
      name: 'ai-curator',
      component: AiCurator,
    },
  ],
})

export default router
