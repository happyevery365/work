<script setup>
import { ref, onBeforeMount, onBeforeUnmount } from "vue";
import { useStore } from "vuex";
import ArgonInput from "@/components/ArgonInput.vue";
import ArgonButton from "@/components/ArgonButton.vue";
import router from "@/router";
import axios from "axios";  // 引入axios
import { ipAddress } from './config.js';
const ipaddress = ref('');
const body = document.getElementsByTagName("body")[0];

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

const goToSignin = () => {
  router.push({ name: 'Signin' });
};

// State for showing/hiding verification input and handling countdown
const showVerificationInput = ref(false);
const countdown = ref(60);
const countdownTimer = ref(null);

// 预设验证码
const verificationCode = ref('');  // 用于保存从后端获取的验证码

// 用户输入的验证码
const userVerificationCode = ref('');

// Function to start the countdown and show verification input
const getVerificationCode = async () => {
  const email = document.getElementById("email").value;

  // 验证邮箱格式
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  if (!email || !emailPattern.test(email)) {
    alert("请输入有效的邮箱地址");
    return;  // 终止倒计时和验证码输入框显示
  }

  // 调用后端接口发送验证码
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/send_sms_code/`, {
      to_email: email,
    });

    if (response.data.ifsend) {
      // 成功发送验证码，保存后端返回的验证码
      verificationCode.value = response.data.sms_code;

      // 开始倒计时
      showVerificationInput.value = true;  // 显示验证码输入框
      countdownTimer.value = setInterval(() => {
        if (countdown.value > 0) {
          countdown.value--;
        } else {
          clearInterval(countdownTimer.value);
        }
      }, 1000);
    } else {
      // 如果验证码发送失败
      alert("验证码发送失败");
    }
  } catch (error) {
    alert("请求失败，请稍后再试");
    console.error(error);
  }
};

// Function to reset the countdown
const resendVerificationCode = () => {
  countdown.value = 60;
  getVerificationCode();
};

// 表单验证函数
const validateForm = async (event) => {
  event.preventDefault(); // 阻止表单默认提交行为

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const password2 = document.getElementById("password2").value;
  const email = document.getElementById("email").value;

  // 检查用户名长度
  if (username.length <= 6) {
    alert("用户名需要大于六个字节");
    return false;
  }

  // 检查密码长度
  if (password.length <= 6) {
    alert("密码需要大于六个字节");
    return false;
  }

  // 检查两次输入的密码是否一致
  if (password !== password2) {
    alert("两次输入的密码不一致");
    return false;
  }

  // 检查邮箱格式
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  if (!emailPattern.test(email)) {
    alert("邮箱格式错误");
    return false;
  }

  // 如果没有输入邮箱
  if (!email) {
    alert("请输入邮箱");
    return false;
  }

  // 验证验证码
  if (!userVerificationCode.value) {
    alert("请输入验证码");
    return false;
  }

  // 检查验证码是否正确
  if (userVerificationCode.value !== verificationCode.value) {
    alert("验证码错误");
    return false;
  }

  // 如果验证通过，发送请求
  try {
    const response = await axios.post(`http://${ipaddress.value}:8080/api/register/`, {
      username: username,
      password: password,
      email: email,
    });

    const message = response.data.message;

    if (message !== "注册成功") {
      alert(message);  // 如果返回的 message 不是 "注册成功"，则弹出 alert 提示
    } else {
      alert("注册成功");
      // 这里可以做跳转等操作，例如跳转到登录页
      router.push({name: "Signin"});
    }
  } catch (error) {
    alert("注册失败，请稍后再试");
    console.error(error);
  }
};
</script>

<template>
  <main class="mt-0 main-content">
    <section>
      <div class="page-header min-vh-100">
        <div class="container">
          <div class="row">
            <div class="mx-auto col-xl-4 col-lg-5 col-md-7 d-flex flex-column mx-lg-0">
              <div class="card card-plain">
                <div class="pb-0 card-header text-start">
                  <h4 class="font-weight-bolder">注册</h4>
                  <p class="mb-0">输入注册信息</p>
                </div>
                <div class="card-body">
                  <!-- 使用 @submit.prevent 来防止页面刷新 -->
                  <form role="form" @submit.prevent="validateForm">
                    <div class="mb-3">
                      <argon-input
                          id="username"
                          type="text"
                          placeholder="用户名"
                          name="username"
                          size="lg"
                      />
                    </div>
                    <div class="mb-3">
                      <argon-input
                          id="password"
                          type="password"
                          placeholder="密码"
                          name="password"
                          size="lg"
                      />
                    </div>
                    <div class="mb-3">
                      <argon-input
                          id="password2"
                          type="password"
                          placeholder="请确认密码"
                          name="password2"
                          size="lg"
                      />
                    </div>
                    <div class="mb-3">
                      <argon-input
                          id="email"
                          type="email"
                          placeholder="邮箱"
                          name="email"
                          size="lg"
                      />
                    </div>

                    <!-- "Get Verification Code" Button -->
                    <div class="mb-3" v-if="!showVerificationInput">
                      <argon-button
                          class="mt-2"
                          variant="gradient"
                          color="success"
                          fullWidth
                          size="lg"
                          @click="getVerificationCode"
                      >
                        获取验证码
                      </argon-button>
                    </div>

                    <!-- Verification Code Input with Resend Button -->
                    <div class="mb-3" v-if="showVerificationInput">
                      <argon-input
                          id="identification"
                          type="text"
                          placeholder="输入验证码"
                          name="identification"
                          size="lg"
                          v-model="userVerificationCode"
                      />
                      <div class="text-center mt-2">
                        <argon-button
                            variant="gradient"
                            color="success"
                            size="sm"
                            @click="resendVerificationCode"
                            :disabled="countdown > 0"
                        >
                          {{ countdown > 0 ? `重新发送(${countdown})` : '重新发送' }}
                        </argon-button>
                      </div>
                    </div>

                    <div class="text-center">
                      <argon-button
                          class="mt-4"
                          variant="gradient"
                          color="success"
                          fullWidth
                          size="lg"
                      >
                        注册
                      </argon-button>
                    </div>
                  </form>
                </div>
                <div class="px-1 pt-0 text-center card-footer px-lg-2">
                  <p class="mx-auto mb-4 text-sm">
                    已有账号?
                    <a
                        href="javascript:;"
                        class="text-success text-gradient font-weight-bold"
                        @click="goToSignin"
                    >登录</a>
                  </p>
                </div>
              </div>
            </div>
            <div
                class="top-0 my-auto text-center col-6 d-lg-flex d-none h-100 pe-0 position-absolute end-0 justify-content-center flex-column">
              <div
                  class="position-relative bg-gradient-primary h-100 m-3 px-7 border-radius-lg d-flex flex-column justify-content-center overflow-hidden"
                  style="background-image: url(&quot;https://file.moyublog.com/d/file/2023-04-10/2b0e8b76d4fcd03e74dd592bc5a53bde.jpg&quot;); background-size: cover;">
                <span class="mask bg-gradient-success opacity-6"></span>
                <h4 class="mt-5 text-white font-weight-bolder position-relative">
                  "Mr. K的比价网页"
                </h4>
                <p class="text-white position-relative">
                  The more effortless the writing looks, the more effort the writer actually put into the process.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
