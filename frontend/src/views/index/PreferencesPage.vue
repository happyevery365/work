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

    <button class="confirm-button" @click="savePreferences">确认选择</button>
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
    async savePreferences() {
      try {
        const response = await axios.post(`http://${this.ipAddress}:8000/api/save-preferences/`, {
          username: this.username,
          preferences: this.selectedPreferences
        });

        if (response.data.success) {
          this.$router.push({ name: 'GoodsPage', query: { username: this.username } });
        } else {
          alert('保存喜好失败');
        }
      } catch (error) {
        console.error('Error saving preferences:', error);
        alert('保存喜好时发生错误');
      }
    }
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
</style>