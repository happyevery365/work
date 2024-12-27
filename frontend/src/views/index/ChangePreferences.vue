<template>
  <div class="preferences-container">
    <h2>选择您的喜好</h2>
    <!-- 使用一个容器来包裹每行的按钮 -->
    <div class="categories-grid">
      <!-- 将类别分成每行最多4个 -->
      <div class="category-row" v-for="(row, index) in categoryRows" :key="index">
        <button
          v-for="subCategory in row"
          :key="subCategory"
          :class="['category-item', { selected: isSelected(subCategory) }]"
          @click="toggleSelection(subCategory)"
        >
          {{ subCategory }}
        </button>
      </div>
    </div>
    <div class="user-info">
    <span class="username">{{ message }}</span>
    </div>
    <button class="confirm-button" @click="changePreferences">确认选择</button>
    <!-- 返回按钮区域 -->
    <div class="return-button-container">
      <button @click="goBack" class="return-button">返回</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ipAddress } from './config.js';

export default {
  data() {
    return {
      categories: [
        "电脑", "配件", "办公", "文具", "工业", "商业", "农业", "家电", "手机", "通信",
        "数码", "家具", "家装", "家居", "厨具", "女装", "男装", "内衣", "配饰", "女鞋", "男鞋",
        "运动", "户外", "汽车", "珠宝", "文玩", "箱包", "食品", "生鲜", "酒类", "健康", "母婴",
        "童装", "玩具", "宠物", "美妆", "个户", "家清", "香氛", "娱乐", "图书", "乐器", "鲜花"
      ],
      selectedPreferences: [], // 用户选择的喜好
      username: '', // 用户名变量
      message:'',
      ipAddress:''
    };
  },
  created() {
    this.ipAddress = ipAddress;
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
      console.log("用户登录的用户名:", this.username);
    }
    this.message = '';
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
    toggleSelection(category) {
      const index = this.selectedPreferences.indexOf(category);
      if (index > -1) {
        this.selectedPreferences.splice(index, 1); // 取消选中
      } else {
        this.selectedPreferences.push(category); // 选中
      }
    },
    isSelected(category) {
      return this.selectedPreferences.includes(category);
    },
    async changePreferences() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8080/api/change-preferences/`, {
          username: this.username,
          preferences: this.selectedPreferences
        });
        this.message = response.data.message;
      } catch (error) {
        console.error('Error saving preferences:', error);
        alert('保存喜好时发生错误');
      }
    },
    goBack() {
      this.$router.push({name: 'MyRoom', query: {username: this.username}});
    },
  }
};
</script>

<style scoped>
.preferences-container {
  text-align: center;
  color: #4682b4;
}

h2 {
  color: #4682b4;
  margin-bottom: 10px;
  font-size: 12px;
}

.categories-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-items: center;
  padding: 10px;
}

.category-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
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

.confirm-button {
  margin-top: 10px;
  background-color: #4682b4;
  color: white;
  padding: 2px 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 8px;
}

.confirm-button:hover {
  background-color: #36648b;
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

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2vh;
}

.username {
  font-size: 4vw;
}
</style>