import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体，确保图表中的中文显示正常
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def create_exact_rose_chart_from_image():
    """
    创建与提供图片样式完全匹配的南丁格尔玫瑰图。
    该函数通过硬编码数据和精确的样式调整来实现对原图的复制。
    """
    
    # 1. 硬编码数据和顺序：
    # 按照原图的顺时针方向，从右上方的“能源”开始，列出所有行业及其估算值。
    # 这些数值是根据原图扇形区域的相对大小估算得出的。
    ordered_industries_and_values = [
        ('Energy', 650),        
        ('Transportation', 750),
        ('Finance', 800),       
        ('Healthcare', 700),    
        ('Retail', 600),        
        ('Other', 200),         
        ('AI', 1100),           
        ('Travel', 900),        
        ('Food', 180),          
        ('Data', 160),          
        ('HR', 150),            
        ('Hardware', 140),      
        ('Logistics', 130),     
        ('Sales', 120),         
        ('Recruiting', 100),    
        ('Education', 1000),    
        ('Crypto', 200),        
        ('Consumer', 1500),     
        ('Product', 300),       
        ('Marketing', 1200),    
        ('Security', 250),      
        ('Media', 200),         
        ('Manuf...', 180),      
        ('Real Es...', 160),    
        ('Aerospace', 140),     
        ('Infrastru...', 130),  
        ('Support', 110),       
        ('Fitness', 100),       
        ('Legal', 150),         
        ('Construction', 120),  
    ]
    
    # 将数据转换为DataFrame
    df = pd.DataFrame(ordered_industries_and_values, columns=['Industry', 'Num'])
    
    industries = df['Industry'].tolist()
    values = df['Num'].to_numpy()
    n_sectors = len(industries)

    # 2. 创建图表和极坐标子图
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='polar')
    
    # 角度计算
    # `theta` 数组定义了每个扇形的起始角度。`endpoint=False` 确保不会有重复的 2*pi。
    theta = np.linspace(0, 2*np.pi, n_sectors, endpoint=False) 
    width = 2*np.pi / n_sectors # 每个扇形的宽度

    # 3. 自定义颜色列表，尽可能匹配原图的配色
    colors_list = [
        '#7EC0EE', '#6A8BEE', '#526CC8',  # 蓝色系：Energy, Transportation, Finance
        '#A0D7BB', '#FFDAB9', '#FFB6C1',  # 浅绿、浅橙、粉色系：Healthcare, Retail, Other
        '#EA8C8C', '#CC6666',             # 红色系：AI, Travel
        '#FFDD88', '#FFCD66', '#FFBC44',  # 浅橙色系：Food, Data, HR
        '#9C7C75', '#846D66', '#6D5B52',  # 棕色系：Hardware, Logistics, Sales
        '#9966CC', '#CC99FF',             # 紫色系：Recruiting, Education (Education 颜色更亮)
        '#FFEB3B', '#FFD700',             # 亮黄色系：Crypto, Consumer (Consumer 颜色更亮)
        '#FFA77A', '#FF8F6A',             # 橙色系：Product, Marketing (Marketing 颜色更深)
        '#B0B0B0', '#959595', '#7A7A7A',  # 灰色系：Security, Media, Manuf...
        '#B39DD6', '#9B81D0', '#856EC9',  # 浅紫色系：Real Es..., Aerospace, Infrastru...
        '#87CEFA', '#6EBCEB',             # 浅蓝色系：Support, Fitness
        '#AFEEEE', '#8EE0EE'              # 青色/绿松石色系：Legal, Construction
    ]
    
    # 如果行业数量超过预定义颜色数量，则循环使用颜色列表
    if len(colors_list) < n_sectors:
        colors = [colors_list[i % len(colors_list)] for i in range(n_sectors)]
    else:
        colors = colors_list[:n_sectors]

    # 4. 绘制玫瑰图主体扇形
    bars = ax.bar(theta, values, width=width, alpha=0.85, color=colors,
                  edgecolor='none', linewidth=0) # 不显示扇形边缘，更接近原图柔和的风格
    
    # 5. 设置极坐标样式和旋转
    ax.set_theta_zero_location('N')  # 将0度设置在顶部（北方）
    ax.set_theta_direction(-1)      # 设置为顺时针方向
    
    # 旋转整个图表，使“能源”扇形（第一个扇形）位于原图右上角的大致位置（约北偏东45度）
    ax.set_theta_offset(np.deg2rad(45)) 
    
    # 隐藏径向刻度标签（数值）和角度刻度标签（0, 90等）
    ax.set_rticks([])  
    ax.set_xticklabels([]) 
    ax.grid(False) # 隐藏所有网格线，使图表更简洁

    # 6. 设置背景颜色
    fig.patch.set_facecolor('#FDF8ED') # 设置整个图表背景色为原图的浅米色
    ax.set_facecolor('#FDF8ED') # 设置极坐标区域背景色为浅米色
    
    # 7. 添加图表标题
    ax.set_title('行业与裁员关系', 
                pad=40, fontsize=28, fontweight='normal', color='black',
                fontproperties='SimHei') # 确保标题中文显示，并匹配原图字体样式
    
    # 8. 添加行业标签和连接线
    # 连接线从中心延伸，长度与扇形长度相关，标签放置在连接线末端之外
    line_extension_factor = 1.1 # 连接线相对于扇形半径的延伸系数
    text_extension_factor = 1.2 # 文本标签相对于扇形半径的放置系数
    
    max_radial_for_rmax = 0 # 用于动态调整极轴最大半径，确保所有标签可见

    for i, industry in enumerate(industries):
        # 计算每个扇形中间的角度
        mid_angle_for_bar = theta[i] + width / 2 
        
        # 计算连接线的终点半径，使其略超出扇形
        line_end_r = values[i] * line_extension_factor
        
        # 绘制连接线：从中心(0)到扇形延伸点
        ax.plot([mid_angle_for_bar, mid_angle_for_bar], [0, line_end_r], 
                color='gray', linewidth=0.8, linestyle='-', alpha=0.7)
        
        # 计算文本标签的放置半径
        text_r = values[i] * text_extension_factor
        
        # 根据扇形所在的象限调整文本的水平对齐方式
        # `display_angle` 是考虑了图表旋转后的实际显示角度
        display_angle = (mid_angle_for_bar + ax.get_theta_offset()) % (2 * np.pi)

        ha_align = 'left'
        # 如果扇形位于图表的左半部分（视觉上），则文本右对齐
        # 象限判断：介于 90度 (pi/2) 和 270度 (3pi/2) 之间
        if np.pi/2 < display_angle <= 3*np.pi/2:
            ha_align = 'right'
        
        # 放置文本标签，文本将保持水平对齐
        ax.text(mid_angle_for_bar, text_r, industry, 
                ha=ha_align, va='center', fontsize=11, color='black', fontweight='normal')
        
        # 更新用于设置极轴最大半径的值，确保所有标签都不会被截断
        if text_r > max_radial_for_rmax:
            max_radial_for_rmax = text_r

    # 9. 设置极轴（径向轴）的最大半径，确保所有标签都在图表内部可见
    ax.set_rmax(max_radial_for_rmax * 1.1) # 增加10%的填充空间
    
    # 10. 调整布局并显示图表
    plt.tight_layout()
    plt.show()

# 运行函数以生成图表
if __name__ == "__main__":
    create_exact_rose_chart_from_image()