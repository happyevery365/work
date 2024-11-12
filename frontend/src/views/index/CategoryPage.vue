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

    <!-- 商品展示区域 -->
    <div class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-item">
        <img :src="product.img_url" alt="Product Image" class="product-image" />
        <div class="product-info">
          <p class="product-title">{{ product.title }}</p>
          <p class="product-price">Price: {{ product.price }}</p>
          <p class="product-deal">Deal: {{ product.deal }}</p>
          <p class="product-shop">Shop: {{ product.shop }}</p>
          <p class="product-location">Location: {{ product.location }}</p>
          <button @click="goToProduct(product.product_url)" class="product-button">
            点此查看
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
      englishName: '',
      username: '',
      selectedPlatform: {
        TaoBao: false,
        JingDong: false,
        PinDuoDuo: false,
        TianMao: false
      }
    };
  },
  created() {
    this.englishName = this.$route.query.category;
    this.username = this.$route.query.username;
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/get_category/', { data: this.englishName });
        this.products = response.data.goods;
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    },
    goToProduct(url) {
      window.open(url, '_blank'); // Open the product URL in a new tab
    },
    goBack() {
      this.$router.push({ name: 'Product_Categories', query: { username: this.username } });
    },
    togglePlatform(platform) {
      // Toggle the selected platform
      this.selectedPlatform[platform] = !this.selectedPlatform[platform];
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

/* 商品展示区域样式 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.product-item {
  text-align: center;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.product-image {
  width: 100%;
  height: auto;
  margin-bottom: 8px;
}

.product-info p {
  margin: 4px 0;
  font-size: 14px;
}
</style>
