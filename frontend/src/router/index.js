import { createRouter, createWebHistory } from 'vue-router';
import IndexPage from '../views/index/IndexPage.vue';
import PreferencesPage from '../views/index/PreferencesPage.vue';
import GoodsPage from '../views/index/GoodsPage.vue';  // 新增商品展示页面
import Product_Categories from '../views/index/Product_Categories';
import CategoryPage from '../views/index/CategoryPage';
import SearchPage from '../views/index/SearchPage';

const routes = [
  {
    path: '/',
    name: 'IndexPage',
    component: IndexPage,
  },
  {
    path: '/goods',
    name: 'GoodsPage',
    component: GoodsPage,  // 商品展示页面
    meta: { requiresAuth: true },
  },
  {
    path: '/PreferencesPage',
    name: 'PreferencesPage',
    component: PreferencesPage,  // 商品展示页面
    meta: { requiresAuth: true },
  },
  {
    path: '/Product_Categories',
    name: 'Product_Categories',
    component: Product_Categories,  // 商品分类页面
    meta: { requiresAuth: true },
  },
  {
    path: '/CategoryPage',
    name: 'CategoryPage',
    component: CategoryPage,  // 商品分类页面
    meta: { requiresAuth: true },
  },
  {
    path: '/SearchPage',
    name: 'SearchPage',
    component: SearchPage,  // 商品分类页面
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token'); // 获取登录的 token

  // 如果目标路由需要认证并且没有 token，跳转到 IndexPage
  if (to.matched.some(record => record.meta.requiresAuth) && !token) {
    next({ name: 'IndexPage' });
  } else {
    next(); // 允许进入页面
  }
});

export default router;
