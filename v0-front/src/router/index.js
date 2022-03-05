import { createRouter, createWebHistory } from 'vue-router'

import AccountView from '../views/AccountView.vue'
import FindCourses from '../views/FindCourses.vue'
import LoginView from '../views/LoginView.vue'
import MyCourses from '../views/MyCourses.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  {
    path: '/account',
    name: 'account',
    component: AccountView
  },
  {
    path: '/find-courses',
    name: 'find-courses',
    component: FindCourses
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/my-courses',
    name: 'home',
    component: MyCourses
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  { path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
