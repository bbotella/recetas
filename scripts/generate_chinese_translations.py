#!/usr/bin/env python3
"""
Script to generate Chinese translations for all recipes
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import (
    init_database,
    get_all_recipes,
    save_recipe_translation,
    get_recipe_translation,
)

# Category translations
CATEGORY_TRANSLATIONS = {
    "Postres": "甜点",
    "Pollo": "鸡肉",
    "Pescado": "鱼类",
    "Carnes": "肉类",
    "Bebidas": "饮品",
    "Verduras": "蔬菜",
    "Aperitivos": "开胃菜",
    "Otros": "其他",
}


def get_chinese_recipe_translations():
    """
    Complete Chinese translations for all 73 recipes.
    This function contains high-quality translations generated by Claude AI.
    """
    return {
        "Alcachofas Rellenas": {
            "title": "酿朝鲜蓟",
            "description": "煮熟的朝鲜蓟塞入瘦肉、火腿和香料的混合馅料，用白汁和奶酪烤制。",
            "ingredients": """- 朝鲜蓟
- 瘦肉
- 火腿
- 香料
- 黄油
- 白汁
- 奶酪丝""",
            "instructions": """1. 煮熟朝鲜蓟。

2. 用瘦肉、火腿、香料和黄油块的混合物塞满朝鲜蓟。

3. 用白汁和奶酪丝覆盖，放入烤箱烤制。""",
            "category": "肉类",
        },
        "Arenques Asados en Vino": {
            "title": "红酒烤鲱鱼",
            "description": "新鲜鲱鱼与白葡萄酒、香草和蔬菜一起烤制，制作出美味的地中海菜肴。",
            "ingredients": """- 新鲜鲱鱼
- 白葡萄酒
- 洋葱
- 大蒜
- 月桂叶
- 橄榄油
- 盐和胡椒""",
            "instructions": """1. 清洗和处理鲱鱼。

2. 用酒、香草和调料腌制。

3. 在烤箱中烤制至金黄色并完全熟透。""",
            "category": "鱼类",
        },
        "Batido de Coco": {
            "title": "椰子奶昔",
            "description": "清爽的椰子奶昔，质地顺滑，带有热带风味。",
            "ingredients": """- 椰奶
- 牛奶
- 糖
- 冰块
- 香草精""",
            "instructions": """1. 在搅拌机中混合椰奶和牛奶。

2. 加入糖和香草精。

3. 加入冰块搅拌至光滑起泡。

4. 立即倒入冷藏的杯子中享用。""",
            "category": "饮品",
        },
        "Batido de Limón o Naranja": {
            "title": "柠檬或橙子奶昔",
            "description": "用新鲜柠檬或橙汁制作的柑橘奶昔，非常适合炎热的天气。",
            "ingredients": """- 新鲜柠檬或橙汁
- 牛奶
- 糖
- 冰块
- 柠檬或橙子皮屑""",
            "instructions": """1. 挤出新鲜柑橘汁。

2. 在搅拌机中与牛奶和糖混合。

3. 加入冰块和果皮屑。

4. 搅拌至光滑，冷藏享用。""",
            "category": "饮品",
        },
        "Batido de Plátano": {
            "title": "香蕉奶昔",
            "description": "香浓的香蕉奶昔，富含风味和营养。",
            "ingredients": """- 成熟香蕉
- 牛奶
- 糖
- 冰块
- 肉桂（可选）""",
            "instructions": """1. 去皮并切片成熟香蕉。

2. 在搅拌机中与牛奶和糖混合。

3. 加入冰块搅拌至光滑。

4. 如需要可撒上肉桂粉，然后享用。""",
            "category": "饮品",
        },
        "Bizcocho y Tortada": {
            "title": "海绵蛋糕和西班牙蛋糕",
            "description": "轻盈的海绵蛋糕配传统西班牙蛋糕制作方法。",
            "ingredients": """- 鸡蛋
- 糖
- 面粉
- 发酵粉
- 黄油
- 牛奶
- 香草精""",
            "instructions": """1. 将鸡蛋和糖打至蓬松。

2. 逐渐加入面粉和发酵粉。

3. 拌入融化的黄油和牛奶。

4. 在预热的烤箱中烤至金黄色。""",
            "category": "甜点",
        },
        "Budin de Merluza": {
            "title": "鳕鱼布丁",
            "description": "用新鲜鳕鱼、鸡蛋和白汁制作的咸味鱼肉布丁。",
            "ingredients": """- 新鲜鳕鱼片
- 鸡蛋
- 白汁
- 面包屑
- 黄油
- 盐和胡椒""",
            "instructions": """1. 煮熟并拆散鳕鱼。

2. 与打散的鸡蛋和白汁混合。

3. 倒入涂黄油的模具中。

4. 烤制至凝固并呈金黄色。""",
            "category": "鱼类",
        },
        "Calamares en su Tinta Dana-Ona": {
            "title": "墨鱼汁炖鱿鱼（达纳-奥纳风味）",
            "description": "传统西班牙菜，用鱿鱼自身的墨汁配洋葱和香料炖煮。",
            "ingredients": """- 带墨囊的新鲜鱿鱼
- 洋葱
- 大蒜
- 西红柿
- 白葡萄酒
- 橄榄油
- 盐和胡椒""",
            "instructions": """1. 清洗鱿鱼并保留墨囊。

2. 将洋葱和大蒜炒至金黄。

3. 加入鱿鱼煮至软嫩。

4. 加入墨汁、西红柿和酒，炖煮至浓稠。""",
            "category": "鱼类",
        },
        "Canelones en Salsa de Queso": {
            "title": "奶酪汁肉馅面管",
            "description": "填充肉馅的意大利面管，配浓郁的奶酪汁。",
            "ingredients": """- 意大利面管
- 肉馅
- 奶酪汁
- 奶酪丝
- 洋葱
- 大蒜
- 香草""",
            "instructions": """1. 将意大利面管煮至刚好熟透。

2. 准备肉馅，用洋葱和香草调味。

3. 将肉馅填入面管中。

4. 淋上奶酪汁，烤制至起泡。""",
            "category": "其他",
        },
        "Chocolate para Adorno a Baño": {
            "title": "装饰用巧克力涂层",
            "description": "光滑的巧克力涂层，非常适合装饰蛋糕和糕点。",
            "ingredients": """- 黑巧克力
- 黄油
- 糖粉
- 牛奶或奶油
- 香草精""",
            "instructions": """1. 在双锅炉中融化巧克力和黄油。

2. 逐渐加入糖粉和牛奶。

3. 搅拌至光滑有光泽。

4. 趁热用于涂层或装饰。""",
            "category": "甜点",
        },
        "Cocktail de Tomate": {
            "title": "番茄鸡尾酒",
            "description": "清爽的番茄鸡尾酒，配香草和香料。",
            "ingredients": """- 新鲜番茄汁
- 伍斯特沙司
- 塔巴斯科辣椒酱
- 芹菜盐
- 柠檬汁
- 黑胡椒
- 芹菜茎用作装饰""",
            "instructions": """1. 将番茄汁与伍斯特沙司和塔巴斯科酱混合。

2. 加入芹菜盐和柠檬汁。

3. 用黑胡椒调味。

4. 加冰块，用芹菜茎装饰享用。""",
            "category": "饮品",
        },
        "Corona de Cordero": {
            "title": "羊肉皇冠",
            "description": "优雅的羊肉皇冠烤肉，适合特殊场合。",
            "ingredients": """- 羊肉皇冠烤肉
- 大蒜
- 迷迭香
- 百里香
- 橄榄油
- 盐和胡椒
- 红酒""",
            "instructions": """1. 用香草和大蒜给羊肉皇冠调味。

2. 在热锅中煎至褐色。

3. 在烤箱中烤至所需熟度。

4. 静置后切片享用。""",
            "category": "肉类",
        },
        "Crema Pastelera": {
            "title": "卡仕达酱",
            "description": "浓郁丝滑的卡仕达酱，适合填充糕点和蛋糕。",
            "ingredients": """- 牛奶
- 蛋黄
- 糖
- 玉米淀粉
- 黄油
- 香草精""",
            "instructions": """1. 在平底锅中加热牛奶。

2. 将蛋黄与糖和玉米淀粉一起打散。

3. 逐渐将热牛奶加入蛋黄混合物中。

4. 煮至浓稠，然后加入黄油和香草。""",
            "category": "甜点",
        },
        "Crema de Chocolate": {
            "title": "巧克力奶油",
            "description": "浓郁的巧克力奶油甜点，带有浓厚的可可风味。",
            "ingredients": """- 黑巧克力
- 淡奶油
- 牛奶
- 糖
- 蛋黄
- 香草精""",
            "instructions": """1. 将巧克力与奶油和牛奶一起融化。

2. 将蛋黄与糖打散。

3. 将两种混合物合并煮至浓稠。

4. 加入香草，冷藏后享用。""",
            "category": "甜点",
        },
        "Crepes": {
            "title": "可丽饼",
            "description": "薄而精致的煎饼，适合甜味或咸味馅料。",
            "ingredients": """- 面粉
- 鸡蛋
- 牛奶
- 黄油
- 盐
- 糖（甜味可丽饼用）""",
            "instructions": """1. 将面粉、鸡蛋和牛奶混合制作面糊。

2. 加入融化的黄油和盐。

3. 在热锅中摊成薄层。

4. 根据需要填充配料并卷起。""",
            "category": "甜点",
        },
        "Emparedados de Merluza": {
            "title": "鳕鱼三明治",
            "description": "优雅的鱼肉三明治，配鳕鱼片和美味配菜。",
            "ingredients": """- 新鲜鳕鱼片
- 面包片
- 蛋黄酱
- 生菜
- 西红柿
- 柠檬汁
- 盐和胡椒""",
            "instructions": """1. 将鳕鱼片煮至可剥离。

2. 轻微烤制面包片。

3. 在面包上涂抹蛋黄酱。

4. 层层叠叠放上鳕鱼、生菜和西红柿。""",
            "category": "鱼类",
        },
        "Espinacas a la Crema": {
            "title": "奶油菠菜",
            "description": "新鲜菠菜配浓郁的奶油汁，加大蒜和香草。",
            "ingredients": """- 新鲜菠菜
- 淡奶油
- 黄油
- 大蒜
- 肉豆蔻
- 盐和胡椒""",
            "instructions": """1. 在开水中焯菠菜。

2. 用黄油炒大蒜。

3. 加入菠菜和奶油。

4. 用肉豆蔻、盐和胡椒调味。""",
            "category": "蔬菜",
        },
        "Faisán a la Belga": {
            "title": "比利时风味野鸡",
            "description": "用比利时烹饪技法和啤酒制作的嫩野鸡。",
            "ingredients": """- 野鸡
- 比利时啤酒
- 洋葱
- 胡萝卜
- 芹菜
- 香草
- 黄油""",
            "instructions": """1. 用黄油将野鸡块煎至褐色。

2. 加入蔬菜和香草。

3. 倒入啤酒慢慢炖煮。

4. 煮至软嫩后享用。""",
            "category": "肉类",
        },
        "Faisán a la Cazuela": {
            "title": "砂锅野鸡",
            "description": "乡村风味的野鸡炖菜，配蔬菜和红酒慢炖。",
            "ingredients": """- 野鸡块
- 红酒
- 洋葱
- 胡萝卜
- 蘑菇
- 大蒜
- 香草""",
            "instructions": """1. 在砂锅中将野鸡煎至褐色。

2. 加入蔬菜和红酒。

3. 盖上盖子慢炖。

4. 煮至肉质软嫩。""",
            "category": "肉类",
        },
        "Filete Estrogonoff": {
            "title": "牛肉斯特罗加诺夫",
            "description": "经典的牛肉斯特罗加诺夫，配嫩牛肉条和奶油汁。",
            "ingredients": """- 牛里脊肉
- 蘑菇
- 洋葱
- 酸奶油
- 牛肉高汤
- 面粉
- 黄油""",
            "instructions": """1. 将牛肉切条炒制。

2. 分别煮蘑菇和洋葱。

3. 用面粉和高汤制作奶油汁。

4. 将所有配料合并享用。""",
            "category": "肉类",
        },
        "Flan de Coco": {
            "title": "椰子布丁",
            "description": "椰子卡仕达配焦糖汁，经典布丁的热带风味变化。",
            "ingredients": """- 椰奶
- 鸡蛋
- 糖
- 香草精
- 焦糖汁""",
            "instructions": """1. 制作焦糖并铺在模具底部。

2. 将鸡蛋与糖和椰奶打散。

3. 将混合物倒在焦糖上。

4. 在水浴中烤制至凝固。""",
            "category": "甜点",
        },
        "Flan de Coco (Versión 2)": {
            "title": "椰子布丁（版本2）",
            "description": "椰子布丁的另一种制作方法，用新鲜椰子和奶油。",
            "ingredients": """- 新鲜椰子
- 淡奶油
- 鸡蛋
- 糖
- 香草
- 焦糖""",
            "instructions": """1. 刨新鲜椰子并提取椰奶。

2. 与奶油和香草一起加热。

3. 将鸡蛋与糖打散并合并。

4. 在焦糖模具中烤制。""",
            "category": "甜点",
        },
        "Galletas Rellenas": {
            "title": "夹心饼干",
            "description": "精致的饼干，填充甜奶油或果酱。",
            "ingredients": """- 面粉
- 黄油
- 糖
- 鸡蛋
- 香草精
- 所选馅料""",
            "instructions": """1. 用面粉、黄油和糖制作饼干面团。

2. 擀平并切成形状。

3. 烤至金黄色。

4. 冷却后填入奶油或果酱。""",
            "category": "甜点",
        },
        "Guisantes con Jamón": {
            "title": "火腿豌豆",
            "description": "传统西班牙菜，青豌豆配火腿和洋葱。",
            "ingredients": """- 新鲜青豌豆
- 火腿
- 洋葱
- 大蒜
- 橄榄油
- 鸡汤
- 欧芹""",
            "instructions": """1. 用橄榄油炒洋葱和大蒜。

2. 加入火腿稍微煮一下。

3. 加入豌豆和鸡汤。

4. 炖煮至豌豆软嫩。""",
            "category": "蔬菜",
        },
        "Helado de Coco": {
            "title": "椰子冰淇淋",
            "description": "奶香浓郁的自制椰子冰淇淋，带有热带风味。",
            "ingredients": """- 椰奶
- 淡奶油
- 糖
- 蛋黄
- 香草精
- 椰丝""",
            "instructions": """1. 加热椰奶和奶油。

2. 将蛋黄与糖打散。

3. 制作卡仕达基底并冷却。

4. 在冰淇淋机中搅拌。""",
            "category": "甜点",
        },
        "Helado de Fresa": {
            "title": "草莓冰淇淋",
            "description": "新鲜草莓冰淇淋，带有天然水果风味。",
            "ingredients": """- 新鲜草莓
- 淡奶油
- 糖
- 蛋黄
- 香草精
- 柠檬汁""",
            "instructions": """1. 将草莓与糖一起打成泥。

2. 用奶油和蛋黄制作卡仕达基底。

3. 将草莓泥与卡仕达混合。

4. 在冰淇淋机中搅拌。""",
            "category": "甜点",
        },
        "Helado de Plátano": {
            "title": "香蕉冰淇淋",
            "description": "浓郁的香蕉冰淇淋，天然甜味，质地奶香。",
            "ingredients": """- 成熟香蕉
- 淡奶油
- 糖
- 蛋黄
- 香草精
- 柠檬汁""",
            "instructions": """1. 将成熟香蕉与柠檬汁一起捣碎。

2. 用奶油和鸡蛋制作卡仕达基底。

3. 将香蕉混合物与卡仕达合并。

4. 搅拌至冷冻。""",
            "category": "甜点",
        },
        "Huevos al Curry": {
            "title": "咖喱蛋",
            "description": "水煮蛋配香料咖喱汁和芳香香料。",
            "ingredients": """- 水煮蛋
- 咖喱粉
- 洋葱
- 西红柿
- 椰奶
- 大蒜
- 生姜""",
            "instructions": """1. 炒洋葱、大蒜和生姜。

2. 加入咖喱粉和西红柿。

3. 倒入椰奶炖煮。

4. 加入切半的鸡蛋加热。""",
            "category": "其他",
        },
        "Lenguado Relleno de Gambas y Champiñones": {
            "title": "虾仁蘑菇酿比目鱼",
            "description": "优雅的比目鱼片，填充虾仁和蘑菇的混合馅料。",
            "ingredients": """- 比目鱼片
- 虾仁
- 蘑菇
- 白葡萄酒
- 黄油
- 奶油
- 香草""",
            "instructions": """1. 准备虾仁和蘑菇馅料。

2. 将比目鱼片塞满馅料并固定。

3. 用黄油煎至金黄色。

4. 用酒和奶油汁收尾。""",
            "category": "鱼类",
        },
        "Lomo Relleno": {
            "title": "酿猪里脊",
            "description": "嫩猪里脊填充美味馅料和香草。",
            "ingredients": """- 猪里脊
- 馅料混合物
- 大蒜
- 香草
- 橄榄油
- 白葡萄酒
- 盐和胡椒""",
            "instructions": """1. 将猪里脊切开并填入馅料。

2. 卷起并牢固绑好。

3. 将各面煎至褐色。

4. 在烤箱中烤制至完全熟透。""",
            "category": "肉类",
        },
        "Lomo a la Naranja con Olla": {
            "title": "橙汁猪里脊配蔬菜",
            "description": "猪里脊配橙汁和蔬菜在一锅中烹制。",
            "ingredients": """- 猪里脊
- 橙汁
- 洋葱
- 胡萝卜
- 土豆
- 大蒜
- 香草""",
            "instructions": """1. 在锅中将猪里脊煎至褐色。

2. 加入蔬菜和橙汁。

3. 盖上盖子慢炖。

4. 煮至肉和蔬菜都软嫩。""",
            "category": "肉类",
        },
        "Manzanas Asadas": {
            "title": "烤苹果",
            "description": "嫩烤苹果，填充肉桂、糖和坚果。",
            "ingredients": """- 苹果
- 肉桂
- 糖
- 黄油
- 坚果
- 葡萄干
- 蜂蜜""",
            "instructions": """1. 给苹果去核并填入馅料。

2. 放在烤盘中加黄油。

3. 烤至软嫩并焦糖化。

4. 配汤汁温热享用。""",
            "category": "甜点",
        },
        "Merluza a la Bechamel": {
            "title": "白汁鳕鱼",
            "description": "新鲜鳕鱼片配奶香白汁并烤制。",
            "ingredients": """- 鳕鱼片
- 白汁
- 黄油
- 面粉
- 牛奶
- 奶酪
- 肉豆蔻""",
            "instructions": """1. 用黄油、面粉和牛奶制作白汁。

2. 给鳕鱼片调味。

3. 用白汁和奶酪覆盖。

4. 在烤箱中烤制至金黄色。""",
            "category": "鱼类",
        },
        "Moka": {
            "title": "摩卡",
            "description": "咖啡风味甜点，配巧克力和奶油。",
            "ingredients": """- 浓咖啡
- 黑巧克力
- 淡奶油
- 糖
- 蛋黄
- 香草精""",
            "instructions": """1. 将巧克力与咖啡一起融化。

2. 将蛋黄与糖打散。

3. 合并煮至浓稠。

4. 拌入打发的奶油并冷藏。""",
            "category": "甜点",
        },
        "Mus de Pollo": {
            "title": "鸡肉慕斯",
            "description": "轻盈蓬松的鸡肉慕斯，适合作为开胃菜。",
            "ingredients": """- 熟鸡肉
- 奶油
- 明胶
- 鸡汤
- 香草
- 盐和胡椒""",
            "instructions": """1. 将熟鸡肉打成泥至光滑。

2. 在温鸡汤中溶解明胶。

3. 与鸡肉混合并拌入奶油。

4. 冷藏至凝固。""",
            "category": "鸡肉",
        },
        "Pastel de Patata": {
            "title": "土豆蛋糕",
            "description": "层层叠叠的土豆蛋糕，配肉馅和蔬菜。",
            "ingredients": """- 土豆
- 肉馅
- 洋葱
- 鸡蛋
- 牛奶
- 奶酪
- 香草""",
            "instructions": """1. 将切片土豆与肉馅层层叠叠。

2. 将鸡蛋与牛奶打散并倒入。

3. 顶部撒上奶酪。

4. 烤制至金黄色并凝固。""",
            "category": "其他",
        },
        "Paté de Pollo": {
            "title": "鸡肉酱",
            "description": "光滑奶香的鸡肉酱，配香草和香料。",
            "ingredients": """- 鸡肝
- 黄油
- 洋葱
- 香草
- 白兰地
- 奶油
- 盐和胡椒""",
            "instructions": """1. 将鸡肝与洋葱一起炒制。

2. 加入白兰地和香草。

3. 与黄油一起搅拌至光滑。

4. 过滤并在模具中冷藏。""",
            "category": "鸡肉",
        },
        "Pescado al Horno - Salsa Holandesa": {
            "title": "烤鱼配荷兰汁",
            "description": "烤箱烤制的鱼，配浓郁的荷兰汁。",
            "ingredients": """- 鱼片
- 黄油
- 蛋黄
- 柠檬汁
- 白葡萄酒
- 香草
- 盐和胡椒""",
            "instructions": """1. 用酒和香草烤制鱼片。

2. 用蛋黄和黄油制作荷兰汁。

3. 加入柠檬汁并调味。

4. 将鱼配温热的汁享用。""",
            "category": "鱼类",
        },
        "Pescado al Horno con Vino": {
            "title": "红酒烤鱼",
            "description": "鱼片配白葡萄酒和芳香香草烤制。",
            "ingredients": """- 鱼片
- 白葡萄酒
- 洋葱
- 大蒜
- 香草
- 橄榄油
- 柠檬""",
            "instructions": """1. 将鱼放在烤盘中。

2. 加入酒、洋葱和香草。

3. 淋上橄榄油。

4. 烤制至鱼肉易剥离。""",
            "category": "鱼类",
        },
        "Pinchito Dana-Ona": {
            "title": "达纳-奥纳肉串",
            "description": "腌制肉串，烤制至完美。",
            "ingredients": """- 肉块
- 腌料配料
- 蔬菜
- 橄榄油
- 大蒜
- 香草
- 香料""",
            "instructions": """1. 用香草和香料腌制肉块。

2. 与蔬菜一起穿在串上。

3. 用中火烤制。

4. 经常翻动至完全熟透。""",
            "category": "肉类",
        },
        "Pizza Napolitana": {
            "title": "那不勒斯披萨",
            "description": "经典意大利披萨，配番茄酱、马苏里拉奶酪和罗勒。",
            "ingredients": """- 披萨面团
- 番茄酱
- 马苏里拉奶酪
- 新鲜罗勒
- 橄榄油
- 大蒜""",
            "instructions": """1. 擀平披萨面团。

2. 均匀涂抹番茄酱。

3. 加入马苏里拉奶酪和罗勒。

4. 在高温烤箱中烤制至酥脆。""",
            "category": "其他",
        },
        "Pizza Napolitana (Versión 2)": {
            "title": "那不勒斯披萨（版本2）",
            "description": "那不勒斯披萨的另一种制作方法，配额外配料。",
            "ingredients": """- 披萨面团
- 番茄酱
- 马苏里拉奶酪
- 凤尾鱼
- 橄榄
- 牛至
- 橄榄油""",
            "instructions": """1. 准备披萨基底配酱。

2. 加入马苏里拉奶酪和配料。

3. 撒上牛至调味。

4. 烤制至金黄色并起泡。""",
            "category": "其他",
        },
        "Pollo Marengo": {
            "title": "马伦戈鸡",
            "description": "经典法式鸡肉菜，配西红柿、蘑菇和白葡萄酒。",
            "ingredients": """- 鸡块
- 西红柿
- 蘑菇
- 白葡萄酒
- 洋葱
- 大蒜
- 香草""",
            "instructions": """1. 用油将鸡块煎至褐色。

2. 加入洋葱和蘑菇。

3. 倒入酒和西红柿。

4. 炖煮至鸡肉软嫩。""",
            "category": "鸡肉",
        },
        "Pollo a la Vasca": {
            "title": "巴斯克风味鸡",
            "description": "鸡肉配甜椒和西红柿，巴斯克风味。",
            "ingredients": """- 鸡块
- 甜椒
- 西红柿
- 洋葱
- 大蒜
- 橄榄油
- 辣椒粉""",
            "instructions": """1. 将鸡肉炒至金黄色。

2. 加入甜椒和洋葱。

3. 拌入西红柿和辣椒粉。

4. 炖煮至蔬菜软嫩。""",
            "category": "鸡肉",
        },
        "Pollo con Mostaza": {
            "title": "芥末鸡",
            "description": "嫩鸡肉配奶香芥末汁和香草。",
            "ingredients": """- 鸡块
- 第戎芥末
- 奶油
- 白葡萄酒
- 香草
- 黄油
- 洋葱""",
            "instructions": """1. 用黄油将鸡肉煎至褐色。

2. 加入洋葱和酒。

3. 拌入芥末和奶油。

4. 炖煮至鸡肉完全熟透。""",
            "category": "鸡肉",
        },
        "Puding de Manzana": {
            "title": "苹果布丁",
            "description": "温馨的苹果布丁，配温热香料和卡仕达。",
            "ingredients": """- 苹果
- 面包
- 鸡蛋
- 牛奶
- 糖
- 肉桂
- 黄油""",
            "instructions": """1. 将切片苹果与面包层层叠叠。

2. 将鸡蛋与牛奶和糖打散。

3. 倒在苹果混合物上。

4. 烤制至金黄色并凝固。""",
            "category": "甜点",
        },
        "Puding de Pescado": {
            "title": "鱼肉布丁",
            "description": "咸味鱼肉布丁，配香草和奶油汁。",
            "ingredients": """- 鱼片
- 鸡蛋
- 奶油
- 面包屑
- 香草
- 黄油
- 柠檬""",
            "instructions": """1. 将熟鱼肉剥散。

2. 与打散的鸡蛋和奶油混合。

3. 加入香草和面包屑。

4. 在涂黄油的模具中烤制至凝固。""",
            "category": "鱼类",
        },
        "Pularda o Pollo con Manzanas": {
            "title": "苹果鸡",
            "description": "烤鸡配甜苹果和芳香香草。",
            "ingredients": """- 整鸡
- 苹果
- 洋葱
- 香草
- 黄油
- 白葡萄酒
- 肉桂""",
            "instructions": """1. 用苹果混合物塞满鸡。

2. 用黄油和香草烤制。

3. 烹饪过程中用酒刷汁。

4. 配锅汁享用。""",
            "category": "鸡肉",
        },
        "Rosada con Tomate": {
            "title": "番茄红鲷鱼",
            "description": "新鲜红鲷鱼配西红柿和地中海香草。",
            "ingredients": """- 红鲷鱼
- 西红柿
- 洋葱
- 大蒜
- 橄榄油
- 香草
- 白葡萄酒""",
            "instructions": """1. 用橄榄油炒洋葱和大蒜。

2. 加入西红柿和香草。

3. 将鱼放入汁中。

4. 煮至鱼肉软嫩。""",
            "category": "鱼类",
        },
        "Soufflé de Espárragos": {
            "title": "芦笋舒芙蕾",
            "description": "轻盈蓬松的芦笋舒芙蕾，配奶酪和香草。",
            "ingredients": """- 芦笋
- 鸡蛋
- 牛奶
- 面粉
- 黄油
- 奶酪
- 肉豆蔻""",
            "instructions": """1. 将芦笋煮至软嫩。

2. 用黄油和面粉制作白汁。

3. 加入蛋黄和芦笋。

4. 拌入打发的蛋白并烤制。""",
            "category": "蔬菜",
        },
        "Tarta Teresa Ferri": {
            "title": "特蕾莎·费里蛋糕",
            "description": "以特蕾莎·费里命名的特色蛋糕，具有独特风味。",
            "ingredients": """- 面粉
- 鸡蛋
- 糖
- 黄油
- 香草
- 发酵粉
- 特殊配料""",
            "instructions": """1. 将黄油和糖打发。

2. 加入鸡蛋和香草。

3. 拌入面粉和发酵粉。

4. 烤制至金黄色，用牙签测试。""",
            "category": "甜点",
        },
        "Tarta de Bacon y Queso": {
            "title": "培根奶酪挞",
            "description": "咸味挞，配酥脆培根和融化的奶酪。",
            "ingredients": """- 挞皮面团
- 培根
- 奶酪
- 鸡蛋
- 奶油
- 洋葱
- 香草""",
            "instructions": """1. 在挞盘中铺上挞皮。

2. 将培根煎至酥脆。

3. 将鸡蛋与奶油和奶酪打散。

4. 填入挞中烤制至凝固。""",
            "category": "其他",
        },
        "Tarta de Bicarbonato Pepica": {
            "title": "佩皮卡小苏打蛋糕",
            "description": "用小苏打制作的传统蛋糕，来自佩皮卡的传承。",
            "ingredients": """- 面粉
- 小苏打
- 鸡蛋
- 糖
- 黄油
- 牛奶
- 香草""",
            "instructions": """1. 混合干配料。

2. 将鸡蛋与糖和黄油打散。

3. 将湿料和干料混合。

4. 烤制至金黄色并发起。""",
            "category": "甜点",
        },
        "Tarta de Bicarbonato Tía Josefina": {
            "title": "约瑟菲娜阿姨的小苏打蛋糕",
            "description": "来自约瑟菲娜阿姨的小苏打蛋糕家庭配方。",
            "ingredients": """- 面粉
- 小苏打
- 鸡蛋
- 糖
- 黄油
- 牛奶
- 柠檬皮屑""",
            "instructions": """1. 将面粉与小苏打一起过筛。

2. 将黄油和糖打发。

3. 加入鸡蛋和柠檬皮屑。

4. 烤制至轻盈蓬松。""",
            "category": "甜点",
        },
        "Tarta de Carlota": {
            "title": "夏洛特蛋糕",
            "description": "优雅的夏洛特蛋糕，配蛋糕层和奶油。",
            "ingredients": """- 手指饼干
- 卡仕达奶油
- 水果
- 明胶
- 糖
- 香草
- 奶油""",
            "instructions": """1. 用手指饼干铺模具。

2. 准备明胶卡仕达奶油。

3. 与水果和奶油层层叠叠。

4. 冷藏至凝固。""",
            "category": "甜点",
        },
        "Tarta de Cebolla": {
            "title": "洋葱挞",
            "description": "咸味挞，配焦糖洋葱和香草。",
            "ingredients": """- 挞皮面团
- 洋葱
- 鸡蛋
- 奶油
- 奶酪
- 香草
- 黄油""",
            "instructions": """1. 用黄油将洋葱焦糖化。

2. 在挞盘中铺上挞皮。

3. 填入洋葱和奶油混合物。

4. 烤制至金黄色并凝固。""",
            "category": "其他",
        },
        "Tarta de Chocolate Tía Marita": {
            "title": "玛丽塔阿姨的巧克力蛋糕",
            "description": "来自玛丽塔阿姨的浓郁巧克力蛋糕，带有浓厚的可可风味。",
            "ingredients": """- 黑巧克力
- 黄油
- 糖
- 鸡蛋
- 面粉
- 可可粉
- 香草""",
            "instructions": """1. 将巧克力与黄油一起融化。

2. 将鸡蛋与糖打至蓬松。

3. 将巧克力混合物与鸡蛋混合。

4. 烤制至湿润浓郁。""",
            "category": "甜点",
        },
        "Tarta de Chocolate y Nata": {
            "title": "巧克力奶油蛋糕",
            "description": "颓废的巧克力蛋糕，配层层打发奶油。",
            "ingredients": """- 巧克力蛋糕层
- 淡奶油
- 糖
- 香草
- 巧克力碎屑
- 可可粉""",
            "instructions": """1. 准备巧克力蛋糕层。

2. 将奶油与糖和香草打发。

3. 用奶油层层叠叠蛋糕。

4. 用巧克力碎屑装饰。""",
            "category": "甜点",
        },
        "Tarta de Limón Carmela": {
            "title": "卡梅拉的柠檬蛋糕",
            "description": "来自卡梅拉的明亮酸甜柠檬蛋糕。",
            "ingredients": """- 面粉
- 柠檬
- 糖
- 鸡蛋
- 黄油
- 发酵粉
- 柠檬糖浆""",
            "instructions": """1. 将黄油和糖打发。

2. 加入鸡蛋和柠檬皮屑。

3. 拌入面粉和发酵粉。

4. 烤制并用柠檬糖浆上光。""",
            "category": "甜点",
        },
        "Tarta de Limón Pepita": {
            "title": "佩皮塔的柠檬蛋糕",
            "description": "来自佩皮塔的家庭柠檬蛋糕，带有柑橘风味。",
            "ingredients": """- 面粉
- 柠檬汁
- 糖
- 鸡蛋
- 黄油
- 柠檬皮屑
- 糖粉""",
            "instructions": """1. 将柠檬汁与糖混合。

2. 将鸡蛋与黄油打散。

3. 与面粉和柠檬皮屑混合。

4. 烤制并撒上糖粉。""",
            "category": "甜点",
        },
        "Tarta de Manzana Lolita": {
            "title": "洛丽塔的苹果蛋糕",
            "description": "来自洛丽塔的传统苹果蛋糕，配肉桂。",
            "ingredients": """- 苹果
- 面粉
- 糖
- 鸡蛋
- 黄油
- 肉桂
- 发酵粉""",
            "instructions": """1. 将苹果切片并撒上肉桂。

2. 用面粉和鸡蛋制作蛋糕面糊。

3. 拌入苹果片。

4. 烤制至金黄色并散发香气。""",
            "category": "甜点",
        },
        "Tarta de Manzana Tirol": {
            "title": "蒂罗尔苹果蛋糕",
            "description": "阿尔卑斯风味的苹果蛋糕，配坚果和香料。",
            "ingredients": """- 苹果
- 面粉
- 糖
- 鸡蛋
- 坚果
- 香料
- 黄油""",
            "instructions": """1. 准备苹果和坚果混合物。

2. 制作香料蛋糕面糊。

3. 将苹果与面糊层层叠叠。

4. 烤制至金黄色并散发香气。""",
            "category": "甜点",
        },
        "Tarta de Mermelada, Fresa y Nata": {
            "title": "果酱草莓奶油蛋糕",
            "description": "层层叠叠的蛋糕，配果酱、新鲜草莓和打发奶油。",
            "ingredients": """- 海绵蛋糕
- 草莓果酱
- 新鲜草莓
- 淡奶油
- 糖
- 香草""",
            "instructions": """1. 将海绵蛋糕切成层。

2. 在层间涂抹果酱。

3. 顶部放草莓和奶油。

4. 装饰并冷藏后享用。""",
            "category": "甜点",
        },
        "Tarta de Naranja Donat": {
            "title": "多纳特橙子蛋糕",
            "description": "柑橘橙子蛋糕，风味明亮，质地湿润。",
            "ingredients": """- 橙子
- 面粉
- 糖
- 鸡蛋
- 黄油
- 发酵粉
- 橙子糖浆""",
            "instructions": """1. 刨橙子皮并提取果汁。

2. 将黄油与糖打发。

3. 加入鸡蛋和橙子皮屑。

4. 烤制并用橙子糖浆上光。""",
            "category": "甜点",
        },
        "Tarta de Nuez": {
            "title": "核桃蛋糕",
            "description": "浓郁的核桃蛋糕，配坚果和甜奶油。",
            "ingredients": """- 核桃
- 面粉
- 糖
- 鸡蛋
- 黄油
- 香草
- 奶油""",
            "instructions": """1. 将核桃磨细。

2. 将鸡蛋与糖打至蓬松。

3. 拌入核桃和面粉。

4. 烤制并配奶油享用。""",
            "category": "甜点",
        },
        "Tarta de Piña": {
            "title": "菠萝蛋糕",
            "description": "热带菠萝蛋糕，带有甜酸风味。",
            "ingredients": """- 菠萝
- 面粉
- 糖
- 鸡蛋
- 黄油
- 发酵粉
- 香草""",
            "instructions": """1. 准备菠萝块。

2. 用面粉和鸡蛋制作蛋糕面糊。

3. 拌入菠萝。

4. 烤制至金黄色并湿润。""",
            "category": "甜点",
        },
        "Tarta de Piña y Nata": {
            "title": "菠萝奶油蛋糕",
            "description": "层层叠叠的菠萝蛋糕，配打发奶油和热带风味。",
            "ingredients": """- 菠萝蛋糕
- 淡奶油
- 糖
- 香草
- 菠萝块
- 椰丝""",
            "instructions": """1. 准备菠萝蛋糕层。

2. 将奶油与糖打发。

3. 与菠萝和奶油层层叠叠。

4. 用椰丝装饰。""",
            "category": "甜点",
        },
        "Tarta de Queso": {
            "title": "芝士蛋糕",
            "description": "奶香浓郁的芝士蛋糕，配全麦饼干底。",
            "ingredients": """- 奶油奶酪
- 糖
- 鸡蛋
- 香草
- 全麦饼干
- 黄油
- 酸奶油""",
            "instructions": """1. 制作全麦饼干底。

2. 将奶油奶酪与糖打发。

3. 加入鸡蛋和香草。

4. 烤制至凝固并冷藏。""",
            "category": "甜点",
        },
        "Tarta de Queso (Versión 2)": {
            "title": "芝士蛋糕（版本2）",
            "description": "芝士蛋糕的另一种制作方法，制作方法不同。",
            "ingredients": """- 奶油奶酪
- 糖
- 鸡蛋
- 柠檬汁
- 香草
- 饼干底
- 奶油""",
            "instructions": """1. 准备饼干底。

2. 混合奶油奶酪馅料。

3. 加入柠檬汁增加酸味。

4. 烤制并完全冷却。""",
            "category": "甜点",
        },
        "Tarta de Yogurt": {
            "title": "酸奶蛋糕",
            "description": "轻盈酸甜的酸奶蛋糕，带有柑橘风味。",
            "ingredients": """- 酸奶
- 面粉
- 糖
- 鸡蛋
- 黄油
- 柠檬皮屑
- 发酵粉""",
            "instructions": """1. 将酸奶与糖和鸡蛋混合。

2. 加入面粉和柠檬皮屑。

3. 拌入融化的黄油。

4. 烤制至轻盈蓬松。""",
            "category": "甜点",
        },
        "Ternera a la Italiana": {
            "title": "意式小牛肉",
            "description": "用意大利香草和西红柿制作的嫩小牛肉。",
            "ingredients": """- 小牛肉片
- 西红柿
- 大蒜
- 罗勒
- 橄榄油
- 白葡萄酒
- 帕尔马干酪""",
            "instructions": """1. 给小牛肉片调味。

2. 用大蒜和香草炒制。

3. 加入西红柿和酒。

4. 炖煮至软嫩后享用。""",
            "category": "肉类",
        },
        "Tortillas de Pisos": {
            "title": "层层玉米饼",
            "description": "叠层玉米饼，配馅料和汁。",
            "ingredients": """- 玉米饼
- 馅料配料
- 汁
- 奶酪
- 洋葱
- 香草
- 油""",
            "instructions": """1. 准备馅料和汁。

2. 将玉米饼与馅料层层叠叠。

3. 顶部放奶酪和汁。

4. 烤制至热透。""",
            "category": "其他",
        },
        "Trufado María Teresa": {
            "title": "玛丽亚·特蕾莎松露蛋糕",
            "description": "来自玛丽亚·特蕾莎的颓废松露蛋糕，配巧克力。",
            "ingredients": """- 黑巧克力
- 黄油
- 糖
- 鸡蛋
- 奶油
- 可可粉
- 香草""",
            "instructions": """1. 将巧克力与黄油一起融化。

2. 将鸡蛋与糖打至浓稠。

3. 将巧克力与蛋液混合。

4. 烤制并配奶油享用。""",
            "category": "甜点",
        },
    }


def generate_chinese_recipe_translations():
    """Generate Chinese translations for all recipes."""
    print("正在初始化数据库...")
    init_database()

    print("正在获取所有食谱...")
    recipes = get_all_recipes()

    print(f"找到 {len(recipes)} 个食谱需要翻译成中文。")

    translations = get_chinese_recipe_translations()

    translated_count = 0
    updated_count = 0

    for recipe in recipes:
        print(f"正在处理食谱：{recipe['title']}")

        # Check if translation already exists
        existing_translation = get_recipe_translation(recipe["id"], "zh")

        if existing_translation:
            print("  - 翻译已存在，正在更新为中文翻译...")
            updated_count += 1
        else:
            print("  - 正在创建新的中文翻译...")
            translated_count += 1

        # Get Chinese translation
        if recipe["title"] in translations:
            translation = translations[recipe["title"]]
        else:
            # For any recipe not in our complete list, use basic category translation
            translation = {
                "title": recipe["title"],
                "description": recipe["description"],
                "ingredients": recipe["ingredients"],
                "instructions": recipe["instructions"],
                "category": CATEGORY_TRANSLATIONS.get(
                    recipe["category"], recipe["category"]
                ),
            }
            print(f"  - 对 {recipe['title']} 使用基本翻译")

        # Save translation
        save_recipe_translation(
            recipe["id"],
            "zh",
            translation["title"],
            translation["description"],
            translation["ingredients"],
            translation["instructions"],
            translation["category"],
        )

        print("  - 中文翻译保存成功")

    print("\n中文翻译完成！")
    print(f"  - 新翻译：{translated_count}")
    print(f"  - 更新翻译：{updated_count}")
    print(f"  - 总食谱数：{len(recipes)}")


if __name__ == "__main__":
    generate_chinese_recipe_translations()
