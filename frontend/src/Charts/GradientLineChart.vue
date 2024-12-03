<script setup>
import { onMounted, defineProps } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  height: {
    type: String,
    default: '300',
  },
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  chart: {
    type: Object,
    required: true,
    labels: Array,
    datasets: Array,
  },
});

onMounted(() => {
  const ctx = document.getElementById(props.id).getContext('2d');
  const gradientStroke1 = ctx.createLinearGradient(0, 230, 0, 50);
  gradientStroke1.addColorStop(1, 'rgba(203,12,159,0.2)');
  gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
  gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)');

  const gradientStroke2 = ctx.createLinearGradient(0, 230, 0, 50);
  gradientStroke2.addColorStop(1, 'rgba(20,23,39,0.2)');
  gradientStroke2.addColorStop(0.2, 'rgba(72,72,176,0.0)');
  gradientStroke2.addColorStop(0, 'rgba(20,23,39,0)');

  let chartStatus = Chart.getChart(props.id);
  if (chartStatus) chartStatus.destroy();

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: props.chart.labels,
      datasets: props.chart.datasets.map((dataset, index) => ({
        ...dataset,
        borderWidth: 3,
        backgroundColor: index === 0 ? gradientStroke1 : gradientStroke2,
        fill: true,
      })),
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      interaction: { intersect: false, mode: 'index' },
      scales: {
        y: {
          grid: { drawBorder: false, display: true, drawOnChartArea: true, drawTicks: false, borderDash: [5, 5] },
          ticks: { display: true, padding: 10, color: '#fbfbfb', font: { size: 11, family: 'Open Sans' } },
        },
        x: {
          grid: { drawBorder: false, display: false, drawOnChartArea: false, drawTicks: false, borderDash: [5, 5] },
          ticks: { display: true, color: '#ccc', padding: 20, font: { size: 11, family: 'Open Sans' } },
        },
      },
    },
  });
});
</script>

<template>
  <div class="card z-index-2">
    <div class="pb-0 card-header mb-0">
      <h6>{{ props.title }}</h6>
      <p v-if="props.description" class="text-sm" v-html="props.description"></p>
    </div>
    <div class="p-3 card-body">
      <div class="chart">
        <canvas :id="props.id" class="chart-canvas" :height="props.height"></canvas>
      </div>
    </div>
  </div>
</template>
