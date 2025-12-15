import LoginView from '@/views/auth/LoginView.vue'
import OnboardingView from '@/views/auth/OnboardingView.vue'
import SignupView from '@/views/auth/SignupView.vue'
import HomeView from '@/views/HomeView.vue'
import MoathonCreateView from '@/views/moathon/MoathonCreateView.vue'
import MoathonDetailView from '@/views/moathon/MoathonDetailView.vue'
import MoathonListView from '@/views/moathon/MoathonListView.vue'
import MyPageView from '@/views/user/MyPageView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: OnboardingView,
    },
    {
      path: '/moathons',
      name: 'explore',
      component: MoathonListView,
    },
    {
      path: '/moathon',
      children: [
        {
          path: 'create',
          name: 'create',
          component: MoathonCreateView,
        },
        {
          path: ':id',
          name: 'detail',
          component: MoathonDetailView,
        },
      ]
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
    },
  ],
})

export default router
