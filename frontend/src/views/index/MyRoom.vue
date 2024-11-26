<template>
  <!-- 平台图标展示区域 -->
  <div class="app-icons" v-if="appImages.length">
    <div class="app-icon-item" v-for="(app, index) in appImages" :key="index">
      <img :src="app.img_url" :alt="app.appname" class="app-icon-image" />
    </div>
  </div>

  <!-- 功能条栏 -->
  <div class="action-bar">
    <div class="action-item" v-for="(action, index) in actions" :key="index" @click="action.handler">
      {{ action.name }}
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

export default {
  data() {
    return {
      searchQuery: '',
      appImages: [],
      goods: [],
      username: '',
      navItems: [
        {name: '首页', page: 'GoodsPage'},
        {name: '分类', page: 'Product_Categories'},
        {name: '比价', page: 'PriceCompare'},
        {name: '我的', page: 'MyRoom'}
      ],
      actions: [
        {name: '我的收藏', handler: () => this.$router.push({name: 'MyFavorites', query: {username: this.username} })},
        {name: '修改密码', handler: () => this.$router.push({name: 'ChangePassword', query: {username: this.username}})},
        {name: '修改喜好', handler: () => this.$router.push({name: 'ChangePreferences', query: {username: this.username}})},
        {name: '降价信息', handler: () => this.$router.push({name: 'DiscountInfo', query: {username: this.username}})},
        {name: '退出登录', handler: () => this.logout()}
      ],
      currentPage: 'MyRoom'
    };
  },
  created() {
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
    }
  },
  mounted() {
    this.fetchAppImages();
  },
  methods: {
    async fetchAppImages() {
      const response = await axios.get('http://192.168.117.146:8000/api/get-app-images/');
      this.appImages = response.data.appImages;
    },
    goToPage(page) {
      this.$router.push({name: page, query: {username: this.username}});
      this.currentPage = page;
    },
    logout() {
      localStorage.setItem('token', '');
      localStorage.setItem('isLoggedIn', 'false');
      this.$router.push({name: 'IndexPage'});
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

/* 功能条栏 */
.action-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2vh; /* 设置选项间距 */
  margin: 3vh auto;
  width: 90%; /* 控制条栏宽度，增加左右间隙 */
}

.action-item {
  width: 100%; /* 让选项占据整个条栏宽度 */
  text-align: center;
  color: #007bff;
  cursor: pointer;
  font-size: 4vw;
  padding: 2vh 0;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.action-item:hover {
  background-color: #e9ecef;
  transform: scale(1.02); /* 增加轻微缩放效果 */
}

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
  font-size: 3.5vw;
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

@media (max-width: 600px) {
  .bottom-nav {
    font-size: 3vw;
  }
}

h2 {
  font-size: 4.5vw;
  margin-top: 4vh;
}
</style>
