<script setup>
import GradientLineChart from "@/examples/Charts/GradientLineChart.vue";
import { onBeforeMount, onBeforeUnmount, ref } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import axios from "axios";
import { ipAddress } from './config.js';
const ipaddress = ref('');

const store = useStore();
const route = useRoute();
const body = document.getElementsByTagName("body")[0];

const username = route.query.username || "未知用户";
let productInfo = {};

if (route.query.productInfo) {
  try {
    productInfo = JSON.parse(route.query.productInfo);
  } catch (e) {
    console.error("商品信息解析错误:", e);
    productInfo = {};
  }
}

const isFavorite = ref(false);
const errormessage = ref("");
const isChartLoaded = ref(false);
const isButtonDisabled = ref(false); // 控制按钮状态
const loadingMessage = ref(""); // 控制加载提示
const chartData = ref({
  labels: [],
  datasets: [],
});

const fetchPriceChart = async () => {
  try {
    isButtonDisabled.value = true;
    loadingMessage.value = "正在查询数据，请稍候……";

    const response = await axios.post(
      `http://${ipaddress.value}:8080/api/fetchPriceData/`,
      { product_url: productInfo.product_url, username }
    );

    if (response.data.success) {
      const priceData = response.data.data;
      if (priceData && priceData.length > 0) {
        chartData.value = {
          labels: priceData.map((entry) => entry[0]),
          datasets: [
            {
              label: "价格历史",
              data: priceData.map((entry) => entry[1]),
              borderColor: "#4bc0c0",
              fill: false,
            },
          ],
        };
        isChartLoaded.value = true;
      } else {
        console.error("返回的数据格式不正确或没有历史价格数据");
      }
    } else {
      console.error("获取图表失败:", response.data.message);
      alert(response.data.message);
    }
  } catch (error) {
    console.error("请求失败:", error);
  } finally {
    isButtonDisabled.value = false;
    loadingMessage.value = "";
  }
};

const starGood = async () => {
  try {
    const response = await axios.post(
      `http://${ipaddress.value}:8080/api/star_goods/`,
      { product: productInfo, username }
    );
    errormessage.value = response.data.message;
    isFavorite.value = true;
  } catch (error) {
    console.error("请求失败:", error);
  }
};

const unstarGood = async () => {
  try {
    const response = await axios.post(
      `http://${ipaddress.value}:8080/api/unstar_goods/`,
      { product: productInfo, username }
    );
    errormessage.value = response.data.message;
    isFavorite.value = false;
  } catch (error) {
    console.error("请求失败:", error);
  }
};

const searchIfStarred = async () => {
  try {
    const response = await axios.post(
      `http://${ipaddress.value}:8080/api/searchIfStarred/`,
      { product_url: productInfo.product_url, username }
    );
    isFavorite.value = response.data.isStarred;
  } catch (error) {
    console.error("请求失败:", error);
  }
};

const searchHistoricalPrice = () => {
  fetchPriceChart();
};

const toggleFavorite = async () => {
  if (isFavorite.value) {
    await unstarGood();
  } else {
    await starGood();
  }
};

onBeforeMount(async () => {
  ipaddress.value = ipAddress;
  store.state.hideConfigButton = true;
  store.state.showNavbar = false;
  store.state.showSidenav = false;
  store.state.showFooter = false;
  body.classList.remove("bg-gray-100");

  await searchIfStarred();
});

onBeforeUnmount(() => {
  store.state.hideConfigButton = false;
  store.state.showNavbar = true;
  store.state.showSidenav = true;
  store.state.showFooter = true;
  body.classList.add("bg-gray-100");
});
</script>

<template>
  <div class="py-4 container-fluid">
    <div class="product-container">
      <img :src="productInfo.img_url || 'https://via.placeholder.com/200'" alt="商品图片" class="product-img" />

      <div class="product-details">
        <div class="product-title">{{ productInfo.title || '未知商品' }}</div>
        <div class="product-price">价格: ¥{{ productInfo.price || 'N/A' }}</div>
        <div class="product-info">交易量: {{ productInfo.deal || 'N/A' }}</div>
        <div class="product-info">商店: {{ productInfo.shop || 'N/A' }}</div>
        <div class="product-info">地点: {{ productInfo.location || 'N/A' }}</div>
        <div class="product-info">是否包邮: {{ productInfo.postFree === 1 ? '是' : '否' }}</div>
      </div>

      <div class="button-container">
        <a :href="'http:' + productInfo.product_url" target="_blank" class="button product-button">
          查看商品
        </a>

        <button @click="toggleFavorite" :class="['button favorite-button', { active: isFavorite }]">
          {{ isFavorite ? '已经收藏' : '收藏商品' }}
        </button>

        <button
          @click="searchHistoricalPrice"
          class="button history-price-button"
          :disabled="isButtonDisabled"
        >
          搜历史价
        </button>
      </div>
    </div>

    <div v-if="loadingMessage" class="loading-message">
      {{ loadingMessage }}
    </div>

    <div v-if="isChartLoaded" class="row mt-4">
      <div class="col-lg-12">
        <div class="card z-index-2">
          <gradient-line-chart
            id="chart-line"
            title="价格历史"
            description="商品价格波动趋势"
            :chart="chartData"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 商品信息容器 */
.product-container {
  background-color: #ffffff; /* 白色背景 */
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* 软阴影 */
  margin-bottom: 30px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

/* 商品图片样式 */
.product-img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  margin-right: 20px;
}

/* 商品信息区域 */
.product-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 20px;
}

/* 商品标题样式，允许换行并显示完整标题 */
.product-title {
  font-size: 2rem;
  font-weight: bold;
  color: #388e3c; /* 绿色 */
  margin-bottom: 10px;
  word-wrap: break-word; /* 支持换行 */
  white-space: normal;  /* 允许文字换行 */
  overflow: visible; /* 取消省略号 */
  display: block; /* 确保标题占满整行 */
  max-width: 80%; /* 限制最大宽度，避免标题过长 */
}

/* 商品价格样式 */
.product-price {
  font-size: 1.4rem;
  color: #e91e63; /* 红色 */
  margin-bottom: 15px;
}

/* 商品信息 */
.product-info {
  font-size: 1rem;
  color: #333;
  margin: 5px 0;
  word-wrap: break-word;
}

/* 按钮容器 */
.button-container {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  flex-wrap: wrap;
}

/* 按钮样式 */
.button {
  padding: 12px 24px;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
}

/* 查看商品按钮样式 */
.product-button {
  background-color: #388e3c; /* 绿色 */
  color: #fff;
}

.product-button:hover {
  background-color: #2c6e2b;
}

/* 收藏按钮样式 */
.favorite-button {
  background-color: #ff9800; /* 默认颜色 */
  color: #fff;
}

.favorite-button.active {
  background-color: #e91e63; /* 激活时的颜色 */
}

.favorite-button:hover {
  background-color: #e65100; /* 悬浮时的颜色 */
}

/* 搜索历史价按钮样式 */
.history-price-button {
  background-color: #3f51b5; /* 蓝色 */
  color: #fff;
}

.history-price-button:hover {
  background-color: #303f9f; /* 悬浮时的颜色 */
}
</style>
