import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_simple_demo():
    """创建简单的可视化演示"""
    
    # 加载数据
    try:
        with open('public/static/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print("成功加载真实数据")
    except:
        print("使用示例数据")
        # 创建示例数据
        np.random.seed(42)
        industries = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Retail']
        states = ['Seed', 'Series A', 'Series B', 'Series C', 'Post-IPO']
        
        df = pd.DataFrame({
            'Industry': np.random.choice(industries, 100),
            'State': np.random.choice(states, 100),
            'Num': np.random.randint(10, 1000, 100),
            'Location': np.random.choice(['California', 'New York', 'Texas'], 100)
        })
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Vue项目图表的Python实现示例', fontsize=16, fontweight='bold')
    
    # 1. 柱状图 - 对应ChartBar.vue
    state_data = df.groupby('State')['Num'].sum()
    axes[0,0].bar(state_data.index, state_data.values, color='skyblue', alpha=0.7)
    axes[0,0].set_title('融资阶段与裁员关系 (ChartBar.vue)')
    axes[0,0].set_ylabel('裁员人数')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. 饼图 - 对应ChartCircle.vue
    industry_data = df.groupby('Industry')['Num'].sum()
    axes[0,1].pie(industry_data.values, labels=industry_data.index, autopct='%1.1f%%')
    axes[0,1].set_title('行业与裁员关系 (ChartCircle.vue)')
    
    # 3. 水平条形图 - 对应ChartLine.vue
    location_data = df.groupby('Location')['Num'].sum().sort_values()
    axes[1,0].barh(location_data.index, location_data.values, color='lightcoral', alpha=0.7)
    axes[1,0].set_title('地区与裁员关系 (ChartLine.vue)')
    axes[1,0].set_xlabel('裁员人数')
    
    # 4. 散点图 - 对应ChartMap.vue的散点部分
    if 'lng' in df.columns and 'lat' in df.columns:
        scatter = axes[1,1].scatter(df['lng'], df['lat'], s=df['Num']/10, 
                                  c=df['Num'], cmap='viridis', alpha=0.6)
        axes[1,1].set_title('地理位置散点图 (ChartMap.vue)')
        axes[1,1].set_xlabel('经度')
        axes[1,1].set_ylabel('纬度')
        plt.colorbar(scatter, ax=axes[1,1])
    else:
        # 如果没有地理数据，显示简单的散点图
        axes[1,1].scatter(range(len(df)), df['Num'], alpha=0.6)
        axes[1,1].set_title('数据散点图')
        axes[1,1].set_xlabel('数据点')
        axes[1,1].set_ylabel('裁员人数')
    
    plt.tight_layout()
    plt.show()
    
    # 显示结论
    print("\n" + "="*60)
    print("结论：各Python库对Vue项目图表的支持情况")
    print("="*60)
    print("1. ChartBar.vue (柱状图):")
    print("   ✅ Matplotlib: 完全支持")
    print("   ✅ Seaborn: 支持，样式更美观")
    print("   ❌ Mayavi: 不适合2D图表")
    
    print("\n2. ChartCircle.vue (饼图/玫瑰图):")
    print("   ✅ Matplotlib: 支持饼图，玫瑰图需自定义")
    print("   ❌ Seaborn: 不直接支持饼图")
    print("   ❌ Mayavi: 不适合2D图表")
    
    print("\n3. ChartLine.vue (条形图):")
    print("   ✅ Matplotlib: 完全支持")
    print("   ✅ Seaborn: 支持，样式丰富")
    print("   ❌ Mayavi: 不适合")
    
    print("\n4. ChartMap.vue (地图+散点图):")
    print("   ⚠️ Matplotlib: 散点图支持，地图需额外库(basemap/cartopy)")
    print("   ❌ Seaborn: 不支持地图")
    print("   ✅ Mayavi: 可以做3D地理可视化")
    
    print("\n5. scatter.vue (气泡散点图):")
    print("   ✅ Matplotlib: 完全支持")
    print("   ✅ Seaborn: 支持")
    print("   ✅ Mayavi: 可以创建3D气泡效果")
    
    print("\n" + "="*60)
    print("推荐方案:")
    print("="*60)
    print("🥇 首选: Matplotlib - 最全面，可实现80%的图表")
    print("🥈 配合: Seaborn - 统计图表，样式美观")
    print("🥉 特殊: Mayavi - 3D可视化需求")
    print("💡 地图: 考虑Folium、Plotly或Basemap")

if __name__ == "__main__":
    create_simple_demo()
