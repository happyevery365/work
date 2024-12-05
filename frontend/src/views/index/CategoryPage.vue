<template>
  <div>
    <!-- 返回按钮 -->
    <button @click="goBack" class="back-button">返回</button>

    <!-- 平台选择框 -->
    <div class="platform-selection">
      <div
        class="platform-box"
        :class="{'selected': selectedPlatform.TaoBao}"
        @click="togglePlatform('TaoBao')"
      >
        淘宝
      </div>
      <div
        class="platform-box"
        :class="{'selected': selectedPlatform.JingDong}"
        @click="togglePlatform('JingDong')"
      >
        京东
      </div>
      <div
        class="platform-box"
        :class="{'selected': selectedPlatform.PinDuoDuo}"
        @click="togglePlatform('PinDuoDuo')"
      >
        拼多多
      </div>
      <div
        class="platform-box"
        :class="{'selected': selectedPlatform.TianMao}"
        @click="togglePlatform('TianMao')"
      >
        天猫
      </div>
    </div>
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
  </div>
</template>

<script>
import axios from 'axios';
import { ipAddress } from './config.js';

export default {
  data() {
    return {
      products: [],
      englishName: '',
      username: '',
      goods: [],
      selectedPlatform: {
        TaoBao: false,
        JingDong: false,
        PinDuoDuo: false,
        TianMao: false
      },
      ipAddress:''
    };
  },
  created() {
    this.ipAddress = ipAddress;
    this.englishName = this.$route.query.category;
    this.username = this.$route.query.username;
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8000/api/get_category/`, {data: this.englishName});
        this.goods = response.data.goods;
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    },
    goBack() {
      this.$router.push({name: 'Product_Categories', query: {username: this.username}});
    },
    togglePlatform(platform) {
      // Toggle the selected platform
      this.selectedPlatform[platform] = !this.selectedPlatform[platform];
    },
    goToDetailPage(item) {
      // 构造目标页面 URL
    const detailPageUrl = `${window.location.origin}/DetailPage?username=${encodeURIComponent(
      this.username
    )}&product=${encodeURIComponent(JSON.stringify(item))}`;

    // 在新窗口中打开目标页面
    window.open(detailPageUrl, '_blank'); // '_blank' 表示新窗口;
    }
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
  margin-bottom: 20px; /* 给返回按钮和平台选择框之间添加一些空间 */
}

.back-button:hover {
  background-color: #0056b3;
}

/* 平台选择框的样式 */
.platform-selection {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px; /* 给平台选择框和商品展示区域之间添加一些空间 */
}

.platform-box {
  width: 80px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.platform-box.selected {
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
