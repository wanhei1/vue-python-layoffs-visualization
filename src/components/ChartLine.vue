<!-- <script setup>
import * as echarts from 'echarts/core'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { BarChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  BarChart,
  CanvasRenderer
])

const props = defineProps({
  data: Array,
  theme: String
})
watch(
  () => props.data,
  (newData) => {
    data2 = {
      xAxis: {
        data: newData.map((item) => item.name)
      },
      series: [
        {
          name: '公司人员规模与裁员人数',
          data: newData.map((item) => item.value)
        }
      ]
    }
    if (myChart) {
      myChart.setOption(data2)
    }
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

const chart = ref(null)
let myChart = null
let data2 = null

const initChart = async (theme) => {
  if (chart.value) {
    myChart = echarts.init(chart.value, theme)
    myChart.showLoading()

    const option = {
      title: {
        text: '公司规模与裁员的关系'
      },
      tooltip: {},
      xAxis: {
        data: [],
        splitLine: {
          show: false
        }
      },
      yAxis: {},
      series: [
        {
          name: '公司人员规模与裁员人数',
          type: 'bar',
          data: [],
          emphasis: {
            focus: 'series'
          },
          animationDelay: function (idx) {
            return idx * 10
          }
        }
        // {
        //   name: 'bar2',
        //   type: 'bar',
        //   data: data2,
        //   emphasis: {
        //     focus: 'series'
        //   },
        //   animationDelay: function (idx) {
        //     return idx * 10 + 100
        //   }
        // }
      ],
      animationEasing: 'elasticOut'
      // animationDelayUpdate: function (idx) {
      //   return idx * 5
      // }
    }

    myChart.setOption(option)
    if (data2) myChart.setOption(data2)
    myChart.hideLoading()
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

onMounted(() => {
  initChart('light')
})

onBeforeUnmount(() => {
  if (myChart) {
    myChart.dispose()
  }
  window.removeEventListener('resize', () => {
    myChart.resize()
  })
})
</script>

<template><div ref="chart" class="chart"></div></template>

<style lan="less" scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style> -->

<script setup>
import * as echarts from 'echarts/core'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { ScatterChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  ScatterChart,
  CanvasRenderer
])

const props = defineProps({
  data: Array,
  theme: String
})

watch(
  () => props.data,
  (newData) => {
    data2 = {
      xAxis: {
        type: 'category',
        data: newData.map((item) => item.name)
      },
      series: [
        {
          name: '公司人员规模与裁员人数',
          data: newData.map((item) => [
            item.name,
            item.value,
            item.mean_money,
            item.mean_num,
            item.count,
            item.scale
          ]),
          type: 'scatter'
        }
      ]
    }
    if (myChart) {
      myChart.setOption(data2)
    }
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

const emit = defineEmits(['scaleHighLight'])
const highlight = (type) => {
  emit('scaleHighLight', type)
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
        text: '公司规模与裁员的关系'
      },
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          return `
            <strong>公司规模:</strong> ${params.data[5]}<br>
            <strong>公司数:</strong> ${params.data[4]}<br>
            <strong>平均裁员比例:</strong> ${params.data[1].toFixed(2)}%<br>
            <strong>平均裁员人数:</strong> ${params.data[3].toFixed(2)}<br>
            <strong>平均筹集资金:</strong> ${Number(params.data[2].toFixed(2))}<strong>(百万美元)</strong>
          `
        }
      },
      xAxis: {
        type: 'category',
        data: [],
        splitLine: {
          show: false
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}%'
        }
      },
      series: [
        {
          name: '公司人员规模与裁员人数',
          type: 'scatter',
          symbolSize: function (data) {
            return Math.sqrt(data[3]) * 0.8
          },
          data: [],
          emphasis: {
            focus: 'series'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(75, 0, 130, 0.5)',
            shadowOffsetY: 5,
            color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
              {
                offset: 0,
                color: 'rgb(186, 85, 211)'
              },
              {
                offset: 1,
                color: 'rgb(138, 43, 226)'
              }
            ])
          },
          animationDelay: function (idx) {
            return idx * 10
          }
        }
      ],
      animationEasing: 'elasticOut'
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

onBeforeUnmount(() => {
  if (myChart) {
    myChart.dispose()
  }
  window.removeEventListener('resize', () => {
    myChart.resize()
  })
})
</script>

<template><div ref="chart" class="chart"></div></template>

<style lan="less" scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style>
