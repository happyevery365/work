<template>
  <div class="detail-page">
    <!-- 返回按钮 -->
    <div class="back-button" @click="goBack">＜</div>
    <p>   </p>
    <div class="product-info">
      <div class="product-image">
        <img :src="product.img_url" alt="商品图片" />
      </div>
      <div class="product-details">
        <div class="product-link-container">
          <a :href="product.product_url" target="_blank" class="product-link">查看商品</a>
          <div class="star-icon" @click="toggleStar">
            <span :class="['star', isStarred ? 'star-filled' : 'star-empty']">★</span>
          </div>
        </div>
        <p class="product-title">{{ product.title }}</p>
        <div class="product-price-postFree">
          <p class="product-price">价格: {{ product.price }}</p>
          <p v-if="product.postFree === 1" class="product-postFree">包邮</p>
        </div>
        <p class="product-description">{{ product.description }}</p>
        <p class="product-shop">{{ product.shop }}</p>
        <p class="product-location">位置: {{ product.location }}</p>
      </div>
    </div>

    <!-- 图表显示区域 -->
    <div v-if="chartImageData">
      <img :src="'data:image/png;base64,' + chartImageData" alt="价格走势图" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      product: {},  // 商品信息
      isStarred: false,  // 是否已标记为星标
      username: '',
      chartImageData: null  // 存储图表的 Base64 数据
    };
  },
  created() {
    // 从路由查询参数中获取商品信息
    const product = JSON.parse(this.$route.query.product);
    this.username = this.$route.query.username;
    if (product) {
      this.product = product;
    }
    // 获取价格历史图表
    this.fetchPriceChart();
  },
  methods: {
    goBack() {
      this.$router.push({name: 'GoodsPage', query: {username: this.username}});  // 返回到 GoodsPage 页面
    },
    toggleStar() {
      if (this.isStarred) {
        this.unstarProduct();
      } else {
        this.starProduct();
      }
    },
    // 调用后端函数标记为星标
    starProduct() {
      this.isStarred = true;
    },
    // 调用后端函数取消星标
    unstarProduct() {
      this.isStarred = false;
    },
    // 获取价格历史图表
    async fetchPriceChart() {
      try {
        const response = await axios.post('http://192.168.117.146:8000/api/fetchPriceData/', {product_url: this.product.product_url});
        if (response.data.success) {
          this.chartImageData = response.data.image_data;  // 获取图像的 Base64 数据
        } else {
          console.error("获取图表失败:", response.data.message);
        }
      } catch (error) {
        console.error("请求失败:", error);
      }
    }
  }
};
</script>

<style scoped>
.detail-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  height: 100vh;
}

.product-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  width: 100%;
}

.product-image img {
  width: 100%;
  max-width: 250px;
  height: auto;
  border-radius: 10px;
  margin-bottom: 12px;
}

.product-details {
  width: 100%;
  text-align: center;
}

.product-title {
  font-size: 8px;
  color: #333;
  margin-bottom: 6px;
}

.product-price-postFree {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.product-price,
.product-postFree {
  font-size: 8px;
  color: #333;
}

.product-postFree {
  color: #28a745;
}

.product-description,
.product-shop,
.product-location {
  font-size: 8px;
  margin-top: 4px;
}

.product-link-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.product-link {
  margin-top: 4px;
  display: inline-block;
  padding: 3px 8px;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  font-size: 6px;
}

.product-link:hover {
  background-color: #0056b3;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 18px;
  color: #007bff;
  cursor: pointer;
}

.star-icon {
  cursor: pointer;
}

.star {
  font-size: 20px;
}

.star-empty {
  color: rgba(0, 0, 0, 0.11);
}

.star-filled {
  color: pink;
}

canvas {
  width: 100%;
  height: 300px;
  margin-top: 20px;
}

img {
  width: 100%;
  max-width: 500px;
  height: auto;
  margin-top: 20px;
}
</style>
