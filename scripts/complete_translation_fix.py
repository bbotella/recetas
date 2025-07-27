#!/usr/bin/env python3
"""
Script para corregir COMPLETAMENTE las traducciones problemáticas.
Este script reemplaza completamente las traducciones con contenido mixto
con traducciones completamente en el idioma objetivo.
"""

import os
import sys
import re

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database  # noqa: E402


def identify_mixed_language_translations():
    """Identifica traducciones que contienen contenido mixto de idiomas."""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtener todas las traducciones
    cursor.execute("""
        SELECT id, recipe_id, language, title, description, ingredients, instructions
        FROM recipe_translations
        WHERE language IN ('en', 'zh', 'ca', 'eu')
    """)
    
    translations = cursor.fetchall()
    problematic_translations = []
    
    for translation in translations:
        trans_id, recipe_id, language, title, description, ingredients, instructions = translation
        
        # Verificar si tiene contenido mixto
        is_problematic = False
        
        # Verificar patrones de contenido mixto
        mixed_patterns = [
            r'Traditional Spanish family recipe:',
            r'Discover the culinary magic of .* asados en',
            r'发现.* asados en .*的烹饪魔力',
            r'Descobreix la màgia culinària de .* asados en',
            r'Deskubritu .* asados en .*ren magia',
            r'Wine-Roasted Herrings.*asados en',
            r'Special traditional recipe:',
            r'Recepta especial valenciana:',
            r'Euskal sukaldaritzako errezeta berezia:',
            r'特色传统食谱：',
            r'.*wine.*asados.*',
            r'.*ardoa.*asados.*',
            r'.*vi.*asados.*',
            r'.*酒.*asados.*',
            # Detectar mezclas de idiomas
            r'[a-zA-Z]+\s+asados\s+en\s+[a-zA-Z]+',
            r'[一-龯]+\s+asados\s+en\s+[一-龯]+',
        ]
        
        for pattern in mixed_patterns:
            if re.search(pattern, description, re.IGNORECASE) or \
               re.search(pattern, ingredients, re.IGNORECASE) or \
               re.search(pattern, instructions, re.IGNORECASE):
                is_problematic = True
                break
        
        if is_problematic:
            problematic_translations.append(translation)
    
    conn.close()
    
    print(f"🔍 Found {len(problematic_translations)} translations with mixed language content")
    return problematic_translations


def get_original_recipe(recipe_id):
    """Obtiene la receta original en español."""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title, description, ingredients, instructions, category
        FROM recipes WHERE id = ?
    """, [recipe_id])
    
    recipe = cursor.fetchone()
    conn.close()
    
    return recipe


def generate_complete_replacement_translation(original_recipe, target_lang):
    """Genera una traducción completamente nueva basada en la receta original."""
    
    if not original_recipe:
        return None
    
    original_title, original_description, original_ingredients, original_instructions, original_category = original_recipe
    
    # Obtener traducciones específicas basadas en el título
    if target_lang == 'en':
        return generate_english_translation(original_title, original_description, original_ingredients, original_instructions, original_category)
    elif target_lang == 'zh':
        return generate_chinese_translation(original_title, original_description, original_ingredients, original_instructions, original_category)
    elif target_lang == 'ca':
        return generate_catalan_translation(original_title, original_description, original_ingredients, original_instructions, original_category)
    elif target_lang == 'eu':
        return generate_basque_translation(original_title, original_description, original_ingredients, original_instructions, original_category)
    
    return None


def generate_english_translation(title, description, ingredients, instructions, category):
    """Genera traducciones completamente en inglés."""
    
    # Traducciones específicas de títulos
    title_translations = {
        "Alcachofas Rellenas": "Stuffed Artichokes",
        "Arenques Asados en Vino": "Wine-Roasted Herrings",
        "Batido de Coco": "Coconut Smoothie",
        "Batido de Limón o Naranja": "Lemon or Orange Smoothie",
        "Batido de Plátano": "Banana Smoothie",
        "Bizcocho y Tortada": "Sponge Cake and Tortada",
        "Budin de Merluza": "Hake Pudding",
        "Calamares en su Tinta Dana-Ona": "Squid in Their Ink Dana-Ona",
        "Canelones en Salsa de Queso": "Cannelloni in Cheese Sauce",
        "Chocolate para Adorno a Baño": "Decorating Chocolate",
        "Cocktail de Tomate": "Tomato Cocktail",
        "Corona de Cordero": "Crown of Lamb",
        "Crema Pastelera": "Pastry Cream",
        "Crema de Chocolate": "Chocolate Cream",
        "Crepes": "Crepes",
        "Emparedados de Merluza": "Hake Sandwiches",
        "Espinacas a la Crema": "Creamed Spinach",
        "Faisán a la Belga": "Belgian-Style Pheasant",
        "Flan de Coco": "Coconut Flan",
        "Helado de Fresa": "Strawberry Ice Cream",
        "Helado de Coco": "Coconut Ice Cream",
        "Huevos al Curry": "Curry Eggs",
        "Lenguado Relleno de Gambas y Champiñones": "Sole Stuffed with Shrimp and Mushrooms",
        "Manzanas Asadas": "Baked Apples",
        "Mus de Pollo": "Chicken Mousse",
        "Paté de Pollo": "Chicken Pâté",
        "Pescado al Horno con Vino": "Baked Fish with Wine",
        "Pinchito Dana-Ona": "Dana-Ona Skewers",
        "Pizza Napolitana": "Neapolitan Pizza",
        "Pollo Marengo": "Chicken Marengo",
        "Pollo a la Vasca": "Basque-Style Chicken",
        "Puding de Pescado": "Fish Pudding",
        "Rosada con Tomate": "Red Mullet with Tomato",
        "Soufflé de Espárragos": "Asparagus Soufflé",
        "Tarta de Queso": "Cheese Cake",
        "Tarta de Chocolate": "Chocolate Cake",
        "Tarta de Limón": "Lemon Tart",
        "Tarta de Manzana": "Apple Tart",
    }
    
    # Descripciones específicas completamente en inglés
    description_translations = {
        "Arenques Asados en Vino": "Discover the exquisite flavors of wine-roasted herrings, where the delicate fish is enhanced by the rich complexity of wine. This traditional recipe transforms simple ingredients into an elegant dish that showcases the perfect marriage between seafood and wine.",
        "Alcachofas Rellenas": "Immerse yourself in the fascinating world of stuffed artichokes, where the juiciness of the meat merges with an incomparable blend of flavors and aromas. This recipe combines tradition and innovation, creating a dish that melts in your mouth.",
        "Batido de Coco": "This coconut smoothie is an escape to tropical paradise, a perfect combination of sweet coconut flavor and creamy texture. It's the perfect refresher for hot summer days.",
        "Pollo Marengo": "Discover the culinary magic of Chicken Marengo, where classic flavors and modern techniques meet to create an exceptional dish combining tradition and innovation.",
        "Tarta de Queso": "This cheese cake is our family's most treasured recipe, made with secrets and love passed down from generation to generation.",
        "Corona de Cordero": "This crown of lamb is the pride of celebratory dining, where the juiciness of the meat combines with complex flavors specially designed for special occasions.",
    }
    
    # Traducir título
    translated_title = title_translations.get(title, title)
    
    # Traducir descripción
    translated_description = description_translations.get(title, f"A traditional Spanish family recipe for {translated_title.lower()}.")
    
    # Traducir ingredientes
    translated_ingredients = translate_ingredients_to_english(ingredients)
    
    # Traducir instrucciones
    translated_instructions = translate_instructions_to_english(instructions)
    
    # Traducir categoría
    category_translations = {
        "Postres": "Desserts",
        "Bebidas": "Drinks",
        "Pollo": "Chicken",
        "Pescado": "Fish",
        "Carnes": "Meat",
        "Verduras": "Vegetables",
        "Otros": "Others",
    }
    translated_category = category_translations.get(category, category)
    
    return {
        "title": translated_title,
        "description": translated_description,
        "ingredients": translated_ingredients,
        "instructions": translated_instructions,
        "category": translated_category,
    }


def translate_ingredients_to_english(ingredients):
    """Traduce ingredientes completamente al inglés."""
    
    ingredient_map = {
        "Alcachofas": "Artichokes",
        "Arenques": "Herrings",
        "Sal": "Salt",
        "Aceite": "Oil",
        "Cebolla": "Onion",
        "Ajo": "Garlic",
        "Tomate": "Tomato",
        "Perejil": "Parsley",
        "Huevos": "Eggs",
        "Harina": "Flour",
        "Leche": "Milk",
        "Mantequilla": "Butter",
        "Azúcar": "Sugar",
        "Agua": "Water",
        "Vino": "Wine",
        "Vino blanco": "White wine",
        "Vino tinto": "Red wine",
        "Patatas": "Potatoes",
        "Arroz": "Rice",
        "Pollo": "Chicken",
        "Pescado": "Fish",
        "Carne": "Meat",
        "Queso": "Cheese",
        "Limón": "Lemon",
        "Naranja": "Orange",
        "Merluza": "Hake",
        "Gambas": "Shrimp",
        "Champiñones": "Mushrooms",
        "Espinacas": "Spinach",
        "Nata": "Cream",
        "Cordero": "Lamb",
        "Faisán": "Pheasant",
        "Endivias": "Endives",
        "Manteca": "Lard",
        "Jamón": "Ham",
        "Especias": "Spices",
        "Bechamel": "Bechamel sauce",
        "Coco": "Coconut",
        "Plátano": "Banana",
        "Fresas": "Strawberries",
        "Chocolate": "Chocolate",
        "Manzanas": "Apples",
        "Canela": "Cinnamon",
        "gramos": "grams",
        "litros": "liters",
        "cucharadas": "tablespoons",
        "cucharaditas": "teaspoons",
        "tazas": "cups",
        "piezas": "pieces",
        "dientes": "cloves",
        "rebanadas": "slices",
    }
    
    translated = ingredients
    for spanish, english in ingredient_map.items():
        translated = translated.replace(spanish, english)
    
    return translated


def translate_instructions_to_english(instructions):
    """Traduce instrucciones completamente al inglés."""
    
    instruction_map = {
        "Se cuecen": "Cook",
        "Se rellenan": "Stuff",
        "Se cortan": "Cut",
        "Se fríe": "Fry",
        "Se fríen": "Fry",
        "Se mezcla": "Mix",
        "Se mezclan": "Mix",
        "Se añade": "Add",
        "Se añaden": "Add",
        "Se sirve": "Serve",
        "Se sirven": "Serve",
        "Se pone": "Put",
        "Se ponen": "Put",
        "Se hace": "Make",
        "Se hacen": "Make",
        "Se bate": "Beat",
        "Se baten": "Beat",
        "Se calienta": "Heat",
        "Se calientan": "Heat",
        "Se derrite": "Melt",
        "Se derriten": "Melt",
        "Se deja": "Leave",
        "Se dejan": "Leave",
        "Se quita": "Remove",
        "Se quitan": "Remove",
        "Se pela": "Peel",
        "Se pelan": "Peel",
        "Se pica": "Chop",
        "Se pican": "Chop",
        "Se ralla": "Grate",
        "Se rallan": "Grate",
        "Se asa": "Roast",
        "Se asan": "Roast",
        "Se cuece": "Cook",
        "caliente": "hot",
        "frío": "cold",
        "tibio": "warm",
        "minutos": "minutes",
        "horas": "hours",
        "hora": "hour",
        "hasta que": "until",
        "luego": "then",
        "después": "after",
        "mientras": "while",
        "finalmente": "finally",
        "al horno": "in the oven",
        "al fuego": "on the fire",
        "a fuego lento": "over low heat",
        "a fuego medio": "over medium heat",
        "a fuego alto": "over high heat",
        "en la sartén": "in the pan",
        "en el horno": "in the oven",
    }
    
    translated = instructions
    for spanish, english in instruction_map.items():
        translated = translated.replace(spanish, english)
    
    return translated


def generate_chinese_translation(title, description, ingredients, instructions, category):
    """Genera traducciones completamente en chino."""
    
    title_translations = {
        "Alcachofas Rellenas": "酿朝鲜蓟",
        "Arenques Asados en Vino": "红酒烤鲱鱼",
        "Batido de Coco": "椰子奶昔",
        "Batido de Limón o Naranja": "柠檬或橙子奶昔",
        "Batido de Plátano": "香蕉奶昔",
        "Bizcocho y Tortada": "海绵蛋糕和玉米饼",
        "Budin de Merluza": "鳕鱼布丁",
        "Calamares en su Tinta Dana-Ona": "墨鱼汁鱿鱼",
        "Canelones en Salsa de Queso": "奶酪酱通心粉",
        "Chocolate para Adorno a Baño": "装饰巧克力",
        "Cocktail de Tomate": "番茄鸡尾酒",
        "Corona de Cordero": "羊肉花环",
        "Crema Pastelera": "卡仕达酱",
        "Crema de Chocolate": "巧克力奶油",
        "Crepes": "可丽饼",
        "Emparedados de Merluza": "鳕鱼三明治",
        "Espinacas a la Crema": "奶油菠菜",
        "Faisán a la Belga": "比利时野鸡",
        "Flan de Coco": "椰子布丁",
        "Helado de Fresa": "草莓冰淇淋",
        "Helado de Coco": "椰子冰淇淋",
        "Huevos al Curry": "咖喱鸡蛋",
        "Lenguado Relleno de Gambas y Champiñones": "虾仁蘑菇酿比目鱼",
        "Manzanas Asadas": "烤苹果",
        "Mus de Pollo": "鸡肉慕斯",
        "Paté de Pollo": "鸡肉酱",
        "Pescado al Horno con Vino": "红酒烤鱼",
        "Pinchito Dana-Ona": "西班牙串烧",
        "Pizza Napolitana": "那不勒斯披萨",
        "Pollo Marengo": "马伦戈鸡",
        "Pollo a la Vasca": "巴斯克鸡",
        "Puding de Pescado": "鱼布丁",
        "Rosada con Tomate": "番茄红鲻鱼",
        "Soufflé de Espárragos": "芦笋舒芙蕾",
        "Tarta de Queso": "芝士蛋糕",
        "Tarta de Chocolate": "巧克力蛋糕",
        "Tarta de Limón": "柠檬塔",
        "Tarta de Manzana": "苹果塔",
    }
    
    description_translations = {
        "Arenques Asados en Vino": "发现红酒烤鲱鱼的精致风味，精美的鱼肉在丰富复杂的酒香中得到升华。这道传统食谱将简单的食材转化为优雅的菜肴，展现了海鲜与酒类的完美结合。",
        "Alcachofas Rellenas": "沉浸在酿朝鲜蓟的迷人世界中，肉质的鲜美与无与伦比的风味和香气融合。这个食谱结合了传统与创新，创造出一道入口即化的菜肴。",
        "Batido de Coco": "这款椰子奶昔是逃往热带天堂的完美选择，甜美椰子风味与奶油质地的完美结合。它是炎热夏日的完美清凉剂。",
        "Pollo Marengo": "发现马伦戈鸡的烹饪魔力，经典风味与现代技术相遇，创造出一道结合传统与创新的非凡菜肴。",
        "Tarta de Queso": "这个芝士蛋糕是我们家族最珍贵的食谱，用代代相传的秘密和爱心制作。",
        "Corona de Cordero": "这个羊肉花环是庆祝餐桌的骄傲，肉质的鲜美与复杂的风味相结合，专为特殊场合设计。",
    }
    
    translated_title = title_translations.get(title, title)
    translated_description = description_translations.get(title, f"传统西班牙家庭{translated_title}食谱。")
    translated_ingredients = translate_ingredients_to_chinese(ingredients)
    translated_instructions = translate_instructions_to_chinese(instructions)
    
    category_translations = {
        "Postres": "甜点",
        "Bebidas": "饮料",
        "Pollo": "鸡肉",
        "Pescado": "鱼类",
        "Carnes": "肉类",
        "Verduras": "蔬菜",
        "Otros": "其他",
    }
    translated_category = category_translations.get(category, category)
    
    return {
        "title": translated_title,
        "description": translated_description,
        "ingredients": translated_ingredients,
        "instructions": translated_instructions,
        "category": translated_category,
    }


def translate_ingredients_to_chinese(ingredients):
    """Traduce ingredientes completamente al chino."""
    
    ingredient_map = {
        "Alcachofas": "朝鲜蓟",
        "Arenques": "鲱鱼",
        "Sal": "盐",
        "Aceite": "油",
        "Cebolla": "洋葱",
        "Ajo": "大蒜",
        "Tomate": "番茄",
        "Perejil": "欧芹",
        "Huevos": "鸡蛋",
        "Harina": "面粉",
        "Leche": "牛奶",
        "Mantequilla": "黄油",
        "Azúcar": "糖",
        "Agua": "水",
        "Vino": "酒",
        "Vino blanco": "白酒",
        "Vino tinto": "红酒",
        "Patatas": "土豆",
        "Arroz": "米饭",
        "Pollo": "鸡肉",
        "Pescado": "鱼",
        "Carne": "肉",
        "Queso": "奶酪",
        "Limón": "柠檬",
        "Naranja": "橙子",
        "Merluza": "鳕鱼",
        "Gambas": "虾",
        "Champiñones": "蘑菇",
        "Espinacas": "菠菜",
        "Nata": "奶油",
        "Cordero": "羊肉",
        "Faisán": "野鸡",
        "Endivias": "菊苣",
        "Manteca": "猪油",
        "Jamón": "火腿",
        "Especias": "香料",
        "Bechamel": "白酱",
        "Coco": "椰子",
        "Plátano": "香蕉",
        "Fresas": "草莓",
        "Chocolate": "巧克力",
        "Manzanas": "苹果",
        "Canela": "肉桂",
        "gramos": "克",
        "litros": "升",
        "cucharadas": "汤匙",
        "cucharaditas": "茶匙",
        "tazas": "杯",
        "piezas": "个",
        "dientes": "瓣",
        "rebanadas": "片",
    }
    
    translated = ingredients
    for spanish, chinese in ingredient_map.items():
        translated = translated.replace(spanish, chinese)
    
    return translated


def translate_instructions_to_chinese(instructions):
    """Traduce instrucciones completamente al chino."""
    
    instruction_map = {
        "Se cuecen": "煮",
        "Se rellenan": "填充",
        "Se cortan": "切",
        "Se fríe": "炒",
        "Se fríen": "炒",
        "Se mezcla": "混合",
        "Se mezclan": "混合",
        "Se añade": "加入",
        "Se añaden": "加入",
        "Se sirve": "上菜",
        "Se sirven": "上菜",
        "Se pone": "放入",
        "Se ponen": "放入",
        "Se hace": "制作",
        "Se hacen": "制作",
        "Se bate": "搅拌",
        "Se baten": "搅拌",
        "Se calienta": "加热",
        "Se calientan": "加热",
        "Se derrite": "融化",
        "Se derriten": "融化",
        "Se deja": "放置",
        "Se dejan": "放置",
        "Se quita": "取出",
        "Se quitan": "取出",
        "Se pela": "去皮",
        "Se pelan": "去皮",
        "Se pica": "切碎",
        "Se pican": "切碎",
        "Se ralla": "磨碎",
        "Se rallan": "磨碎",
        "Se asa": "烤",
        "Se asan": "烤",
        "Se cuece": "煮",
        "caliente": "热",
        "frío": "冷",
        "tibio": "温",
        "minutos": "分钟",
        "horas": "小时",
        "hora": "小时",
        "hasta que": "直到",
        "luego": "然后",
        "después": "之后",
        "mientras": "同时",
        "finalmente": "最后",
        "al horno": "在烤箱中",
        "al fuego": "在火上",
        "a fuego lento": "小火",
        "a fuego medio": "中火",
        "a fuego alto": "大火",
        "en la sartén": "在平底锅中",
        "en el horno": "在烤箱中",
    }
    
    translated = instructions
    for spanish, chinese in instruction_map.items():
        translated = translated.replace(spanish, chinese)
    
    return translated


def generate_catalan_translation(title, description, ingredients, instructions, category):
    """Genera traducciones completamente en catalán."""
    
    title_translations = {
        "Alcachofas Rellenas": "Carxofes Farcides",
        "Arenques Asados en Vino": "Arencs Rostits en Vi",
        "Batido de Coco": "Batut de Coco",
        "Batido de Limón o Naranja": "Batut de Llimó o Taronja",
        "Batido de Plátano": "Batut de Plàtan",
        "Bizcocho y Tortada": "Biscuit i Tortada",
        "Budin de Merluza": "Budin de Lluç",
        "Calamares en su Tinta Dana-Ona": "Calamars en la seva Tinta Dana-Ona",
        "Canelones en Salsa de Queso": "Canelons en Salsa de Formatge",
        "Chocolate para Adorno a Baño": "Xocolata per a Decorar",
        "Cocktail de Tomate": "Còctel de Tomàquet",
        "Corona de Cordero": "Corona de Xai",
        "Crema Pastelera": "Crema Pastissera",
        "Crema de Chocolate": "Crema de Xocolata",
        "Crepes": "Crepes",
        "Emparedados de Merluza": "Entrepans de Lluç",
        "Espinacas a la Crema": "Espinacs a la Crema",
        "Faisán a la Belga": "Faisà a la Belga",
        "Flan de Coco": "Flam de Coco",
        "Helado de Fresa": "Gelat de Maduixa",
        "Helado de Coco": "Gelat de Coco",
        "Huevos al Curry": "Ous al Curry",
        "Lenguado Relleno de Gambas y Champiñones": "Llenguado Farcit de Gambes i Xampinyons",
        "Manzanas Asadas": "Pomes Rostides",
        "Mus de Pollo": "Mus de Pollastre",
        "Paté de Pollo": "Paté de Pollastre",
        "Pescado al Horno con Vino": "Peix al Forn amb Vi",
        "Pinchito Dana-Ona": "Pinchos Dana-Ona",
        "Pizza Napolitana": "Pizza Napolitana",
        "Pollo Marengo": "Pollastre Marengo",
        "Pollo a la Vasca": "Pollastre a la Basca",
        "Puding de Pescado": "Puding de Peix",
        "Rosada con Tomate": "Rosada amb Tomàquet",
        "Soufflé de Espárragos": "Soufflé d'Espàrrecs",
        "Tarta de Queso": "Tarta de Formatge",
        "Tarta de Chocolate": "Tarta de Xocolata",
        "Tarta de Limón": "Tarta de Llimó",
        "Tarta de Manzana": "Tarta de Poma",
    }
    
    description_translations = {
        "Arenques Asados en Vino": "Descobreix els sabors exquisits dels arencs rostits en vi, on el peix delicat s'intensifica amb la complexitat rica del vi. Aquesta recepta tradicional transforma ingredients simples en un plat elegant que mostra el matrimoni perfecte entre marisc i vi.",
        "Alcachofas Rellenas": "Submergeix-te en el fascinant món de les carxofes farcides, on la sucositat de la carn es fusiona amb una barreja incomparable de sabors i aromes. Aquesta recepta combina tradició i innovació.",
        "Batido de Coco": "Aquest batut de coco és una escapada al paradís tropical, una combinació perfecta del sabor dolç del coco i una textura cremosa. És el refrescant perfecte per als dies càlids d'estiu.",
        "Pollo Marengo": "Descobreix la màgia culinària del pollastre Marengo, on els sabors clàssics i les tècniques modernes es troben per crear un plat excepcional que combina tradició i innovació.",
        "Tarta de Queso": "Aquesta tarta de formatge és la recepta més preuada de la nostra família, feta amb secrets i amor transmesos de generació en generació.",
        "Corona de Cordero": "Aquesta corona de xai és l'orgull del menjar de celebració, on la jugositat de la carn es combina amb sabors complexos especialment dissenyats per a ocasions especials.",
    }
    
    translated_title = title_translations.get(title, title)
    translated_description = description_translations.get(title, f"Recepta tradicional valenciana de {translated_title.lower()}.")
    translated_ingredients = translate_ingredients_to_catalan(ingredients)
    translated_instructions = translate_instructions_to_catalan(instructions)
    
    category_translations = {
        "Postres": "Postres",
        "Bebidas": "Begudes",
        "Pollo": "Pollastre",
        "Pescado": "Peix",
        "Carnes": "Carns",
        "Verduras": "Verdures",
        "Otros": "Altres",
    }
    translated_category = category_translations.get(category, category)
    
    return {
        "title": translated_title,
        "description": translated_description,
        "ingredients": translated_ingredients,
        "instructions": translated_instructions,
        "category": translated_category,
    }


def translate_ingredients_to_catalan(ingredients):
    """Traduce ingredientes completamente al catalán."""
    
    ingredient_map = {
        "Alcachofas": "Carxofes",
        "Arenques": "Arencs",
        "Sal": "Sal",
        "Aceite": "Oli",
        "Cebolla": "Ceba",
        "Ajo": "All",
        "Tomate": "Tomàquet",
        "Perejil": "Julivert",
        "Huevos": "Ous",
        "Harina": "Farina",
        "Leche": "Llet",
        "Mantequilla": "Mantega",
        "Azúcar": "Sucre",
        "Agua": "Aigua",
        "Vino": "Vi",
        "Vino blanco": "Vi blanc",
        "Vino tinto": "Vi negre",
        "Patatas": "Patates",
        "Arroz": "Arròs",
        "Pollo": "Pollastre",
        "Pescado": "Peix",
        "Carne": "Carn",
        "Queso": "Formatge",
        "Limón": "Llimó",
        "Naranja": "Taronja",
        "Merluza": "Lluç",
        "Gambas": "Gambes",
        "Champiñones": "Xampinyons",
        "Espinacas": "Espinacs",
        "Nata": "Nata",
        "Cordero": "Xai",
        "Faisán": "Faisà",
        "Endivias": "Endívies",
        "Manteca": "Llard",
        "Jamón": "Pernil",
        "Especias": "Espècies",
        "Bechamel": "Bechamel",
        "Coco": "Coco",
        "Plátano": "Plàtan",
        "Fresas": "Maduixes",
        "Chocolate": "Xocolata",
        "Manzanas": "Pomes",
        "Canela": "Canyella",
        "gramos": "grams",
        "litros": "litres",
        "cucharadas": "culleradetes",
        "cucharaditas": "culleradetes",
        "tazas": "tasses",
        "piezas": "peces",
        "dientes": "dents",
        "rebanadas": "rodanxes",
    }
    
    translated = ingredients
    for spanish, catalan in ingredient_map.items():
        translated = translated.replace(spanish, catalan)
    
    return translated


def translate_instructions_to_catalan(instructions):
    """Traduce instrucciones completamente al catalán."""
    
    instruction_map = {
        "Se cuecen": "Es couen",
        "Se rellenan": "Es farceixen",
        "Se cortan": "Es tallen",
        "Se fríe": "Es fregeix",
        "Se fríen": "Es fregeixen",
        "Se mezcla": "Es barreja",
        "Se mezclan": "Es barregen",
        "Se añade": "S'afegeix",
        "Se añaden": "S'afegeixen",
        "Se sirve": "Es serveix",
        "Se sirven": "Es serveixen",
        "Se pone": "Es posa",
        "Se ponen": "Es posen",
        "Se hace": "Es fa",
        "Se hacen": "Es fan",
        "Se bate": "Es bat",
        "Se baten": "Es baten",
        "Se calienta": "Es calenta",
        "Se calientan": "Es calfan",
        "Se derrite": "Es desfà",
        "Se derriten": "Es desfan",
        "Se deja": "Es deixa",
        "Se dejan": "Es deixen",
        "Se quita": "Es treu",
        "Se quitan": "Es treuen",
        "Se pela": "Es pela",
        "Se pelan": "Es pelen",
        "Se pica": "Es pica",
        "Se pican": "Es piquen",
        "Se ralla": "Es ratlla",
        "Se rallan": "Es ratllen",
        "Se asa": "Es rosta",
        "Se asan": "Es rosten",
        "Se cuece": "Es cou",
        "caliente": "calent",
        "frío": "fred",
        "tibio": "tebi",
        "minutos": "minuts",
        "horas": "hores",
        "hora": "hora",
        "hasta que": "fins que",
        "luego": "després",
        "después": "després",
        "mientras": "mentre",
        "finalmente": "finalment",
        "al horno": "al forn",
        "al fuego": "al foc",
        "a fuego lento": "a foc lent",
        "a fuego medio": "a foc mitjà",
        "a fuego alto": "a foc fort",
        "en la sartén": "a la paella",
        "en el horno": "al forn",
    }
    
    translated = instructions
    for spanish, catalan in instruction_map.items():
        translated = translated.replace(spanish, catalan)
    
    return translated


def generate_basque_translation(title, description, ingredients, instructions, category):
    """Genera traducciones completamente en euskera."""
    
    title_translations = {
        "Alcachofas Rellenas": "Artxindurriak Beterik",
        "Arenques Asados en Vino": "Arenke Errea Ardoan",
        "Batido de Coco": "Koko Irabiagaia",
        "Batido de Limón o Naranja": "Limoi edo Laranja Irabiagaia",
        "Batido de Plátano": "Platano Irabiagaia",
        "Bizcocho y Tortada": "Bizkoitza eta Tortada",
        "Budin de Merluza": "Legatza Budina",
        "Calamares en su Tinta Dana-Ona": "Txipiroi Tinta Beltzean Dana-Ona",
        "Canelones en Salsa de Queso": "Kaneloiak Gazta Saltsan",
        "Chocolate para Adorno a Baño": "Apaintze Txokolatea",
        "Cocktail de Tomate": "Tomate Cocktail",
        "Corona de Cordero": "Bildots Corona",
        "Crema Pastelera": "Pasteleria Krema",
        "Crema de Chocolate": "Txokolate Krema",
        "Crepes": "Krep",
        "Emparedados de Merluza": "Legatza Entrepanak",
        "Espinacas a la Crema": "Espinakak Kremarekin",
        "Faisán a la Belga": "Faisan Belgikarra",
        "Flan de Coco": "Koko Flana",
        "Helado de Fresa": "Marrubi Izozkia",
        "Helado de Coco": "Koko Izozkia",
        "Huevos al Curry": "Arrautzak Curryarekin",
        "Lenguado Relleno de Gambas y Champiñones": "Lenguado Izkira eta Perretxikoekin Betea",
        "Manzanas Asadas": "Sagar Erretuak",
        "Mus de Pollo": "Oilasko Musa",
        "Paté de Pollo": "Oilasko Patea",
        "Pescado al Horno con Vino": "Arraña Labetan Ardoarekin",
        "Pinchito Dana-Ona": "Pintxo Dana-Ona",
        "Pizza Napolitana": "Pizza Napolitarra",
        "Pollo Marengo": "Oilasko Marengo",
        "Pollo a la Vasca": "Oilasko Euskalduna",
        "Puding de Pescado": "Arraina Budina",
        "Rosada con Tomate": "Rosada Tomatearekin",
        "Soufflé de Espárragos": "Esparrago Soufflea",
        "Tarta de Queso": "Gazta Tarta",
        "Tarta de Chocolate": "Txokolate Tarta",
        "Tarta de Limón": "Limoi Tarta",
        "Tarta de Manzana": "Sagar Tarta",
    }
    
    description_translations = {
        "Arenques Asados en Vino": "Deskubritu ardoan erretako arenkeen zapore ezin hobeak, non arrain delikatuak ardoaren konplexutasun aberatsarekin indartu den. Errezeta tradizional honek osagai sinpleak plater elegante batean bihurtzen ditu, itsas janarien eta ardoaren ezkontzaren perfektua erakutsiz.",
        "Alcachofas Rellenas": "Sumergitu artxindurri beteak munduan, non haragiaren zukutasuna zapore eta usain nahasketa ezin hobearekin bat egiten duen. Errezeta honek tradizio eta berrikuntza konbinatzen ditu.",
        "Batido de Coco": "Koko irabiagai hau paradisu tropikalerako ihes bide bat da, koko zapore gozo eta testura krematsuen konbinazio perfektua. Udako egun beroentzako freskagarri ezin hobea da.",
        "Pollo Marengo": "Deskubritu Marengo oilaskoaren magia kulinarioa, non zapore klasikoak eta teknika modernoak elkar topo egiten duten tradizio eta berrikuntza konbinatzen duen plater ezin hobea sortzeko.",
        "Tarta de Queso": "Gazta tarta hau gure familiaren errezeta preziatuena da, belaunaldiz belaunaldi transmititako sekretu eta maitasunez egina.",
        "Corona de Cordero": "Bildots corona hau ospakizuneko jatorraren harro da, non haragiaren zukutasuna zapore konplexuekin uztartzen den okasio berezietarako bereziki diseinatua.",
    }
    
    translated_title = title_translations.get(title, title)
    translated_description = description_translations.get(title, f"Euskal sukaldaritzako {translated_title.lower()}ren errezeta tradizionala.")
    translated_ingredients = translate_ingredients_to_basque(ingredients)
    translated_instructions = translate_instructions_to_basque(instructions)
    
    category_translations = {
        "Postres": "Postrea",
        "Bebidas": "Edariak",
        "Pollo": "Oilaskoa",
        "Pescado": "Arraina",
        "Carnes": "Haragiak",
        "Verduras": "Barazkiak",
        "Otros": "Besteak",
    }
    translated_category = category_translations.get(category, category)
    
    return {
        "title": translated_title,
        "description": translated_description,
        "ingredients": translated_ingredients,
        "instructions": translated_instructions,
        "category": translated_category,
    }


def translate_ingredients_to_basque(ingredients):
    """Traduce ingredientes completamente al euskera."""
    
    ingredient_map = {
        "Alcachofas": "Artxindurriak",
        "Arenques": "Arenkeak",
        "Sal": "Gatza",
        "Aceite": "Olioa",
        "Cebolla": "Tipula",
        "Ajo": "Baratxuria",
        "Tomate": "Tomatea",
        "Perejil": "Perrexila",
        "Huevos": "Arrautzak",
        "Harina": "Irina",
        "Leche": "Esnea",
        "Mantequilla": "Gurina",
        "Azúcar": "Azukrea",
        "Agua": "Ura",
        "Vino": "Ardoa",
        "Vino blanco": "Ardo txuria",
        "Vino tinto": "Ardo gorria",
        "Patatas": "Patatас",
        "Arroz": "Arroza",
        "Pollo": "Oilaskoa",
        "Pescado": "Arraina",
        "Carne": "Haragia",
        "Queso": "Gazta",
        "Limón": "Limoia",
        "Naranja": "Laranja",
        "Merluza": "Legatza",
        "Gambas": "Izkira",
        "Champiñones": "Perretxikoak",
        "Espinacas": "Espinakak",
        "Nata": "Nata",
        "Cordero": "Bildotsa",
        "Faisán": "Faisana",
        "Endivias": "Endibiak",
        "Manteca": "Txerri-koipea",
        "Jamón": "Urdaiazpikoa",
        "Especias": "Kondairua",
        "Bechamel": "Betxamel",
        "Coco": "Kokoa",
        "Plátano": "Platanoa",
        "Fresas": "Marrubiak",
        "Chocolate": "Txokolatea",
        "Manzanas": "Sagarrak",
        "Canela": "Kanela",
        "gramos": "gramo",
        "litros": "litro",
        "cucharadas": "koilarakada",
        "cucharaditas": "koilarakada txiki",
        "tazas": "katilu",
        "piezas": "ale",
        "dientes": "ale",
        "rebanadas": "xerrak",
    }
    
    translated = ingredients
    for spanish, basque in ingredient_map.items():
        translated = translated.replace(spanish, basque)
    
    return translated


def translate_instructions_to_basque(instructions):
    """Traduce instrucciones completamente al euskera."""
    
    instruction_map = {
        "Se cuecen": "Egosi",
        "Se rellenan": "Bete",
        "Se cortan": "Ebaki",
        "Se fríe": "Frijitu",
        "Se fríen": "Frijitu",
        "Se mezcla": "Nahastu",
        "Se mezclan": "Nahastu",
        "Se añade": "Gehitu",
        "Se añaden": "Gehitu",
        "Se sirve": "Zerbitzatu",
        "Se sirven": "Zerbitzatu",
        "Se pone": "Jarri",
        "Se ponen": "Jarri",
        "Se hace": "Egin",
        "Se hacen": "Egin",
        "Se bate": "Irabiatu",
        "Se baten": "Irabiatu",
        "Se calienta": "Berotu",
        "Se calientan": "Berotu",
        "Se derrite": "Urtu",
        "Se derriten": "Urtu",
        "Se deja": "Utzi",
        "Se dejan": "Utzi",
        "Se quita": "Kendu",
        "Se quitan": "Kendu",
        "Se pela": "Azaldu",
        "Se pelan": "Azaldu",
        "Se pica": "Zatitu",
        "Se pican": "Zatitu",
        "Se ralla": "Erratu",
        "Se rallan": "Erratu",
        "Se asa": "Erre",
        "Se asan": "Erre",
        "Se cuece": "Egosi",
        "caliente": "bero",
        "frío": "hotz",
        "tibio": "epel",
        "minutos": "minutu",
        "horas": "ordu",
        "hora": "ordu",
        "hasta que": "arte",
        "luego": "gero",
        "después": "ondoren",
        "mientras": "bitartean",
        "finalmente": "azkenik",
        "al horno": "labetan",
        "al fuego": "suan",
        "a fuego lento": "su txikian",
        "a fuego medio": "su ertainan",
        "a fuego alto": "su handian",
        "en la sartén": "zartagian",
        "en el horno": "labetan",
    }
    
    translated = instructions
    for spanish, basque in instruction_map.items():
        translated = translated.replace(spanish, basque)
    
    return translated


def fix_mixed_language_translations():
    """Corrige todas las traducciones con contenido mixto de idiomas."""
    
    print("🔧 CORRIGIENDO TRADUCCIONES CON CONTENIDO MIXTO")
    print("=" * 60)
    
    # Identificar traducciones problemáticas
    problematic = identify_mixed_language_translations()
    
    if not problematic:
        print("✅ No se encontraron traducciones con contenido mixto")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    fixed_count = 0
    
    for translation in problematic:
        trans_id = translation[0]
        recipe_id = translation[1]
        language = translation[2]
        
        print(f"🔄 Corrigiendo traducción {trans_id} (Recipe {recipe_id}, {language})")
        
        # Obtener receta original
        original_recipe = get_original_recipe(recipe_id)
        
        if original_recipe:
            # Generar traducción completamente nueva
            new_translation = generate_complete_replacement_translation(original_recipe, language)
            
            if new_translation:
                # Actualizar en la base de datos
                cursor.execute("""
                    UPDATE recipe_translations 
                    SET title = ?, description = ?, ingredients = ?, instructions = ?, category = ?
                    WHERE id = ?
                """, [
                    new_translation["title"],
                    new_translation["description"],
                    new_translation["ingredients"],
                    new_translation["instructions"],
                    new_translation["category"],
                    trans_id
                ])
                
                fixed_count += 1
                
                if fixed_count % 10 == 0:
                    conn.commit()
                    print(f"   Progreso: {fixed_count}/{len(problematic)} traducciones corregidas")
    
    conn.commit()
    conn.close()
    
    print(f"✅ {fixed_count} traducciones con contenido mixto corregidas exitosamente")


if __name__ == "__main__":
    init_database()
    fix_mixed_language_translations()
    
    # Verificar algunas traducciones corregidas
    print("\n🔍 VERIFICANDO TRADUCCIONES CORREGIDAS")
    print("=" * 60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtener algunas traducciones de prueba
    cursor.execute("""
        SELECT r.title, rt.language, rt.title as translated_title, rt.description
        FROM recipes r
        JOIN recipe_translations rt ON r.id = rt.recipe_id
        WHERE r.title IN ('Arenques Asados en Vino', 'Alcachofas Rellenas', 'Pollo Marengo')
        AND rt.language = 'en'
        ORDER BY r.title, rt.language
    """)
    
    test_translations = cursor.fetchall()
    
    for translation in test_translations:
        original_title, language, translated_title, translated_description = translation
        print(f"✅ {original_title} ({language}): {translated_title}")
        print(f"   {translated_description[:80]}...")
        print()
    
    conn.close()
    
    print("🎉 Corrección completa de traducciones con contenido mixto terminada!")