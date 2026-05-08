<script setup>
import * as echarts from 'echarts/core'
import {
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { BarChart, LineChart } from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import { ref, onMounted, watch } from 'vue'
import { RadarChart } from 'echarts/charts'

echarts.use([
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  BarChart,
  LineChart,
  CanvasRenderer,
  UniversalTransition,
  RadarChart
])

const props = defineProps({
  data: Array,
  theme: String
})
watch(
  () => props.data,
  async (newData) => {
    data2 = {
      xAxis: {
        data: newData.map((item) => item.name)
      },
      series: [
        { name: '裁员人数', data: newData.map((item) => item.value) },
        {
          name: '百分比',
          data: newData.map((item) =>
            ((item.value / item.valueBefore) * 100).toFixed(2)
          )
        }
      ]
    }
    myChart.setOption(data2)
  }
)

// watch(
//   () => props.data,
//   async (newData) => {
//     data2 = {
//       series: [
//         {
//           data: [
//             {
//               value: newData.map((item) => item.value),
//               name: '裁员人数',
//               areaStyle: {
//                 color: 'rgba(0, 0, 255, 0.6)'
//               }
//             }
//           ]
//         },
//         {
//           data: [
//             {
//               value: newData.map((item) =>
//                 ((item.value / item.valueBefore) * 100).toFixed(2)
//               ),
//               name: '百分比',
//               areaStyle: {
//                 color: new echarts.graphic.RadialGradient(0.1, 0.6, 1, [
//                   {
//                     //color: 'rgba(255, 145, 124, 0.1)',
//                     color: 'rgba(0, 255, 0, 0.1)',
//                     offset: 0
//                   },
//                   {
//                     color: 'rgba(255, 145, 124, 0.9)',
//                     offset: 1
//                   }
//                 ])
//               }
//             }
//           ]
//         }
//       ]
//     }
//     myChart.setOption(data2)
//   }
// )

watch(
  () => props.theme,
  (newData) => {
    if (myChart) {
      myChart.dispose()
      initChart(newData)
    }
  }
)

const emit = defineEmits(['stateHighLight'])
const highlight = (type) => {
  emit('stateHighLight', type)
}

const chart = ref(null)
let myChart = null
let data2 = null

const initChart = async (theme) => {
  if (chart.value) {
    myChart = echarts.init(chart.value, theme)
    myChart.showLoading()

    const colors = ['#5470C6', '#EE6666', '#91CC75']
    const option = {
      color: colors,
      title: {
        text: '融资阶段与裁员的关系'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      grid: {
        top: '15%',
        left: '15%',
        right: '20%'
      },
      legend: {
        top: '7%',
        data: ['裁员人数', '百分比']
      },
      xAxis: [
        {
          type: 'category',
          axisTick: {
            alignWithLabel: true
          },
          data: []
        }
      ],
      yAxis: [
        {
          type: 'value',
          name: '裁员人数',
          position: 'right',
          alignTicks: true,
          axisLine: {
            show: true,
            lineStyle: {
              color: colors[0]
            }
          },
          axisLabel: {
            formatter: '{value}'
          }
        },
        {
          type: 'value',
          name: '百分比',
          position: 'left',
          alignTicks: true,
          axisLine: {
            show: true,
            lineStyle: {
              color: colors[1]
            }
          },
          axisLabel: {
            formatter: '{value}%'
          }
        }
      ],
      series: [
        {
          name: '裁员人数',
          type: 'bar',
          data: []
        },
        {
          name: '百分比',
          type: 'line',
          yAxisIndex: 1,
          color: colors[1],
          data: []
        }
      ]
    }

    // const option = {
    //   title: {
    //     text: '融资阶段与裁员的关系'
    //   },
    //   //backgroundColor: 'rgba(250, 235, 215, 0.7)', // 设置背景颜色，可以使用颜色值或 rgba 值
    //   legend: {
    //     left: '45%',
    //     top: '20%',
    //     data: ['裁员人数', '百分比']
    //   },
    //   tooltip: {
    //     trigger: 'item', // 触发类型为数据项
    //     formatter: function (params) {
    //       // 自定义 tooltip 的显示内容
    //       return `${params.seriesName}: ${params.value}`
    //     }
    //   },

    //   radar: [
    //     {
    //       indicator: [
    //         { name: 'Post-IPO', max: 200000 },
    //         { name: 'Acquired', max: 200000 },
    //         { name: 'Series A-Z', max: 200000 },
    //         { name: 'Unknown', max: 200000 },
    //         { name: 'Private Equity...', max: 200000 },
    //         { name: 'Seed', max: 200000 },
    //         { name: 'Subsidi...', max: 200000 }
    //       ],
    //       center: ['30%', '60%'],
    //       radius: 120,
    //       startAngle: 90,
    //       splitNumber: 4,
    //       shape: 'circle',
    //       axisName: {
    //         formatter: '【{value}】',
    //         color: '#22c3aa' // 坐标轴名称颜色
    //       },
    //       splitArea: {
    //         areaStyle: {
    //           color: ['#d2f5a6', '#87f7cf', '#d2f5a6', '#f7f494'],
    //           shadowColor: 'rgba(0, 0, 0, 0.2)', //阴影颜色
    //           shadowBlur: 10
    //         }
    //       },
    //       axisLine: {
    //         lineStyle: {
    //           color: 'rgba(200, 0, 0, 0.3)' //坐标轴颜色
    //         }
    //       },
    //       splitLine: {
    //         lineStyle: {
    //           color: 'rgba(200, 0, 0, 0.3)' //坐标轴颜色
    //         }
    //       }
    //     },
    //     {
    //       indicator: [
    //         { name: 'Post-IPO', max: 45 },
    //         { name: 'Acquired', max: 45 },
    //         { name: 'Series A-Z', max: 45 },
    //         { name: 'Unknown', max: 45 },
    //         { name: 'Private Equity...', max: 45 },
    //         { name: 'Seed', max: 45 },
    //         { name: 'Subsidi...', max: 45 }
    //       ],
    //       center: ['70%', '60%'],
    //       radius: 120,
    //       axisName: {
    //         /* color: '#fff',
    //       backgroundColor: '#666',
    //       borderRadius: 3,
    //       padding: [3, 5], */
    //         formatter: '【{value}】',
    //         color: '#22c3aa' // 坐标轴名称颜色
    //       },
    //       axisLine: {
    //         lineStyle: {
    //           color: 'rgba(0, 0, 150, 0.3)' //坐标轴颜色
    //         }
    //       },
    //       splitLine: {
    //         lineStyle: {
    //           color: 'rgba(0, 0, 150, 0.3)' //坐标轴颜色
    //         }
    //       }
    //     }
    //   ],
    //   series: [
    //     {
    //       type: 'radar',
    //       id: '1',
    //       //name :'裁员人数',
    //       emphasis: {
    //         lineStyle: {
    //           width: 4
    //         }
    //       },
    //       data: [
    //         {
    //           value: [188228, 15409, 51148, 15238, 3432, 167, 359],
    //           name: '裁员人数',
    //           areaStyle: {
    //             color: 'rgba(0, 0, 255, 0.6)'
    //           }
    //         }
    //       ]
    //     },
    //     {
    //       type: 'radar',
    //       radarIndex: 1,
    //       //name :'百分比'
    //       data: [
    //         {
    //           value: [5.34, 11.48, 14.56, 17.16, 13.65, 40.14, 4.72],
    //           name: '百分比',
    //           areaStyle: {
    //             color: new echarts.graphic.RadialGradient(0.1, 0.6, 1, [
    //               {
    //                 //color: 'rgba(255, 145, 124, 0.1)',
    //                 color: 'rgba(0, 255, 0, 0.1)',
    //                 offset: 0
    //               },
    //               {
    //                 color: 'rgba(255, 145, 124, 0.9)',
    //                 offset: 1
    //               }
    //             ])
    //           }
    //         }
    //       ]
    //     }
    //   ]
    // }

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

<style lan="less" scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style>
