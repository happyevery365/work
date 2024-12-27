<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router"; // 导入 useRouter 以便导航

const store = useStore();
const isRTL = computed(() => store.state.isRTL);

const router = useRouter(); // 获取路由实例

// 定义退出登录方法
function logout() {
  localStorage.setItem('token', ''); // 清空 token
  router.push({ name: 'Signin' }); // 跳转到 Signin 页面
}
</script>

<template>
  <nav
    class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl"
    :class="isRTL ? 'top-0 position-sticky z-index-sticky' : ''"
    v-bind="$attrs"
    id="navbarBlur"
    data-scroll="true"
  >
    <div class="px-3 py-1 container-fluid">
      <div
        class="mt-2 collapse navbar-collapse mt-sm-0 me-md-0 me-sm-4"
        :class="isRTL ? 'px-0' : 'me-sm-4'"
        id="navbar"
      >
        <div
          class="pe-md-3 d-flex align-items-center"
          :class="isRTL ? 'me-md-auto' : 'ms-md-auto'"
        >
        </div>
        <ul class="navbar-nav justify-content-end">
          <li class="nav-item d-flex align-items-center">
            <!-- 替换 router-link 为 button，添加 click 事件 -->
            <button
              @click="logout"
              class="px-0 nav-link font-weight-bold bg-transparent border-0 text-danger"
              style="font-size: 16px;"
            >
              <i class="fa fa-user" :class="isRTL ? 'ms-sm-2' : 'me-sm-2'"></i>
              <span v-if="isRTL" class="d-sm-inline d-none">يسجل دخول</span>
              <span v-else class="d-sm-inline d-none">退出登录</span>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
