import { createApp } from 'vue'
import App from './App.vue'
import './assets/style.css';
import router from './router/index.js';
import 'amfe-flexible'
const app = createApp(App);
app.use(router);
app.mount('#app');
// 重置登录状态
localStorage.setItem('isLoggedIn', 'false');
