<script setup>
import axios from 'axios'
import * as echarts from 'echarts/core'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import { GraphChart } from 'echarts/charts'
import { LabelLayout } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import { onMounted, ref, watch } from 'vue'

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  LegendComponent,
  GraphChart,
  CanvasRenderer,
  LabelLayout
])

// 数据获取
let data = null
const fetchData = async () => {
  const response = await axios.get('/static/data.json')
  return response.data
}
const industryData = ref([])
const industryNum = (data) => {
  const totals = {}
  data.forEach((item) => {
    if (totals[item.Industry]) {
      totals[item.Industry] += item.Num
    } else {
      totals[item.Industry] = item.Num
    }
  })
  return Object.keys(totals).map((Industry) => ({
    name: Industry,
    value: totals[Industry]
  }))
}

// 数据初始化
onMounted(async () => {
  data = await fetchData()
  industryData.value = industryNum(data)
  initChart()
})

// 颜色列表
const colorList = [
  new echarts.graphic.LinearGradient(0, 0, 1, 1, [
    { offset: 0, color: 'rgba(59, 181, 182, 1)' },
    { offset: 1, color: 'rgba(66, 227, 151, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(1, 0, 0, 1, [
    { offset: 0, color: 'rgba(254, 220, 69, 1)' },
    { offset: 1, color: 'rgba(251, 112, 153, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(0, 1, 1, 0, [
    { offset: 0, color: 'rgba(0, 138, 255, 1)' },
    { offset: 1, color: 'rgba(0, 216, 255, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(0, 0, 1, 1, [
    { offset: 0, color: 'rgba(246, 191, 159, 1)' },
    { offset: 1, color: 'rgba(219, 138, 222, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(1, 0, 0, 1, [
    { offset: 0, color: 'rgba(247, 138, 158, 1)' },
    { offset: 0.5, color: 'rgba(245, 111, 135, 0.5)' },
    { offset: 1, color: 'rgba(254, 152, 139, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(0, 1, 1, 0, [
    { offset: 0, color: 'rgba(144, 125, 228, 1)' },
    { offset: 1, color: 'rgba(33, 223, 209, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(0, 0, 1, 1, [
    { offset: 0, color: 'rgba(32, 156, 255, 1)' },
    { offset: 1, color: 'rgba(104, 224, 207, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(1, 0, 0, 1, [
    { offset: 0, color: 'rgba(94, 209, 225, 1)' },
    { offset: 0.5, color: 'rgba(191, 194, 254, 0.5)' },
    { offset: 1, color: 'rgba(232, 189, 219, 0.2)' }
  ]),
  new echarts.graphic.LinearGradient(0, 1, 1, 0, [
    { offset: 0, color: 'rgba(238, 114, 125, 1)' },
    { offset: 1, color: 'rgba(253, 162, 63, 0.2)' }
  ])
]
const colorListLen = colorList.length

// 绘制圆圈
function drawCircles(maxLength, radius, max_x, max_y) {
  let circles = []
  let anti_crash_count = 0
  while (circles.length < maxLength) {
    let circle = {
      x: getRandomNumber(radius, max_x - radius),
      y: getRandomNumber(radius, max_y - radius),
      radius
    }

    let isOverlapping = false

    for (let j = 0; j < circles.length; j++) {
      let previous_circle = circles[j]
      let distance = Math.hypot(
        circle.x - previous_circle.x,
        circle.y - previous_circle.y
      )

      if (distance < circle.radius + previous_circle.radius) {
        isOverlapping = true
        break
      }
    }

    if (!isOverlapping) {
      circles.push(circle)
    }
    anti_crash_count++
    if (anti_crash_count > 10000) {
      break
    }
  }
  return circles
}

function getRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min) + min)
}

const chart = ref(null)
let myChart = null

const initChart = () => {
  if (chart.value) {
    myChart = echarts.init(chart.value)
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: function (params) {
          if (params['data']['name'] !== '') {
            return `<b>${params['data']['name']}</b>：<b>${params['data']['value']}</b>`
          }
        }
      },
      series: [
        {
          name: '词条分布',
          type: 'graph',
          layout: 'none',
          label: {
            show: true,
            color: '#fff'
          },
          data: []
        }
      ]
    }
    myChart.setOption(option)
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

watch(
  () => industryData.value,
  (newData) => {
    if (myChart && newData) {
      const max = Math.max(...newData.map((item) => item.value))
      const number = Math.round(max * 0.5)
      const graphCanvas = chart.value.getBoundingClientRect()
      const randomCircleArr = drawCircles(
        newData.length,
        ((max + number) / max) * 40,
        graphCanvas.width,
        graphCanvas.height
      )
      newData.forEach((e, i) => {
        e.itemStyle = {
          color: colorList[Math.floor(Math.random() * colorListLen)],
          shadowBlur: 16,
          shadowOffsetY: 16,
          shadowColor: 'rgba(0,0,0,0.1)'
        }
        if (randomCircleArr[i]) {
          e.x = randomCircleArr[i].x
          e.y = randomCircleArr[i].y
          e.symbolSize = ((e.value + number) / max) * 70
        } else {
          e.symbolSize = 0
          e.x = 0
          e.y = 0
        }
      })
      const option = {
        series: [{ data: newData }]
      }
      myChart.setOption(option)
    }
  }
)
</script>

<template>
  <div class="home">
    <div class="body">
      <div class="button">
        <el-button @click="$router.push('/')" round> 页面切换：主页 </el-button>
      </div>
      <div ref="chart" class="chart"></div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.home {
  height: 100vh;
  background-color: antiquewhite;
  .body {
    height: 90%;
    width: 80%;
    margin: auto;
    .button {
      position: fixed;
      left: 88vw;
      top: 3vh;
      z-index: 999;
    }
  }
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
