import VideoDetail from '@/components/video/VideoDetail.vue'
import LoginView from '@/views/auth/LoginView.vue'
import OnboardingView from '@/views/auth/OnboardingView.vue'
import SignupView from '@/views/auth/SignupView.vue'
import BankSearchView from '@/views/finance/BankSearchView.vue'
import CommoditySearchView from '@/views/finance/CommoditySearchView.vue'
import VideoSearchView from '@/views/finance/VideoSearchView.vue'
import HomeView from '@/views/HomeView.vue'
import MoathonCreateView from '@/views/moathon/MoathonCreateView.vue'
import MoathonDetailView from '@/views/moathon/MoathonDetailView.vue'
import MoathonListView from '@/views/moathon/MoathonListView.vue'
import MoathonRecommendView from '@/views/moathon/MoathonRecommendView.vue'
import ProductListView from '@/views/product/ProductListView.vue'
import ProductDetailView from '@/views/product/ProductDetailView.vue'
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
          path: 'recommend',
          name: 'moathonRecommend',
          component: MoathonRecommendView,
        },
        {
          path: 'create',
          name: 'moathonCreate',
          component: MoathonCreateView,
          // 다이렉트 모드는 productId가 필수이므로, 없으면 추천 페이지로 리다이렉트하는 가드 추가
          beforeEnter: (to, from, next) => {
            if (!to.query.productId) {
              next({ name: 'moathonRecommend' })
            } else {
              next()
            }
          }
        },
        {
          path: ':id',
          name: 'moathonDetail',
          component: MoathonDetailView,
        },
      ]
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
    },
    {
      path: '/video',
      children: [
        {
          path: 'search',
          name: 'videoSearch',
          component: VideoSearchView,
        },
        {
          path: ':id',
          name: 'videoDetail',
          component: VideoDetail,
        },
      ]
    },
    {
      path: '/bank',
      name: 'bank',
      component: BankSearchView,
    },
    {
      path: '/commodity',
      name: 'commodity',
      component: CommoditySearchView,
    },
    {
      path: '/products',
      children: [
        {
          path: '',
          name: 'products',
          component: ProductListView,
        },
        {
          path: ':id',
          name: 'productDetail',
          component: ProductDetailView,
        }
      ],
    },
  ],
})

export default router
