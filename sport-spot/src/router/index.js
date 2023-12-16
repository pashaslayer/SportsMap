// here we will setup all the new routes

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CaptchaView from '../views/CaptchaView.vue'
import PickSportsView from '../views/PickSportsView.vue'

// route array that contains paths as elements
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/LoginView.vue')
  },
  {
    path: '/registration',
    name: 'registration',
    component: () => import(/* webpackChunkName: "registration" */ '../views/RegistrationView.vue')
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import(/* webpackChunkName: "admin" */ '../views/AdminView.vue')
  },
  {
    path: '/map',
    name: 'MapView',
    component: () => import(/* webpackChunkName: "map" */ '../views/MapView.vue')
  },
  {
    // here a example of 
    path: '/picksports',
    name: 'PickSportsView',
    component: PickSportsView,
    // Add a beforeEnter guard to check if the user has a valid JWT token
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        // User has a token, allow access to the route
        next();
      } else {
        // User does not have a token, redirect to the login page
        next('/login');
      }
    },
  },
  {
    // here a example of 
    path: '/captcha',
    name: 'CaptchaView',
    component: CaptchaView,
    // Add a beforeEnter guard to check if the user has a valid JWT token
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('jwt_token');
      if (token) {
        // User has a token, allow access to the route
        next();
      } else {
        // User does not have a token, redirect to the login page
        next('/login');
      }
    },
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
