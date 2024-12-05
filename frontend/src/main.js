import { createApp } from 'vue'
import App from './App.vue'
import './assets/style.css';
import router from './router/index.js';
import 'amfe-flexible'
import store from "./store";
import ArgonDashboard from "./argon-dashboard";
const app = createApp(App);
app.use(router);
app.mount('#app');
app.use(store);
app.use(ArgonDashboard);
// 重置登录状态
// 每次应用启动时清除 token
localStorage.setItem('isLoggedIn', 'false');
