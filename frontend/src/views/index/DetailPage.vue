<template>
  <div class="detail-page">
    <div class="product-info">
      <div class="product-image">
        <img :src="product.img_url" alt="商品图片"/>
      </div>
      <div class="product-details">
        <div class="product-link-container">
          <a :href="product.product_url" target="_blank" class="product-link">查看商品</a>
          <div class="star-icon" @click="toggleStar">
            <span :class="['star', isStarred ? 'star-filled' : 'star-empty']">★</span>
          </div>
          <!-- 修改按钮部分 -->
          <button
            class="product-link"
            @click="handlePriceHistoryClick"
            :disabled="buttonDisabled"
            :class="{ 'disabled-button': buttonDisabled }"
          >
            搜历史价
          </button>
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
      <div class="user-info">
       <span class="username">{{ message }}</span>
      </div>
      <div class="chart-container" v-if="isChartLoaded">
      <gradient-line-chart
        id="chart-line"
        description="<i class='fa fa-arrow-up text-success'></i>
        <span class='font-weight-bold'></span>"
        :chart="chartData"
      />
    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import GradientLineChart from "@/Charts/GradientLineChart.vue";
import { ipAddress } from './config.js';
export default {
  components: {
    GradientLineChart, // 注册组件
  },
  data() {
    return {
      product: {},  // 商品信息
      isStarred: false,  // 是否已标记为星标
      username: '',
      errormessage: '',
      chartData: {
      labels: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-03-01'],  // 这是示例日期
      datasets: [
        {
          label: 'Sales Overview',
          data: [1500, 2000, 1700, 2200, 200],
          borderColor: '#4bc0c0',
          fill: false,
        }
      ]
      },
       isChartLoaded: false, // 控制图表是否加载
       message:'',
       buttonDisabled: false, // 用于控制按钮的可用性
       ipAddress:''
    };
  },
  created() {
    this.ipAddress = ipAddress;
    // 从路由查询参数中获取商品信息
    const product = JSON.parse(this.$route.query.product);
    this.username = this.$route.query.username;
    if (product) {
      this.product = product;
    }
    this.errormessage = '';
    this.message = '';
    this.isChartLoaded = false;
    this.buttonDisabled = false;
    // 搜索该商品是否已经被标记
    this.searchIfStarred();
    // 获取价格历史图表
    //this.fetchPriceChart();
  },
  methods: {
     // 点击搜历史价按钮时，禁用按钮并调用fetchPriceChart
    handlePriceHistoryClick() {
      this.buttonDisabled = true;  // 禁用按钮
      this.fetchPriceChart();  // 获取价格历史图表
    },
    toggleStar() {
      if (this.isStarred) {
        this.unstarGood();
      } else {
        this.starGood();
      }
    },
    // 获取价格历史图表
    async fetchPriceChart() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8000/api/fetchPriceData/`, {product_url: this.product.product_url, username:this.username});
        this.message = response.data.message;
        if (response.data.success) {
      // 假设响应的数据格式是一个日期和价格的元组列表
      const priceData = response.data.data; // 例如：[{date: '2024-01-01', price: 1500}, ...]
      if (priceData && priceData.length > 0) {
        // 提取日期和价格
        const labels = priceData.map(entry => entry[0]);  // 提取日期
        const data = priceData.map(entry => entry[1]);    // 提取价格

        // 更新 chartData
        this.chartData = {
          labels: labels,  // 日期列表
          datasets: [
            {
              label: '价格历史',
              data: data,  // 价格列表
              borderColor: '#4bc0c0',
              fill: false,
            }
          ]
        };
        this.isChartLoaded = true;
      } else {
        console.error("返回的数据格式不正确或没有历史价格数据");
      }
    } else {
      console.error("获取图表失败:", response.data.message);
    }
  } catch (error) {
    console.error("请求失败:", error);
  }
},
    async searchIfStarred() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8000/api/searchIfStarred/`, {product_url: this.product.product_url, username: this.username});
        this.isStarred = response.data.isStarred;
      } catch (error) {
        console.error("请求失败:", error);
      }
    },
    async starGood() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8000/api/star_goods/`, {product: this.product, username: this.username});
        this.errormessage = response.data.message;
        this.isStarred = true;
      } catch (error) {
        console.error("请求失败:", error);
      }
    },
    async unstarGood() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8000/api/unstar_goods/`, {product: this.product, username: this.username});
        this.errormessage = response.data.message;
        this.isStarred = false;
      } catch (error) {
        console.error("请求失败:", error);
      }
    },
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
  margin-bottom: 5px;
  margin-top: 100px;  /* 图片上方留出一定的空隙 */
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
  width: 100% !important;  /* 强制图表占满容器宽度 */
  height: 300px;
}

img {
  width: 100%;
  max-width: 500px;
  height: auto;
  margin-top: 20px;
}

.chart-container {
  width: 100%;  /* 确保图表宽度适应屏幕 */
  margin-top: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  width: 100%;  /* 设置图表容器的宽度 */
  max-width: 600px;  /* 限制最大宽度 */
}
/* 添加禁用按钮的样式 */
.disabled-button {
  background-color: #cccccc; /* 设置禁用时按钮的背景颜色 */
  color: #888888; /* 设置禁用时按钮的文字颜色 */
  cursor: not-allowed; /* 禁用时鼠标指针变为禁止符号 */
}

</style>
