<script setup>
import {computed} from "vue";
import {useRoute} from "vue-router";
import {useStore} from "vuex";

import SidenavItem from "./SidenavItem.vue";

const store = useStore();
const isRTL = computed(() => store.state.isRTL);

const getRoute = () => {
  const route = useRoute();
  const routeArr = route.path.split("/");
  return routeArr[1];
};
const username = computed(() => store.getters.getUsername); // 获取用户名
</script>
<template>
  <div
      class="collapse navbar-collapse w-auto h-auto h-100"
      id="sidenav-collapse-main"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-item
            to="/dashboard-default"
            :class="getRoute() === 'dashboard-default' ? 'active' : ''"
            :navText="isRTL ? 'لوحة القيادة' : '主页'"
            :username="username"
        >
          <template v-slot:icon>
            <i class="ni ni-tv-2 text-primary text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>

      <li class="nav-item">
        <sidenav-item
            to="/virtual-reality"
            :class="getRoute() === 'virtual-reality' ? 'active' : ''"
            :navText="isRTL ? 'الواقع الافتراضي' : '搜索'"
            :username="username"
        >
          <template v-slot:icon>
            <i class="ni ni-app text-info text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>

      <li class="nav-item">
        <sidenav-item
            to="/tables"
            :class="getRoute() === 'tables' ? 'active' : ''"
            :navText="isRTL ? 'الجداول' : '收藏'"
            :username="username"
        >
          <template v-slot:icon>
            <i
                class="ni ni-calendar-grid-58 text-warning text-sm opacity-10"
            ></i>
          </template>
        </sidenav-item>
      </li>

      <li class="nav-item">
        <sidenav-item
            to="/billing"
            :class="getRoute() === 'billing' ? 'active' : ''"
            :navText="isRTL ? 'الفواتیر' : '我的'"
            :username="username"
        >
          <template v-slot:icon>
            <i class="ni ni-credit-card text-success text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>

    </ul>
  </div>


</template>