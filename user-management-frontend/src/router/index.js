// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from '../views/WelcomePage.vue';
import AdminLogin from '../views/AdminLogin.vue';  // Make sure this path is correct!
import AdminDashboard from '../views/AdminDashboard.vue';
import UserDashboard from '../views/UserDashboard.vue';
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: WelcomePage
  },

  {
    path: '/admin-login',
    name: 'AdminLogin',
    component: AdminLogin  // The component to load when "/admin-login" is navigated to
  },

  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/user',
    name: 'UserDashboard',
    component: UserDashboard
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage
  }
  // Add other routes here as needed...
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
