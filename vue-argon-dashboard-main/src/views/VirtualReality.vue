<script setup>
import {computed, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import axios from "axios";
import router from "@/router";
import { ipAddress } from './config.js';
const ipaddress = ref('');
const route = useRoute();
const username = ref(route.query.username || '');
const goods = ref([]);  // To store the fetched goods
const selectedGoods = ref([]);  // To store randomly selected goods
const PreferGoods = ref([]);
const user_not_preferences = ref([]);
const isLoading = ref(false); // To track the loading state

// 平台商品数据
const taobaoGoods = ref([]);
const jingdongGoods = ref([]);
const weipinhuiGoods = ref([]);
const selectedPlatform = ref("taobao"); // 当前选择的平台，默认淘宝
const platformGoods = ref([]); // 当前平台的商品
const pricelessProduct = ref(null); // Store the cheapest product
const searchQuery = ref(""); // To store the search query

const selectedCategory = ref(null);
const selectedCategory_English = ref(null);
const selectedCategoryGoods = ref([]);
const randomCategories = ref([]);
// 随机选择7个条目
function randomizeCategories() {
  randomCategories.value = prefer_categories.sort(() => Math.random() - 0.5).slice(0, 7);
}
// 存储Cookie的函数
function SetCookie() {
  if (username.value === "kuangshuaiyu") {
    // Call API to save cookies
    axios.post(`http://${ipaddress.value}:8080/api/save_cookie/`, { username: username })
      .then(response => {
        console.log("Cookies saved successfully:", response.data);
      })
      .catch(error => {
        console.error("Error saving cookies:", error);
      });
  }
}

// 判断是否为 'kuangshuaiyu'
const showCookieButton = computed(() => {
  return username.value === 'kuangshuaiyu'; // 如果 username 为 'kuangshuaiyu'，显示按钮
});

const categoryMapping = {
  '电脑': 'Computer',
  '配件': 'Accessories',
  '办公': 'Office',
  '文具': 'Stationery',
  '工业': 'Industrial',
  '商业': 'Business',
  '农业': 'Agriculture',
  '家电': 'HomeAppliance',
  '手机': 'MobilePhone',
  '通信': 'Telecom',
  '数码': 'Digital',
  '家具': 'Furniture',
  '家装': 'HomeDecoration',
  '家居': 'HomeLiving',
  '厨具': 'Kitchenware',
  '女装': 'WomenClothing',
  '男装': 'MenClothing',
  '内衣': 'Underwear',
  '配饰': 'Accessories',
  '女鞋': 'WomenShoes',
  '男鞋': 'MenShoes',
  '运动': 'Sports',
  '户外': 'Outdoor',
  '汽车': 'Automobile',
  '珠宝': 'Jewelry',
  '文玩': 'Collectibles',
  '箱包': 'Luggage',
  '食品': 'Food',
  '生鲜': 'FreshFood',
  '酒类': 'Alcohol',
  '健康': 'Health',
  '母婴': 'MotherBaby',
  '童装': 'KidsClothing',
  '玩具': 'Toys',
  '宠物': 'Pets',
  '美妆': 'Beauty',
  '个户': 'Personal',
  '家清': 'Household',
  '香氛': 'Fragrance',
  '娱乐': 'Entertainment',
  '图书': 'Books',
  '乐器': 'MusicalInstruments',
  '鲜花': 'Flowers',
};

// Fetch goods from the backend
async function fetchGoods() {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/get-goods/`, {username: username.value});
    goods.value = response.data.goods;
     selectRandomGoods2();
  } catch (error) {
    console.error('Error fetching goods:', error);
  }
}
// 选择品类的函数
function selectCategoryItem(label) {
  const categoryInEnglish = categoryMapping[label]; // 获取英文标签
  if (selectedCategory.value === categoryInEnglish) {
    selectedCategory.value = null; // 如果已选择该品类，取消选择
  } else {
    selectedCategory.value = label; // 否则，选择该品类
    selectedCategory_English.value = categoryInEnglish;
    fetchProducts();
  }
}
async function fetchPreferGoods() {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/get-preferrencegoods/`, {username: username.value});
    PreferGoods.value = response.data.goods;
  } catch (error) {
    console.error('Error fetching prefer goods:', error);
  }
}

async function fetchNotPreferences() {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/check_user_not_preferences/`, {username: username.value});
    user_not_preferences.value = response.data.not_preferred_categories;
  } catch (error) {
    console.error('Error fetching prefer goods:', error);
  }
}
function selectRandomGoods() {
  let shuffled = [...selectedCategoryGoods.value].sort(() => 0.5 - Math.random());  // Shuffle the goods array
  selectedGoods.value = shuffled.slice(0, 8);  // Select the first 8 items
}

function selectRandomGoods2() {
  let shuffled = [...goods.value].sort(() => 0.5 - Math.random());  // Shuffle the goods array
  selectedGoods.value = shuffled.slice(0, 8);  // Select the first 8 items
}
// Fetch goods when component is mounted
onMounted(() => {
  ipaddress.value = ipAddress;
  randomizeCategories();
  fetchGoods();
  fetchPreferGoods();
  fetchNotPreferences();
  platformGoods.value = taobaoGoods.value; // 初始化为淘宝商品
});

// 随机选择不喜欢的类别
function selectRandomNotPreferredCategories() {
  let shuffled = [...notPreferredCategories.value].sort(() => 0.5 - Math.random());  // Shuffle the categories
  return shuffled.slice(0, 8);  // Select up to 5 items
}

const prefer_categories = [
  {icon: {component: 'ni ni-satisfied', background: 'dark'}, label: '电脑', description: '畅销商品，性价比高'},
  {icon: {component: 'ni ni-laptop', background: 'info'}, label: '配件', description: '电脑配件和硬件产品'},
  {icon: {component: 'ni ni-settings', background: 'primary'}, label: '办公', description: '办公设备与耗材'},
  {icon: {component: 'ni ni-paper-diploma', background: 'success'}, label: '文具', description: '书写工具和学习用品'},
  {icon: {component: 'ni ni-building', background: 'danger'}, label: '工业', description: '机械设备和零件'},
  {icon: {component: 'ni ni-briefcase-24', background: 'warning'}, label: '商业', description: '商业用品和设备'},
  {icon: {component: 'ni ni-satisfied', background: 'dark'}, label: '农业', description: '农用工具和设备'},
  {icon: {component: 'ni ni-tv-2', background: 'info'}, label: '家电', description: '各种家用电器'},
  {icon: {component: 'ni ni-mobile-button', background: 'primary'}, label: '手机', description: '智能手机与配件'},
  {icon: {component: 'ni ni-sound-wave', background: 'success'}, label: '通信', description: '通信设备与配件'},
  {icon: {component: 'ni ni-camera-compact', background: 'danger'}, label: '数码', description: '数码产品与设备'},
  {icon: {component: 'ni ni-shop', background: 'warning'}, label: '家具', description: '家庭家具与装饰品'},
  {icon: {component: 'ni ni-hat-3', background: 'dark'}, label: '家装', description: '装修材料与工具'},
  {icon: {component: 'ni ni-archive-2', background: 'info'}, label: '家居', description: '家庭日常用品'},
  {icon: {component: 'ni ni-box-2', background: 'primary'}, label: '厨具', description: '厨房用具和小家电'},
  {icon: {component: 'ni ni-single-02', background: 'success'}, label: '女装', description: '时尚女装与饰品'},
  {icon: {component: 'ni ni-user-run', background: 'danger'}, label: '男装', description: '经典男装与服饰'},
  {icon: {component: 'ni ni-diamond', background: 'warning'}, label: '珠宝', description: '高级珠宝与手表'},
  {icon: {component: 'ni ni-world', background: 'dark'}, label: '生鲜', description: '新鲜水果与蔬菜'},
  {icon: {component: 'ni ni-basket', background: 'info'}, label: '食品', description: '日常食品与零食'},
  {icon: {component: 'ni ni-wine-glass-2', background: 'primary'}, label: '酒类', description: '红酒、啤酒与白酒'},
  {icon: {component: 'ni ni-ambulance', background: 'success'}, label: '健康', description: '健康产品与医疗设备'},
  {icon: {component: 'ni ni-baby-carriage', background: 'danger'}, label: '母婴', description: '母婴用品与玩具'},
  {icon: {component: 'ni ni-collection', background: 'warning'}, label: '图书', description: '畅销书与文具'},
  {icon: {component: 'ni ni-collection', background: 'warning'}, label: '乐器', description: '畅销书与文具'},
  {icon: {component: 'ni ni-diamond', background: 'warning'}, label: '鲜花', description: '各种鲜花与植物'},
];

const notPreferredCategories = ref([]);

// Watch `user_not_preferences` and update `notPreferredCategories`
onMounted(() => {
  ipaddress.value = ipAddress;
  fetchNotPreferences().then(() => {
    notPreferredCategories.value = prefer_categories.filter(category =>
        user_not_preferences.value.includes(category.label)
    );
    notPreferredCategories.value = selectRandomNotPreferredCategories();
  });
  // 随机选择最多五个不喜欢的类别
});


// 搜索商品函数
async function searchGoods() {
  if (!searchQuery.value) {
    alert("请输入搜索内容");
    return;
  }

  isLoading.value = true;

  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/search/`, {
      searchQuery: searchQuery.value,
      username: username.value,
    });

    taobaoGoods.value = response.data.taobao_goods || [];
    jingdongGoods.value = response.data.jingdong_goods || [];
    weipinhuiGoods.value = response.data.weipinhui_goods || [];
    pricelessProduct.value = response.data.priceless_product || [];

    updatePlatformGoods(); // 更新当前平台商品
  } catch (error) {
    console.error("Error searching goods:", error);
  } finally {
    isLoading.value = false;
  }
}

// 更新当前平台的商品
function updatePlatformGoods() {
  if (selectedPlatform.value === "taobao") {
    platformGoods.value = taobaoGoods.value;
  } else if (selectedPlatform.value === "jingdong") {
    platformGoods.value = jingdongGoods.value;
  } else if (selectedPlatform.value === "weipinhui") {
    platformGoods.value = weipinhuiGoods.value;
  } else if (selectedPlatform.value === "priceless") {
    platformGoods.value = pricelessProduct.value; // 显示最便宜商品
  }
}

// 切换平台
function switchPlatform(platform) {
  selectedPlatform.value = platform;
  updatePlatformGoods();
}


async function fetchProducts() {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/get_category/`, {data: selectedCategory_English.value});
    selectedCategoryGoods.value = response.data.goods;
    selectRandomGoods();
  } catch (error) {
    console.error('Error fetching goods:', error);
  }
}

// 跳转到 rtl.vue 页面，并传递商品信息和username
function goToProductDetail(product) {
  const url = router.resolve({
    name: 'RTL',  // 假设目标页面的 name 为 RTL
    query: {
      username: username.value,  // 传递当前用户名
      productInfo: JSON.stringify(product)  // 传递商品信息，转为字符串
    }
  }).href;

  // 在新页面中打开
  window.open(url, '_blank');
}
</script>

<style scoped>
.product-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
}

.product-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.form-check-label {
  font-size: 16px;
  font-weight: 500;
}

.btn-primary {
  margin-top: 20px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.search-bar-container {
  margin-top: 20px;
  margin-bottom: 20px;
}

.search-bar input {
  width: 80%;
  margin-right: 10px;
}

.search-bar button {
  width: 20%;
}

.platform-buttons {
  display: flex;
  justify-content: center; /* 确保按钮居中对齐 */
  gap: 10px; /* 按钮间距 */
}

.platform-btn {
  width: 100px; /* 固定按钮宽度 */
  transition: background-color 0.3s ease, color 0.3s ease; /* 平滑的颜色过渡效果 */
}

/* 激活按钮的样式 */
.platform-btn.btn-primary {
  background-color: #007bff; /* 选中时的背景颜色 */
  color: white; /* 选中时文字颜色 */
}

.platform-btn.btn-secondary {
  background-color: #6c757d; /* 未选中时的背景颜色 */
  color: white; /* 未选中时文字颜色 */
}

.platform-btn:hover {
  background-color: #0056b3; /* 悬停时的背景颜色 */
}
</style>
<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-lg-12">
        <!-- 第一个row，搜索部分 -->
        <div class="row mb-4">
          <div class="col-lg-12">
            <div class="card z-index-2">
              <div class="p-3 pb-0 card-header">
                <h6 class="mb-2">搜索商品</h6>
                <!-- 搜索框 -->
                <div class="search-bar-container d-flex justify-content-center">
                  <div class="d-flex align-items-center">
                    <input
                      v-model="searchQuery"
                      type="text"
                      class="form-control"
                      placeholder="请输入商品名称"
                      style="width: 500px;"
                    />
                    <button @click="searchGoods" class="btn btn-primary">搜索</button>
                  </div>
                </div>
              </div>

              <div v-if="showCookieButton" class="text-center mt-3">
            <button @click="SetCookie" class="btn btn-secondary">
              存储 Cookie
            </button>
          </div>
              <!-- 平台切换按钮 -->
              <div v-if="taobaoGoods.length || jingdongGoods.length || weipinhuiGoods.length" class="platform-buttons text-center mb-4">
                <!-- 平台切换按钮 -->
                 <button
                  v-for="platform in ['taobao', 'jingdong', 'weipinhui', 'priceless']"
                  :key="platform"
                  :class="[ 'btn', platform === selectedPlatform ? 'btn-primary' : 'btn-secondary', 'mx-2' ]"
                  @click="switchPlatform(platform)"
                  class="platform-btn"
                >
                  {{ platform === 'taobao' ? '淘宝' : platform === 'jingdong' ? '京东' : platform === 'weipinhui' ? '唯品会' : '最便宜' }}
                </button>
              </div>
              <!-- 显示加载状态或搜索结果 -->
              <div class="table-responsive">
                <div v-if="isLoading" class="text-center mt-1 mb-4">
                  <p class="mt-3">正在搜索，请稍候...</p>
                </div>
                <div v-else>
                  <div v-if="!platformGoods || platformGoods.length === 0" class="text-center mt-1 mb-4">
                    <p class="mt-3">搜索后将会有商品哦~</p>
                  </div>
                  <div v-else>
                    <div class="row mx-3">
                      <div class="col-lg-2 col-md-3 col-6 mb-4" v-for="(product, index) in platformGoods" :key="index">
                        <div class="card" @click="goToProductDetail(product)">
                          <img :src="product.img_url" alt="Product Image" class="card-img-top"/>
                          <div class="card-body">
                            <p class="card-text">{{ product.price }} 元</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 第二个row，包含推荐品类和喜欢商品 -->
        <div class="row mt-4">
          <div class="col-lg-5">
            <!-- 显示不为空的推荐品类 -->
            <div v-if="randomCategories && randomCategories.length > 0">
              <div class="card">
                <div class="p-3 pb-0 card-header">
                  <div class="d-flex justify-content-between">
                    <h6 class="mb-2">推荐品类</h6>
                    <button @click="randomizeCategories" class="btn btn-link">换一换</button>
                  </div>
                </div>
                <div class="p-3 card-body">
                  <ul class="list-group">
                    <li
                      v-for="({ icon: { component, background }, label, description }, index) in randomCategories"
                      :key="index"
                      class="mb-2 border-0 list-group-item d-flex justify-content-between border-radius-lg ps-0"
                    >
                      <div class="d-flex align-items-center">
                        <div :class="`text-center shadow icon icon-shape icon-sm bg-gradient-${background} me-3`">
                          <i :class="`${component} text-white opacity-10`"></i>
                        </div>
                        <div class="d-flex flex-column">
                          <h6 class="mb-1 text-sm text-dark">{{ label }}</h6>
                          <span class="text-xs" v-html="description"></span>
                        </div>
                      </div>
                      <div class="d-flex">
                        <button
                          class="btn btn-sm"
                          :class="{
                            'btn-success': selectedCategory === label,
                            'btn-secondary': selectedCategory !== label
                          }"
                          @click="selectCategoryItem(label)"
                        >
                          {{ selectedCategory === label ? '已选' : '选择' }}
                        </button>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div v-else>
              <p class="text-center text-muted">暂无推荐品类</p>
            </div>
          </div>

          <!-- 猜您喜欢部分 -->
          <div class="col-lg-7 mb-lg">
            <div class="card z-index-2">
              <div class="p-3 pb-0 card-header">
                <div class="d-flex justify-content-between">
                  <h6 class="mb-2">商品</h6>
                  <button @click="selectRandomGoods" class="btn btn-link">换一换</button>
                </div>
              </div>
              <div class="table-responsive">
                <div class="row mx-3">
              <!-- 遍历商品列表 -->
              <div class="col-lg-3 col-md-4 col-6 mb-4" v-for="(product, index) in selectedGoods" :key="index">
                <div class="card" @click="goToProductDetail(product)">
                  <img :src="product.img_url" alt="Product Image" class="card-img-top" />
                  <div class="card-body">
                    <p class="card-text">{{ product.price }} 元</p>
                  </div>
                </div>
              </div>
            </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>