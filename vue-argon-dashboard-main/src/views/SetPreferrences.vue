<script setup>
import { onBeforeMount, onBeforeUnmount, ref } from "vue";
import { useStore } from "vuex";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { ipAddress } from './config.js';
const ipaddress = ref('');
// Access the route to get the query params
const route = useRoute();
const router = useRouter();

const body = document.getElementsByTagName("body")[0];
const store = useStore();

const username = ref(route.query.username || ''); // Store the username from query params

const selectedPreferences = ref([]);  // To store selected preferences
const selectedStates = ref([]); // To manage individual selection states

onBeforeMount(() => {
  ipaddress.value = ipAddress;
  store.state.hideConfigButton = true;
  store.state.showNavbar = false;
  store.state.showSidenav = false;
  store.state.showFooter = false;
  body.classList.remove("bg-gray-100");
});

onBeforeUnmount(() => {
  store.state.hideConfigButton = false;
  store.state.showNavbar = true;
  store.state.showSidenav = true;
  store.state.showFooter = true;
  body.classList.add("bg-gray-100");
});

// Categories data (same as provided)
const categories = [
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
];

// Toggle the selection state of a category
const toggleSelected = (category) => {
  const index = selectedPreferences.value.indexOf(category.label);

  if (index === -1) {
    // If the category is not selected, add it
    selectedPreferences.value.push(category.label);
  } else {
    // If the category is selected, remove it
    selectedPreferences.value.splice(index, 1);
  }

  // Update selectedStates to reflect the selection
  updateSelectedStates();
};

// Update selectedStates based on selectedPreferences
const updateSelectedStates = () => {
  selectedStates.value = categories.map(category => selectedPreferences.value.includes(category.label));
};

// Method to save preferences
async function savePreferences() {
  if(selectedPreferences.value === null) {
    alert('至少选择一个品类');
  }
  else{
    try {
      const response = await axios.post(`http://${ipaddress.value}:8080/api/save-preferences/`, {
        username: username.value, // Using the username from the route query
        preferences: selectedPreferences.value
      });
      if (response.data.success) {
        router.push({name: '主页', query: {username: username.value}});
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
      alert('保存喜好时发生错误');
    }
  }

}

// Initialize selectedStates based on selectedPreferences on mount
onBeforeMount(() => {
  updateSelectedStates();
});
</script>

<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-lg-12">
        <h5 class="text-center mb-4">欢迎！您可以在此页添加您的喜好~</h5>
        <div class="row mt-4">
          <div class="col-lg-6" v-for="(category, index) in categories" :key="index">
            <div class="card">
              <div class="p-3 pb-0 card-header"></div>
              <div class="p-3 card-body">
                <ul :class="`list-group`">
                  <li
                      :key="index"
                      :class="`mb-2 border-0 list-group-item d-flex justify-content-between border-radius-lg`"
                  >
                    <div class="d-flex align-items-center">
                      <div
                          :class="`text-center shadow icon icon-shape icon-sm bg-gradient-${category.icon.background}`"
                      >
                        <i :class="`${category.icon.component} text-white opacity-10`"></i>
                      </div>
                      <div class="d-flex flex-column">
                        <h6 class="mb-1 text-sm text-dark">{{ category.label }}</h6>
                        <span class="text-xs" v-html="category.description"> </span>
                      </div>
                    </div>
                    <div class="d-flex">
                      <button
                          class="btn btn-sm btn-primary"
                          :class="{'btn-success': selectedStates[index], 'btn-secondary': !selectedStates[index]}"
                          @click="toggleSelected(category)"
                      >
                        {{ selectedStates[index] ? '已选' : '未选' }}
                      </button>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Confirmation Button at the bottom -->
        <div class="text-center mt-4">
          <button class="btn btn-primary" @click="savePreferences">
            确认保存喜好
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
