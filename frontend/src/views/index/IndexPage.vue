<template>
  <div class="container">
    <h1 class="title"><span>Mr. K的比价APP</span></h1>
    <div class="auth-box">
      <div class="auth-tabs">
        <div :class="{ activeTab: isLogin }" @click="switchToLogin">登录</div>
        <div :class="{ activeTab: !isLogin }" @click="switchToRegister">注册</div>
      </div>
      <div v-if="isLogin" class="login-area">
        <p>{{ loginMessage }}</p>
        <input v-model="loginData.username" placeholder="用户名" class="auth-input" />
        <input v-model="loginData.password" type="password" placeholder="密码" class="auth-input" />
        <div class="auth-action" @click="login">登录</div>
      </div>
      <div v-else class="register-area">
        <p>{{ registerMessage }}</p>
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
        const response = await axios.post('http://127.0.0.1:8000/api/login/', {
          username: this.loginData.username,
          password: this.loginData.password
        });
        this.loginMessage = response.data.message;
        if (response.data.message === '登录成功') {
          this.loginMessage = '登录成功，正在检查喜好...';
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
        const response = await axios.post('http://127.0.0.1:8000/api/check-preferences/', {
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
        if (!this.registerData.email) {
          this.registerMessage = '邮箱不能为空';
        } else {
          const response = await axios.post('http://127.0.0.1:8000/api/send_sms_code/', {
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
      if (this.isCountingDown) return;
      this.getVerificationCode();
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
        const response = await axios.post('http://127.0.0.1:8000/api/register/', {
          username: this.registerData.username,
          password: this.registerData.password,
          email: this.registerData.email
        });
        this.registerMessage = response.data.message;
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
  padding: 10px;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #4682b4;
  text-shadow: 1px 1px #add8e6;
  margin-bottom: 8px;
  text-align: center;
}

.auth-box {
  width: 70%;
  max-width: 400px;
  padding: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  background-color: #f0f8ff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.auth-tabs {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-bottom: 15px;
}

.auth-tabs div {
  width: 40%;
  padding: 5px;
  font-size: 12px;
  text-align: center;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9fdfd;
  transition: background-color 0.3s;
}

.auth-tabs .activeTab {
  background-color: #4682b4;
  color: white;
}

.auth-input {
  display: flex;
  width: 80%;
  max-width: 220px; /* 缩短输入框的宽度 */
  margin: 6px auto;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  text-align: center;
  background-color: #f0f8ff;
}

.verification-wrapper {
  display: flex;
  align-items: center;
  width: 80%;
  max-width: 250px;
  margin: 6px auto;
}

.verification-input {
  flex: 2; /* 输入框稍微占多一些宽度 */
  margin-right: 8px;
}

.verification-button {
  flex: 1;
  height: 40px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #4682b4;
  color: white;
  font-size: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.verification-button:hover {
  background-color: #5f9ea0;
}

.auth-action {
  width: 60%;
  max-width: 180px;
  padding: 8px;
  font-size: 14px;
  text-align: center;
  color: white;
  background-color: #4682b4;
  border: 1px solid #4682b4;
  border-radius: 4px;
  cursor: pointer;
  margin: 10px auto;
  transition: background-color 0.3s;
}

.auth-action:hover {
  background-color: #5f9ea0;
}

.error-message {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

@media (max-width: 480px) {
  .title {
    font-size: 14px;
  }

  .auth-box {
    padding: 10px;
    max-width: 260px;
  }

  .auth-tabs div {
    font-size: 10px;
    padding: 3px;
  }

  .auth-input {
    font-size: 12px;
    padding: 5px;
  }

  .auth-action {
    font-size: 12px;
    padding: 5px;
  }
}
</style>