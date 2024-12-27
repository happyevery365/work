<template>
  <div>
    <!-- 返回按钮 -->
    <button @click="goBack" class="back-button">返回</button>

    <div v-if="goods.length">
    <div class="products-grid">
        <button @click="selectPlatform('taobao')" :class="{'selected': selectedPlatform === 'taobao'}">淘宝</button>
        <button @click="selectPlatform('jingdong')" :class="{'selected': selectedPlatform === 'jingdong'}">京东</button>
        <button @click="selectPlatform('weipinhui')" :class="{'selected': selectedPlatform === 'weipinhui'}">唯品会</button>
        <button @click="selectPlatform('priceless')" :class="{'selected': selectedPlatform === 'priceless'}">最便宜</button>
    </div>
    <!-- 商品展示 -->
    <div class="products-grid">
      <!-- 平台选择按钮 -->

      <div class="product-item" v-for="(item, index) in goods" :key="index" @click="goToDetailPage(item)">
        <img :src="item.img_url" alt="商品图片" class="product-image" />
        <div class="product-details">
          <p class="product-title">{{ item.title }}</p>
          <p class="product-price">价格: {{ item.price }}</p>
        </div>
      </div>
    </div>
    </div>
    <p v-else>正在搜索</p>
  </div>
</template>

<script>
import axios from 'axios';
import { ipAddress } from './config.js';

export default {
  data() {
    return {
      goods: [],  // 用于存储商品列表
      username: '',
      searchQuery: '',
      ipAddress: '',
      selectedPlatform: 'taobao', // 默认平台为淘宝
      platformData: {
        taobao_goods: [],
        jingdong_goods: [],
        weipinhui_goods: [],
        priceless_goods: []
      }
    };
  },
  created() {
    this.ipAddress = ipAddress;
    this.searchQuery = this.$route.query.searchQuery;
    this.username = this.$route.query.username;
    this.SearchProducts();
  },
  methods: {
    async SearchProducts() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8080/api/search/`, {
          searchQuery: this.searchQuery,
          username: this.username
        });

        // 获取返回的商品数据
        this.platformData.taobao_goods = response.data.taobao_goods;
        this.platformData.jingdong_goods = response.data.jingdong_goods;
        this.platformData.weipinhui_goods = response.data.weipinhui_goods;
        this.platformData.priceless_goods = response.data.priceless_product;

        // 默认显示淘宝商品
        this.goods = this.platformData.taobao_goods;
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    },
    // 切换平台显示的商品
    selectPlatform(platform) {
      this.selectedPlatform = platform;
      this.goods = this.platformData[`${platform}_goods`]; // 根据选择的平台更新商品列表
    },
    goBack() {
      this.$router.push({name: 'GoodsPage', query: {username: this.username}});
    },
    goToDetailPage(item) {
      // 构造目标页面 URL
      const detailPageUrl = `${window.location.origin}/DetailPage?username=${encodeURIComponent(this.username)}&product=${encodeURIComponent(JSON.stringify(item))}`;

      // 在新窗口中打开目标页面
      window.open(detailPageUrl, '_blank'); // '_blank' 表示新窗口
    },
  }
};
</script>

<style scoped>
/* 返回按钮样式 */
.back-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #0056b3;
}

/* 平台选择按钮样式 */
.platform-selection {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px; /* 给平台选择框和商品展示区域之间添加一些空间 */
}

.platform-selection button {
  padding: 10px 20px;
  background-color: #f1f1f1;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
}

.platform-selection button.selected {
  background-color: orange;
  color: white;
  border-color: orange;
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
</style>
