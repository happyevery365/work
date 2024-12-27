<template>
  <!-- 平台图标展示区域 -->
  <div class="app-icons" v-if="appImages.length">
    <div class="app-icon-item" v-for="(app, index) in appImages" :key="index">
      <img :src="app.img_url" :alt="app.appname" class="app-icon-image" />
    </div>
  </div>

  <div class="user-info">
    <span class="username">修改密码</span>
  </div>
  <div class="user-info">
    <span class="username">{{ errormessage }}</span>
  </div>

  <!-- 修改框区域 -->
  <div class="search-background">
    <div class="search-container">
      <div class="search-input-wrapper">
        <input type="text" v-model="oldpassword" placeholder="请输入原密码" class="search-input" />
      </div>
    </div>
  </div>
  <div class="search-background">
    <div class="search-container">
      <div class="search-input-wrapper">
        <input type="text" v-model="newpassword" placeholder="请输入新密码" class="search-input" />
        <button @click="changePassword" class="search-button">确认</button>
      </div>
    </div>
  </div>

  <!-- 返回按钮区域 -->
  <div class="return-button-container">
    <button @click="goBack" class="return-button">返回</button>
  </div>
</template>

<script>
import axios from "axios";
import { ipAddress } from './config.js';

export default {
  data() {
    return {
      appImages: [],
      username: '',
      oldpassword:'',
      newpassword:'',
      errormessage:'',
      ipAddress:''
    };
  },
  created() {
    this.ipAddress = ipAddress;
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
    }
    this.errormessage = '';
  },
  methods: {
    async changePassword() {
      if (!this.oldpassword) {
        this.errormessage = '原密码不能为空';
        return;
      }
      if (!this.newpassword) {
        this.errormessage = '新密码不能为空';
        return;
      }
      this.errormessage = '';
      try {
        const response = await axios.post(`http://${this.ipAddress}:8080/api/change_password/`, {
          username: this.username,
          oldpassword: this.oldpassword,
          newpassword: this.newpassword,
        });
        this.errormessage = response.data.message;
      } catch (error) {
        console.error("Failed to change password:", error);
      }
    },
    goBack() {
      this.$router.push({name: 'MyRoom', query: {username: this.username}});
    },
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

.search-background {
  background-color: #ffffff;
  padding: 2vh;
  border-radius: 2vw;
}

.search-container {
  display: flex;
  justify-content: center;
}

.search-input-wrapper {
  display: flex;
  max-width: 80vw;
  width: 100%;
}

.search-input {
  flex: 1;
  padding: 2vh;
  font-size: 3.5vw;
  border: 1px solid #ccc;
  border-radius: 2vw 0 0 2vw;
}

.search-button {
  padding: 0 3vw;
  font-size: 3.5vw;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0 2vw 2vw 0;
  cursor: pointer;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2vh;
}

.username {
  font-size: 4vw;
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

.return-button-container {
  display: flex;
  justify-content: center;
  margin-top: 2vh;
}

.return-button {
  padding: 1.5vh 5vw;
  font-size: 4vw;
  font-weight: bold;
  background-color: #ff4b2b;
  color: white;
  border: none;
  border-radius: 2vw;
  cursor: pointer;
  transition: all 0.3s;
}

.return-button:hover {
  background-color: #ff6f61;
  box-shadow: 0px 4px 10px rgba(255, 75, 43, 0.4);
}
</style>
