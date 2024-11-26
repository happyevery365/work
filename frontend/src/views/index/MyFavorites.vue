<template>
  <!-- 平台图标展示区域 -->
  <div class="app-icons" v-if="appImages.length">
    <div class="app-icon-item" v-for="(app, index) in appImages" :key="index">
      <img :src="app.img_url" :alt="app.appname" class="app-icon-image" />
    </div>
  </div>

  <!-- 商品展示区域 -->
  <div v-if="goods.length" class="products-grid">
    <div class="product-item" v-for="(item, index) in goods" :key="index" @click="goToDetailPage(item)">
      <img :src="item.img_url" alt="商品图片" class="product-image" />
      <div class="product-details">
        <p class="product-title">{{ item.title }}</p>
        <p class="product-price">价格: {{ item.price }}</p>
      </div>
    </div>
  </div>
  <!-- 用户信息和退出登录按钮 -->
  <div v-else class="user-info">
    <span class="username">暂无商品信息</span>
  </div>

  <!-- 返回按钮区域 -->
  <div class="return-button-container">
    <button @click="goBack" class="return-button">返回</button>
  </div>


</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      appImages: [],
      goods: [],
      username: ''
    };
  },
  created() {
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
    }
  },
  mounted() {
    this.fetchPreferrences();
    this.fetchAppImages();
  },
  methods: {
    async fetchPreferrences() {
      const response = await axios.post('http://192.168.117.146:8000/api/get-preferrencegoods/', {username: this.username});
      this.goods = response.data.goods;
    },
    async fetchAppImages() {
      const response = await axios.get('http://192.168.117.146:8000/api/get-app-images/');
      this.appImages = response.data.appImages;
    },
    goToDetailPage(item) {
      // 构造目标页面 URL
    const detailPageUrl = `${window.location.origin}/DetailPage?username=${encodeURIComponent(
      this.username
    )}&product=${encodeURIComponent(JSON.stringify(item))}`;
    // 在新窗口中打开目标页面
    window.open(detailPageUrl, '_blank'); // '_blank' 表示新窗口
    },
    goBack() {
      this.$router.push({name: 'MyRoom', query: {username: this.username}});
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

@media (max-width: 600px) {
  .bottom-nav {
    font-size: 3vw;
  }
}

h2 {
  font-size: 4.5vw;
  margin-top: 4vh;
}

.return-button-container {
  display: flex;
  justify-content: center;
  margin-top: 2vh;
}

.return-button {
  padding: 1.5vh 5vw;
  font-size: 4vw;
  font-weight: bold;
  background-color: #ff4b2b;
  color: white;
  border: none;
  border-radius: 2vw;
  cursor: pointer;
  transition: all 0.3s;
}

.return-button:hover {
  background-color: #ff6f61;
  box-shadow: 0px 4px 10px rgba(255, 75, 43, 0.4);
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
