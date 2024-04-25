
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ExploreView from '../views/ExploreView.vue';
import UserProfileView from '../views/UserProfileView.vue';
import RegisterForm from '../components/RegisterForm.vue';
import LoginForm from '../components/LoginForm.vue';
import PostForm from '../components/PostForm.vue';


const ROUTE_NAMES = {
  HOME: 'home',
  REGISTER: 'register',
  LOGIN: 'login',
  NEW_POST: 'new post',
  LOGOUT: 'logout',
  EXPLORE: 'explore',
  ALL_POSTS: 'all posts'
};


const routes = [
  { path: '/', name: ROUTE_NAMES.HOME, component: HomeView },
  { path: '/register', name: ROUTE_NAMES.REGISTER, component: RegisterForm, meta: { auth: false } },
  { path: '/login', name: ROUTE_NAMES.LOGIN, component: LoginForm, meta: { auth: false } },
  { path: '/posts/new', name: ROUTE_NAMES.NEW_POST, component: PostForm, meta: { auth: true } },
  { path: '/logout', name: ROUTE_NAMES.LOGOUT, component: LoginForm },
  { path: '/explore', name: ROUTE_NAMES.EXPLORE, component: ExploreView, meta: { auth: true } },
  { path: '/users/:id', name: ROUTE_NAMES.ALL_POSTS, component: UserProfileView, meta: { auth: true } }
];


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token"); 
  if (to.meta.auth && !token) {
    next("/login"); 
  } else if (!to.meta.auth && token) {
    next("/explore"); 
  } else {
    next(); 
  }
});


export default router;
