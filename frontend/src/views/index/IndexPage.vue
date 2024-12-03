<template>
  <div class="container">
    <h1 class="title"><span>Mr. K的比价网页</span></h1>
    <div class="auth-box">
      <div class="auth-tabs">
        <div :class="{ activeTab: isLogin }" @click="switchToLogin">登录</div>
        <div :class="{ activeTab: !isLogin }" @click="switchToRegister">注册</div>
      </div>
      <div v-if="isLogin" class="login-area">
        <p class="error-message">{{ loginMessage }}</p>
        <input v-model="loginData.username" placeholder="用户名" class="auth-input" />
        <input v-model="loginData.password" type="password" placeholder="密码" class="auth-input" />
        <div class="auth-action" @click="login">登录</div>
      </div>
      <div v-else class="register-area">
        <p class="error-message">{{ registerMessage }}</p>
        <p v-if="passwordMismatch" class="error-message">两次输入的密码不一致</p>
        <p v-if="emptyPassword" class="error-message">请输入密码</p>
        <p v-if="emptyEmail" class="error-message">请输入邮箱</p>
        <input v-model="registerData.username" placeholder="用户名" class="auth-input" />
        <input v-model="registerData.password" type="password" placeholder="密码" class="auth-input" />
        <input v-model="registerData.confirmPassword" type="password" placeholder="确认密码" class="auth-input" />
        <input v-model="registerData.email" type="email" placeholder="邮箱" class="auth-input" />
        <div class="verification-wrapper">
          <input v-model="registerData.test" placeholder="验证码" class="auth-input verification-input" />
          <button class="verification-button" @click="startCountdown" :disabled="isCountingDown">
            {{ isCountingDown ? `重新发送(${countdown}s)` : "获取验证码" }}
          </button>
        </div>
        <div class="auth-action" @click="register">注册</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isLogin: true,
      loginMessage: '',
      registerMessage: '',
      passwordMismatch: false,
      emptyPassword: false,
      emptyEmail: false,
      isCountingDown: false,
      countdown: 60,
      timer: null,
      loginData: {
        username: '',
        password: ''
      },
      registerData: {
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        test: '',
        verifycode: ''
      }
    };
  },
  methods: {
    switchToLogin() {
      this.isLogin = true;
      this.clearMessages();
      this.resetCountdown();
    },
    switchToRegister() {
      this.isLogin = false;
      this.clearMessages();
      this.resetCountdown();
    },
    clearMessages() {
      this.loginMessage = '';
      this.registerMessage = '';
      this.passwordMismatch = false;
      this.emptyPassword = false;
      this.emptyEmail = false;
      this.loginData.username = '';
      this.loginData.password = '';
      this.registerData.username = '';
      this.registerData.password = '';
      this.registerData.confirmPassword = '';
      this.registerData.email = '';
      this.registerData.test = '';
      this.registerData.verifycode = '';
    },
    resetCountdown() {
      this.isCountingDown = false;
      this.countdown = 60;
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
    async login() {
      try {
        const response = await axios.post('http://192.168.117.146:8000/api/login/', {
          username: this.loginData.username,
          password: this.loginData.password
        });
        this.loginMessage = response.data.message;
        if (response.data.message === '登录成功') {
          //this.loginMessage = '登录成功，正在检查喜好...';
          localStorage.setItem('token', response.data.token);
          await this.checkUserPreferences();
        } else {
          this.loginMessage = '登录失败，请检查用户名和密码';
        }
      } catch (error) {
        console.error('Error during login:', error);
        this.loginMessage = '登录时出现错误';
      }
    },
    async checkUserPreferences() {
      try {
        const response = await axios.post('http://192.168.117.146:8000/api/check-preferences/', {
          username: this.loginData.username,
        });
        if (response.data.has_preferences) {
          this.$router.push({ name: 'GoodsPage', query: { username: this.loginData.username } });
        } else {
          this.$router.push({ name: 'PreferencesPage', query: { username: this.loginData.username } });
        }
      } catch (error) {
        console.error('Error checking user preferences:', error);
        this.loginMessage = '检查喜好时出现错误';
      }
    },
    async getVerificationCode() {
  try {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // 邮箱格式的正则表达式

    if (!this.registerData.email) {
      this.registerMessage = '邮箱不能为空';
    } else if (!emailRegex.test(this.registerData.email)) {
      this.registerMessage = '请检查邮箱格式'; // 邮箱格式错误提示
    } else {
      const response = await axios.post('http://192.168.117.146:8000/api/send_sms_code/', {
        to_email: this.registerData.email,
      });
      if (response.data.ifsend) {
        this.registerData.verifycode = response.data.sms_code;
      } else {
        this.registerMessage = '验证码发送失败';
      }
    }
  } catch (error) {
    this.registerMessage = '请求失败，请稍后再试';
  }
},
    startCountdown() {
      if (!this.registerData.email) {
        this.registerMessage = '邮箱不能为空';
        return;
      }
      if (this.isCountingDown) return;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // 邮箱格式的正则表达式

      if (!emailRegex.test(this.registerData.email)) {
        this.registerMessage = '请检查邮箱格式'; // 邮箱格式错误提示
        return ;
      }
      this.getVerificationCode();
      this.registerMessage = '';
      this.isCountingDown = true;
      this.countdown = 60;
      this.timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          this.isCountingDown = false;
          clearInterval(this.timer);
          this.timer = null;
          this.registerData.verifycode = '';
        }
      }, 1000);
    },
    async register() {
      this.emptyPassword = false;
      this.emptyEmail = false;

      if (!this.registerData.password) {
        this.emptyPassword = true;
        return;
      }
      if (!this.registerData.email) {
        this.emptyEmail = true;
        return;
      }
      if (this.registerData.password !== this.registerData.confirmPassword) {
        this.passwordMismatch = true;
        this.registerMessage = '注册失败：密码不一致';
        return;
      }
      this.passwordMismatch = false;
      if (this.registerData.verifycode !== this.registerData.test) {
        this.registerMessage = '注册失败：验证码错误';
        return;
      }
      if (!this.registerData.verifycode) {
        this.registerMessage = '注册失败：请申请验证码';
        return;
      }

      try {
        const response = await axios.post('http://192.168.117.146:8000/api/register/', {
          username: this.registerData.username,
          password: this.registerData.password,
          email: this.registerData.email
        });
        this.registerMessage = response.data.message;
        if (this.registerMessage === "注册成功") {
        // 等待两秒后调用 switchToLogin()
            setTimeout(() => {
                this.switchToLogin();
            }, 2000);  // 2000 毫秒，即两秒
        }
      } catch (error) {
        this.registerMessage = '注册失败';
      }
    }
  },
  beforeUnmount() {
    this.resetCountdown();
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* 使容器占满屏幕 */
  width: 100%; /* 占据整个屏幕宽度 */
  padding: 10px;
  box-sizing: border-box;
}

.title {
  font-size: 15px; /* 缩小标题字体 */
  font-weight: bold;
  color: #4682b4;
  text-shadow: 1px 1px #add8e6;
  margin-bottom: 20px;
  text-align: center;
}

.auth-box {
  width: 60%;
  max-width: 320px; /* 设置更小的最大宽度 */
  padding: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  background-color: #f0f8ff;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto; /* 确保框居中 */
}

.auth-tabs {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-bottom: 1px;
}

.auth-tabs div {
  width: 45%;
  padding: 4px 0;
  text-align: center;
  cursor: pointer;
  font-size: 12px;  /* 调整字体大小 */
}

.auth-tabs .activeTab {
  font-weight: bold;
  color: #4682b4;
}

.auth-input {
  width: 100%;
  max-width: 280px;
  padding: 4px;
  margin: 2px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.auth-action {
  width: 30%;
  max-width: 280px;
  padding: 2px;
  text-align: center;
  background-color: #4682b4;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 auto;
  transition: background-color 0.3s;
  font-size: 10px; /* 缩小按钮的字体 */
  margin-top: 10px; /* 增加登录按钮和搜索框的间距 */
}

.auth-action:hover {
  background-color: #365f7d;
}

.error-message {
  color: red;
  font-size: 8px;
}
</style>
