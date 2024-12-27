<template>
  <!-- 平台图标展示区域 -->
  <div class="app-icons" v-if="appImages.length">
    <div class="app-icon-item" v-for="(app, index) in appImages" :key="index">
      <img :src="app.img_url" :alt="app.appname" class="app-icon-image" />
    </div>
  </div>
  <div class="preferences-container">

    <!-- 使用一个容器来包裹每行的按钮 -->
    <div class="categories-grid">
      <!-- 将类别分成每行最多4个 -->
      <div class="category-row" v-for="(row, index) in categoryRows" :key="index">
        <button
          v-for="subCategory in row"
          :key="subCategory"
          class="category-item"
          @click="goToCategory(subCategory)"
        >
          {{ subCategory }}
        </button>
      </div>
    </div>
  </div>

  <!-- 固定底部导航栏 -->
  <div class="bottom-nav">
    <div
      v-for="(navItem, index) in navItems"
      :key="index"
      class="nav-item"
      :class="{ selected: currentPage === navItem.page }"
      @click="goToPage(navItem.page)"
    >
      {{ navItem.name }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ipAddress } from './config.js';

export default {
  data() {
    return {
      username: '', // 用户名变量
      categories: [
        "电脑", "配件", "办公", "文具", "工业", "商业", "农业", "家电", "手机", "通信",
        "数码", "家具", "家装", "家居", "厨具", "女装", "男装", "内衣", "配饰", "女鞋", "男鞋",
        "运动", "户外", "汽车", "珠宝", "文玩", "箱包", "食品", "生鲜", "酒类", "健康", "母婴",
        "童装", "玩具", "宠物", "美妆", "个户", "家清", "香氛", "娱乐", "图书", "乐器", "鲜花"
      ],
      appImages: [],
      navItems: [
        { name: '首页', page: 'GoodsPage' },
        { name: '分类', page: 'Product_Categories' },
        { name: '比价', page: 'PriceCompare' },
        { name: '我的', page: 'MyRoom' }
      ],
      currentPage: 'Product_Categories', // Set the current page as "Product_Categories"
      ipAddress:''
    };
  },
  created() {
    this.ipAddress = ipAddress;
    // 获取登录时传递的用户名并存储到 username 变量
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
      console.log("用户登录的用户名:", this.username);
    }
  },
  mounted(){
    this.fetchAppImages();
  },
  computed: {
    // 计算每行最多显示四个类别的行
    categoryRows() {
      let rows = [];
      for (let i = 0; i < this.categories.length; i += 4) {
        rows.push(this.categories.slice(i, i + 4));  // 每行取四个类别
      }
      return rows;
    }
  },
  methods: {
    async fetchAppImages() {
      const response = await axios.get(`http://${this.ipAddress}:8080/api/get-app-images/`);
      this.appImages = response.data.appImages;
    },
    // 根据中文类别名称跳转到对应的英文页面
    goToCategory(category) {
      const categoryMap = {
        '电脑': 'Computer', '配件': 'Accessories', '办公': 'Office', '文具': 'Stationery',
        '工业': 'Industrial', '商业': 'Business', '农业': 'Agriculture', '家电': 'HomeAppliance',
        '手机': 'MobilePhone', '通信': 'Telecom', '数码': 'Digital', '家具': 'Furniture',
        '家装': 'HomeDecoration', '家居': 'HomeLiving', '厨具': 'Kitchenware', '女装': 'WomenClothing',
        '男装': 'MenClothing', '内衣': 'Underwear', '配饰': 'Accessories', '女鞋': 'WomenShoes',
        '男鞋': 'MenShoes', '运动': 'Sports', '户外': 'Outdoor', '汽车': 'Automobile', '珠宝': 'Jewelry',
        '文玩': 'Collectibles', '箱包': 'Luggage', '食品': 'Food', '生鲜': 'FreshFood', '酒类': 'Alcohol',
        '健康': 'Health', '母婴': 'MotherBaby', '童装': 'KidsClothing', '玩具': 'Toys', '宠物': 'Pets',
        '美妆': 'Beauty', '个户': 'Personal', '家清': 'Household', '香氛': 'Fragrance', '娱乐': 'Entertainment',
        '图书': 'Books', '乐器': 'MusicalInstruments', '鲜花': 'Flowers'
      };

      // 查找并获取对应的英文名称
      const englishName = categoryMap[category];
      if (englishName) {
        this.$router.push({ name: 'CategoryPage', query: { category: englishName, username: this.username } });
      }
    },
    goToPage(page) {
      this.$router.push({name: page, query: {username: this.username}});
      this.currentPage = page;
    }
  }
};
</script>

<style scoped>
/* 保证内容与视口大小一致 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 10vh;
  box-sizing: border-box;
}

/* 分类按钮样式 */
.category-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 一行四个按钮 */
  gap: 5px;
  justify-items: center; /* 按钮居中 */
  margin-top: 2vh;
  margin-bottom: 5vh;
}

.category-buttons button {
  padding: 8px 10px; /* 缩小按钮的间距 */
  font-size: 5px; /* 缩小按钮文字大小 */
  background-color: rgba(251, 249, 249, 0.93);
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  width: 100%; /* 让按钮宽度自动适应父容器 */
}

.category-buttons button:hover {
  background-color: #e0e0e0;
}

/* 固定底部导航栏 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  background-color: #007bff;
  padding: 1vh 0;
  box-sizing: border-box;
  font-size: 3.5vw; /* 设置初始字体大小 */
}

.nav-item {
  color: white;
  cursor: pointer;
  text-align: center;
  flex-grow: 1;
  padding: 1vh 0;
  box-sizing: border-box;
}

.nav-item.selected {
  background-color: #0056b3;
  border-radius: 2vw;
  padding: 1vh 2vw;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .category-buttons button {
    font-size: 12px;
    padding: 8px 10px;
  }
}

@media (max-width: 600px) {
  .bottom-nav {
    font-size: 3vw;
  }
}

.preferences-container {
  text-align: center;
  color: #4682b4;
}

h2 {
  color: #4682b4;
  margin-bottom: 10px;
  font-size: 12px;
}

.category-item {
  padding: 2px;
  font-size: 8px;
  color: #4682b4;
  background-color: white;
  border: 1px solid #4682b4;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.category-item.selected {
  background-color: #4682b4;
  color: white;
}

.category-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.categories-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-items: center;
  padding: 10px;
}

.app-icons {
  display: flex;
  justify-content: center;
  gap: 3vw;
  margin-bottom: 4vh;
}

.app-icon-item {
  flex: 0 1 20%;
  max-width: 15vw;
}

.app-icon-image {
  width: 100%;
  height: auto;
}
</style>
