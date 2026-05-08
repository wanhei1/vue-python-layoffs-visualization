import pandas as pd
import json

def analyze_data_transformation():
    """分析tech_layoffs.xlsx到data.json的数据转换过程"""
    
    print("📊 数据转换分析报告")
    print("="*60)
    
    # 1. 读取原始Excel文件
    try:
        print("\n1. 📁 读取原始Excel文件...")
        df_excel = pd.read_excel('tech_layoffs.xlsx')
        print("✅ Excel文件读取成功")
        print(f"   - 数据行数: {len(df_excel)}")
        print(f"   - 数据列数: {len(df_excel.columns)}")
        print(f"   - 列名: {list(df_excel.columns)}")
        
        # 显示前几行数据
        print("\n📋 Excel文件前5行数据:")
        print(df_excel.head())
        
        # 数据类型信息
        print("\n🔍 Excel数据类型:")
        print(df_excel.dtypes)
        
    except Exception as e:
        print(f"❌ Excel文件读取失败: {e}")
        return
    
    # 2. 读取处理后的JSON文件
    try:
        print("\n2. 📁 读取处理后的JSON文件...")
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
        
        df_json = pd.DataFrame(data_json)
        print("✅ JSON文件读取成功")
        print(f"   - 数据行数: {len(df_json)}")
        print(f"   - 数据列数: {len(df_json.columns)}")
        print(f"   - 列名: {list(df_json.columns)}")
        
        # 显示前几行数据
        print("\n📋 JSON文件前5行数据:")
        print(df_json.head())
        
        # 数据类型信息
        print("\n🔍 JSON数据类型:")
        print(df_json.dtypes)
        
    except Exception as e:
        print(f"❌ JSON文件读取失败: {e}")
        return
    
    # 3. 对比分析
    print("\n3. 🔄 数据转换对比分析")
    print("="*40)
    
    print("📈 数据量对比:")
    print(f"   Excel原始数据: {len(df_excel)} 行")
    print(f"   JSON处理数据: {len(df_json)} 行")
    print(f"   数据变化: {len(df_json) - len(df_excel)} 行")
    
    print("\n📊 字段对比:")
    excel_cols = set(df_excel.columns)
    json_cols = set(df_json.columns)
    
    print(f"   Excel字段: {excel_cols}")
    print(f"   JSON字段: {json_cols}")
    print(f"   新增字段: {json_cols - excel_cols}")
    print(f"   删除字段: {excel_cols - json_cols}")
    print(f"   保留字段: {excel_cols & json_cols}")
    
    # 4. 关键字段分析
    print("\n4. 🎯 关键字段数据分析")
    print("="*40)
    
    # 分析Industry字段
    if 'Industry' in df_json.columns:
        print("\n🏭 行业分布分析 (JSON数据):")
        industry_counts = df_json['Industry'].value_counts()
        print(industry_counts.head(10))
        
        print("\n💼 行业裁员总数分析:")
        if 'Num' in df_json.columns:
            industry_layoffs = df_json.groupby('Industry')['Num'].sum().sort_values(ascending=False)
            print(industry_layoffs.head(10))
    
    # 分析时间字段
    if 'Time' in df_json.columns:
        print("\n📅 时间分布分析:")
        df_json['Time'] = pd.to_datetime(df_json['Time'])
        time_counts = df_json['Time'].dt.date.value_counts().head(10)
        print(time_counts)
    
    # 分析地理位置
    if 'Location' in df_json.columns:
        print("\n🌍 地理位置分析:")
        location_counts = df_json['Location'].value_counts().head(10)
        print(location_counts)
    
    # 5. 数据质量检查
    print("\n5. ✅ 数据质量检查")
    print("="*40)
    
    print("📋 JSON数据缺失值统计:")
    missing_data = df_json.isnull().sum()
    print(missing_data[missing_data > 0])
    
    print("\n📊 数值字段统计:")
    if 'Num' in df_json.columns:
        print("裁员人数统计:")
        print(df_json['Num'].describe())
    
    if 'Money' in df_json.columns:
        print("\n资金统计:")
        print(df_json['Money'].describe())
    
    # 6. 推断数据处理流程
    print("\n6. 🔧 推断的数据处理流程")
    print("="*40)
    
    print("📝 可能的处理步骤:")
    print("   1. 使用pandas读取Excel文件")
    print("   2. 数据清洗和标准化")
    print("   3. 字段重命名和格式转换")
    print("   4. 时间字段标准化为UTC格式")
    print("   5. 导出为JSON格式供Vue项目使用")
    
    return df_excel, df_json

if __name__ == "__main__":
    df_excel, df_json = analyze_data_transformation()
