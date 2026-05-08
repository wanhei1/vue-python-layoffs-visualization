<script setup>
import * as echarts from 'echarts/core'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import { PieChart } from 'echarts/charts'
import { LabelLayout } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import { ref, onMounted, watch } from 'vue'

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  LegendComponent,
  PieChart,
  CanvasRenderer,
  LabelLayout
])

const props = defineProps({
  data: Array,
  theme: String
})
watch(
  () => props.data,
  async (newData) => {
    data2 = {
      series: [{ data: newData }]
    }
    myChart.setOption(data2)
  }
)

watch(
  () => props.theme,
  (newData) => {
    if (myChart) {
      myChart.dispose()
      initChart(newData)
    }
  }
)

const emit = defineEmits(['industryHighLight'])
const highlight = (type) => {
  emit('industryHighLight', type)
}

const chart = ref(null)
let myChart = null
let data2 = null

const initChart = async (theme) => {
  if (chart.value) {
    myChart = echarts.init(chart.value, theme)
    myChart.showLoading()

    const option = {
      title: {
        text: '行业与裁员关系',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      series: [
        {
          name: '行业与裁员人数',
          type: 'pie',
          radius: [10, 100],
          roseType: 'area',
          itemStyle: {
            borderRadius: 5
          },
          data: []
        }
      ]
    }

    myChart.setOption(option)
    if (data2) myChart.setOption(data2)

    myChart.on('mouseover', function (params) {
      highlight(params.name)
    })

    myChart.on('mouseout', function () {
      highlight(null)
    })

    myChart.hideLoading()

    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

onMounted(() => {
  initChart('light')
})
</script>

<template>
  <div ref="chart" class="chart"></div>
</template>

<style lang="less" scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style>
