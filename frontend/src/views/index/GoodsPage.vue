<template>
  <div>
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

    <div class="search-container">
    <div class="search-input-wrapper">
      <input type="text" v-model="searchQuery" placeholder="请输入搜索内容" class="search-input" />
      <button @click="performSearch" class="search-button">搜索</button>
    </div>
  </div>

    <!-- 商品展示区域 -->
    <h2>猜您喜欢</h2>
    <div v-if="goods.length">
      <div class="products-grid">
        <div class="product-item" v-for="(item, index) in goods" :key="index">
          <div class="product-left">
            <img :src="item.img_url" alt="商品图片" class="product-image" />
          </div>
          <div class="product-right">
            <p class="product-title">{{ item.title }}</p>
            <p class="product-price">Price: {{ item.price }}</p>
            <p class="product-deal">Deal: {{ item.deal }}</p>
            <p class="product-shop">Shop: {{ item.shop }}</p>
            <p class="product-location">Location: {{ item.location }}</p>
            <p v-if="item.postFree === 1">包邮</p>
            <button @click="goToProduct(item.product_url)" class="product-button">点我跳转</button>
          </div>
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
  </div>
</template>

<script>
import axios from 'axios';

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
    };
  },
  created() {
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
      console.log("用户登录的用户名:", this.username);
    }
  },
  methods: {
    async performSearch() {
      if (!this.searchQuery) {
        alert('搜索框不能为空');
        return;
      }
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/search/', { data: this.searchQuery });
        this.goods = response.data.goods || [];
      } catch (error) {
        console.error('Error performing search:', error);
      }
    },
    async fetchGoods() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/get-goods/', { data: this.username });
        this.goods = response.data.goods;
      } catch (error) {
        console.error('Error fetching goods:', error);
      }
    },
    async fetchAppImages() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/get-app-images/');
        this.appImages = response.data.appImages;
      } catch (error) {
        console.error('Error fetching app images:', error);
      }
    },
    goToProduct(url) {
      window.location.href = url;
    },
    goToPage(page) {
      this.$router.push({ name: page, query: { username: this.username } });
      this.currentPage = page;
    },
    logout() {
      localStorage.setItem('token', '');
      this.$router.push({ name: 'IndexPage' });
    }
  },
  mounted() {
    this.fetchGoods();
    this.fetchAppImages();
  }
};
</script>

<style scoped>
/* 平台图标展示样式 */
.app-icons {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.app-icon-item {
  flex: 0 1 25%; /* 保证每行显示4个图标 */
  max-width: 80px; /* 确保图标不超过一定宽度 */
}

.app-icon-image {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 保证图片不被裁剪 */
  max-width: 60px; /* 控制最大宽度，避免图标过大 */
  max-height: 60px; /* 控制最大高度 */
}

/* 搜索框和搜索按钮样式 */
.search-container {
  display: flex;
  justify-content: center;
  padding: 10px 15px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  max-width: 280px; /* 缩小搜索框宽度 */
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding-right: 50px; /* 为按钮留出空间 */
  box-sizing: border-box;
  height: 36px;
}

.search-button {
  position: absolute;
  right: 4px; /* 贴合输入框右侧 */
  top: 50%;
  transform: translateY(-50%); /* 垂直居中 */
  height: 28px; /* 与输入框高度匹配 */
  padding: 0 12px;
  font-size: 14px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.search-button:hover {
  background-color: #0056b3;
}


/* 用户信息与退出按钮样式 */
.user-info {
  display: flex;
  justify-content: space-between; /* "你好，username" 和退出按钮在同一行 */
  align-items: center;
  padding: 10px 15px;
}

.username {
  font-size: 14px;
}

.logout-button {
  font-size: 14px;
  text-decoration: underline;
  color: #f44336;
  border: none;
  background: none;
  cursor: pointer;
}

.logout-button:hover {
  color: red;
}

/* 商品展示区域样式 */
.products-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.product-left {
  width: 30%;
}

.product-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.product-right {
  width: 65%;
  padding-left: 15px;
}

.product-title {
  font-size: 16px;
  font-weight: bold;
}

.product-info p {
  margin: 4px 0;
  font-size: 14px;
}

button {
  margin-top: 10px;
}

/* 固定底部导航栏 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-around;
  background-color: #4682b4;
  padding: 10px 0;
  z-index: 1000;
}

.nav-item {
  padding: 10px 20px;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.nav-item.selected {
  background-color: #1e3a5f;
}
</style>
