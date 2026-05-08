<script setup>
import ChartMap from '../components/ChartMap.vue'
import ChartLine from '../components/ChartLine.vue'
import ChartCircle from '../components/ChartCircle.vue'
import ChartBar from '../components/ChartBar.vue'

import axios from 'axios'
import { onMounted, ref, watch } from 'vue'

//数据获取
let data = null
const fetchData = async () => {
  const response = await axios.get('/static/data.json')
  return response.data
}

//地图数据获取
const locationData = ref([])
const locationNum = (data) => {
  const totals = {}
  data.forEach((item) => {
    if (totals[item.Location]) {
      totals[item.Location] += item.Num
    } else {
      totals[item.Location] = item.Num
    }
  })
  return Object.keys(totals).map((location) => ({
    name: location,
    value: totals[location]
  }))
}
const locationSortData = ref([])
const pointData = ref([])
const highlightData = ref([])

//分类数据获取
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

//融资阶段数据获取
const stateData = ref([])
const stateNum = (data) => {
  const totals = {}
  const totalsBefore = {}
  data.forEach((item) => {
    if (/^Series\s/.test(item.State)) {
      if (totals['Series A-Z']) {
        totals['Series A-Z'] += item.Num
        totalsBefore['Series A-Z'] += item.Before
      } else {
        totals['Series A-Z'] = item.Num
        totalsBefore['Series A-Z'] = item.Before
      }
    } else if (totals[item.State]) {
      totals[item.State] += item.Num
      totalsBefore[item.State] += item.Before
    } else {
      totals[item.State] = item.Num
      totalsBefore[item.State] = item.Before
    }
  })
  return Object.keys(totals).map((State) => ({
    name: State,
    value: totals[State],
    valueBefore: totalsBefore[State]
  }))
}

//公司规模数据获取
const scaleData = ref([])
const scaleNum = (data) => {
  const totals = {}

  data.forEach((item) => {
    const groupLabel = item.level
    if (groupLabel) {
      if (!totals[groupLabel]) {
        totals[groupLabel] = {
          Num: 0,
          Before: 0,
          Money: 0,
          count: 0,
          scale: ''
        }
      }
      totals[groupLabel].Num += item.Num
      totals[groupLabel].Before += item.Before
      totals[groupLabel].Money += item.Money
      totals[groupLabel].count += 1
      totals[groupLabel].scale = item.Scale
    }
  })

  return Object.keys(totals).map((groupLabel) => {
    const group = totals[groupLabel]
    return {
      name: groupLabel,
      Num: group.Num,
      Before: group.Before,
      value: (group.Num / group.Before) * 100,
      mean_money: group.Money / group.count,
      mean_num: group.Num / group.count,
      count: group.count,
      scale: group.scale
    }
  })
}

//年份选择
const options = [
  {
    value: 2020,
    label: 2020
  },
  {
    value: 2021,
    label: 2021
  },
  {
    value: 2022,
    label: 2022
  },
  {
    value: 2023,
    label: 2023
  },
  {
    value: 2024,
    label: 2024
  }
]
const year = ref([2020, 2021, 2022, 2023, 2024])

//监听年份变化
watch(year, (newYears) => {
  let tempData = data.filter((item) => newYears.includes(item.Year))
  if (selectLocation !== null) {
    tempData = tempData.filter((item) => item.Location === selectLocation)
    changData(tempData)
  }
  changData(tempData)
})

//改变主题
const themeText = ref('Theme : light')
let theme = ref('light')
const changeTheme = () => {
  if (theme.value === 'light') {
    theme.value = 'dark'
    themeText.value = 'Theme : dark'
  } else {
    theme.value = 'light'
    themeText.value = 'Theme : light'
  }
}

//改变地图
const mapText = ref('图形切换：地图')
let isMap = ref(true)
const changeMap = () => {
  isMap.value = !isMap.value
  if (!isMap.value) mapText.value = '图形切换：柱状图'
  else {
    mapText.value = '图形切换：地图'
    updataLocation(null)
  }
}

//改变数据
const changData = (data) => {
  locationData.value = locationNum(data)
  industryData.value = industryNum(data)
  stateData.value = stateNum(data)
  scaleData.value = scaleNum(data)
  if (!selectLocation) {
    locationSortData.value = locationData.value
      .sort((a, b) => b.value - a.value)
      .slice(0, 20)
  } else {
    locationSortData.value = data
      .sort((a, b) => b.Num - a.Num)
      .slice(0, 20)
      .map((item) => ({
        name: item.Company + '-' + item.Year,
        value: item.Num
      }))
  }
  pointData.value = data.map((item) => ({
    name: item.Company + '-' + item.Year,
    value: [item.lng, item.lat, item.Num]
  }))
}

//选中州
let tempData = null
let selectLocation = null
const updataLocation = (Location) => {
  if (Location) {
    selectLocation = Location
    tempData = data.filter(
      (item) => item.Location === Location && year.value.includes(item.Year)
    )
    changData(tempData)
  } else {
    selectLocation = null
    changData(data)
  }
}

//融资阶段高亮数据获取
const stateHighLight = (type) => {
  if (type) {
    if (!selectLocation) {
      const update = []
      if (type === 'Series A-Z') {
        data.forEach((item, index) => {
          if (/^Series\s/.test(item.State)) {
            update.push(index)
          }
        })
      } else {
        data.forEach((item, index) => {
          if (item.State == type) {
            update.push(index)
          }
        })
      }
      highlightData.value = update
    } else {
      const update = []
      if (type === 'Series A-Z') {
        tempData.forEach((item, index) => {
          if (/^Series\s/.test(item.State)) {
            update.push(index)
          }
        })
      } else {
        tempData.forEach((item, index) => {
          if (item.State == type) {
            update.push(index)
          }
        })
      }
      highlightData.value = update
    }
  } else {
    highlightData.value = null
  }
}

//行业高亮数据获取
const industryHighLight = (type) => {
  if (type) {
    if (!selectLocation) {
      const update = []
      data.forEach((item, index) => {
        if (item.Industry == type) {
          update.push(index)
        }
      })
      highlightData.value = update
    } else {
      const update = []
      tempData.forEach((item, index) => {
        if (item.Industry == type) {
          update.push(index)
        }
      })
      highlightData.value = update
    }
  } else {
    highlightData.value = null
  }
}

//公司规模高亮数据获取
const scaleHighLight = (type) => {
  if (type) {
    if (!selectLocation) {
      const update = []
      data.forEach((item, index) => {
        if (item.level == type) {
          update.push(index)
        }
      })
      highlightData.value = update
    } else {
      const update = []
      tempData.forEach((item, index) => {
        if (item.level == type) {
          update.push(index)
        }
      })
      highlightData.value = update
    }
  } else {
    highlightData.value = null
  }
}

//数据初始化
onMounted(async () => {
  data = await fetchData()
  changData(data)
})
</script>

<template>
  <!--change-->
  <div :class="[theme]">
    <div class="home">
      <el-row class="header">
        <div class="font">年份选择：</div>
        <el-col :span="3" :offset="2" class="title">
          <el-select
            v-model="year"
            multiple
            collapse-tags
            placeholder="年份"
            style="width: 150px"
          >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="6" :offset="4" class="title">
          <span>美国科技公司裁员可视化</span>
        </el-col>
        <el-col :span="2" :offset="1" class="title">
          <el-button @click="changeTheme" round>
            {{ themeText }}
          </el-button>
        </el-col>
        <el-col :span="3" class="title">
          <el-button @click="changeMap" round>
            {{ mapText }}
          </el-button>
        </el-col>
        <el-col :span="2" class="title">
          <el-button @click="$router.push('/scatter')" round>
            页面切换：散点图
          </el-button>
        </el-col>
      </el-row>
      <el-row class="body">
        <el-col :span="12" class="map">
          <ChartMap
            :data="locationData"
            :sortData="locationSortData"
            :pointData="pointData"
            :theme="theme"
            :isMap="isMap"
            :highlight="highlightData"
            @updataLocation="updataLocation"
          />
        </el-col>
        <el-col :span="12">
          <el-row>
            <el-col :span="12" class="pic1">
              <ChartBar
                :data="stateData"
                :theme="theme"
                @stateHighLight="stateHighLight"
              />
            </el-col>
            <el-col :span="12" class="pic1">
              <ChartCircle
                :data="industryData"
                :theme="theme"
                @industryHighLight="industryHighLight"
              />
            </el-col>
          </el-row>
          <el-row class="pic2">
            <ChartLine
              :data="scaleData"
              :theme="theme"
              @scaleHighLight="scaleHighLight"
            />
          </el-row>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style lang="less" scoped>
.header {
  height: 10vh;
  width: 100%;
  /*change*/
  background-color: var(--header-bg-color);
  .font {
    position: fixed;
    font-size: 1.1vw;
    top: 3px;
    left: 4vw;
    line-height: 10vh;
    color: var(--header-text-color);
  }
  .title {
    text-align: center;
    font-size: 2vw;
    line-height: 10vh;
    /*change*/
    color: var(--header-text-color);
  }
}

/*change*/
:root {
  --header-bg-color: #ffffff;
  --header-text-color: #000000;
}

.dark {
  --header-bg-color: #100c2a;
  --header-text-color: #ffffff;
}

.home {
  height: 100vh;
  background-color: antiquewhite;
  .header {
    height: 10vh;
  }

  .body {
    height: 90vh;
  }

  .map {
    .echarts-map {
      width: 50vw;
      height: 90vh;
    }
  }

  .pic1 {
    height: 55vh;
  }

  .pic2 {
    height: 35vh;
  }
}
</style>
