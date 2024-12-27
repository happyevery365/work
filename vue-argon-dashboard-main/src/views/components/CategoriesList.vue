<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";

const store = useStore();
const isRTL = computed(() => store.state.isRTL);

defineProps({
  title: {
    type: String,
    default: "商品库",
  },
  categories: {
    type: Array,
    required: true,
    icon: {
      component: String,
      background: String,
    },
    label: String,
    description: String,
  },
});

// 添加选中状态
const selectedStates = ref([]);

const toggleSelected = (index) => {
  selectedStates.value[index] = !selectedStates.value[index];
};
</script>

<template>
  <div class="card">
    <div class="p-3 pb-0 card-header">
    </div>
    <div class="p-3 card-body">
      <ul :class="`list-group ${isRTL ? 'pe-0' : ''}`">
        <li
          v-for="(
            { icon: { component, background }, label, description }, index
          ) of categories"
          :key="index"
          :class="`mb-2 border-0 list-group-item d-flex justify-content-between border-radius-lg
          ${isRTL ? 'pe-0' : 'ps-0'}`"
        >
          <div class="d-flex align-items-center">
            <div
              :class="`text-center shadow icon icon-shape icon-sm bg-gradient-${background} ${
                isRTL ? 'ms-3' : 'me-3'
              }`"
            >
              <i :class="`${component} text-white opacity-10`"></i>
            </div>
            <div class="d-flex flex-column">
              <h6 class="mb-1 text-sm text-dark">{{ label }}</h6>
              <!-- eslint-disable-next-line vue/no-v-html -->
              <span class="text-xs" v-html="description"> </span>
            </div>
          </div>
          <div class="d-flex">
            <!-- 替换为选中按钮 -->
            <button
              class="btn btn-sm btn-primary"
              :class="{'btn-success': selectedStates[index], 'btn-secondary': !selectedStates[index]}"
              @click="toggleSelected(index)"
            >
              {{ selectedStates[index] ? '已选' : '未选' }}
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
