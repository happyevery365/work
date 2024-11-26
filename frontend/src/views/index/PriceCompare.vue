<template>
  <!-- 平台图标展示区域 -->
  <div class="app-icons" v-if="appImages.length">
    <div class="app-icon-item" v-for="(app, index) in appImages" :key="index">
      <img :src="app.img_url" :alt="app.appname" class="app-icon-image" />
    </div>
  </div>

  <!-- 用户信息和退出登录按钮 -->
  <div class="user-info">
    <span class="username">为提高正确性，请详细填写以下信息</span>
  </div>

  <!-- 搜索框区域 -->
  <div class="search-background">
    <div class="search-container">
      <div class="search-input-wrapper">
        <input type="text" v-model="brand" placeholder="请输入品牌名称" class="search-input" />
      </div>
    </div>
  </div>
  <div class="search-background">
    <div class="search-container">
      <div class="search-input-wrapper">
        <input type="text" v-model="specification" placeholder="请输入规格信息（尺寸，型号，分量等）" class="search-input" />
      </div>
    </div>
  </div>
  <div class="search-background">
    <div class="search-container">
      <div class="search-input-wrapper">
        <input type="text" v-model="searchQuery" placeholder="请输入商品名称（必填）" class="search-input" />
        <button @click="performPriceCompare" class="search-button">搜索</button>
      </div>
    </div>
  </div>

  <div class="user-info">
    <span class="username">{{ cheapest_good_source }}</span>
  </div>
  <div v-if="cheapest_good.length" class="products-grid">
    <div class="product-item" v-for="(item, index) in cheapest_good" :key="index" @click="goToDetailPage(item)">
      <img :src="item.img_url" alt="商品图片" class="product-image" />
      <div class="product-details">
        <p class="product-title">{{ item.title }}</p>
        <p class="product-price">价格: {{ item.price }}</p>
      </div>
    </div>
  </div>
  <div v-else class="user-info">
    <span class="username">比价未开始</span>
  </div>

  <!-- 商品展示区域 -->
  <div class="user-info">
    <span class="username">淘宝</span>
  </div>
  <div v-if="goods_taobao.length" class="products-grid">
    <div class="product-item" v-for="(item, index) in goods_taobao" :key="index" @click="goToDetailPage(item)">
      <img :src="item.img_url" alt="商品图片" class="product-image" />
      <div class="product-details">
        <p class="product-title">{{ item.title }}</p>
        <p class="product-price">价格: {{ item.price }}</p>
      </div>
    </div>
  </div>
  <div v-else class="user-info">
    <span class="username">暂无商品信息</span>
  </div>

  <div class="user-info">
    <span class="username">京东</span>
  </div>
  <div v-if="goods_jingdong.length" class="products-grid">
    <div class="product-item" v-for="(item, index) in goods_jingdong" :key="index" @click="goToDetailPage(item)">
      <img :src="item.img_url" alt="商品图片" class="product-image" />
      <div class="product-details">
        <p class="product-title">{{ item.title }}</p>
        <p class="product-price">价格: {{ item.price }}</p>
      </div>
    </div>
  </div>
  <div v-else class="user-info">
    <span class="username">暂无商品信息</span>
  </div>

  <div class="user-info">
    <span class="username">唯品会</span>
  </div>
  <div v-if="goods_weipinhui.length" class="products-grid">
    <div class="product-item" v-for="(item, index) in goods_weipinhui" :key="index" @click="goToDetailPage(item)">
      <img :src="item.img_url" alt="商品图片" class="product-image" />
      <div class="product-details">
        <p class="product-title">{{ item.title }}</p>
        <p class="product-price">价格: {{ item.price }}</p>
      </div>
    </div>
  </div>
  <div v-else class="user-info">
    <span class="username">暂无商品信息</span>
  </div>

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

export default {
  data() {
    return {
      searchQuery: '',
      brand:'',
      specification:'',
      appImages: [],
      goods_taobao: [],
      goods_jingdong: [],
      goods_weipinhui: [],
      cheapest_good_source:'',
      cheapest_good:[],
      username: '',
      navItems: [
        { name: '首页', page: 'GoodsPage' },
        { name: '分类', page: 'Product_Categories' },
        { name: '比价', page: 'PriceCompare' },
        { name: '我的', page: 'MyRoom' }
      ],
      currentPage: 'PriceCompare'
    };
  },
  created() {
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
    }
  },
  mounted() {
    this.fetchAppImages();
  },
  methods: {
    async performPriceCompare() {
      if (!this.searchQuery) {
        alert('搜索框不能为空');
        return;
      }
      // 合并 searchQuery、brand 和 specification，使用空格分隔
      const combinedQuery = `${this.brand} ${this.searchQuery} ${this.specification}`.trim();
      try {
        const response = await axios.post('http://192.168.117.146:8000/api/price_compare/', {
          searchQuery: combinedQuery,
          username: this.username,
        });
        this.goods_taobao = response.data.goods_taobao;
        this.goods_jingdong = response.data.goods_jingdong;
        this.goods_weipinhui = response.data.goods_weipinhui;
        this.cheapest_good = response.data.cheapest_good;
        this.cheapest_good_source = response.data.cheapest_good_source;
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    },
    async fetchAppImages() {
      const response = await axios.get('http://192.168.117.146:8000/api/get-app-images/');
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

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2vh;
}

.username {
  font-size: 4vw;
}
</style>
