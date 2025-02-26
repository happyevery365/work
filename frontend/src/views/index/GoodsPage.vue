<template>
  <!-- 平台图标展示区域 -->
  <div class="app-icons" v-if="appImages.length">
    <div class="app-icon-item" v-for="(app, index) in appImages" :key="index">
      <img :src="app.img_url" :alt="app.appname" class="app-icon-image" />
    </div>
  </div>

  <!-- 用户信息和退出登录按钮 -->
  <div class="user-info">
    <span class="username">你好，{{ username }}</span>
    <button @click="logout" class="logout-button">退出登录</button>
  </div>

  <!-- 搜索框区域 -->
  <div class="search-background">
    <div class="search-container">
      <div class="search-input-wrapper">
        <input type="text" v-model="searchQuery" placeholder="请输入搜索内容" class="search-input" />
        <button @click="performSearch" class="search-button">搜索</button>
      </div>
    </div>
  </div>

  <!-- 商品展示区域 -->
  <h2>猜您喜欢</h2>
  <div v-if="goods.length" class="products-grid">
    <div class="product-item" v-for="(item, index) in goods" :key="index" @click="goToDetailPage(item)">
      <img :src="item.img_url" alt="商品图片" class="product-image" />
      <div class="product-details">
        <p class="product-title">{{ item.title }}</p>
        <p class="product-price">价格: {{ item.price }}</p>
      </div>
    </div>
  </div>
  <p v-else>暂无商品信息</p>

  <!-- 固定底部导航栏 -->
  <div class="bottom-nav">
    <div
      v-for="(navItem, index) in navItems"
      :key="index"
      class="nav-item"
      :class="{ selected: currentPage === navItem.page }"
      @click="goToPage(navItem.page)"
    >
      {{ navItem.name }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ipAddress } from './config.js';

export default {
  data() {
    return {
      searchQuery: '',
      appImages: [],
      goods: [],
      username: '',
      navItems: [
        { name: '首页', page: 'GoodsPage' },
        { name: '分类', page: 'Product_Categories' },
        { name: '比价', page: 'PriceCompare' },
        { name: '我的', page: 'MyRoom' }
      ],
      currentPage: 'GoodsPage',
      ipAddress:''
    };
  },
  created() {
    this.ipAddress = ipAddress;
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
    }
  },
  mounted() {
    this.fetchGoods();
    this.fetchAppImages();
  },
  methods: {
    async performSearch() {
      if (!this.searchQuery) {
        alert('搜索框不能为空');
        return;
      }
      this.$router.push({ name: 'SearchPage', query: { username: this.username, searchQuery: this.searchQuery } });
    },
    async fetchGoods() {
      const response = await axios.post(`http://${this.ipAddress}:8080/api/get-goods/`, {username: this.username});
      this.goods = response.data.goods;
    },
    async fetchAppImages() {
      const response = await axios.get(`http://${this.ipAddress}:8080/api/get-app-images/`);
      this.appImages = response.data.appImages;
    },
    goToPage(page) {
      this.$router.push({name: page, query: {username: this.username}});
      this.currentPage = page;
    },
    goToDetailPage(item) {
      // 构造目标页面 URL
    const detailPageUrl = `${window.location.origin}/DetailPage?username=${encodeURIComponent(
      this.username
    )}&product=${encodeURIComponent(JSON.stringify(item))}`;

    // 在新窗口中打开目标页面
    window.open(detailPageUrl, '_blank'); // '_blank' 表示新窗口
    },
    logout() {
      localStorage.setItem('token', '');
      localStorage.setItem('isLoggedIn', 'false');
      this.$router.push({name: 'IndexPage'});
    }
  }
};
</script>

<style scoped>
/* 保证内容与视口大小一致 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 10vh;
  box-sizing: border-box;
}

.app-icons {
  display: flex;
  justify-content: center;
  gap: 3vw;
  margin-bottom: 4vh;
}

.app-icon-item {
  flex: 0 1 20%;
  max-width: 15vw;
}

.app-icon-image {
  width: 100%;
  height: auto;
}

.search-background {
  background-color: #ffffff;
  padding: 2vh;
  border-radius: 2vw;
}

.search-container {
  display: flex;
  justify-content: center;
}

.search-input-wrapper {
  display: flex;
  max-width: 80vw;
  width: 100%;
}

.search-input {
  flex: 1;
  padding: 2vh;
  font-size: 3.5vw;
  border: 1px solid #ccc;
  border-radius: 2vw 0 0 2vw;
}

.search-button {
  padding: 0 3vw;
  font-size: 3.5vw;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0 2vw 2vw 0;
  cursor: pointer;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2vh;
}

.username {
  font-size: 4vw;
}

.logout-button {
  font-size: 4vw;
  color: #f44336;
  border: none;
  background: none;
  cursor: pointer;
}

.products-grid {
  display: grid;
  gap: 4vw;
  grid-template-columns: repeat(auto-fill, minmax(45%, 1fr));
}

.product-item {
  background-color: white;
  border-radius: 2vw;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 3vw;
  text-align: center;
}

.product-image {
  width: 100%;
  height: auto;
  border-radius: 2vw;
}

.product-details {
  margin-top: 2vw;
}

.product-title {
  font-size: 4vw;
  font-weight: bold;
}

.product-price {
  font-size: 4vw;
  color: #333;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  background-color: #007bff;
  padding: 1vh 0;
  box-sizing: border-box;
  font-size: 3.5vw; /* 设置初始字体大小 */
}

.nav-item {
  color: white;
  cursor: pointer;
  text-align: center;
  flex-grow: 1;
  padding: 1vh 0;
  box-sizing: border-box;
}

.nav-item.selected {
  background-color: #0056b3;
  border-radius: 2vw;
  padding: 1vh 2vw;
}

@media (max-width: 600px) {
  .bottom-nav {
    font-size: 3vw;
  }
}

h2 {
  font-size: 4.5vw;
  margin-top: 4vh;
}
</style>
