<template>
  <div>
    <!-- 返回按钮 -->
    <button @click="goBack" class="back-button">返回</button>
    <!-- 商品展示 -->
    <div v-if="goods.length" class="products-grid">
      <div class="product-item" v-for="(item, index) in goods" :key="index" @click="goToDetailPage(item)">
        <img :src="item.img_url" alt="商品图片" class="product-image" />
        <div class="product-details">
          <p class="product-title">{{ item.title }}</p>
          <p class="product-price">价格: {{ item.price }}</p>
        </div>
      </div>
    </div>
    <p v-else>正在搜索</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      goods: [],
      username: '',
      searchQuery: ''
    };
  },
  created() {
    const savedState = sessionStorage.getItem('GoodsPageState');
    if (savedState) {
      // 如果有保存的状态，从 sessionStorage 恢复
      const { goods, searchQuery, username } = JSON.parse(savedState);
      this.goods = goods;
      this.searchQuery = searchQuery;
      this.username = username;
    } else {
      // 初始化页面
      this.searchQuery = this.$route.query.searchQuery;
      this.username = this.$route.query.username;
      this.SearchProducts();
    }
  },
  methods: {
    async SearchProducts() {
      try {
        const response = await axios.post('http://192.168.117.146:8000/api/search/', {
          searchQuery: this.searchQuery,
          username: this.username
        });
        this.goods = response.data.goods;

        // 保存状态到 sessionStorage
        this.savePageState();
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    },
    goBack() {
      this.$router.push({ name: 'GoodsPage', query: { username: this.username } });
    },
    goToDetailPage(item) {
      // 构造目标页面 URL
    const detailPageUrl = `${window.location.origin}/DetailPage?username=${encodeURIComponent(
      this.username
    )}&product=${encodeURIComponent(JSON.stringify(item))}`;

    // 在新窗口中打开目标页面
    window.open(detailPageUrl, '_blank'); // '_blank' 表示新窗口
    },
    savePageState() {
      const state = {
        goods: this.goods,
        searchQuery: this.searchQuery,
        username: this.username
      };
      sessionStorage.setItem('GoodsPageState', JSON.stringify(state));
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
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #0056b3;
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
