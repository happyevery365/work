<template>
  <!-- 分类按钮区域 -->
  <div class="category-buttons">
    <button v-for="(englishName, chineseName) in categories" :key="chineseName" @click="goToCategory(englishName)">
      {{ chineseName }}
    </button>
  </div>

  <!-- 返回按钮 -->
  <button @click="goBack" class="back-button">返回</button>
</template>

<script>
export default {
  data() {
    return {
      username: '', // 用户名变量
      categories: {
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
      }
    };
  },
  created() {
    // 获取登录时传递的用户名并存储到 username 变量
    const username = this.$route.query.username;
    if (username) {
      this.username = username;
      console.log("用户登录的用户名:", this.username);
    }
  },
  methods: {
    goToCategory(englishName) {
      this.$router.push({ name: 'CategoryPage', query: { category: englishName, username: this.username } });
    },
    goBack() {
      this.$router.push({ name: 'GoodsPage', query: { username: this.username } });
    }
  }
};
</script>

<style scoped>
.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 20px;
}

.category-buttons button {
  padding: 6px 12px;
  font-size: 14px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.category-buttons button:hover {
  background-color: #e0e0e0;
}

.back-button {
  display: block;
  margin: 20px auto 0;
  padding: 8px 16px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  .goods-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 480px) {
  .goods-grid {
    grid-template-columns: 1fr;
  }
}
</style>
