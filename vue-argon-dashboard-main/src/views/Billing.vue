<script setup>
import { computed, onMounted, ref } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import router from "@/router";
import { ipAddress } from './config.js';
const ipaddress = ref('');
const route = useRoute();
const username = ref(route.query.username || "");
const user_preferences = ref([]);

const prefer_categories = [
  { icon: { component: "ni ni-satisfied", background: "dark" }, label: "电脑", description: "畅销商品，性价比高" },
  { icon: { component: "ni ni-laptop", background: "info" }, label: "配件", description: "电脑配件和硬件产品" },
  { icon: { component: "ni ni-settings", background: "primary" }, label: "办公", description: "办公设备与耗材" },
  { icon: { component: "ni ni-paper-diploma", background: "success" }, label: "文具", description: "书写工具和学习用品" },
  { icon: { component: "ni ni-building", background: "danger" }, label: "工业", description: "机械设备和零件" },
  { icon: { component: "ni ni-briefcase-24", background: "warning" }, label: "商业", description: "商业用品和设备" },
  { icon: { component: "ni ni-satisfied", background: "dark" }, label: "农业", description: "农用工具和设备" },
  { icon: { component: "ni ni-tv-2", background: "info" }, label: "家电", description: "各种家用电器" },
  { icon: { component: "ni ni-mobile-button", background: "primary" }, label: "手机", description: "智能手机与配件" },
  { icon: { component: "ni ni-sound-wave", background: "success" }, label: "通信", description: "通信设备与配件" },
  { icon: { component: "ni ni-camera-compact", background: "danger" }, label: "数码", description: "数码产品与设备" },
  { icon: { component: "ni ni-shop", background: "warning" }, label: "家具", description: "家庭家具与装饰品" },
  { icon: { component: "ni ni-hat-3", background: "dark" }, label: "家装", description: "装修材料与工具" },
  { icon: { component: "ni ni-archive-2", background: "info" }, label: "家居", description: "家庭日常用品" },
  { icon: { component: "ni ni-box-2", background: "primary" }, label: "厨具", description: "厨房用具和小家电" },
  { icon: { component: "ni ni-single-02", background: "success" }, label: "女装", description: "时尚女装与饰品" },
  { icon: { component: "ni ni-user-run", background: "danger" }, label: "男装", description: "经典男装与服饰" },
  { icon: { component: "ni ni-diamond", background: "warning" }, label: "珠宝", description: "高级珠宝与手表"},
  {icon: {component: "ni ni-world", background: "dark"}, label: "生鲜", description: "新鲜水果与蔬菜"},
  {icon: {component: "ni ni-basket", background: "info"}, label: "食品", description: "日常食品与零食"},
  {icon: {component: "ni ni-wine-glass-2", background: "primary"}, label: "酒类", description: "红酒、啤酒与白酒"},
  {icon: {component: "ni ni-ambulance", background: "success"}, label: "健康", description: "健康产品与医疗设备"},
  {icon: {component: "ni ni-baby-carriage", background: "danger"}, label: "母婴", description: "母婴用品与玩具"},
  {icon: {component: "ni ni-collection", background: "warning"}, label: "图书", description: "畅销书与文具"},
  {icon: {component: 'ni ni-collection', background: 'warning'}, label: '乐器', description: '畅销书与文具'},
  {icon: {component: 'ni ni-diamond', background: 'warning'}, label: '鲜花', description: '各种鲜花与植物'},
];
const filteredPreferences = computed(() =>
  user_preferences.value
    .map((pref) => prefer_categories.find((category) => category.label === pref))
    .filter(Boolean)
);

// Fetch user preferences
async function fetchPreferences() {
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/check_user_preference_category/`, {
      username: username.value,
    });
    user_preferences.value = response.data.user_preferences;
  } catch (error) {
    console.error("Error fetching preferences:", error);
  }
}

async function deletePreferences(preference) {
  if (user_preferences.value.length <= 1) {
    alert("至少要有一种收藏品类！");
    return;
  }


  try {
    await axios.post(`http://${ipaddress.value}:8080/api/delete_user_preferences/`, {
      username: username.value,
      preferences: preference,
    });
    user_preferences.value = user_preferences.value.filter((pref) => pref !== preference);
  } catch (error) {
    console.error("Error deleting preferences:", error);
  }
}

const oldPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const passwordMessage = ref('');

const handlePasswordChange = async () => {
  if (newPassword.value.length <= 6) {
    alert('密码长度要大于六字节');
    return; // Return early to stop further execution
  }
  if (newPassword.value !== confirmPassword.value) {
    passwordMessage.value = '新密码和确认密码不匹配';
    return;
  }

  try {
    // Send the POST request
    const response = await axios.post(`http://${ipaddress.value}:8080/api/change_password/`, {
      username: username.value,
      oldpassword: oldPassword.value,
      newpassword: newPassword.value,
    });

    // Use the response to check for success and show a message
    if (response.data.success) {
      alert('密码修改成功');
      localStorage.setItem('token', ''); // 清空 token
      router.push({ name: 'Signin' }); // 跳转到 Signin 页面
    } else {
      alert('密码修改失败: ' + response.data.message); // Show the failure message
    }

  } catch (error) {
    passwordMessage.value = '密码修改失败';
    const message = error.response?.data?.message || '未知错误';
    alert(message);
    console.error('Error changing password:', error);
  }
};
const goods = ref([]); // 新更新价格的商品
const goodsOld = ref([]); // 以往更新价格的商品

// 获取新更新价格的商品
async function newChangedGoods() {
  try {
    const response = await axios.post(
      `http://${ipaddress.value}:8080/api/newChangedGoods/`,
      { username: username.value }
    );
    goods.value = response.data.goods || [];
  } catch (error) {
    console.error("Error fetching new changed goods:", error);
  }
}

// 获取以往更新价格的商品
async function oldChangedGoods() {
  try {
    const response = await axios.post(
      `http://${ipaddress.value}:8080/api/oldChangedGoods/`,
      { username: username.value }
    );
    goodsOld.value = response.data.goods || [];
  } catch (error) {
    console.error("Error fetching old changed goods:", error);
  }
}

// Fetch data when component is mounted
onMounted(() => {
  ipaddress.value = ipAddress;
  fetchPreferences();
  newChangedGoods();
  oldChangedGoods();
});
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

<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <!-- First Row: Change Password -->
      <div class="col-lg-6 mb-4">
        <div class="card">
          <div class="p-3 pb-0 card-header">
            <h6 class="mb-2">修改密码</h6>
          </div>
          <div class="p-3 card-body">
            <div class="mb-3">
              <label for="oldPassword" class="form-label">原密码</label>
              <input type="password" id="oldPassword" v-model="oldPassword" class="form-control" placeholder="请输入原密码" />
            </div>
            <div class="mb-3">
              <label for="newPassword" class="form-label">新密码</label>
              <input type="password" id="newPassword" v-model="newPassword" class="form-control" placeholder="请输入新密码" />
            </div>
            <div class="mb-3">
              <label for="confirmPassword" class="form-label">确认新密码</label>
              <input type="password" id="confirmPassword" v-model="confirmPassword" class="form-control" placeholder="请确认新密码" />
            </div>
            <button class="btn btn-primary" @click="handlePasswordChange">确认修改</button>
            <p v-if="passwordMessage" class="mt-2 text-danger">{{ passwordMessage }}</p>
          </div>
        </div>
      </div>

      <!-- User Preferences -->
      <div class="col-lg-5">
        <div v-if="filteredPreferences.length > 0">
          <div class="card">
            <div class="p-3 pb-0 card-header">
              <h6 class="mb-2">收藏品类</h6>
            </div>
            <div class="p-3 card-body preferences-container3">
              <ul class="list-group">
                <li
                  v-for="({ icon: { component, background }, label, description }, index) in filteredPreferences"
                  :key="index"
                  class="mb-2 border-0 list-group-item3 d-flex justify-content-between border-radius-lg ps-0"
                >
                  <div class="d-flex align-items-center">
                    <div :class="`text-center shadow icon icon-shape icon-sm bg-gradient-${background} me-3`">
                      <i :class="`${component} text-white opacity-10`"></i>
                    </div>
                    <div class="d-flex flex-column">
                      <h6 class="mb-1 text-sm3 text-dark">{{ label }}</h6>
                      <span class="text-xs">{{ description }}</span>
                    </div>
                  </div>
                  <button class="btn btn-sm btn-danger" @click="deletePreferences(label)">
                    取消收藏
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div v-else>
          <div class="card">
            <p class="text-center text-muted">暂无推荐品类</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Price Update Reminders -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <h6 class="mb-0">降价提醒</h6>
          </div>
          <div class="card-body3">
            <div class="row">
              <!-- New Price Updated Products -->
              <div class="col-md-6">
                <h6 class="text-center">新更新价格的商品</h6>
                <div class="product-list">
                  <!-- 新商品 -->
                  <div v-for="(item, index) in goods" :key="index" class="product-item" @click="goToProductDetail(item)">
                    <img :src="item.img_url" class="product-image" alt="商品图片" />
                    <div class="product-info">
                      <h5 class="product-title">{{ item.title }}</h5>
                      <p class="product-price">新价格：{{ item.price }}</p>
                      <p class="product-date">更新时间：{{ item.update_date }}</p>
                    </div>
                  </div>
                  <p v-if="goods.length === 0" class="text-center text-muted">暂无价格更新商品</p>
                </div>
              </div>

              <!-- Past Price Updated Products -->
              <div class="col-md-6">
                <h6 class="text-center">以往商品价格</h6>
                <div class="product-list">
                  <!-- 旧商品 -->
                  <div v-for="(item, index) in goodsOld" :key="index" class="product-item" @click="goToProductDetail(item)">
                  <img :src="item.img_url" class="product-image" alt="商品图片" />
                    <div class="product-info">
                      <p class="product-price">历史价格：{{ item.price }}</p>
                      <p class="product-date">更新时间：{{ item.update_date }}</p>
                    </div>
                  </div>
                  <p v-if="goodsOld.length === 0" class="text-center text-muted">暂无价格更新商品</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
/* 限制商品列表的高度，启用滚动条 */
.product-list {
  max-height: 300px;
  overflow-y: auto;
  padding: 10px;
}

/* 商品项布局 */
.product-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

/* 商品图片样式 */
.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin-right: 15px;
  border-radius: 5px;
}

/* 商品信息样式 */
.product-info {
  flex: 1;
}

.product-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.product-price {
  font-size: 14px;
  color: #333;
}

.product-date {
  font-size: 12px;
  color: #999;
}

.card-body3{
  text-align: center;
}



</style>
