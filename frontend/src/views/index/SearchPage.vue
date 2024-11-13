<template>
  <div class="search-page">
    <!-- 显示搜索结果或者提示用户登录 -->
    <div v-if="isLoggedIn">
      <h2>搜索结果</h2>
      <div class="embedded-taobao">
        <!-- 使用 iframe 嵌入淘宝搜索页面 -->
        <iframe
          :src="taobaoUrl"
          frameborder="0"
          class="taobao-iframe"
        ></iframe>
      </div>
    </div>
    <div v-else>
      <!-- 显示用户确认登录按钮 -->
      <h2>请确认您已经登录淘宝</h2>
      <p>请点击下方按钮确认登录。</p>
      <button @click="confirmLogin">我已经确认登录淘宝</button>
      <div class="embedded-taobao-login">
        <iframe
          src="https://login.taobao.com/member/login.jhtml"
          frameborder="0"
          class="taobao-iframe"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: this.$route.query.searchQuery || '',
      isLoggedIn: false,  // 用户登录状态
    };
  },
  computed: {
    taobaoUrl() {
      // 将搜索关键字编码到淘宝搜索 URL 中
      return `https://s.taobao.com/search?q=${encodeURIComponent(this.searchQuery)}`;
    },
  },
  methods: {
    confirmLogin() {
      // 当用户点击按钮时，记录登录状态并显示搜索结果
      this.isLoggedIn = true;  // 假设用户已经登录
      localStorage.setItem('isLoggedIn', 'true'); // 记录登录状态
    },

    checkLoginStatus() {
      // 检查 localStorage 中是否存在登录状态
      const loggedIn = localStorage.getItem('isLoggedIn') === 'true';
      if (loggedIn) {
        this.isLoggedIn = true; // 如果已记录为登录状态，直接显示搜索结果
      }
    },
  },
  mounted() {
    // 检查是否已记录登录状态
    this.checkLoginStatus();
  },
};
</script>

<style scoped>
.search-page {
  padding: 20px;
}

.embedded-taobao {
  margin-top: 20px;
  width: 100%;
  height: 500px;
  border: 1px solid #ddd;
}

.taobao-iframe {
  width: 100%;
  height: 100%;
}

.embedded-taobao-login {
  margin-top: 20px;
  width: 100%;
  height: 500px;
  border: 1px solid #ddd;
}

h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

p {
  font-size: 18px;
  color: #333;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
