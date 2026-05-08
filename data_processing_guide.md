# 数据处理流程指南

## 📋 项目概述
本项目将 tech_layoffs.xlsx 原始数据转换为适用于Vue.js可视化项目的JSON格式。

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

### 3. 字段转换映射
- Location_HQ → Location (标准化为州/国家名称)
- Laid_Off → Num (直接映射)
- Date_layoffs → Time (转换为UTC格式字符串)
- Company_Size_before_Layoffs → Before (直接映射)
- Company_Size_after_layoffs → After (直接映射)
- Industry → Industry (直接映射)
- Stage → State (融资阶段标准化)
- Money_Raised_in_$_mil → Money (转换为浮点数)

### 4. Vue项目中的使用
数据通过axios加载，在各个组件中进行聚合和可视化处理。

## 📊 数据质量特点
- 无缺失值 (完整性: 100%)
- 时间范围: 主要集中在2020年和2022-2023年
- 地理分布: 主要集中在加州 (50.6%)
- 行业分布: Consumer行业占比最高 (24.1%)
- 公司规模: 中小型公司为主 (平均裁员303人)
