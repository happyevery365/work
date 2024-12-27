<script setup>
import {onBeforeUnmount, onBeforeMount, ref} from "vue";
import { useStore } from "vuex";

import ArgonInput from "@/components/ArgonInput.vue";
import ArgonButton from "@/components/ArgonButton.vue";
import router from "@/router";
import axios from 'axios';
import { ipAddress } from './config.js';
const ipaddress = ref('');
const body = document.getElementsByTagName("body")[0];
const loginData = ref({
  username: "",
  password: "",
});
const store = useStore();
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
const goToSignup = () => {
  router.push({ name: 'Signup' });
};

const login = async () => {
  try {
    // Make the login request
    const response = await axios.post(`http://${ipaddress.value}:8080/api/login/`, {
      username: loginData.value.username,
      password: loginData.value.password,
    });

    // If login is successful
    if (response.data.message === '登录成功') {
      // Store the token in local storage
      localStorage.setItem('token', response.data.token);
      store.dispatch("updateUsername", loginData.value.username); // 更新 Vuex Store
      // Call function to check user preferences
      await checkUserPreferences();
    } else {
      alert('登录失败，请检查用户名和密码');
    }
  } catch (error) {
    console.error('Error during login:', error);
    alert('登录时出现错误');
  }
};

// Function to check user preferences
const checkUserPreferences = async () => {
  try {
    // Check if the user has set preferences
    const response = await axios.post(`http://${ipaddress.value}:8080/api/check-preferences/`, {
      username: loginData.value.username,
    });

    // If user has preferences, redirect to GoodsPage, otherwise to PreferencesPage
    if (response.data.has_preferences) {
      router.push({ name: '主页', query: { username: loginData.value.username } });
    } else {
      router.push({ name: 'SetPreferrences', query: { username: loginData.value.username } });
    }
  } catch (error) {
    console.error('Error checking user preferences:', error);
    alert('检查喜好时出现错误');
  }
};
</script>
<template>

  <main class="mt-0 main-content">
    <section>
      <div class="page-header min-vh-100">
        <div class="container">
          <div class="row">
            <div
              class="mx-auto col-xl-4 col-lg-5 col-md-7 d-flex flex-column mx-lg-0"
            >
              <div class="card card-plain">
                <div class="pb-0 card-header text-start">
                  <h4 class="font-weight-bolder">登录</h4>
                  <p class="mb-0">输入账号和密码</p>
                </div>
                <div class="card-body">
                  <form @submit.prevent="login">
                    <div class="mb-3">
                      <argon-input
                          v-model="loginData.username"
                        id="email"
                        placeholder="用户名"
                        name="email"
                        size="lg"
                      />
                    </div>
                    <div class="mb-3">
                      <argon-input
                          v-model="loginData.password"
                        id="password"
                        type="password"
                        placeholder="密码"
                        name="password"
                        size="lg"
                      />
                    </div>


                    <div class="text-center">
                      <argon-button
                          @click="login"
                        class="mt-4"
                        variant="gradient"
                        color="success"
                        fullWidth
                        size="lg"
                        >登录</argon-button
                      >
                    </div>
                  </form>
                </div>
                <div class="px-1 pt-0 text-center card-footer px-lg-2">
                  <p class="mx-auto mb-4 text-sm">
                    没有账号?
                    <a
                      href="javascript:;"
                      class="text-success text-gradient font-weight-bold"
                      @click="goToSignup"
                      >注册</a
                    >
                  </p>
                </div>
              </div>
            </div>
            <div
              class="top-0 my-auto text-center col-6 d-lg-flex d-none h-100 pe-0 position-absolute end-0 justify-content-center flex-column"
            >
              <div
                class="position-relative bg-gradient-primary h-100 m-3 px-7 border-radius-lg d-flex flex-column justify-content-center overflow-hidden"
                style="
                  background-image: url(&quot;https://file.moyublog.com/d/file/2023-04-10/2b0e8b76d4fcd03e74dd592bc5a53bde.jpg&quot;);
                  background-size: cover;
                "
              >
                <span class="mask bg-gradient-success opacity-6"></span>
                <h4
                  class="mt-5 text-white font-weight-bolder position-relative"
                >
                  "Mr. K的比价网页"
                </h4>
                <p class="text-white position-relative">
                  The more effortless the writing looks, the more effort the
                  writer actually put into the process.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
