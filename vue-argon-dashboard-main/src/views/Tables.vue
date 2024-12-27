<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import { ipAddress } from './config.js';
const ipaddress = ref('');
const route = useRoute();
const router = useRouter();
const username = ref(route.query.username || "");
const goods = ref([]);
const selectedGoods = ref([]);
const PreferGoods = ref([]);

// Fetch goods from the backend
async function fetchGoods() {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/get-goods/`, {
      username: username.value,
    });
    goods.value = response.data.goods;
    selectRandomGoods();
  } catch (error) {
    console.error("Error fetching goods:", error);
  }
}

async function fetchPreferGoods() {
  try {
    const response = await axios.post(
      `http://${ipaddress.value}:8080/api/get-preferrencegoods/`,
      { username: username.value }
    );
    PreferGoods.value = response.data.goods;
  } catch (error) {
    console.error("Error fetching prefer goods:", error);
  }
}

function selectRandomGoods() {
  const shuffled = [...goods.value].sort(() => 0.5 - Math.random());
  selectedGoods.value = shuffled.slice(0, 6);
}

// Function to unstar goods
async function unstarGood(item) {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/unstar_goods/`, {
      product: item,
      username: username.value,
    });
    console.log(response.data.message);
    // Remove the unstarred item from PreferGoods
    PreferGoods.value = PreferGoods.value.filter((goodsItem) => goodsItem !== item);
  } catch (error) {
    console.error("请求失败:", error);
  }
}

// Navigate to product detail (RTL page)
function goToProductDetail(product) {
  const url = router.resolve({
    name: "RTL",
    query: {
      username: username.value,
      productInfo: JSON.stringify(product),
    },
  }).href;
  window.open(url, "_blank");
}

onMounted(() => {
  ipaddress.value = ipAddress;
  fetchGoods();
  fetchPreferGoods();
});
</script>

<style>
/* 商品容器布局，每行显示四个商品 */
.goods-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 每行四列 */
  gap: 20px; /* 商品之间的间距 */
}

.product-img2 {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
  cursor: pointer; /* 添加鼠标指针样式 */
}

.product-title2 {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 限制为两行文字 */
  -webkit-box-orient: vertical;
  font-size: 18px;
  color: #333;
  line-height: 1.5em;
  max-height: 3em;
  margin: 0 auto;
  text-align: center;
}

.card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.card-body {
  padding: 8px;
}

.btn-danger {
  font-size: 10px;
}
</style>

<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-lg-12">
        <!-- 您的收藏 -->
        <div class="row mt-4">
          <div class="col-lg-12">
            <div class="card">
              <div class="p-3 pb-0 card-header">
                <div class="d-flex justify-content-between">
                  <h6 class="mb-2">您的收藏</h6>
                </div>
              </div>
              <div class="card-body">
                <div class="goods-container">
                  <div
                    class="card text-center"
                    v-for="(item, index) in PreferGoods"
                    :key="index"
                  >
                    <img
                      :src="item.img_url"
                      alt="商品图片"
                      class="product-img2 mx-auto mt-3"
                      @click="goToProductDetail(item)"
                    />
                    <div class="card-body">
                      <h6 class="product-title2">{{ item.title }}</h6>
                      <p class="text-sm mb-1">店铺: {{ item.shop }}</p>
                      <p class="text-sm mb-0">价格: {{ item.price }} 元</p>
                      <button
                        class="btn btn-danger btn-sm mt-2"
                        @click="unstarGood(item)"
                      >
                        取消收藏
                      </button>
                    </div>
                  </div>
                </div>
                <p v-if="PreferGoods.length === 0" class="text-center mt-4">暂无收藏商品</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
