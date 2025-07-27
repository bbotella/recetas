#!/usr/bin/env python3
"""
Script para corregir todas las traducciones fallback problemáticas.
Este script identifica y corrige las traducciones que tienen prefijos
como "Traditional Spanish family recipe:" mezclados con español.
"""

import os
import sys
import re

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database  # noqa: E402


def identify_problematic_translations():
    """Identifica traducciones con prefijos problemáticos."""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Buscar traducciones con prefijos problemáticos
    problematic_patterns = [
        'Traditional Spanish family recipe:',
        'Recepta tradicional valenciana:',
        'Euskal sukaldaritzako errezeta tradizionala:',
        '传统西班牙家庭食谱：',
        '特色传统食谱：'
    ]
    
    problematic_translations = []
    
    for pattern in problematic_patterns:
        translations = cursor.execute("""
            SELECT id, recipe_id, language, title, description, ingredients, instructions
            FROM recipe_translations
            WHERE description LIKE ? OR ingredients LIKE ? OR instructions LIKE ?
        """, [f'%{pattern}%', f'%{pattern}%', f'%{pattern}%']).fetchall()
        
        problematic_translations.extend(translations)
    
    conn.close()
    
    print(f"🔍 Found {len(problematic_translations)} problematic translations")
    return problematic_translations


def generate_proper_translation(text, target_lang, context):
    """Genera una traducción adecuada sin prefijos problemáticos."""
    
    # Limpiar prefijos problemáticos
    text = re.sub(r'^Traditional Spanish family recipe:\s*', '', text)
    text = re.sub(r'^Recepta tradicional valenciana:\s*', '', text)
    text = re.sub(r'^Euskal sukaldaritzako errezeta tradizionala:\s*', '', text)
    text = re.sub(r'^传统西班牙家庭食谱：\s*', '', text)
    text = re.sub(r'^特色传统食谱：\s*', '', text)
    
    # Generar traducciones específicas por idioma
    if target_lang == 'en':
        return translate_to_english(text, context)
    elif target_lang == 'zh':
        return translate_to_chinese(text, context)
    elif target_lang == 'ca':
        return translate_to_catalan(text, context)
    elif target_lang == 'eu':
        return translate_to_basque(text, context)
    
    return text


def translate_to_english(text, context):
    """Traduce texto al inglés."""
    
    # Traducciones básicas de ingredientes
    ingredient_translations = {
        'Alcachofas': 'Artichokes',
        'Sal': 'Salt',
        'Aceite': 'Oil',
        'Cebolla': 'Onion',
        'Ajo': 'Garlic',
        'Tomate': 'Tomato',
        'Perejil': 'Parsley',
        'Huevos': 'Eggs',
        'Harina': 'Flour',
        'Leche': 'Milk',
        'Mantequilla': 'Butter',
        'Azúcar': 'Sugar',
        'Agua': 'Water',
        'Vino': 'Wine',
        'Patatas': 'Potatoes',
        'Arroz': 'Rice',
        'Pollo': 'Chicken',
        'Pescado': 'Fish',
        'Carne': 'Meat',
        'Queso': 'Cheese',
        'Limón': 'Lemon',
        'Naranja': 'Orange',
        'Merluza': 'Hake',
        'Gambas': 'Shrimp',
        'Champiñones': 'Mushrooms',
        'Espinacas': 'Spinach',
        'Nata': 'Cream',
        'Cordero': 'Lamb',
        'Jamón': 'Ham',
        'Especias': 'Spices',
        'Manteca': 'Lard',
        'Coco': 'Coconut',
        'Plátano': 'Banana',
        'Fresas': 'Strawberries',
        'Chocolate': 'Chocolate',
        'Manzanas': 'Apples',
        'Canela': 'Cinnamon',
        'Arenques': 'Herrings',
        'Faisán': 'Pheasant',
        'Endivias': 'Endives',
        'Ternera': 'Veal',
        'Guisantes': 'Peas',
        'Mostaza': 'Mustard',
        'Bechamel': 'Bechamel sauce'
    }
    
    # Traducciones de instrucciones
    instruction_translations = {
        'Se cuecen': 'Cook',
        'Se rellenan': 'Stuff',
        'Se cortan': 'Cut',
        'Se fríe': 'Fry',
        'Se mezcla': 'Mix',
        'Se añade': 'Add',
        'Se sirve': 'Serve',
        'Se pone': 'Put',
        'Se hace': 'Make',
        'Se bate': 'Beat',
        'Se calienta': 'Heat',
        'Se derrite': 'Melt',
        'Se deja': 'Leave',
        'Se quita': 'Remove',
        'Se pela': 'Peel',
        'Se pica': 'Chop',
        'Se ralla': 'Grate',
        'caliente': 'hot',
        'frío': 'cold',
        'minutos': 'minutes',
        'hora': 'hour',
        'hasta que': 'until',
        'luego': 'then',
        'después': 'after',
        'mientras': 'while',
        'finalmente': 'finally',
        'al horno': 'in the oven',
        'a fuego lento': 'over low heat',
        'a fuego medio': 'over medium heat',
        'a fuego alto': 'over high heat'
    }
    
    # Aplicar traducciones
    translated = text
    
    if context == 'ingredients':
        for spanish, english in ingredient_translations.items():
            translated = translated.replace(spanish, english)
    elif context == 'instructions':
        for spanish, english in instruction_translations.items():
            translated = translated.replace(spanish, english)
    elif context == 'description':
        # Para descripciones, generar una traducción contextual
        if 'Descubre la magia culinaria' in text:
            translated = re.sub(r'Descubre la magia culinaria de ([^,]+)', 
                              r'Discover the culinary magic of \1', translated)
        
        # Traducir frases comunes
        translated = translated.replace('donde la', 'where the')
        translated = translated.replace('que despierta', 'that awakens')
        translated = translated.replace('los sentidos', 'the senses')
        translated = translated.replace('cada bocado', 'every bite')
        translated = translated.replace('una experiencia', 'an experience')
        translated = translated.replace('gastronómica', 'gastronomic')
        translated = translated.replace('memorable', 'memorable')
        translated = translated.replace('tradición', 'tradition')
        translated = translated.replace('innovación', 'innovation')
        
        # Aplicar traducciones de ingredientes también en descripciones
        for spanish, english in ingredient_translations.items():
            translated = translated.replace(spanish.lower(), english.lower())
    
    return translated


def translate_to_chinese(text, context):
    """Traduce texto al chino."""
    
    # Traducciones básicas de ingredientes
    ingredient_translations = {
        'Alcachofas': '朝鲜蓟',
        'Sal': '盐',
        'Aceite': '油',
        'Cebolla': '洋葱',
        'Ajo': '大蒜',
        'Tomate': '番茄',
        'Perejil': '欧芹',
        'Huevos': '鸡蛋',
        'Harina': '面粉',
        'Leche': '牛奶',
        'Mantequilla': '黄油',
        'Azúcar': '糖',
        'Agua': '水',
        'Vino': '酒',
        'Patatas': '土豆',
        'Arroz': '米饭',
        'Pollo': '鸡肉',
        'Pescado': '鱼',
        'Carne': '肉',
        'Queso': '奶酪',
        'Limón': '柠檬',
        'Naranja': '橙子',
        'Merluza': '鳕鱼',
        'Gambas': '虾',
        'Champiñones': '蘑菇',
        'Espinacas': '菠菜',
        'Nata': '奶油',
        'Cordero': '羊肉',
        'Jamón': '火腿',
        'Especias': '香料',
        'Manteca': '猪油',
        'Coco': '椰子',
        'Plátano': '香蕉',
        'Fresas': '草莓',
        'Chocolate': '巧克力',
        'Manzanas': '苹果',
        'Canela': '肉桂',
        'Arenques': '鲱鱼',
        'Faisán': '野鸡',
        'Endivias': '菊苣',
        'Ternera': '小牛肉',
        'Guisantes': '豌豆',
        'Mostaza': '芥末',
        'Bechamel': '白酱'
    }
    
    # Traducciones de instrucciones
    instruction_translations = {
        'Se cuecen': '煮',
        'Se rellenan': '填充',
        'Se cortan': '切',
        'Se fríe': '炒',
        'Se mezcla': '混合',
        'Se añade': '加入',
        'Se sirve': '上菜',
        'Se pone': '放入',
        'Se hace': '制作',
        'Se bate': '搅拌',
        'Se calienta': '加热',
        'Se derrite': '融化',
        'Se deja': '放置',
        'Se quita': '取出',
        'Se pela': '去皮',
        'Se pica': '切碎',
        'Se ralla': '磨碎',
        'caliente': '热',
        'frío': '冷',
        'minutos': '分钟',
        'hora': '小时',
        'hasta que': '直到',
        'luego': '然后',
        'después': '之后',
        'mientras': '同时',
        'finalmente': '最后',
        'al horno': '在烤箱中',
        'a fuego lento': '小火',
        'a fuego medio': '中火',
        'a fuego alto': '大火'
    }
    
    # Aplicar traducciones
    translated = text
    
    if context == 'ingredients':
        for spanish, chinese in ingredient_translations.items():
            translated = translated.replace(spanish, chinese)
    elif context == 'instructions':
        for spanish, chinese in instruction_translations.items():
            translated = translated.replace(spanish, chinese)
    elif context == 'description':
        # Para descripciones, generar una traducción contextual
        if 'Descubre la magia culinaria' in text:
            translated = re.sub(r'Descubre la magia culinaria de ([^,]+)', 
                              r'发现\1的烹饪魔力', translated)
        
        # Traducir frases comunes
        translated = translated.replace('donde la', '其中')
        translated = translated.replace('que despierta', '唤醒')
        translated = translated.replace('los sentidos', '感官')
        translated = translated.replace('cada bocado', '每一口')
        translated = translated.replace('una experiencia', '一种体验')
        translated = translated.replace('gastronómica', '美食')
        translated = translated.replace('memorable', '难忘')
        translated = translated.replace('tradición', '传统')
        translated = translated.replace('innovación', '创新')
        
        # Aplicar traducciones de ingredientes también en descripciones
        for spanish, chinese in ingredient_translations.items():
            translated = translated.replace(spanish.lower(), chinese)
    
    return translated


def translate_to_catalan(text, context):
    """Traduce texto al catalán valenciano."""
    
    # Traducciones básicas de ingredientes
    ingredient_translations = {
        'Alcachofas': 'Carxofes',
        'Sal': 'Sal',
        'Aceite': 'Oli',
        'Cebolla': 'Ceba',
        'Ajo': 'All',
        'Tomate': 'Tomàquet',
        'Perejil': 'Julivert',
        'Huevos': 'Ous',
        'Harina': 'Farina',
        'Leche': 'Llet',
        'Mantequilla': 'Mantega',
        'Azúcar': 'Sucre',
        'Agua': 'Aigua',
        'Vino': 'Vi',
        'Patatas': 'Patates',
        'Arroz': 'Arròs',
        'Pollo': 'Pollastre',
        'Pescado': 'Peix',
        'Carne': 'Carn',
        'Queso': 'Formatge',
        'Limón': 'Llimó',
        'Naranja': 'Taronja',
        'Merluza': 'Lluç',
        'Gambas': 'Gambes',
        'Champiñones': 'Xampinyons',
        'Espinacas': 'Espinacs',
        'Nata': 'Nata',
        'Cordero': 'Xai',
        'Jamón': 'Pernil',
        'Especias': 'Espècies',
        'Manteca': 'Llard',
        'Coco': 'Coco',
        'Plátano': 'Plàtan',
        'Fresas': 'Maduixes',
        'Chocolate': 'Xocolata',
        'Manzanas': 'Pomes',
        'Canela': 'Canyella',
        'Arenques': 'Arencs',
        'Faisán': 'Faisà',
        'Endivias': 'Endívies',
        'Ternera': 'Vedella',
        'Guisantes': 'Pèsols',
        'Mostaza': 'Mostassa',
        'Bechamel': 'Bechamel'
    }
    
    # Traducciones de instrucciones
    instruction_translations = {
        'Se cuecen': 'Es couen',
        'Se rellenan': 'Es farceixen',
        'Se cortan': 'Es tallen',
        'Se fríe': 'Es fregeix',
        'Se mezcla': 'Es barreja',
        'Se añade': 'S\'afegeix',
        'Se sirve': 'Es serveix',
        'Se pone': 'Es posa',
        'Se hace': 'Es fa',
        'Se bate': 'Es bat',
        'Se calienta': 'Es calenta',
        'Se derrite': 'Es desfà',
        'Se deja': 'Es deixa',
        'Se quita': 'Es treu',
        'Se pela': 'Es pela',
        'Se pica': 'Es pica',
        'Se ralla': 'Es ratlla',
        'caliente': 'calent',
        'frío': 'fred',
        'minutos': 'minuts',
        'hora': 'hora',
        'hasta que': 'fins que',
        'luego': 'després',
        'después': 'després',
        'mientras': 'mentre',
        'finalmente': 'finalment',
        'al horno': 'al forn',
        'a fuego lento': 'a foc lent',
        'a fuego medio': 'a foc mitjà',
        'a fuego alto': 'a foc fort'
    }
    
    # Aplicar traducciones
    translated = text
    
    if context == 'ingredients':
        for spanish, catalan in ingredient_translations.items():
            translated = translated.replace(spanish, catalan)
    elif context == 'instructions':
        for spanish, catalan in instruction_translations.items():
            translated = translated.replace(spanish, catalan)
    elif context == 'description':
        # Para descripciones, generar una traducción contextual
        if 'Descubre la magia culinaria' in text:
            translated = re.sub(r'Descubre la magia culinaria de ([^,]+)', 
                              r'Descobreix la màgia culinària de \1', translated)
        
        # Traducir frases comunes
        translated = translated.replace('donde la', 'on la')
        translated = translated.replace('que despierta', 'que desperta')
        translated = translated.replace('los sentidos', 'els sentits')
        translated = translated.replace('cada bocado', 'cada mossegada')
        translated = translated.replace('una experiencia', 'una experiència')
        translated = translated.replace('gastronómica', 'gastronòmica')
        translated = translated.replace('memorable', 'memorable')
        translated = translated.replace('tradición', 'tradició')
        translated = translated.replace('innovación', 'innovació')
        
        # Aplicar traducciones de ingredientes también en descripciones
        for spanish, catalan in ingredient_translations.items():
            translated = translated.replace(spanish.lower(), catalan.lower())
    
    return translated


def translate_to_basque(text, context):
    """Traduce texto al euskera."""
    
    # Traducciones básicas de ingredientes
    ingredient_translations = {
        'Alcachofas': 'Artxindurriak',
        'Sal': 'Gatza',
        'Aceite': 'Olioa',
        'Cebolla': 'Tipula',
        'Ajo': 'Baratxuria',
        'Tomate': 'Tomatea',
        'Perejil': 'Perrexila',
        'Huevos': 'Arrautzak',
        'Harina': 'Irina',
        'Leche': 'Esnea',
        'Mantequilla': 'Gurina',
        'Azúcar': 'Azukrea',
        'Agua': 'Ura',
        'Vino': 'Ardoa',
        'Patatas': 'Patatак',
        'Arroz': 'Arroza',
        'Pollo': 'Oilaskoa',
        'Pescado': 'Arraina',
        'Carne': 'Haragia',
        'Queso': 'Gazta',
        'Limón': 'Limoia',
        'Naranja': 'Laranja',
        'Merluza': 'Legatza',
        'Gambas': 'Izkira',
        'Champiñones': 'Perretxikoak',
        'Espinacas': 'Espinakak',
        'Nata': 'Nata',
        'Cordero': 'Bildotsa',
        'Jamón': 'Urdaiazpikoa',
        'Especias': 'Kondairua',
        'Manteca': 'Txerri-koipea',
        'Coco': 'Kokoa',
        'Plátano': 'Platanoa',
        'Fresas': 'Marrubiak',
        'Chocolate': 'Txokolatea',
        'Manzanas': 'Sagarrak',
        'Canela': 'Kanela',
        'Arenques': 'Arenkeak',
        'Faisán': 'Faisana',
        'Endivias': 'Endibiak',
        'Ternera': 'Txahal-haragia',
        'Guisantes': 'Ilarrak',
        'Mostaza': 'Mostaza',
        'Bechamel': 'Betxamel'
    }
    
    # Traducciones de instrucciones
    instruction_translations = {
        'Se cuecen': 'Egosi',
        'Se rellenan': 'Bete',
        'Se cortan': 'Ebaki',
        'Se fríe': 'Frijitu',
        'Se mezcla': 'Nahastu',
        'Se añade': 'Gehitu',
        'Se sirve': 'Zerbitzatu',
        'Se pone': 'Jarri',
        'Se hace': 'Egin',
        'Se bate': 'Irabiatu',
        'Se calienta': 'Berotu',
        'Se derrite': 'Urtu',
        'Se deja': 'Utzi',
        'Se quita': 'Kendu',
        'Se pela': 'Azaldu',
        'Se pica': 'Zatitu',
        'Se ralla': 'Erratu',
        'caliente': 'bero',
        'frío': 'hotz',
        'minutos': 'minutu',
        'hora': 'ordu',
        'hasta que': 'arte',
        'luego': 'gero',
        'después': 'ondoren',
        'mientras': 'bitartean',
        'finalmente': 'azkenik',
        'al horno': 'labetan',
        'a fuego lento': 'su txikian',
        'a fuego medio': 'su ertainan',
        'a fuego alto': 'su handian'
    }
    
    # Aplicar traducciones
    translated = text
    
    if context == 'ingredients':
        for spanish, basque in ingredient_translations.items():
            translated = translated.replace(spanish, basque)
    elif context == 'instructions':
        for spanish, basque in instruction_translations.items():
            translated = translated.replace(spanish, basque)
    elif context == 'description':
        # Para descripciones, generar una traducción contextual
        if 'Descubre la magia culinaria' in text:
            translated = re.sub(r'Descubre la magia culinaria de ([^,]+)', 
                              r'Deskubritu \1ren magia kulinarioa', translated)
        
        # Traducir frases comunes
        translated = translated.replace('donde la', 'non')
        translated = translated.replace('que despierta', 'esnatu')
        translated = translated.replace('los sentidos', 'zentzumenak')
        translated = translated.replace('cada bocado', 'hozka bakoitzean')
        translated = translated.replace('una experiencia', 'esperientzia bat')
        translated = translated.replace('gastronómica', 'gastronomikoa')
        translated = translated.replace('memorable', 'gogoangarria')
        translated = translated.replace('tradición', 'tradizio')
        translated = translated.replace('innovación', 'berrikuntza')
        
        # Aplicar traducciones de ingredientes también en descripciones
        for spanish, basque in ingredient_translations.items():
            translated = translated.replace(spanish.lower(), basque.lower())
    
    return translated


def fix_all_translations():
    """Corrige todas las traducciones problemáticas."""
    
    print("🔧 CORRIGIENDO TRADUCCIONES PROBLEMÁTICAS")
    print("=" * 60)
    
    # Identificar traducciones problemáticas
    problematic = identify_problematic_translations()
    
    if not problematic:
        print("✅ No se encontraron traducciones problemáticas")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    fixed_count = 0
    
    for translation in problematic:
        trans_id = translation[0]
        recipe_id = translation[1]
        language = translation[2]
        title = translation[3]
        description = translation[4]
        ingredients = translation[5]
        instructions = translation[6]
        
        print(f"🔄 Corrigiendo traducción {trans_id} (Recipe {recipe_id}, {language})")
        
        # Corregir cada campo
        fixed_description = generate_proper_translation(description, language, 'description')
        fixed_ingredients = generate_proper_translation(ingredients, language, 'ingredients')
        fixed_instructions = generate_proper_translation(instructions, language, 'instructions')
        
        # Actualizar en la base de datos
        cursor.execute("""
            UPDATE recipe_translations 
            SET description = ?, ingredients = ?, instructions = ?
            WHERE id = ?
        """, [fixed_description, fixed_ingredients, fixed_instructions, trans_id])
        
        fixed_count += 1
        
        if fixed_count % 10 == 0:
            conn.commit()
            print(f"   Progreso: {fixed_count}/{len(problematic)} traducciones corregidas")
    
    conn.commit()
    conn.close()
    
    print(f"✅ {fixed_count} traducciones corregidas exitosamente")


if __name__ == "__main__":
    init_database()
    fix_all_translations()