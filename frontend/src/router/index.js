import { createRouter, createWebHistory } from 'vue-router';
import IndexPage from '../views/index/IndexPage.vue';
import PreferencesPage from '../views/index/PreferencesPage.vue';
import GoodsPage from '../views/index/GoodsPage.vue';  // 新增商品展示页面
import Product_Categories from '../views/index/Product_Categories';
import CategoryPage from '../views/index/CategoryPage';
import SearchPage from '../views/index/SearchPage';
import DetailPage from '../views/index/DetailPage';
import PriceCompare from '../views/index/PriceCompare';
import MyRoom from '../views/index/MyRoom';
import ChangePassword from '../views/index/ChangePassword';
import ChangePreferences from '../views/index/ChangePreferences';
import MyFavorites from '../views/index/MyFavorites';
import DiscountInfo from '../views/index/DiscountInfo';
import GradientLineChart from '../Charts/GradientLineChart';
import LoginPage from '../views/index/PC/LoginPage.vue'; // 引入电脑页面

// 检测设备类型，判断是否为电脑设备
function isDesktop() {
  const userAgent = navigator.userAgent.toLowerCase();

  // 检测是否是移动设备，基本上大多数移动设备都会匹配到这些条件
  const isMobile = /iphone|ipod|android.*mobile/i.test(userAgent);

  // 检测是否为平板设备，这样的设备通常会有"tablet"关键字
  const isTablet = /ipad|android(?!.*mobile)/i.test(userAgent);

  // 如果是移动设备或者平板设备，则认为是移动端，否则为桌面设备
  return !(isMobile || isTablet);
}
const routes = [
  {
    path: '/',
    name: 'IndexPage',
    component: IndexPage,
  },
  {
    path: '/goods',
    name: 'GoodsPage',
    component: GoodsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/PreferencesPage',
    name: 'PreferencesPage',
    component: PreferencesPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/Product_Categories',
    name: 'Product_Categories',
    component: Product_Categories,
    meta: { requiresAuth: true },
  },
  {
    path: '/CategoryPage',
    name: 'CategoryPage',
    component: CategoryPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/SearchPage',
    name: 'SearchPage',
    component: SearchPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/DetailPage',
    name: 'DetailPage',
    component: DetailPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/PriceCompare',
    name: 'PriceCompare',
    component: PriceCompare,
    meta: { requiresAuth: true },
  },
  {
    path: '/MyRoom',
    name: 'MyRoom',
    component: MyRoom,
    meta: { requiresAuth: true },
  },
  {
    path: '/ChangePassword',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: { requiresAuth: true },
  },
  {
    path: '/ChangePreferences',
    name: 'ChangePreferences',
    component: ChangePreferences,
    meta: { requiresAuth: true },
  },
  {
    path: '/MyFavorites',
    name: 'MyFavorites',
    component: MyFavorites,
    meta: { requiresAuth: true },
  },
  {
    path: '/GradientLineChart',
    name: 'GradientLineChart',
    component: GradientLineChart,
    meta: { requiresAuth: true },
  },
  {
    path: '/DiscountInfo',
    name: 'DiscountInfo',
    component: DiscountInfo,
    meta: { requiresAuth: true },
  },
  {
    path: '/PC/LoginPage',
    name: 'LoginPage',
    component: LoginPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token'); // 获取登录的 token

  // 如果目标路由是首页且是电脑设备，跳转到 LoginPage
  if (to.path === '/' && isDesktop()) {
    next({ name: 'LoginPage' }); // 电脑设备访问首页时跳转到 LoginPage
  }
  // 如果是需要认证的页面且没有 token 且是电脑设备，跳转到 LoginPage
  else if (to.matched.some(record => record.meta.requiresAuth) && !token && isDesktop()) {
    next({ name: 'LoginPage' });
  }
  // 如果是需要认证的页面且没有 token 且是手机设备，跳转到 IndexPage
  else if (to.matched.some(record => record.meta.requiresAuth) && !token && !isDesktop()) {
    next({ name: 'IndexPage' });
  } else {
    next(); // 允许进入页面
  }
});

export default router;
