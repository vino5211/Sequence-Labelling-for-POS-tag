import pandas as pd
import folium
from folium import plugins
import numpy as np

# 四朝代地点数据
data = {
    'dynasty': ['唐']*50 + ['宋']*51 + ['元']*55 + ['明']*46,
    'location': [
        # 唐朝
        '吐蕃', '京師', '東都', '突厥', '河南', '太原', '幽州', '淮南', '京兆', '長安',
        '鳳翔', '京城', '河東', '周', '蜀', '河', '唐', '高麗', '河中', '華州',
        '洛陽', '雍州', '范陽', '揚州', '并州', '河陽', '晋', '隴右', '契丹', '同州',
        '漢', '山東', '河西', '齊', '西川', '汴州', '京', '嶺南', '陝州', '朔方',
        '廣州', '洛', '劍南', '新羅', '關中', '河北', '迴紇', '江都', '靈武', '岐',
        # 宋朝
        '契丹', '江', '陝西', '河北', '淮', '淮南', '蜀', '京師', '太原', '河東',
        '揚州', '京', '河', '金', '江南', '江西', '開封府', '建康', '開封', '成都',
        '汴', '秦州', '河陽', '兩浙', '漢', '杭州', '荆湖', '澶州', '河南', '福州',
        '臨安', '潭州', '定州', '福建', '延州', '湖南', '西京', '楚州', '鄜延', '淮西',
        '南京', '青州', '浙', '鄭州', '大名', '廣州', '四川', '鳳翔', '江東', '京城', '京城',
        # 元朝
        '宋', '江南', '河南', '雲南', '高麗', '上都', '江浙', '蒙古', '揚州', '金',
        '京師', '日本', '山東', '陝西', '江淮', '益都', '東平', '太原', '襄陽', '江西',
        '四川', '平陽', '大都', '江', '河間', '真定', '福建', '濟南', '交趾', '遼陽',
        '北京', '大名', '西京', '占城', '大同', '漢', '杭州', '江陵', '蜀', '西川',
        '汴梁', '東京', '河西', '冀寧', '泉州', '西域', '安南', '大都路', '河', '湖南',
        '河', '湖南', '河', '湖南', '河',
        # 明朝
        '南京', '河南', '山西', '山東', '京師', '遼', '江西', '四川', '湖廣', '陝西',
        '浙江', '遼東', '宣府', '天津', '貴州', '雲南', '大同', '福建', '京', '秦',
        '廣東', '河', '永平', '朝鮮', '鳳陽', '薊', '寧夏', '延綏', '保定', '江',
        '蜀', '廣西', '淮安', '薊鎮', '寧遠', '北京', '大河', '荆州', '開封', '萊',
        '遼陽', '南畿', '太原', '徐州', '甘肅', '廣寧'
    ],
    'counts': [
        # 唐朝
        119, 100, 94, 57, 51, 49, 47, 44, 42, 37,
        37, 37, 36, 34, 31, 30, 29, 28, 28, 28,
        28, 28, 27, 27, 24, 24, 23, 23, 23, 23,
        22, 22, 21, 21, 21, 20, 20, 20, 20, 20,
        19, 19, 18, 18, 17, 17, 17, 17, 17, 17,
        # 宋朝
        119, 92, 90, 84, 82, 76, 73, 65, 61, 59,
        59, 50, 49, 49, 42, 42, 42, 38, 37, 36,
        33, 33, 32, 30, 29, 29, 29, 28, 28, 27,
        27, 27, 26, 26, 26, 25, 25, 24, 24, 24,
        24, 24, 24, 24, 23, 23, 23, 22, 22, 22, 22,
        # 元朝
        63, 51, 49, 43, 40, 38, 35, 32, 32, 29,
        28, 26, 26, 26, 24, 24, 22, 22, 22, 21,
        21, 20, 19, 18, 17, 17, 16, 16, 16, 15,
        13, 13, 13, 13, 12, 12, 12, 12, 12, 12,
        11, 11, 11, 11, 11, 11, 10, 10, 10, 10,
        10, 10, 10, 10, 10,
        # 明朝
        65, 54, 52, 43, 41, 36, 33, 33, 30, 27,
        27, 26, 26, 25, 23, 22, 21, 20, 20, 20,
        19, 19, 18, 17, 17, 17, 17, 16, 15, 15,
        15, 14, 14, 14, 14, 13, 13, 13, 13, 13,
        13, 13, 13, 13, 12, 12
    ]
}

df = pd.DataFrame(data)

# 古代地名与现代地理坐标的对应关系（保持不变）
location_mapping = {
    # 唐朝地名
    '吐蕃': {'modern_name': '西藏', 'lat': 31.0, 'lon': 88.0},
    '京師': {'modern_name': '西安市', 'lat': 34.3, 'lon': 108.9},
    '東都': {'modern_name': '洛阳市', 'lat': 34.7, 'lon': 112.5},
    '突厥': {'modern_name': '蒙古', 'lat': 46.0, 'lon': 105.0},
    '太原': {'modern_name': '太原市', 'lat': 37.9, 'lon': 112.6},
    '幽州': {'modern_name': '北京市', 'lat': 39.9, 'lon': 116.4},
    '淮南': {'modern_name': '淮南市', 'lat': 32.6, 'lon': 117.0},
    '京兆': {'modern_name': '西安市', 'lat': 34.3, 'lon': 108.9},
    '長安': {'modern_name': '西安市', 'lat': 34.3, 'lon': 108.9},
    '鳳翔': {'modern_name': '凤翔区', 'lat': 34.5, 'lon': 107.4},
    '京城': {'modern_name': '西安市', 'lat': 34.3, 'lon': 108.9},
    '河東': {'modern_name': '运城市', 'lat': 35.0, 'lon': 111.0},
    '周': {'modern_name': '周口市', 'lat': 33.6, 'lon': 114.7},
    '蜀': {'modern_name': '四川省', 'lat': 30.7, 'lon': 104.1},
    '河': {'modern_name': '黄河流域', 'lat': 35.0, 'lon': 110.0},
    '唐': {'modern_name': '河北唐山', 'lat': 39.6, 'lon': 118.2},
    '高麗': {'modern_name': '朝鲜半岛', 'lat': 38.0, 'lon': 127.0},
    '河中': {'modern_name': '运城市', 'lat': 35.0, 'lon': 111.0},
    '華州': {'modern_name': '渭南市', 'lat': 34.5, 'lon': 109.5},
    '洛陽': {'modern_name': '洛阳市', 'lat': 34.7, 'lon': 112.5},
    '雍州': {'modern_name': '西安市', 'lat': 34.3, 'lon': 108.9},
    '范陽': {'modern_name': '保定市', 'lat': 38.9, 'lon': 115.5},
    '揚州': {'modern_name': '扬州市', 'lat': 32.4, 'lon': 119.4},
    '并州': {'modern_name': '太原市', 'lat': 37.9, 'lon': 112.6},
    '河陽': {'modern_name': '孟州市', 'lat': 34.9, 'lon': 112.8},
    '晋': {'modern_name': '山西省', 'lat': 37.9, 'lon': 112.6},
    '隴右': {'modern_name': '甘肃省', 'lat': 36.1, 'lon': 103.8},
    '契丹': {'modern_name': '内蒙古', 'lat': 42.0, 'lon': 113.0},
    '同州': {'modern_name': '大荔县', 'lat': 34.8, 'lon': 109.9},
    '漢': {'modern_name': '汉中市', 'lat': 33.1, 'lon': 107.0},
    '山東': {'modern_name': '山东省', 'lat': 36.7, 'lon': 117.0},
    '河西': {'modern_name': '甘肃河西', 'lat': 38.9, 'lon': 100.5},
    '齊': {'modern_name': '济南市', 'lat': 36.7, 'lon': 117.0},
    '西川': {'modern_name': '成都市', 'lat': 30.7, 'lon': 104.1},
    '汴州': {'modern_name': '开封市', 'lat': 34.8, 'lon': 114.3},
    '京': {'modern_name': '西安市', 'lat': 34.3, 'lon': 108.9},
    '嶺南': {'modern_name': '广东省', 'lat': 23.1, 'lon': 113.3},
    '陝州': {'modern_name': '三门峡市', 'lat': 34.8, 'lon': 111.2},
    '朔方': {'modern_name': '银川市', 'lat': 38.5, 'lon': 106.3},
    '廣州': {'modern_name': '广州市', 'lat': 23.1, 'lon': 113.3},
    '洛': {'modern_name': '洛阳市', 'lat': 34.7, 'lon': 112.5},
    '劍南': {'modern_name': '四川省', 'lat': 30.7, 'lon': 104.1},
    '新羅': {'modern_name': '韩国', 'lat': 35.9, 'lon': 127.8},
    '關中': {'modern_name': '西安市', 'lat': 34.3, 'lon': 108.9},
    '河北': {'modern_name': '河北省', 'lat': 38.0, 'lon': 114.5},
    '迴紇': {'modern_name': '新疆', 'lat': 43.8, 'lon': 87.6},
    '江都': {'modern_name': '扬州市', 'lat': 32.4, 'lon': 119.4},
    '靈武': {'modern_name': '灵武市', 'lat': 38.1, 'lon': 106.3},
    '岐': {'modern_name': '岐山县', 'lat': 34.2, 'lon': 107.6},
    
    # 宋朝地名
    '江': {'modern_name': '长江流域', 'lat': 30.0, 'lon': 112.0},
    '陝西': {'modern_name': '陕西省', 'lat': 34.3, 'lon': 108.9},
    '淮': {'modern_name': '淮河流域', 'lat': 33.0, 'lon': 117.0},
    '河南': {'modern_name': '河南省', 'lat': 34.8, 'lon': 113.6},
    '金': {'modern_name': '哈尔滨市', 'lat': 45.8, 'lon': 126.5},
    '江南': {'modern_name': '江苏南部', 'lat': 31.3, 'lon': 120.6},
    '江西': {'modern_name': '江西省', 'lat': 28.7, 'lon': 115.9},
    '開封府': {'modern_name': '开封市', 'lat': 34.8, 'lon': 114.3},
    '建康': {'modern_name': '南京市', 'lat': 32.1, 'lon': 118.8},
    '開封': {'modern_name': '开封市', 'lat': 34.8, 'lon': 114.3},
    '成都': {'modern_name': '成都市', 'lat': 30.7, 'lon': 104.1},
    '汴': {'modern_name': '开封市', 'lat': 34.8, 'lon': 114.3},
    '秦州': {'modern_name': '天水市', 'lat': 34.6, 'lon': 105.7},
    '兩浙': {'modern_name': '浙江省', 'lat': 30.3, 'lon': 120.2},
    '杭州': {'modern_name': '杭州市', 'lat': 30.3, 'lon': 120.2},
    '荆湖': {'modern_name': '湖北省', 'lat': 30.6, 'lon': 112.2},
    '澶州': {'modern_name': '濮阳市', 'lat': 35.8, 'lon': 115.0},
    '福州': {'modern_name': '福州市', 'lat': 26.1, 'lon': 119.3},
    '臨安': {'modern_name': '杭州市', 'lat': 30.3, 'lon': 120.2},
    '潭州': {'modern_name': '长沙市', 'lat': 28.2, 'lon': 112.9},
    '定州': {'modern_name': '定州市', 'lat': 38.5, 'lon': 114.9},
    '福建': {'modern_name': '福建省', 'lat': 26.1, 'lon': 117.3},
    '延州': {'modern_name': '延安市', 'lat': 36.6, 'lon': 109.5},
    '湖南': {'modern_name': '湖南省', 'lat': 28.2, 'lon': 112.9},
    '西京': {'modern_name': '洛阳市', 'lat': 34.7, 'lon': 112.5},
    '楚州': {'modern_name': '淮安市', 'lat': 33.5, 'lon': 119.0},
    '鄜延': {'modern_name': '延安市', 'lat': 36.6, 'lon': 109.5},
    '淮西': {'modern_name': '安徽西部', 'lat': 31.9, 'lon': 117.0},
    '南京': {'modern_name': '商丘市', 'lat': 34.4, 'lon': 115.6},
    '青州': {'modern_name': '青州市', 'lat': 36.7, 'lon': 118.5},
    '浙': {'modern_name': '浙江省', 'lat': 30.3, 'lon': 120.2},
    '鄭州': {'modern_name': '郑州市', 'lat': 34.8, 'lon': 113.6},
    '大名': {'modern_name': '大名县', 'lat': 36.3, 'lon': 115.1},
    '四川': {'modern_name': '四川省', 'lat': 30.7, 'lon': 104.1},
    '江東': {'modern_name': '安徽东部', 'lat': 31.9, 'lon': 118.4},
    
    # 元朝地名
    '宋': {'modern_name': '开封市', 'lat': 34.8, 'lon': 114.3},
    '雲南': {'modern_name': '云南省', 'lat': 25.0, 'lon': 101.7},
    '上都': {'modern_name': '正蓝旗', 'lat': 42.4, 'lon': 116.0},
    '江浙': {'modern_name': '江浙地区', 'lat': 30.0, 'lon': 120.0},
    '蒙古': {'modern_name': '蒙古', 'lat': 46.0, 'lon': 105.0},
    '日本': {'modern_name': '日本', 'lat': 36.2, 'lon': 138.3},
    '江淮': {'modern_name': '江淮地区', 'lat': 32.0, 'lon': 118.0},
    '益都': {'modern_name': '青州市', 'lat': 36.7, 'lon': 118.5},
    '東平': {'modern_name': '东平县', 'lat': 35.9, 'lon': 116.5},
    '襄陽': {'modern_name': '襄阳市', 'lat': 32.0, 'lon': 112.1},
    '平陽': {'modern_name': '临汾市', 'lat': 36.1, 'lon': 111.5},
    '大都': {'modern_name': '北京市', 'lat': 39.9, 'lon': 116.4},
    '河間': {'modern_name': '河间市', 'lat': 38.4, 'lon': 116.1},
    '真定': {'modern_name': '正定县', 'lat': 38.1, 'lon': 114.6},
    '濟南': {'modern_name': '济南市', 'lat': 36.7, 'lon': 117.0},
    '交趾': {'modern_name': '越南', 'lat': 21.0, 'lon': 105.8},
    '遼陽': {'modern_name': '辽阳市', 'lat': 41.3, 'lon': 123.2},
    '北京': {'modern_name': '北京市', 'lat': 39.9, 'lon': 116.4},
    '占城': {'modern_name': '越南中南部', 'lat': 12.0, 'lon': 109.0},
    '大同': {'modern_name': '大同市', 'lat': 40.1, 'lon': 113.3},
    '江陵': {'modern_name': '荆州市', 'lat': 30.3, 'lon': 112.2},
    '汴梁': {'modern_name': '开封市', 'lat': 34.8, 'lon': 114.3},
    '東京': {'modern_name': '开封市', 'lat': 34.8, 'lon': 114.3},
    '冀寧': {'modern_name': '太原市', 'lat': 37.9, 'lon': 112.6},
    '泉州': {'modern_name': '泉州市', 'lat': 24.9, 'lon': 118.6},
    '西域': {'modern_name': '新疆', 'lat': 43.8, 'lon': 87.6},
    '安南': {'modern_name': '越南', 'lat': 21.0, 'lon': 105.8},
    '大都路': {'modern_name': '北京市', 'lat': 39.9, 'lon': 116.4},
    
    # 明朝地名
    '南京': {'modern_name': '南京市', 'lat': 32.1, 'lon': 118.8},
    '山西': {'modern_name': '山西省', 'lat': 37.9, 'lon': 112.6},
    '遼': {'modern_name': '辽宁省', 'lat': 41.3, 'lon': 122.6},
    '湖廣': {'modern_name': '湖北湖南', 'lat': 29.0, 'lon': 112.5},
    '浙江': {'modern_name': '浙江省', 'lat': 30.3, 'lon': 120.2},
    '遼東': {'modern_name': '辽宁东部', 'lat': 41.8, 'lon': 124.4},
    '宣府': {'modern_name': '宣化区', 'lat': 40.6, 'lon': 115.0},
    '天津': {'modern_name': '天津市', 'lat': 39.1, 'lon': 117.2},
    '貴州': {'modern_name': '贵州省', 'lat': 26.6, 'lon': 106.7},
    '雲南': {'modern_name': '云南省', 'lat': 25.0, 'lon': 101.7},
    '朝鮮': {'modern_name': '朝鲜半岛', 'lat': 38.0, 'lon': 127.0},
    '鳳陽': {'modern_name': '凤阳县', 'lat': 32.9, 'lon': 117.5},
    '薊': {'modern_name': '蓟州区', 'lat': 40.0, 'lon': 117.4},
    '寧夏': {'modern_name': '宁夏', 'lat': 38.5, 'lon': 106.3},
    '延綏': {'modern_name': '榆林市', 'lat': 38.3, 'lon': 109.7},
    '保定': {'modern_name': '保定市', 'lat': 38.9, 'lon': 115.5},
    '廣東': {'modern_name': '广东省', 'lat': 23.1, 'lon': 113.3},
    '永平': {'modern_name': '卢龙县', 'lat': 39.9, 'lon': 118.9},
    '秦': {'modern_name': '陕西省', 'lat': 34.3, 'lon': 108.9},
    '廣西': {'modern_name': '广西', 'lat': 23.8, 'lon': 108.8},
    '淮安': {'modern_name': '淮安市', 'lat': 33.5, 'lon': 119.0},
    '薊鎮': {'modern_name': '蓟州区', 'lat': 40.0, 'lon': 117.4},
    '寧遠': {'modern_name': '兴城市', 'lat': 40.6, 'lon': 120.7},
    '北京': {'modern_name': '北京市', 'lat': 39.9, 'lon': 116.4},
    '大河': {'modern_name': '黄河', 'lat': 35.0, 'lon': 110.0},
    '荆州': {'modern_name': '荆州市', 'lat': 30.3, 'lon': 112.2},
    '萊': {'modern_name': '莱州市', 'lat': 37.2, 'lon': 119.9},
    '南畿': {'modern_name': '江苏安徽', 'lat': 32.0, 'lon': 118.8},
    '徐州': {'modern_name': '徐州市', 'lat': 34.3, 'lon': 117.2},
    '甘肅': {'modern_name': '甘肃省', 'lat': 36.1, 'lon': 103.8},
    '廣寧': {'modern_name': '北镇市', 'lat': 41.6, 'lon': 121.8},
    '寧': {'modern_name': '宁夏', 'lat': 38.5, 'lon': 106.3},
    '通州': {'modern_name': '通州区', 'lat': 39.9, 'lon': 116.7},
    '永寧': {'modern_name': '永宁县', 'lat': 38.3, 'lon': 106.3},
    '安慶': {'modern_name': '安庆市', 'lat': 30.5, 'lon': 117.0}
}

def create_dynasties_map():
    """创建四朝代地点分布地图，使用不同形状和颜色"""
    
    # 创建以中国为中心的地图
    m = folium.Map(
        location=[35.0, 110.0],  
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # 添加标题
    title_html = '''
                 <h3 align="center" style="font-size:22px"><b>唐宋元明四朝代地点分布图</b></h3>
                 <p align="center">不同形状和颜色代表不同朝代，标记大小表示史书中出现频次</p>
                 '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # 朝代配置：形状、颜色、图标
    dynasty_config = {
        '唐': {
            'color': '#FF6B35',      # 橙红色
            'icon': 'star',          # 星形
            'prefix': 'fa',
            'shape': '⭐'
        },
        '宋': {
            'color': '#4285F4',      # 蓝色
            'icon': 'square',        # 方形
            'prefix': 'fa',
            'shape': '⬜'
        },
        '元': {
            'color': '#34A853',      # 绿色
            'icon': 'circle',        # 圆形
            'prefix': 'fa',
            'shape': '⚫'
        },
        '明': {
            'color': '#EA4335',      # 红色
            'icon': 'triangle-up',   # 三角形
            'prefix': 'fa',
            'shape': '🔺'
        }
    }
    
    # 根据频次计算标记大小
    def get_marker_size(count):
        if count >= 100:
            return {'size': 20, 'icon_size': (25, 25)}
        elif count >= 80:
            return {'size': 17, 'icon_size': (22, 22)}
        elif count >= 60:
            return {'size': 15, 'icon_size': (20, 20)}
        elif count >= 40:
            return {'size': 13, 'icon_size': (18, 18)}
        elif count >= 20:
            return {'size': 11, 'icon_size': (15, 15)}
        else:
            return {'size': 9, 'icon_size': (12, 12)}
    
    # 创建朝代图层组
    dynasty_groups = {}
    for dynasty in ['唐', '宋', '元', '明']:
        dynasty_groups[dynasty] = folium.FeatureGroup(name=f'{dynasty}朝')
        m.add_child(dynasty_groups[dynasty])
    
    # 在地图上标注地点
    for _, row in df.iterrows():
        dynasty = row['dynasty']
        location = row['location']
        count = row['counts']
        
        if location in location_mapping:
            info = location_mapping[location]
            lat, lon = info['lat'], info['lon']
            modern_name = info['modern_name']
            
            config = dynasty_config[dynasty]
            size_info = get_marker_size(count)
            
            # 使用不同的标记样式
            if dynasty == '唐':
                # 唐朝：星形标记
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(
                        f"<b>{dynasty}朝 - {location}</b><br>"
                        f"现今：{modern_name}<br>"
                        f"出现次数：{count}",
                        max_width=250
                    ),
                    tooltip=f"{dynasty}: {location} ({count}次)",
                    icon=folium.Icon(
                        color='orange',
                        icon='star',
                        prefix='fa'
                    )
                ).add_to(dynasty_groups[dynasty])
                
            elif dynasty == '宋':
                # 宋朝：方形标记
                folium.RegularPolygonMarker(
                    location=[lat, lon],
                    popup=folium.Popup(
                        f"<b>{dynasty}朝 - {location}</b><br>"
                        f"现今：{modern_name}<br>"
                        f"出现次数：{count}",
                        max_width=250
                    ),
                    tooltip=f"{dynasty}: {location} ({count}次)",
                    number_of_sides=4,
                    radius=size_info['size'],
                    color='white',
                    fillColor=config['color'],
                    fillOpacity=0.8,
                    weight=2
                ).add_to(dynasty_groups[dynasty])
                
            elif dynasty == '元':
                # 元朝：圆形标记
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=size_info['size'],
                    popup=folium.Popup(
                        f"<b>{dynasty}朝 - {location}</b><br>"
                        f"现今：{modern_name}<br>"
                        f"出现次数：{count}",
                        max_width=250
                    ),
                    tooltip=f"{dynasty}: {location} ({count}次)",
                    color='white',
                    fillColor=config['color'],
                    fillOpacity=0.8,
                    weight=2
                ).add_to(dynasty_groups[dynasty])
                
            elif dynasty == '明':
                # 明朝：三角形标记
                folium.RegularPolygonMarker(
                    location=[lat, lon],
                    popup=folium.Popup(
                        f"<b>{dynasty}朝 - {location}</b><br>"
                        f"现今：{modern_name}<br>"
                        f"出现次数：{count}",
                        max_width=250
                    ),
                    tooltip=f"{dynasty}: {location} ({count}次)",
                    number_of_sides=3,
                    radius=size_info['size'],
                    rotation=0,
                    color='white',
                    fillColor=config['color'],
                    fillOpacity=0.8,
                    weight=2
                ).add_to(dynasty_groups[dynasty])
            
            # 为高频地点添加文字标签
            if count >= 80:
                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 9pt; font-weight: bold; color: {config["color"]}; text-shadow: 1px 1px 1px white; background: rgba(255,255,255,0.8); padding: 2px; border-radius: 3px;">{location}</div>',
                        icon_size=(60, 20),
                        icon_anchor=(30, 10)
                    )
                ).add_to(dynasty_groups[dynasty])
    
    # 添加图层控制
    folium.LayerControl().add_to(m)
    
    # 添加形状和颜色图例
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 220px; height: 280px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 15px; border-radius: 5px;
                box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
                ">
    <h4 style="margin-top:0; text-align:center; color:#333;">朝代形状图例</h4>
    
    <div style="margin: 8px 0;">
        <span style="color:{dynasty_config['唐']['color']}; font-size:16px;">⭐</span>
        <span style="margin-left:8px;"><b>唐朝 (618-907)</b></span>
        <br><span style="font-size:12px; color:#666; margin-left:24px;">盛世辉煌 - 星形标记</span>
    </div>
    
    <div style="margin: 8px 0;">
        <span style="color:{dynasty_config['宋']['color']}; font-size:16px;">■</span>
        <span style="margin-left:8px;"><b>宋朝 (960-1279)</b></span>
        <br><span style="font-size:12px; color:#666; margin-left:24px;">文治理政 - 方形标记</span>
    </div>
    
    <div style="margin: 8px 0;">
        <span style="color:{dynasty_config['元']['color']}; font-size:16px;">●</span>
        <span style="margin-left:8px;"><b>元朝 (1271-1368)</b></span>
        <br><span style="font-size:12px; color:#666; margin-left:24px;">大一统制 - 圆形标记</span>
    </div>
    
    <div style="margin: 8px 0;">
        <span style="color:{dynasty_config['明']['color']}; font-size:16px;">▲</span>
        <span style="margin-left:8px;"><b>明朝 (1368-1644)</b></span>
        <br><span style="font-size:12px; color:#666; margin-left:24px;">中华复兴 - 三角标记</span>
    </div>
    
    <hr style="margin: 10px 0;">
    <h5 style="margin:5px 0; color:#333;">标记大小表示频次</h5>
    <div style="font-size:12px; color:#666;">
        <div>● 100+ 次 (特大)</div>
        <div>● 80-99 次 (大)</div>
        <div>● 60-79 次 (中大)</div>
        <div>● 40-59 次 (中)</div>
        <div>● 20-39 次 (小)</div>
        <div>● < 20 次 (微小)</div>
    </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

# 创建地图
map_object = create_dynasties_map()

# 保存地图
map_object.save('dynasties_shapes_map.html')

# 统计信息
print("=== 唐宋元明四朝代形状标记地图已创建 ===")
print(f"地图已保存为 'dynasties_shapes_map.html'")

print("\n=== 各朝代形状标记配置 ===")
shapes_info = {
    '唐': '⭐ 星形 - 橙红色 (盛世辉煌)',
    '宋': '■ 方形 - 蓝色 (文治理政)', 
    '元': '● 圆形 - 绿色 (大一统制)',
    '明': '▲ 三角 - 红色 (中华复兴)'
}

for dynasty, info in shapes_info.items():
    dynasty_data = df[df['dynasty'] == dynasty]
    print(f"\n{dynasty}朝 {info}")
    print(f"  地点数量: {len(dynasty_data)}")
    print(f"  最高频次: {dynasty_data['counts'].max()} ({dynasty_data.loc[dynasty_data['counts'].idxmax(), 'location']})")
    print(f"  平均频次: {dynasty_data['counts'].mean():.1f}")
    
    # 显示前3个最频繁地点
    top_3 = dynasty_data.nlargest(3, 'counts')
    print(f"  前3高频地点:")
    for i, row in top_3.iterrows():
        print(f"    {row['location']}: {row['counts']}次")

print(f"\n总计标注地点: {len(df)} 个")
print("每个朝代使用独特的形状和颜色组合，便于区分和对比分析")
