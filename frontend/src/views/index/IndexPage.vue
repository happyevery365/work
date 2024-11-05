<template>
  <div>
    <p>{{ loginMessage }}</p>
    <input v-model="loginData.username" placeholder="请输入用户名" />
    <input v-model="loginData.password" type="password" placeholder="请输入密码" />
    <button @click="login">登录</button>
  </div>

  <div>
    <h2>注册账号</h2>
    <input v-model="registerData.username" placeholder="用户名"/>
    <input v-model="registerData.password" type="password" placeholder="密码"/>
    <input v-model="registerData.email" placeholder="邮箱"/>
    <button @click="register">注册</button>
    <p>{{ registerMessage }}</p>
  </div>

  <div id="app">
    <h1>商品价格查询</h1>
    <input v-model="query_result.query" placeholder="请输入商品名称" />
    <button @click="searchProduct">搜索</button>

    <div v-if="query_result.loading">查询中...</div>
    <div v-if="query_result.error">{{ query_result.error }}</div>

    <div v-if="query_result.results.length">
      <h2>查询结果：</h2>
      <!--ul>
        <li v-for="(result, index) in query_result.results" :key="index">
          <strong>平台：{{ result.platform }}</strong>
          <p>商品名称：{{ result.name }}</p>
          <p>价格：{{ result.price }}</p>
        </li>
      </ul-->
    </div>
  </div>

</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      loginMessage: '',      // 登录信息
      registerMessage: '',    // 注册信息
      loginData: {            // 登录数据
        username: '',
        password: ''
      },
      registerData: {         // 注册数据
        username: '',
        password: '',
        email: ''
      },
      query_result: {
        query: '',
        results: [],
        loading: false,
        error: null
      },
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/login/', {
          username: this.loginData.username,
          password: this.loginData.password
        })
        this.loginMessage = response.data.message
      } catch (error) {
        console.error('Error during login:', error)
      }
    },
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/register/', {
          username: this.registerData.username,
          password: this.registerData.password,
          email: this.registerData.email
        });
        this.registerMessage = response.data.success || response.data.error;
      } catch (error) {
        console.error('Error registering:', error);
        this.registerMessage = '注册失败';
      }
    },
    async searchProduct() {
      this.query_result.loading = true;
      this.query_result.error = null;
      this.query_result.results = [];

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/search_product/', {
          query: this.query_result.query
        });
        this.query_result.results = response.data.results;
      } catch (error) {
        this.query_result.error = '查询失败，请稍后再试';
      } finally {
        this.query_result.loading = false;
      }
    }
  }
}
</script>
