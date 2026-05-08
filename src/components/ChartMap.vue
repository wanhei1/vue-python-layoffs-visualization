<!-- <script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts/core'
import {
  VisualMapComponent,
  GeoComponent,
  GridComponent
} from 'echarts/components'
import { MapChart, BarChart, ScatterChart } from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import axios from 'axios'

echarts.use([
  VisualMapComponent,
  GeoComponent,
  MapChart,
  CanvasRenderer,
  UniversalTransition,
  ScatterChart,
  BarChart,
  GridComponent
])

const chartContainer = ref(null)
let myChart = null

//地图数据获取
const fetchMapData = async () => {
  const response = await axios.get('/static/USA.json')
  return response.data
}

//数据传入并监听
const props = defineProps({
  pointData: Array,
  data: Array,
  sortData: Array,
  theme: String,
  isMap: Boolean,
  highlight: Array
})

//散点图数据
watch(
  () => props.pointData,
  (newData) => {
    if (myChart) {
      if (isMapOption)
        myChart.setOption({
          series: [
            {
              name: 'Points',
              data: newData
            }
          ]
        })
    }
  }
)

//地图数据
watch(
  () => props.data,
  (newData) => {
    if (props.theme === 'dark') {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'white', //白色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#24CFF4', '#2E98CA', '#1E62AC'] //蓝色深浅
          },
          emphasis: {
            // areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },

          itemStyle: {
            areaColor: '#8dd7fc', // 区域填充色
            borderColor: '#53D9FF', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: 'rgb(58,115,192)', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          },
          emphasis: {
            areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25,
            label: {
              show: true,
              color: '#f75a00' //深橙色
            }
          }
        },

        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return '#d94e5d'
                  } else if (value > 200) {
                    return '#eac736'
                  } else {
                    return '#f75a00' //橙色
                  }
                }
              }
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    } else {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'black', //橙色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#FFA07A', '#FF7F50', '#7F3600'] //红色深浅
          },
          emphasis: {
            areaColor: 'red', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true,
          textStyle: {
            color: '#0f0d0d' //黑色
          }
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },
          emphasis: {
            label: {
              show: true,
              color: '#7B93A7' //橙色
            }
          },
          itemStyle: {
            // areaColor: '#fdae61', // 区域填充色
            borderColor: '#e0f3f8', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: '#f46d43', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          }
        },
        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return '#FFB84D'
                  } else if (value > 200) {
                    return '#FFD700'
                  } else {
                    return '#FFFFE0'
                  }
                }
              }
            },
            label: {
              show: false,
              position: 'right',
              formatter: function (params) {
                return params.data[2]
              },
              color: '#f1f3f4',
              fontSize: 12
            },
            emphasis: {
              itemStyle: {
                color: '#f75a00'
              }
              // focus: 'self',
              // blurScope: 'series'
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    }
    if (myChart) {
      if (isMapOption)
        myChart.setOption({
          series: [
            {
              name: 'sum',
              data: newData
            }
          ]
        })
    }
  }
)

//柱状图数据
watch(
  () => props.sortData,
  (newData) => {
    if (props.theme === 'dark') {
      barOption = {
        // backgroundColor: 'rgb(16, 12, 42)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#ffffff'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#ffffff',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    } else {
      barOption = {
        // backgroundColor: 'rgb(250, 235, 215)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#000000'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#000000',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    }
    if (myChart) {
      if (!isMapOption)
        if (props.theme === 'dark') {
          myChart.setOption({
            yAxis: [
              {
                axisLabel: {
                  show: true,
                  textStyle: {
                    color: '#ffffff'
                  }
                },
                data: newData.map((item) => item.name)
              },
              {
                axisLabel: {
                  textStyle: {
                    color: '#ffffff',
                    fontSize: '12'
                  }
                },
                data: newData.map((item) => item.value)
              }
            ],
            series: [
              {
                data: newData.map((item) => item.value)
              },
              { data: newData.map((item) => item.value) }
            ]
          })
        } else {
          myChart.setOption({
            yAxis: [
              {
                axisLabel: {
                  show: true,
                  textStyle: {
                    color: '#000000'
                  }
                },
                data: newData.map((item) => item.name)
              },
              {
                axisLabel: {
                  textStyle: {
                    color: '#0000000',
                    fontSize: '12'
                  }
                },
                data: newData.map((item) => item.value)
              }
            ],
            series: [
              {
                data: newData.map((item) => item.value)
              },
              { data: newData.map((item) => item.value) }
            ]
          })
        }
    }
  }
)

//主题切换
watch(
  () => props.theme,
  async (newData) => {
    if (!isSelected) {
      isSelected = true
      await selectLocation(null)
    }
    if (props.theme === 'dark') {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'white', //白色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#24CFF4', '#2E98CA', '#1E62AC'] //蓝色深浅
          },
          emphasis: {
            // areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },

          itemStyle: {
            areaColor: '#8dd7fc', // 区域填充色
            borderColor: '#53D9FF', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: 'rgb(58,115,192)', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          },
          emphasis: {
            areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25,
            label: {
              show: true,
              color: '#f75a00' //深橙色
            }
          }
        },

        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return '#d94e5d'
                  } else if (value > 200) {
                    return '#eac736'
                  } else {
                    return '#f75a00' //橙色
                  }
                }
              }
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    } else {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'black', //橙色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#FFA07A', '#FF7F50', '#7F3600'] //红色深浅
          },
          emphasis: {
            areaColor: 'red', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true,
          textStyle: {
            color: '#0f0d0d' //黑色
          }
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },
          emphasis: {
            label: {
              show: true,
              color: '#7B93A7' //橙色
            }
          },
          itemStyle: {
            // areaColor: '#fdae61', // 区域填充色
            borderColor: '#e0f3f8', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: '#f46d43', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          }
        },
        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return '#FFB84D'
                  } else if (value > 200) {
                    return '#FFD700'
                  } else {
                    return '#FFFFE0'
                  }
                }
              }
            },
            label: {
              show: false,
              position: 'right',
              formatter: function (params) {
                return params.data[2]
              },
              color: '#f1f3f4',
              fontSize: 12
            },
            emphasis: {
              itemStyle: {
                color: '#f75a00'
              }
              // focus: 'self',
              // blurScope: 'series'
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    }
    if (props.theme === 'dark') {
      barOption = {
        // backgroundColor: 'rgb(16, 12, 42)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#ffffff'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#ffffff',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    } else {
      barOption = {
        // backgroundColor: 'rgb(250, 235, 215)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#000000'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#000000',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    }
    if (myChart) {
      myChart.dispose()
      initChart(newData, isMapOption)
    }
  }
)

//图形切换
watch(
  () => props.isMap,
  (newData) => {
    isMapOption = newData
    if (!newData) myChart.setOption(barOption, true)
    else myChart.setOption(mapOption, true)
  }
)

//高亮
watch(
  () => props.highlight,
  (newData) => {
    if (myChart) {
      if (newData !== null) {
        myChart.dispatchAction({
          type: 'downplay',
          seriesIndex: 1
        })
        newData.forEach((item) =>
          myChart.dispatchAction({
            type: 'highlight',
            seriesIndex: 1,
            dataIndex: item
          })
        )
      } else {
        myChart.dispatchAction({
          type: 'downplay',
          seriesIndex: 1
        })
      }
    }
  }
)

const emit = defineEmits(['updataLocation'])
const selectLocation = (Location) => {
  emit('updataLocation', Location)
}

let isMapOption = true
let isSelected = true

// 地图
let mapOption = {
  title: {
    text: '美国地区与裁员的关系',
    textStyle: {
      color: 'black', //橙色
      fontSize: 20,
      fontWeight: 'normal'
    },
    left: 'center',
    top: '10%',
    z: -1
  },
  grid: {
    left: '10%'
  },
  tooltip: {
    trigger: 'item'
  },
  visualMap: {
    left: 'right',
    min: 0,
    max: 15000,
    seriesIndex: [0],
    inRange: {
      color: ['#FFA07A', '#FF7F50', '#7F3600'] //红色深浅
    },
    emphasis: {
      areaColor: 'red', //浅蓝
      borderWidth: 1.6,
      shadowBlur: 25
    },
    text: ['High', 'Low'],
    calculable: true,
    textStyle: {
      color: '#0f0d0d' //黑色
    }
  },
  geo: {
    id: 'geoMap',
    map: 'USA',
    roam: true,
    zoom: 1.2,
    scaleLimit: {
      min: 1,
      max: 5
    },
    emphasis: {
      label: {
        show: true,
        color: '#7B93A7' //橙色
      }
    },
    itemStyle: {
      // areaColor: '#fdae61', // 区域填充色
      borderColor: '#e0f3f8', // 区域边框颜色
      borderWidth: 1.3, // 区域边框宽度
      shadowBlur: 15, // 阴影模糊度
      shadowColor: '#f46d43', // 阴影颜色
      shadowOffsetX: 7, // 阴影 X 方向偏移量
      shadowOffsetY: 6 // 阴影 Y 方向偏移量
    }
  },
  series: [
    {
      name: 'sum',
      type: 'map',
      geoIndex: 0,
      animationDurationUpdate: 1000,
      universalTransition: false,
      data: props.data
    },
    {
      name: 'Points',
      type: 'scatter',
      coordinateSystem: 'geo',
      geoIndex: 0,
      symbolSize: function (val) {
        return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
          ? 1.3 * Math.log(val[2]) + val[2] / 1000
          : 5
      },
      encode: {
        tooltip: [2],
        label: [3] // Assume that index 3 in value array is the name
      },
      rippleEffect: {
        brushType: 'fill'
      },
      itemStyle: {
        normal: {
          color: function (param) {
            const value = param.value[2]
            if (value > 500) {
              return '#FFB84D'
            } else if (value > 200) {
              return '#FFD700'
            } else {
              return '#FFFFE0'
            }
          }
        }
      },
      label: {
        show: false,
        position: 'right',
        formatter: function (params) {
          return params.data[2]
        },
        color: '#f1f3f4',
        fontSize: 12
      },
      emphasis: {
        itemStyle: {
          color: '#f75a00'
        }
        // focus: 'self',
        // blurScope: 'series'
      },
      showEffectOn: 'render',
      data: props.pointData
    }
  ]
}

// 柱状图
let barOption = {
  grid: {
    left: '2%',
    right: '2%',
    bottom: '2%',
    top: '2%',
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'none'
    },
    formatter: function (params) {
      return params[0].name + ' : ' + params[0].value
    }
  },
  xAxis: {
    show: false,
    type: 'value'
  },
  yAxis: [
    {
      type: 'category',
      inverse: true,
      axisLabel: {
        show: true,
        textStyle: {
          color: '#000000'
        }
      },
      splitLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLine: {
        show: false
      },
      data: []
    },
    {
      type: 'category',
      inverse: true,
      axisTick: 'none',
      axisLine: 'none',
      show: true,
      axisLabel: {
        textStyle: {
          color: '#000000',
          fontSize: '12'
        }
      },
      data: []
    }
  ],
  series: [
    {
      name: '值',
      type: 'bar',
      zlevel: 1,
      itemStyle: {
        normal: {
          barBorderRadius: 30,
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            {
              offset: 0,
              color: 'rgb(57,89,255,1)'
            },
            {
              offset: 1,
              color: 'rgb(46,200,207,1)'
            }
          ])
        }
      },
      barWidth: 20,
      data: []
    },
    {
      name: '背景',
      type: 'bar',
      barWidth: 20,
      barGap: '-100%',
      data: [],
      itemStyle: {
        normal: {
          color: 'rgba(24,31,68,1)',
          barBorderRadius: 30
        }
      }
    }
  ]
}

//地图初始化
const initChart = async (theme = 'light', isMap = true) => {
  if (chartContainer.value) {
    myChart = echarts.init(chartContainer.value, theme)
    myChart.showLoading()

    const USAmap = await fetchMapData()

    //地图注册
    echarts.registerMap('USA', USAmap, {
      Alaska: {
        left: -131,
        top: 25,
        width: 15
      },
      Hawaii: {
        left: -110,
        top: 25,
        width: 5
      },
      'Puerto Rico': {
        left: -77,
        top: 26,
        width: 2
      }
    })

    //获取地区中心点
    const geoCoordMap = USAmap.features.reduce((map, feature) => {
      if (
        feature.properties &&
        feature.properties.name &&
        feature.geometry &&
        feature.geometry.coordinates
      ) {
        // 计算中心点（平均值）
        const coordinates = feature.geometry.coordinates
        const allCoords = coordinates.flat(Infinity)
        const longitudes = allCoords.filter((_, index) => index % 2 === 0)
        const latitudes = allCoords.filter((_, index) => index % 2 !== 0)
        const centerLong =
          longitudes.reduce((a, b) => a + b, 0) / longitudes.length
        const centerLat =
          latitudes.reduce((a, b) => a + b, 0) / latitudes.length
        map[feature.properties.name] = [centerLong, centerLat]
      }
      return map
    }, {})

    // 点击选中地区并修改其他图形
    myChart.on('click', function (params) {
      if (params.componentType === 'series' && params.seriesType === 'map') {
        let centerCoord = [0, 0]
        if (params.name === 'Alaska') centerCoord = [-122, 26]
        else if (params.name === 'Hawaii') centerCoord = [-108, 25]
        else if (params.name === 'Puerto Rico') centerCoord = [-76, 26]
        else centerCoord = geoCoordMap[params.name]

        if (isSelected) {
          myChart.setOption({
            geo: { zoom: 5, center: centerCoord, roam: false },
            series: [
              {
                universalTransition: false,
                type: 'map',
                map: 'USA',
                emphasis: {
                  label: {
                    show: true
                  },
                  itemStyle: {
                    areaColor: 'white' // 设置其他地区的颜色为默认值
                  }
                }
              },
              {
                name: 'Points',
                type: 'scatter',
                coordinateSystem: 'geo',
                geoIndex: 0,
                symbolSize: function (val) {
                  return 2.3 * Math.log(val[2]) + val[2] / 200 > 5
                    ? 2.3 * Math.log(val[2]) + val[2] / 200
                    : 5
                }
              }
            ]
          })
          isSelected = false
          selectLocation(params.name)
        } else {
          myChart.setOption({
            geo: { zoom: 1.2, center: null, roam: true },
            series: [
              { series: { universalTransition: true } },
              {
                name: 'Points',
                symbolSize: function (val) {
                  return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                    ? 1.3 * Math.log(val[2]) + val[2] / 1000
                    : 5
                }
              }
            ]
          })
          isSelected = true
          selectLocation(null)
        }
      }
    })

    if (isMap) {
      myChart.setOption(mapOption)
    } else {
      myChart.setOption(barOption)
    }
    myChart.hideLoading()

    // 大小自适应
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

onMounted(() => {
  initChart(props.theme, isMapOption)
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

<template>
  <div ref="chartContainer" class="chart-container"></div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style> -->
<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts/core'
import {
  VisualMapComponent,
  GeoComponent,
  GridComponent
} from 'echarts/components'
import { MapChart, BarChart, ScatterChart } from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import axios from 'axios'

echarts.use([
  VisualMapComponent,
  GeoComponent,
  MapChart,
  CanvasRenderer,
  UniversalTransition,
  ScatterChart,
  BarChart,
  GridComponent
])

const chartContainer = ref(null)
let myChart = null
// const colors = ['#FFFFE0', '#FFD700', '#FFB84D']
const colors1 = [
  '#ff83a2',
  '#FF4500',
  '#B22222',
  '#FF0000',
  '#FFB6C1',
  '#FF69B4'
]

//地图数据获取0
const fetchMapData = async () => {
  const response = await axios.get('/static/USA.json')
  return response.data
}

//数据传入并监听
const props = defineProps({
  pointData: Array,
  data: Array,
  sortData: Array,
  theme: String,
  isMap: Boolean,
  highlight: Array
})

//散点图数据
watch(
  () => props.pointData,
  (newData) => {
    if (myChart) {
      if (isMapOption)
        myChart.setOption({
          series: [
            {
              name: 'Points',
              data: newData
            }
          ]
        })
    }
  }
)

//地图数据
watch(
  () => props.data,
  (newData) => {
    if (props.theme === 'dark') {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'white', //白色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#24CFF4', '#2E98CA', '#1E62AC'] //蓝色深浅
          },
          emphasis: {
            // areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },

          itemStyle: {
            areaColor: '#8dd7fc', // 区域填充色
            borderColor: '#53D9FF', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: 'rgb(58,115,192)', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          },
          emphasis: {
            areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25,
            label: {
              show: true,
              color: '#f75a00' //深橙色
            }
          }
        },

        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return '#d94e5d'
                  } else if (value > 200) {
                    return '#eac736'
                  } else {
                    return '#f75a00' //橙色
                  }
                }
              }
            },
            emphasis: {
              itemStyle: {
                color: colors1[3]
              }
              // focus: 'self',
              // blurScope: 'series'
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    } else {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'black', //橙色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#FFA07A', '#FF7F50', '#7F3600'] //红色深浅
          },
          emphasis: {
            areaColor: 'red', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true,
          textStyle: {
            color: '#0f0d0d' //黑色
          }
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },
          emphasis: {
            label: {
              show: true,
              color: '#7B93A7' //橙色
            }
          },
          itemStyle: {
            // areaColor: '#fdae61', // 区域填充色
            borderColor: '#e0f3f8', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: '#f46d43', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          }
        },
        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return colors1[2]
                  } else if (value > 200) {
                    return colors1[1]
                  } else {
                    return colors1[0]
                  }
                }
              }
            },
            label: {
              show: false,
              position: 'right',
              formatter: function (params) {
                return params.data[2]
              },
              color: '#f1f3f4',
              fontSize: 12
            },
            emphasis: {
              itemStyle: {
                color: colors1[3]
              }
              // focus: 'self',
              // blurScope: 'series'
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    }
    if (myChart) {
      if (isMapOption)
        myChart.setOption({
          series: [
            {
              name: 'sum',
              data: newData
            }
          ]
        })
    }
  }
)

//柱状图数据
watch(
  () => props.sortData,
  (newData) => {
    if (props.theme === 'dark') {
      barOption = {
        // backgroundColor: 'rgb(16, 12, 42)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#ffffff'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#ffffff',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    } else {
      barOption = {
        // backgroundColor: 'rgb(250, 235, 215)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#000000'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#000000',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    }
    if (myChart) {
      if (!isMapOption)
        if (props.theme === 'dark') {
          myChart.setOption({
            yAxis: [
              {
                axisLabel: {
                  show: true,
                  textStyle: {
                    color: '#ffffff'
                  }
                },
                data: newData.map((item) => item.name)
              },
              {
                axisLabel: {
                  textStyle: {
                    color: '#ffffff',
                    fontSize: '12'
                  }
                },
                data: newData.map((item) => item.value)
              }
            ],
            series: [
              {
                data: newData.map((item) => item.value)
              },
              { data: newData.map((item) => item.value) }
            ]
          })
        } else {
          myChart.setOption({
            yAxis: [
              {
                axisLabel: {
                  show: true,
                  textStyle: {
                    color: '#000000'
                  }
                },
                data: newData.map((item) => item.name)
              },
              {
                axisLabel: {
                  textStyle: {
                    color: '#0000000',
                    fontSize: '12'
                  }
                },
                data: newData.map((item) => item.value)
              }
            ],
            series: [
              {
                data: newData.map((item) => item.value)
              },
              { data: newData.map((item) => item.value) }
            ]
          })
        }
    }
  }
)

//主题切换
watch(
  () => props.theme,
  async (newData) => {
    if (!isSelected) {
      isSelected = true
      await selectLocation(null)
    }
    if (props.theme === 'dark') {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'white', //白色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#24CFF4', '#2E98CA', '#1E62AC'] //蓝色深浅
          },
          emphasis: {
            // areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },

          itemStyle: {
            areaColor: '#8dd7fc', // 区域填充色
            borderColor: '#53D9FF', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: 'rgb(58,115,192)', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          },
          emphasis: {
            areaColor: '#8dd7fc', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25,
            label: {
              show: true,
              color: '#f75a00' //深橙色
            }
          }
        },

        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return '#d94e5d'
                  } else if (value > 200) {
                    return '#eac736'
                  } else {
                    return '#f75a00' //橙色
                  }
                }
              }
            },
            emphasis: {
              itemStyle: {
                color: colors1[3]
              }
              // focus: 'self',
              // blurScope: 'series'
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    } else {
      mapOption = {
        title: {
          text: '美国地区与裁员的关系',
          textStyle: {
            color: 'black', //橙色
            fontSize: 20,
            fontWeight: 'normal'
          },
          left: 'center',
          top: '10%',
          z: -1
        },
        grid: {
          left: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        visualMap: {
          left: 'right',
          min: 0,
          max: 15000,
          seriesIndex: [0],
          inRange: {
            color: ['#FFA07A', '#FF7F50', '#7F3600'] //红色深浅
          },
          emphasis: {
            areaColor: 'red', //浅蓝
            borderWidth: 1.6,
            shadowBlur: 25
          },
          text: ['High', 'Low'],
          calculable: true,
          textStyle: {
            color: '#0f0d0d' //黑色
          }
        },
        geo: {
          id: 'geoMap',
          map: 'USA',
          roam: true,
          zoom: 1.2,
          scaleLimit: {
            min: 1,
            max: 5
          },
          emphasis: {
            label: {
              show: true,
              color: '#7B93A7' //橙色
            }
          },
          itemStyle: {
            // areaColor: '#fdae61', // 区域填充色
            borderColor: '#e0f3f8', // 区域边框颜色
            borderWidth: 1.3, // 区域边框宽度
            shadowBlur: 15, // 阴影模糊度
            shadowColor: '#f46d43', // 阴影颜色
            shadowOffsetX: 7, // 阴影 X 方向偏移量
            shadowOffsetY: 6 // 阴影 Y 方向偏移量
          }
        },
        series: [
          {
            name: 'sum',
            type: 'map',
            geoIndex: 0,
            animationDurationUpdate: 1000,
            universalTransition: false,
            data: props.data
          },
          {
            name: 'Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: function (val) {
              return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                ? 1.3 * Math.log(val[2]) + val[2] / 1000
                : 5
            },
            encode: {
              tooltip: [2],
              label: [3] // Assume that index 3 in value array is the name
            },
            rippleEffect: {
              brushType: 'fill'
            },
            itemStyle: {
              normal: {
                color: function (param) {
                  const value = param.value[2]
                  if (value > 500) {
                    return colors1[2]
                  } else if (value > 200) {
                    return colors1[1]
                  } else {
                    return colors1[0]
                  }
                }
              }
            },
            label: {
              show: false,
              position: 'right',
              formatter: function (params) {
                return params.data[2]
              },
              color: '#f1f3f4',
              fontSize: 12
            },
            emphasis: {
              itemStyle: {
                color: colors1[3]
              }
              // focus: 'self',
              // blurScope: 'series'
            },
            showEffectOn: 'render',
            data: props.pointData
          }
        ]
      }
    }
    if (props.theme === 'dark') {
      barOption = {
        // backgroundColor: 'rgb(16, 12, 42)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#ffffff'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#ffffff',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    } else {
      barOption = {
        // backgroundColor: 'rgb(250, 235, 215)',
        grid: {
          left: '2%',
          right: '2%',
          bottom: '2%',
          top: '2%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'none'
          },
          formatter: function (params) {
            return params[0].name + ' : ' + params[0].value
          }
        },
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: [
          {
            type: 'category',
            inverse: true,
            axisLabel: {
              show: true,
              textStyle: {
                color: '#000000'
              }
            },
            splitLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            data: props.sortData.map((item) => item.name)
          },
          {
            type: 'category',
            inverse: true,
            axisTick: 'none',
            axisLine: 'none',
            show: true,
            axisLabel: {
              textStyle: {
                color: '#000000',
                fontSize: '12'
              }
            },
            data: props.sortData.map((item) => item.value)
          }
        ],
        series: [
          {
            name: '值',
            type: 'bar',
            zlevel: 1,
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  {
                    offset: 0,
                    color: 'rgb(57,89,255,1)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(46,200,207,1)'
                  }
                ])
              }
            },
            barWidth: 20,
            data: props.sortData.map((item) => item.value)
          },
          {
            name: '背景',
            type: 'bar',
            barWidth: 20,
            barGap: '-100%',
            data: props.sortData.map((item) => item.value),
            itemStyle: {
              normal: {
                color: 'rgba(24,31,68,1)',
                barBorderRadius: 30
              }
            }
          }
        ]
      }
    }
    if (myChart) {
      myChart.dispose()
      initChart(newData, isMapOption)
    }
  }
)

//图形切换
watch(
  () => props.isMap,
  (newData) => {
    isMapOption = newData
    if (!newData) myChart.setOption(barOption, true)
    else myChart.setOption(mapOption, true)
  }
)

//高亮
watch(
  () => props.highlight,
  (newData) => {
    if (myChart) {
      if (newData !== null) {
        myChart.dispatchAction({
          type: 'downplay',
          seriesIndex: 1
        })
        newData.forEach((item) =>
          myChart.dispatchAction({
            type: 'highlight',
            seriesIndex: 1,
            dataIndex: item
          })
        )
      } else {
        myChart.dispatchAction({
          type: 'downplay',
          seriesIndex: 1
        })
      }
    }
  }
)

const emit = defineEmits(['updataLocation'])
const selectLocation = (Location) => {
  emit('updataLocation', Location)
}

let isMapOption = true
let isSelected = true

// 地图
let mapOption = {
  title: {
    text: '美国地区与裁员的关系',
    textStyle: {
      color: 'black', //橙色
      fontSize: 20,
      fontWeight: 'normal'
    },
    left: 'center',
    top: '10%',
    z: -1
  },
  grid: {
    left: '10%'
  },
  tooltip: {
    trigger: 'item'
  },
  visualMap: {
    left: 'right',
    min: 0,
    max: 15000,
    seriesIndex: [0],
    inRange: {
      color: ['#FFA07A', '#FF7F50', '#7F3600'] //红色深浅
    },
    emphasis: {
      areaColor: 'red', //浅蓝
      borderWidth: 1.6,
      shadowBlur: 25
    },
    text: ['High', 'Low'],
    calculable: true,
    textStyle: {
      color: '#0f0d0d' //黑色
    }
  },
  geo: {
    id: 'geoMap',
    map: 'USA',
    roam: true,
    zoom: 1.2,
    scaleLimit: {
      min: 1,
      max: 5
    },
    emphasis: {
      label: {
        show: true,
        color: '#7B93A7' //橙色
      }
    },
    itemStyle: {
      // areaColor: '#fdae61', // 区域填充色
      borderColor: '#e0f3f8', // 区域边框颜色
      borderWidth: 1.3, // 区域边框宽度
      shadowBlur: 15, // 阴影模糊度
      shadowColor: '#f46d43', // 阴影颜色
      shadowOffsetX: 7, // 阴影 X 方向偏移量
      shadowOffsetY: 6 // 阴影 Y 方向偏移量
    }
  },
  series: [
    {
      name: 'sum',
      type: 'map',
      geoIndex: 0,
      animationDurationUpdate: 1000,
      universalTransition: false,
      data: props.data
    },
    {
      name: 'Points',
      type: 'scatter',
      coordinateSystem: 'geo',
      geoIndex: 0,
      symbolSize: function (val) {
        return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
          ? 1.3 * Math.log(val[2]) + val[2] / 1000
          : 5
      },
      encode: {
        tooltip: [2],
        label: [3] // Assume that index 3 in value array is the name
      },
      rippleEffect: {
        brushType: 'fill'
      },

      itemStyle: {
        normal: {
          color: function (param) {
            const value = param.value[2]
            if (value > 500) {
              return colors1[2] // '#FFB84D'
            } else if (value > 200) {
              return colors1[1] // '#FFD700'
            } else {
              return colors1[0] // '#FFFFE0'
            }
          }
        }
      },

      label: {
        show: false,
        position: 'right',
        formatter: function (params) {
          return params.data[2]
        },
        color: '#f1f3f4',
        fontSize: 12
      },
      emphasis: {
        itemStyle: {
          color: colors1[3]
        }
        // focus: 'self',
        // blurScope: 'series'
      },
      showEffectOn: 'render',
      data: props.pointData
    }
  ]
}

// 柱状图
let barOption = {
  grid: {
    left: '2%',
    right: '2%',
    bottom: '2%',
    top: '2%',
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'none'
    },
    formatter: function (params) {
      return params[0].name + ' : ' + params[0].value
    }
  },
  xAxis: {
    show: false,
    type: 'value'
  },
  yAxis: [
    {
      type: 'category',
      inverse: true,
      axisLabel: {
        show: true,
        textStyle: {
          color: '#000000'
        }
      },
      splitLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLine: {
        show: false
      },
      data: []
    },
    {
      type: 'category',
      inverse: true,
      axisTick: 'none',
      axisLine: 'none',
      show: true,
      axisLabel: {
        textStyle: {
          color: '#000000',
          fontSize: '12'
        }
      },
      data: []
    }
  ],
  series: [
    {
      name: '值',
      type: 'bar',
      zlevel: 1,
      itemStyle: {
        normal: {
          barBorderRadius: 30,
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            {
              offset: 0,
              color: 'rgb(57,89,255,1)'
            },
            {
              offset: 1,
              color: 'rgb(46,200,207,1)'
            }
          ])
        }
      },
      barWidth: 20,
      data: []
    },
    {
      name: '背景',
      type: 'bar',
      barWidth: 20,
      barGap: '-100%',
      data: [],
      itemStyle: {
        normal: {
          color: 'rgba(24,31,68,1)',
          barBorderRadius: 30
        }
      }
    }
  ]
}

//地图初始化
const initChart = async (theme = 'light', isMap = true) => {
  if (chartContainer.value) {
    myChart = echarts.init(chartContainer.value, theme)
    myChart.showLoading()

    const USAmap = await fetchMapData()

    //地图注册
    echarts.registerMap('USA', USAmap, {
      Alaska: {
        left: -131,
        top: 25,
        width: 15
      },
      Hawaii: {
        left: -110,
        top: 25,
        width: 5
      },
      'Puerto Rico': {
        left: -77,
        top: 26,
        width: 2
      }
    })

    //获取地区中心点
    const geoCoordMap = USAmap.features.reduce((map, feature) => {
      if (
        feature.properties &&
        feature.properties.name &&
        feature.geometry &&
        feature.geometry.coordinates
      ) {
        // 计算中心点（平均值）
        const coordinates = feature.geometry.coordinates
        const allCoords = coordinates.flat(Infinity)
        const longitudes = allCoords.filter((_, index) => index % 2 === 0)
        const latitudes = allCoords.filter((_, index) => index % 2 !== 0)
        const centerLong =
          longitudes.reduce((a, b) => a + b, 0) / longitudes.length
        const centerLat =
          latitudes.reduce((a, b) => a + b, 0) / latitudes.length
        map[feature.properties.name] = [centerLong, centerLat]
      }
      return map
    }, {})

    // 点击选中地区并修改其他图形
    myChart.on('click', function (params) {
      if (params.componentType === 'series' && params.seriesType === 'map') {
        let centerCoord = [0, 0]
        if (params.name === 'Alaska') centerCoord = [-122, 26]
        else if (params.name === 'Hawaii') centerCoord = [-108, 25]
        else if (params.name === 'Puerto Rico') centerCoord = [-76, 26]
        else centerCoord = geoCoordMap[params.name]

        if (isSelected) {
          myChart.setOption({
            geo: { zoom: 5, center: centerCoord, roam: false },
            series: [
              {
                universalTransition: false,
                type: 'map',
                map: 'USA',
                emphasis: {
                  label: {
                    show: true
                  },
                  itemStyle: {
                    areaColor: 'white' // 设置其他地区的颜色为默认值
                  }
                }
              },
              {
                name: 'Points',
                type: 'scatter',
                coordinateSystem: 'geo',
                geoIndex: 0,
                symbolSize: function (val) {
                  return 2.3 * Math.log(val[2]) + val[2] / 200 > 5
                    ? 2.3 * Math.log(val[2]) + val[2] / 200
                    : 5
                }
              }
            ]
          })
          isSelected = false
          selectLocation(params.name)
        } else {
          myChart.setOption({
            geo: { zoom: 1.2, center: null, roam: true },
            series: [
              { series: { universalTransition: true } },
              {
                name: 'Points',
                symbolSize: function (val) {
                  return 1.3 * Math.log(val[2]) + val[2] / 1000 > 5
                    ? 1.3 * Math.log(val[2]) + val[2] / 1000
                    : 5
                }
              }
            ]
          })
          isSelected = true
          selectLocation(null)
        }
      }
    })

    if (isMap) {
      myChart.setOption(mapOption)
    } else {
      myChart.setOption(barOption)
    }
    myChart.hideLoading()

    // 大小自适应
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

onMounted(() => {
  initChart(props.theme, isMapOption)
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

<template>
  <div ref="chartContainer" class="chart-container"></div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style>
