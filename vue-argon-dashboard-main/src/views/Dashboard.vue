<script setup>
import MiniStatisticsCard from "@/examples/Cards/MiniStatisticsCard.vue";
import Carousel from "./components/Carousel.vue";

import {onMounted, ref} from "vue";
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
const selectedStates = ref([]);
const toggleSelected = (index, category) => {
  selectedStates.value[index] = !selectedStates.value[index];

  // 如果选中，添加 label 到 appendCategories 中；否则，删除
  if (selectedStates.value[index]) {
    appendCategories.value.push(category.label);  // 只添加 label
  } else {
    const indexToRemove = appendCategories.value.findIndex(item => item === category.label);  // 根据 label 查找
    if (indexToRemove !== -1) {
      appendCategories.value.splice(indexToRemove, 1);
    }
  }
};
// Fetch goods from the backend
async function fetchGoods() {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/get-goods/`, {username: username.value});
    goods.value = response.data.goods;
     selectRandomGoods();
  } catch (error) {
    console.error('Error fetching goods:', error);
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
  let shuffled = [...goods.value].sort(() => 0.5 - Math.random());  // Shuffle the goods array
  selectedGoods.value = shuffled.slice(0, 8);  // Select the first 8 items
}
// Fetch goods when component is mounted
onMounted(() => {
  ipaddress.value = ipAddress;
  fetchGoods();
  fetchPreferGoods();
  fetchNotPreferences();
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
// 物品信息列表
const categories = [
  { title: "电脑", description: "办公、游戏两不误", icon: 'ni ni-laptop' },
  { title: "配件", description: "提升效率的好帮手", icon: 'ni ni-headphones' },
  { title: "办公", description: "高效办公，事半功倍", icon: 'ni ni-basket' },
  { title: "文具", description: "日常文具，应有尽有", icon: 'ni ni-basket' },
  { title: "工业", description: "设备精良，生产高效", icon: 'ni ni-basket' },
  { title: "商业", description: "打造成功的企业伙伴", icon: 'ni ni-building' },
  { title: "农业", description: "提升产量，助力农业", icon: 'ni ni-ruler-pencil' },
  { title: "家电", description: "家居生活，品质家电", icon: 'ni ni-tv-2' },
  { title: "手机", description: "智能手机，满足需求", icon: 'ni ni-mobile-button' },
  { title: "通信", description: "通信设备，畅通无阻", icon: 'ni ni-chat-round' },
  { title: "数码", description: "科技时尚，数码好物", icon: 'ni ni-building' },
  { title: "家具", description: "舒适家居，温馨之家", icon: 'ni ni-archive-2' },
  { title: "家装", description: "家装设计，梦想之家", icon: 'ni ni-palette' },
  { title: "家居", description: "一站购物，家居用品", icon: 'ni ni-shop' },
  { title: "厨具", description: "厨具用品，轻松烹饪", icon: 'ni ni-basket' },
  { title: "女装", description: "时尚女装，尽显魅力", icon: 'ni ni-hat-3' },
  { title: "男装", description: "男士时尚，展现个性", icon: 'ni ni-basket' },
  { title: "内衣", description: "舒适内衣，贴身呵护", icon: 'ni ni-basket' },
  { title: "配饰", description: "精致配饰，完美搭配", icon: 'ni ni-badge' },
  { title: "女鞋", description: "舒适女鞋，自信出行", icon: 'ni ni-basket' },
  { title: "男鞋", description: "男士鞋履，时尚舒适", icon: 'ni ni-basket' },
  { title: "运动", description: "运动装备，助力健康", icon: 'ni ni-sound-wave' },
  { title: "户外", description: "探索自然，装备必备", icon: 'ni ni-basket' },
  { title: "汽车", description: "畅享驾驶，车行天下", icon: 'ni ni-basket' },
  { title: "珠宝", description: "珍贵珠宝，奢华风采", icon: 'ni ni-basket' },
  { title: "文玩", description: "文物珍品，文化传承", icon: 'ni ni-box-2' },
  { title: "箱包", description: "时尚箱包，旅行必备", icon: 'ni ni-basket' },
  { title: "食品", description: "新鲜食品，满足味蕾", icon: 'ni ni-basket' },
  { title: "生鲜", description: "新鲜蔬果，营养丰富", icon: 'ni ni-building' },
  { title: "酒类", description: "精选酒类，品味生活", icon: 'ni ni-building' },
  { title: "健康", description: "关爱健康，呵护身体", icon: 'ni ni-basket' },
  { title: "母婴", description: "母婴用品，呵护成长", icon: 'ni ni-basket' },
  { title: "童装", description: "活力童装，快乐成长", icon: 'ni ni-basket' },
  { title: "玩具", description: "益智玩具，快乐无穷", icon: 'ni ni-basket' },
  { title: "宠物", description: "宠物用品，关爱宠物", icon: 'ni ni-basket' },
  { title: "美妆", description: "美妆护肤，自信光彩", icon: 'ni ni-building' },
  { title: "个户", description: "个性定制，专属产品", icon: 'ni ni-basket' },
  { title: "家清", description: "清洁用品，保持清新", icon: 'ni ni-basket' },
  { title: "香氛", description: "香氛四溢，舒适空间", icon: 'ni ni-basket' },
  { title: "娱乐", description: "娱乐设备，快乐时光", icon: 'ni ni-tv-2' },
  { title: "图书", description: "拓展视野，丰富知识", icon: 'ni ni-books' },
  { title: "乐器", description: "乐器精选，音符飞扬", icon: 'ni ni-basket' },
  { title: "鲜花", description: "美丽鲜花，点缀生活", icon: 'ni ni-basket' }
];
// 随机选择四个物品
const randomCategories = () => {
  let shuffled = categories.sort(() => 0.5 - Math.random());  // 打乱数组
  return shuffled.slice(0, 4);  // 选取前四个
};

const selectedCategories = randomCategories(); // 随机选择的四个物品

const appendCategories = ref([]);
const confirmPreferences = async () => {
  if (appendCategories.value.length === 0) {
    alert("请选择要添加的品类");
    return;
  }
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/append-preferences/`, {
      username: username.value,
      preferences: appendCategories.value
    });
    alert(response.data.message);  // Show response message
    alert('需要重新登录')
    localStorage.setItem('token', ''); // 清空 token
    router.push({ name: 'Signin' }); // 跳转到 Signin 页面
  } catch (error) {
    console.error('Error confirming preferences:', error);
  }
};
function goToProductDetail(product) {
  const url = router.resolve({
    name: 'RTL',
    query: {
      username: username.value,
      productInfo: JSON.stringify(product),
    },
  }).href;
  window.open(url, '_blank');
}
</script>

<style scoped>
.product-img {
  width: 100px; /* 设置图片宽度 */
  height: 100px; /* 设置图片高度 */
  object-fit: cover; /* 确保图片按比例缩放并裁剪以填充框 */
  border-radius: 5px; /* 可选：添加圆角 */
}
.product-title {
  white-space: nowrap; /* 防止换行 */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 显示省略号 */
  max-width: 150px; /* 根据需求设置最大宽度 */
}
.form-check-label {
  font-size: 16px;
  font-weight: 500;
}

.custom-table-responsive {
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: #888 #f0f0f0; /* 滚动条和背景色 */
}

.custom-table-responsive::-webkit-scrollbar {
  width: 8px; /* 滚动条宽度 */
}

.custom-table-responsive::-webkit-scrollbar-track {
  background: #f0f0f0; /* 轨道背景 */
}

.custom-table-responsive::-webkit-scrollbar-thumb {
  background-color: #888; /* 滚动条颜色 */
  border-radius: 10px; /* 滚动条圆角 */
}

.product-img {
  width: 50px; /* 图片宽度 */
  height: 50px; /* 图片高度 */
  object-fit: cover; /* 保持图片比例 */
  cursor: pointer; /* 鼠标样式 */
}

.btn-primary {
  margin-top: 20px;
}
</style>
<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-lg-12">
        <div class="row" v-if="selectedCategories.length > 0">
      <!-- 随机选择的四个物品展示 -->
      <div class="col-lg-3 col-md-6 col-12" v-for="(category, index) in selectedCategories" :key="index">
        <mini-statistics-card
          :value="category.title"
          :description="category.description"
          :icon="{
            component: category.icon,
            background: 'bg-gradient-primary',
            shape: 'rounded-circle',
          }"
        />
      </div>
    </div>
        <div class="row mt-4">
          <div class="col-lg-7 mb-lg">
            <div class="card z-index-2">
              <div class="p-3 pb-0 card-header">
                <div class="d-flex justify-content-between">
                  <h6 class="mb-2">猜您喜欢</h6>
                  <button @click="selectRandomGoods" class="btn btn-link">换一换</button>
                </div>
              </div>
              <div class="table-responsive">
                <div class="row mx-3">
                  <!-- 显示商品，按四个一行 -->
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

          <div class="col-lg-5">
            <carousel />
          </div>
        </div>



        <div class="row mt-4 align-items-start">
          <div class="col-lg-7 mb-4">
            <div class="card">
      <div class="p-3 pb-0 card-header">
        <div class="d-flex justify-content-between">
          <h6 class="mb-2">您的收藏</h6>
        </div>
      </div>
      <!-- 表格容器，启用垂直滚动条 -->
      <div class="custom-table-responsive" style="max-height: 900px; overflow-y: auto;">
        <table class="table align-items-center">
          <tbody>
            <!-- 无商品时显示提示 -->
            <tr v-if="PreferGoods.length === 0">
              <td colspan="4" class="text-center">
                <p>暂无收藏商品</p>
              </td>
            </tr>
            <!-- 遍历显示所有商品，无限制 -->
            <tr v-for="(item, index) in PreferGoods" :key="index"  @click="goToProductDetail(item)">
              <td class="w-30">
                <div class="px-2 py-1 d-flex align-items-center">
                  <div>
                    <img :src="item.img_url" alt="商品图片" class="product-img" />
                  </div>
                  <div class="ms-4">
                    <p class="mb-0 text-xs font-weight-bold">商品:</p>
                    <h6 class="mb-0 text-sm product-title">{{ item.title }}</h6>
                  </div>
                </div>
              </td>
              <td>
                <div class="text-center">
                  <p class="mb-0 text-xs font-weight-bold">店铺:</p>
                  <h6 class="mb-0 text-sm">{{ item.shop }}</h6>
                </div>
              </td>
              <td>
                <div class="text-center">
                  <p class="mb-0 text-xs font-weight-bold">价格:</p>
                  <h6 class="mb-0 text-sm">{{ item.price }}</h6>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
          </div>
          <div class="col-lg-5">
  <!-- 显示不为空的推荐品类 -->
  <div v-if="notPreferredCategories && notPreferredCategories.length > 0">
    <div class="card">
      <div class="p-3 pb-0 card-header"></div>
      <div class="p-3 card-body">
        <ul class="list-group">
          <!-- 遍历 notPreferredCategories -->
          <li
            v-for="({ icon: { component, background }, label, description }, index) in notPreferredCategories"
            :key="index"
            class="mb-2 border-0 list-group-item d-flex justify-content-between border-radius-lg ps-0"
          >
            <div class="d-flex align-items-center">
              <div
                :class="`text-center shadow icon icon-shape icon-sm bg-gradient-${background} me-3`"
              >
                <i :class="`${component} text-white opacity-10`"></i>
              </div>
              <div class="d-flex flex-column">
                <h6 class="mb-1 text-sm text-dark">{{ label }}</h6>
                <!-- eslint-disable-next-line vue/no-v-html -->
                <span class="text-xs" v-html="description"> </span>
              </div>
            </div>
            <div class="d-flex">
              <!-- 替换为选中按钮 -->
              <button
                class="btn btn-sm"
                :class="{
                  'btn-success': selectedStates[index],
                  'btn-secondary': !selectedStates[index]
                }"
                @click="toggleSelected(index, { label, description, background })"
              >
                {{ selectedStates[index] ? '已选' : '未选' }}
              </button>
            </div>
          </li>
        </ul>
        <!-- 确认按钮 -->
        <div class="text-center mt-3">
          <button @click="confirmPreferences" class="btn btn-primary">
            确认添加喜好
          </button>
        </div>
      </div>
    </div>
  </div>


  <!-- 显示空数组时的提示 -->
  <div v-else>
    <p class="text-center text-muted">暂无推荐品类</p>
  </div>
</div>


        </div>
      </div>
    </div>
  </div>
</template>
