#!/usr/bin/env python3
"""
Script para corregir las traducciones de interfaz en todos los idiomas.
Reemplaza las traducciones de testing por traducciones reales.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fix_interface_translations():
    """Corregir las traducciones de interfaz en todos los idiomas."""

    print("🔄 Corrigiendo traducciones de interfaz...")

    # Traducciones completas para todos los idiomas
    translations = {
        "es": {
            "Home": "Inicio",
            "Categories": "Categorías",
            "Search": "Buscar",
            "Ingredients": "Ingredientes",
            "Instructions": "Instrucciones",
            "View Recipe": "Ver Receta",
            "All categories": "Todas las categorías",
            "Search results": "Resultados de búsqueda",
            "No recipes found": "No se encontraron recetas",
            "Back to all recipes": "Volver a todas las recetas",
            "Language": "Idioma",
            "Aunt Carmen's Recipes": "Recetas de la Tía Carmen",
            "Traditional family recipes": "Recetas familiares tradicionales",
            "Search recipes...": "Buscar recetas...",
            "Recipes found": "Recetas encontradas",
            "No recipes found matching your search.": "No se encontraron recetas que coincidan con tu búsqueda.",
            "View all recipes": "Ver todas las recetas",
            "Search tip": "Consejo de búsqueda",
            'You can search by recipe name, specific ingredients or dish type. Try "chicken", "chocolate" or "cake"!': 'Puedes buscar por nombre de receta, ingredientes específicos o tipo de plato. ¡Prueba "pollo", "chocolate" o "tarta"!',
            "Description:": "Descripción:",
            "More recipes from": "Más recetas de",
            "Recipe from Aunt Carmen": "Receta de la Tía Carmen",
            "Recipe Categories": "Categorías de Recetas",
            "Explore our recipes organized by categories:": "Explora nuestras recetas organizadas por categorías:",
            "View Recipes": "Ver Recetas",
            "Recipes from": "Recetas de",
            "No recipes found in this category.": "No se encontraron recetas en esta categoría.",
            "All Recipes": "Todas las Recetas",
            "Clear search": "Limpiar búsqueda",
            "for": "para",
            "in": "en",
            "Preserving family culinary traditions": "Preservando las tradiciones culinarias familiares",
            "Discover the traditional flavors of family cooking": "Descubre los sabores tradicionales de la cocina familiar",
            "Search by name, ingredients or description...": "Buscar por nombre, ingredientes o descripción...",
            "Preparation": "Preparación",
            "Preparation time": "Tiempo de preparación",
            "Servings": "Porciones",
            "Difficulty": "Dificultad",
            "Easy": "Fácil",
            "Medium": "Medio",
            "Hard": "Difícil",
            "Share": "Compartir",
            "Print": "Imprimir",
            "Favorites": "Favoritos",
            "Desserts": "Postres",
            "Drinks": "Bebidas",
            "Chicken": "Pollo",
            "Fish": "Pescado",
            "Meat": "Carne",
            "Vegetables": "Verduras",
            "Appetizers": "Aperitivos",
            "Others": "Otros",
        },
        "eu": {
            "Home": "Hasiera",
            "Categories": "Kategoriak",
            "Search": "Bilatu",
            "Ingredients": "Osagaiak",
            "Instructions": "Jarraibideak",
            "View Recipe": "Errezeta ikusi",
            "All categories": "Kategoria guztiak",
            "Search results": "Bilaketa emaitzak",
            "No recipes found": "Ez da errezetarik aurkitu",
            "Back to all recipes": "Errezeta guztietara itzuli",
            "Language": "Hizkuntza",
            "Aunt Carmen's Recipes": "Karmen Izebaren Errezetak",
            "Traditional family recipes": "Familia errezetak tradizionalak",
            "Search recipes...": "Bilatu errezetak...",
            "Recipes found": "Errezetak aurkitu",
            "No recipes found matching your search.": "Ez da zure bilaketarekin bat datorren errezetarik aurkitu.",
            "View all recipes": "Errezeta guztiak ikusi",
            "Search tip": "Bilaketa aholkua",
            'You can search by recipe name, specific ingredients or dish type. Try "chicken", "chocolate" or "cake"!': 'Errezeta izenaren, osagai zehatz edo plater motaren arabera bila dezakezu. Saiatu "oilaskoa", "txokolatea" edo "tarta"!',
            "Description:": "Deskribapena:",
            "More recipes from": "Errezeta gehiago",
            "Recipe from Aunt Carmen": "Karmen Izebaren errezeta",
            "Recipe Categories": "Errezeta Kategoriak",
            "Explore our recipes organized by categories:": "Arakatu gure errezetak kategorietan antolatuta:",
            "View Recipes": "Errezetak Ikusi",
            "Recipes from": "Errezetak",
            "No recipes found in this category.": "Ez da errezetarik aurkitu kategoria honetan.",
            "All Recipes": "Errezeta Guztiak",
            "Clear search": "Bilaketa garbitu",
            "for": "honentzat",
            "in": "barruan",
            "Preserving family culinary traditions": "Familiako sukaldaritza tradizioak mantentzen",
            "Discover the traditional flavors of family cooking": "Deskubritu familiako sukaldaritzaren zapore tradizionalak",
            "Search by name, ingredients or description...": "Bilatu izenaren, osagaien edo deskribapenen arabera...",
            "Preparation": "Prestaketa",
            "Preparation time": "Prestaketa denbora",
            "Servings": "Banaketak",
            "Difficulty": "Zailtasuna",
            "Easy": "Erraza",
            "Medium": "Ertaina",
            "Hard": "Zaila",
            "Share": "Partekatu",
            "Print": "Inprimatu",
            "Favorites": "Gogokoak",
            "Desserts": "Postrea",
            "Drinks": "Edariak",
            "Chicken": "Oilaskoa",
            "Fish": "Arraina",
            "Meat": "Haragia",
            "Vegetables": "Barazkiak",
            "Appetizers": "Gozagaiak",
            "Others": "Besteak",
        },
        "ca": {
            "Home": "Inici",
            "Categories": "Categories",
            "Search": "Buscar",
            "Ingredients": "Ingredients",
            "Instructions": "Instruccions",
            "View Recipe": "Veure Recepta",
            "All categories": "Totes les categories",
            "Search results": "Resultats de cerca",
            "No recipes found": "No s'han trobat receptes",
            "Back to all recipes": "Tornar a totes les receptes",
            "Language": "Idioma",
            "Aunt Carmen's Recipes": "Receptes de la Tia Carmen",
            "Traditional family recipes": "Receptes familiars tradicionals",
            "Search recipes...": "Buscar receptes...",
            "Recipes found": "Receptes trobades",
            "No recipes found matching your search.": "No s'han trobat receptes que coincideixin amb la teva cerca.",
            "View all recipes": "Veure totes les receptes",
            "Search tip": "Consell de cerca",
            'You can search by recipe name, specific ingredients or dish type. Try "chicken", "chocolate" or "cake"!': 'Pots buscar per nom de recepta, ingredients específics o tipus de plat. Prova "pollastre", "xocolata" o "pastís"!',
            "Description:": "Descripció:",
            "More recipes from": "Més receptes de",
            "Recipe from Aunt Carmen": "Recepta de la Tia Carmen",
            "Recipe Categories": "Categories de Receptes",
            "Explore our recipes organized by categories:": "Explora les nostres receptes organitzades per categories:",
            "View Recipes": "Veure Receptes",
            "Recipes from": "Receptes de",
            "No recipes found in this category.": "No s'han trobat receptes en aquesta categoria.",
            "All Recipes": "Totes les Receptes",
            "Clear search": "Netejar cerca",
            "for": "per",
            "in": "en",
            "Preserving family culinary traditions": "Preservant les tradicions culinàries familiars",
            "Discover the traditional flavors of family cooking": "Descobreix els sabors tradicionals de la cuina familiar",
            "Search by name, ingredients or description...": "Buscar per nom, ingredients o descripció...",
            "Preparation": "Preparació",
            "Preparation time": "Temps de preparació",
            "Servings": "Racions",
            "Difficulty": "Dificultat",
            "Easy": "Fàcil",
            "Medium": "Mitjà",
            "Hard": "Difícil",
            "Share": "Compartir",
            "Print": "Imprimir",
            "Favorites": "Favorits",
            "Desserts": "Postres",
            "Drinks": "Begudes",
            "Chicken": "Pollastre",
            "Fish": "Peix",
            "Meat": "Carn",
            "Vegetables": "Verdures",
            "Appetizers": "Aperitius",
            "Others": "Altres",
        },
        "en": {
            "Home": "Home",
            "Categories": "Categories",
            "Search": "Search",
            "Ingredients": "Ingredients",
            "Instructions": "Instructions",
            "View Recipe": "View Recipe",
            "All categories": "All categories",
            "Search results": "Search results",
            "No recipes found": "No recipes found",
            "Back to all recipes": "Back to all recipes",
            "Language": "Language",
            "Aunt Carmen's Recipes": "Aunt Carmen's Recipes",
            "Traditional family recipes": "Traditional family recipes",
            "Search recipes...": "Search recipes...",
            "Recipes found": "Recipes found",
            "No recipes found matching your search.": "No recipes found matching your search.",
            "View all recipes": "View all recipes",
            "Search tip": "Search tip",
            'You can search by recipe name, specific ingredients or dish type. Try "chicken", "chocolate" or "cake"!': 'You can search by recipe name, specific ingredients or dish type. Try "chicken", "chocolate" or "cake"!',
            "Description:": "Description:",
            "More recipes from": "More recipes from",
            "Recipe from Aunt Carmen": "Recipe from Aunt Carmen",
            "Recipe Categories": "Recipe Categories",
            "Explore our recipes organized by categories:": "Explore our recipes organized by categories:",
            "View Recipes": "View Recipes",
            "Recipes from": "Recipes from",
            "No recipes found in this category.": "No recipes found in this category.",
            "All Recipes": "All Recipes",
            "Clear search": "Clear search",
            "for": "for",
            "in": "in",
            "Preserving family culinary traditions": "Preserving family culinary traditions",
            "Discover the traditional flavors of family cooking": "Discover the traditional flavors of family cooking",
            "Search by name, ingredients or description...": "Search by name, ingredients or description...",
            "Preparation": "Preparation",
            "Preparation time": "Preparation time",
            "Servings": "Servings",
            "Difficulty": "Difficulty",
            "Easy": "Easy",
            "Medium": "Medium",
            "Hard": "Hard",
            "Share": "Share",
            "Print": "Print",
            "Favorites": "Favorites",
            "Desserts": "Desserts",
            "Drinks": "Drinks",
            "Chicken": "Chicken",
            "Fish": "Fish",
            "Meat": "Meat",
            "Vegetables": "Vegetables",
            "Appetizers": "Appetizers",
            "Others": "Others",
        },
        "zh": {
            "Home": "首页",
            "Categories": "分类",
            "Search": "搜索",
            "Ingredients": "食材",
            "Instructions": "制作方法",
            "View Recipe": "查看食谱",
            "All categories": "所有分类",
            "Search results": "搜索结果",
            "No recipes found": "未找到食谱",
            "Back to all recipes": "返回所有食谱",
            "Language": "语言",
            "Aunt Carmen's Recipes": "卡门阿姨的食谱",
            "Traditional family recipes": "传统家庭食谱",
            "Search recipes...": "搜索食谱...",
            "Recipes found": "找到食谱",
            "No recipes found matching your search.": "未找到与您的搜索匹配的食谱。",
            "View all recipes": "查看所有食谱",
            "Search tip": "搜索提示",
            'You can search by recipe name, specific ingredients or dish type. Try "chicken", "chocolate" or "cake"!': '您可以按食谱名称、特定食材或菜肴类型搜索。试试"鸡肉"、"巧克力"或"蛋糕"！',
            "Description:": "描述：",
            "More recipes from": "更多食谱来自",
            "Recipe from Aunt Carmen": "来自卡门阿姨的食谱",
            "Recipe Categories": "食谱分类",
            "Explore our recipes organized by categories:": "探索我们按分类组织的食谱：",
            "View Recipes": "查看食谱",
            "Recipes from": "食谱来自",
            "No recipes found in this category.": "此分类中未找到食谱。",
            "All Recipes": "所有食谱",
            "Clear search": "清除搜索",
            "for": "用于",
            "in": "在",
            "Preserving family culinary traditions": "保存家庭烹饪传统",
            "Discover the traditional flavors of family cooking": "发现家庭烹饪的传统风味",
            "Search by name, ingredients or description...": "按名称、食材或描述搜索...",
            "Preparation": "准备",
            "Preparation time": "准备时间",
            "Servings": "份量",
            "Difficulty": "难度",
            "Easy": "简单",
            "Medium": "中等",
            "Hard": "困难",
            "Share": "分享",
            "Print": "打印",
            "Favorites": "收藏",
            "Desserts": "甜点",
            "Drinks": "饮料",
            "Chicken": "鸡肉",
            "Fish": "鱼类",
            "Meat": "肉类",
            "Vegetables": "蔬菜",
            "Appetizers": "开胃菜",
            "Others": "其他",
        },
    }

    # Generar archivos .po para cada idioma
    for lang, translations_dict in translations.items():
        po_dir = f"translations/{lang}/LC_MESSAGES"
        os.makedirs(po_dir, exist_ok=True)

        lang_names = {
            "es": "Español",
            "eu": "Euskera/Basque",
            "ca": "Valencià/Valencian Catalan",
            "en": "English",
            "zh": "Chinese (Simplified)",
        }

        po_content = f"""# {lang_names[lang]} translations for Recipe App
# Interface translations corrected
#
msgid ""
msgstr ""
"Project-Id-Version: Recipe App 1.0\\n"
"Report-Msgid-Bugs-To: admin@example.com\\n"
"POT-Creation-Date: 2024-01-01 12:00+0000\\n"
"PO-Revision-Date: 2024-01-01 12:00+0000\\n"
"Last-Translator: Interface Translation System\\n"
"Language: {lang}\\n"
"Language-Team: {lang_names[lang]}\\n"
"Plural-Forms: nplurals=2; plural=(n != 1)\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: Interface Translation System\\n"

"""

        # Agregar traducciones de interfaz
        for english_text, translation in translations_dict.items():
            # Escapar comillas para formato .po
            escaped_english = english_text.replace('"', '\\"')
            escaped_translation = translation.replace('"', '\\"')
            po_content += f'msgid "{escaped_english}"\n'
            po_content += f'msgstr "{escaped_translation}"\n\n'

        po_file_path = f"{po_dir}/messages.po"
        with open(po_file_path, "w", encoding="utf-8") as f:
            f.write(po_content)

        print(f"✅ {lang_names[lang]}: {po_file_path}")

    print("\n✅ Traducciones de interfaz corregidas exitosamente!")


if __name__ == "__main__":
    fix_interface_translations()
