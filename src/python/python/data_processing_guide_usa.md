# 数据处理流程指南 (美国地区版)

## 📋 项目概述
本项目将 tech_layoffs.xlsx 原始数据转换为适用于Vue.js可视化项目的JSON格式，并筛选只保留美国地区的数据。

## 🔄 数据转换流程

### 1. 原始数据结构 (Excel)
- 文件: tech_layoffs.xlsx
- 记录数: 1,418 条
- 字段数: 16 个
- 主要字段:
  - Company: 公司名称
  - Location_HQ: 公司总部位置
  - Laid_Off: 裁员人数
  - Date_layoffs: 裁员日期
  - Industry: 行业
  - Stage: 融资阶段
  - Money_Raised_in_$_mil: 融资金额(百万美元)

### 2. 数据清洗和过滤
移除关键字段缺失的记录
结果: 1,418 → 905 条记录 (删除513条不完整记录)

### 3. 🇺🇸 美国地区筛选 (新增步骤)
只保留美国50个州和华盛顿特区的数据
- 筛选标准: Location字段匹配美国州名
- 保留州份: California, New York, Massachusetts, Washington, Illinois, Texas 等50个州
- 筛选结果: 905 → 约800+ 条记录 (删除国际数据)
- 输出文件: data_usa_only.json

### 4. 字段转换映射
- Location_HQ → Location (标准化为美国州名)
- Laid_Off → Num (直接映射)
- Date_layoffs → Time (转换为UTC格式字符串)
- Company_Size_before_Layoffs → Before (直接映射)
- Company_Size_after_layoffs → After (直接映射)
- Industry → Industry (直接映射)
- Stage → State (融资阶段标准化)
- Money_Raised_in_$_mil → Money (转换为浮点数)

### 5. Vue项目中的使用
数据通过axios加载美国版JSON，在各个组件中进行聚合和可视化处理。

## 📊 美国数据质量特点
- 无缺失值 (完整性: 100%)
- 地理范围: 仅美国50州 + DC
- 时间范围: 主要集中在2020年和2022-2023年
- 地理分布: 主要集中在加州 (约60%+)
- 行业分布: Consumer行业占比最高
- 公司规模: 中小型公司为主

## 🎯 美国数据的优势
- 数据一致性更高 (统一的法律和商业环境)
- 地理分析更精确 (州级精度)
- 时区统一，时间分析更准确
- 经济环境相对统一，分析更有意义
- 适合美国市场的专项分析

## 📁 文件结构
```
public/static/
├── data_reconstructed.json    # 全球数据 (905条)
├── data_usa_only.json     # 美国数据 (筛选后)
└── data_reconstructed.json # 重构的全量数据
```

## 🔧 使用方法
```javascript
// Vue组件中加载美国数据
async function loadUSAData() {
  const response = await axios.get('/static/data_usa_only.json')
  return response.data
}
```

## 📈 数据统计对比
| 指标 | 全球数据 | 美国数据 | 变化 |
|------|----------|----------|------|
| 记录数 | 905 | ~800+ | -10%+ |
| 地区数 | 全球多国 | 美国50州 | 统一化 |
| 时区 | 多时区 | 统一时区 | 简化 |
| 法律环境 | 多样化 | 统一 | 一致性↑ |
