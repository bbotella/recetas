#!/usr/bin/env python3
"""
Script to fix and update Flask-Babel translation files with correct quote escaping.
"""

import os
import json
from datetime import datetime

# Fixed translations for interface elements with proper quote escaping
INTERFACE_TRANSLATIONS = {
    'en': {
        "Aunt Carmen's Recipes": "Aunt Carmen's Recipes",
        "Traditional family recipes": "Traditional family recipes", 
        "Discover the traditional flavors of family cooking": "Discover the traditional flavors of family cooking",
        "Preserving family culinary traditions": "Preserving family culinary traditions",
        "Home": "Home",
        "Categories": "Categories", 
        "Language": "Language",
        "Search Recipes": "Search Recipes",
        "Search by name, ingredients or description...": "Search by name, ingredients or description...",
        "All categories": "All categories",
        "Search": "Search",
        "Search results": "Search results",
        "for": "for",
        "in": "in", 
        "All Recipes": "All Recipes",
        "Clear search": "Clear search",
        "View Recipe": "View Recipe",
        "No recipes found matching your search.": "No recipes found matching your search.",
        "View all recipes": "View all recipes",
        "Search tip": "Search tip",
        "You can search by recipe name, specific ingredients or dish type. Try \\\"chicken\\\", \\\"chocolate\\\" or \\\"cake\\\"!": "You can search by recipe name, specific ingredients or dish type. Try \\\"chicken\\\", \\\"chocolate\\\" or \\\"cake\\\"!",
        "Ingredients": "Ingredients",
        "Instructions": "Instructions",
        "Preparation": "Preparation",
        "Category": "Category",
        "Back to recipes": "Back to recipes",
        "Print recipe": "Print recipe",
        "Share recipe": "Share recipe",
        "Related recipes": "Related recipes",
        "Recipe not found": "Recipe not found",
        "The requested recipe could not be found.": "The requested recipe could not be found.",
        "minutes": "minutes",
        "servings": "servings",
        "Difficulty": "Difficulty",
        "Easy": "Easy",
        "Medium": "Medium", 
        "Hard": "Hard"
    },
    'zh': {
        "Aunt Carmen's Recipes": "卡门阿姨的食谱",
        "Traditional family recipes": "传统家庭食谱",
        "Discover the traditional flavors of family cooking": "探索家庭烹饪的传统风味",
        "Preserving family culinary traditions": "保护家庭烹饪传统",
        "Home": "首页",
        "Categories": "分类", 
        "Language": "语言",
        "Search Recipes": "搜索食谱",
        "Search by name, ingredients or description...": "按名称、配料或描述搜索...",
        "All categories": "所有分类",
        "Search": "搜索",
        "Search results": "搜索结果",
        "for": "关于",
        "in": "在", 
        "All Recipes": "所有食谱",
        "Clear search": "清除搜索",
        "View Recipe": "查看食谱",
        "No recipes found matching your search.": "没有找到符合您搜索的食谱。",
        "View all recipes": "查看所有食谱",
        "Search tip": "搜索提示",
        "You can search by recipe name, specific ingredients or dish type. Try \\\"chicken\\\", \\\"chocolate\\\" or \\\"cake\\\"!": "您可以按食谱名称、特定配料或菜肴类型搜索。试试\\\"鸡肉\\\"、\\\"巧克力\\\"或\\\"蛋糕\\\"！",
        "Ingredients": "配料",
        "Instructions": "制作方法",
        "Preparation": "准备",
        "Category": "分类",
        "Back to recipes": "返回食谱",
        "Print recipe": "打印食谱",
        "Share recipe": "分享食谱",
        "Related recipes": "相关食谱",
        "Recipe not found": "未找到食谱",
        "The requested recipe could not be found.": "无法找到请求的食谱。",
        "minutes": "分钟",
        "servings": "份数",
        "Difficulty": "难度",
        "Easy": "简单",
        "Medium": "中等", 
        "Hard": "困难"
    },
    'ca': {
        "Aunt Carmen's Recipes": "Receptes de la Tia Carmen",
        "Traditional family recipes": "Receptes tradicionals familiars",
        "Discover the traditional flavors of family cooking": "Descobreix els sabors tradicionals de la cuina familiar",
        "Preserving family culinary traditions": "Preservant les tradicions culinàries familiars",
        "Home": "Inici",
        "Categories": "Categories", 
        "Language": "Idioma",
        "Search Recipes": "Cerca Receptes",
        "Search by name, ingredients or description...": "Cerca per nom, ingredients o descripció...",
        "All categories": "Totes les categories",
        "Search": "Cerca",
        "Search results": "Resultats de la cerca",
        "for": "per a",
        "in": "en", 
        "All Recipes": "Totes les Receptes",
        "Clear search": "Neteja la cerca",
        "View Recipe": "Veure Recepta",
        "No recipes found matching your search.": "No s'han trobat receptes que coincideixin amb la vostra cerca.",
        "View all recipes": "Veure totes les receptes",
        "Search tip": "Consell de cerca",
        "You can search by recipe name, specific ingredients or dish type. Try \\\"chicken\\\", \\\"chocolate\\\" or \\\"cake\\\"!": "Pots cercar per nom de recepta, ingredients específics o tipus de plat. Prova \\\"pollastre\\\", \\\"xocolata\\\" o \\\"pastís\\\"!",
        "Ingredients": "Ingredients",
        "Instructions": "Instruccions",
        "Preparation": "Preparació",
        "Category": "Categoria",
        "Back to recipes": "Tornar a les receptes",
        "Print recipe": "Imprimir recepta",
        "Share recipe": "Compartir recepta",
        "Related recipes": "Receptes relacionades",
        "Recipe not found": "Recepta no trobada",
        "The requested recipe could not be found.": "No s'ha pogut trobar la recepta sol·licitada.",
        "minutes": "minuts",
        "servings": "racions",
        "Difficulty": "Dificultat",
        "Easy": "Fàcil",
        "Medium": "Mitjà", 
        "Hard": "Difícil"
    },
    'eu': {
        "Aunt Carmen's Recipes": "Carmen Izebaren Errezetek",
        "Traditional family recipes": "Familia-errezetak tradizionalak",
        "Discover the traditional flavors of family cooking": "Aurkitu familia-sukaldaritzaren zapore tradizionalak",
        "Preserving family culinary traditions": "Familiaren kultura-tradizio kulinarioak mantenduz",
        "Home": "Hasiera",
        "Categories": "Kategoriak", 
        "Language": "Hizkuntza",
        "Search Recipes": "Bilatu Errezetek",
        "Search by name, ingredients or description...": "Bilatu izenez, osagaiez edo deskribpenez...",
        "All categories": "Kategoria guztiak",
        "Search": "Bilatu",
        "Search results": "Bilaketa emaitzak",
        "for": "honentzako",
        "in": "hemen", 
        "All Recipes": "Errezeta Guztiak",
        "Clear search": "Bilaketa garbitu",
        "View Recipe": "Errezeta Ikusi",
        "No recipes found matching your search.": "Ez da zure bilaketarekin bat datorren errezeta aurkitu.",
        "View all recipes": "Errezeta guztiak ikusi",
        "Search tip": "Bilaketa aholkua",
        "You can search by recipe name, specific ingredients or dish type. Try \\\"chicken\\\", \\\"chocolate\\\" or \\\"cake\\\"!": "Errezeta izenez, osagai zehatzez edo plater motaz bilatu dezakezu. Saiatu \\\"oilaskoa\\\", \\\"txokolatea\\\" edo \\\"pastela\\\"!",
        "Ingredients": "Osagaiak",
        "Instructions": "Jarraibideak",
        "Preparation": "Prestaketa",
        "Category": "Kategoria",
        "Back to recipes": "Errezetak itzuli",
        "Print recipe": "Errezeta inprimatu",
        "Share recipe": "Errezeta partekatu",
        "Related recipes": "Erlazionatutako errezetek",
        "Recipe not found": "Errezeta ez da aurkitu",
        "The requested recipe could not be found.": "Eskatutako errezeta ezin izan da aurkitu.",
        "minutes": "minutu",
        "servings": "razio",
        "Difficulty": "Zailtasuna",
        "Easy": "Erraza",
        "Medium": "Ertaina", 
        "Hard": "Zaila"
    }
}

def update_po_file(language_code, translations):
    """Update a .po file with new translations"""
    po_path = f"/Users/bernardobotellacorbi/Documents/dev/tiaCarmen/translations/{language_code}/LC_MESSAGES/messages.po"
    
    if not os.path.exists(po_path):
        print(f"Warning: {po_path} does not exist")
        return
    
    # Read existing file
    with open(po_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the header end
    header_end = 0
    for i, line in enumerate(lines):
        if line.strip() == "" and i > 10:  # Empty line after header
            header_end = i + 1
            break
    
    # Keep header
    new_lines = lines[:header_end]
    
    # Add all translations
    for msgid, msgstr in translations.items():
        # Properly escape quotes in msgid and msgstr
        escaped_msgid = msgid.replace('"', '\\"')
        escaped_msgstr = msgstr.replace('"', '\\"')
        
        new_lines.append(f'msgid "{escaped_msgid}"\n')
        new_lines.append(f'msgstr "{escaped_msgstr}"\n')
        new_lines.append('\n')
    
    # Write updated file
    with open(po_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Updated {po_path} with {len(translations)} translations")

def main():
    """Main function to update all translation files"""
    print("=== UPDATING BABEL TRANSLATION FILES (FIXED) ===")
    
    # Update each language
    for lang_code, translations in INTERFACE_TRANSLATIONS.items():
        print(f"\nProcessing {lang_code}...")
        update_po_file(lang_code, translations)
    
    print("\n=== TRANSLATION FILES UPDATED ===")

if __name__ == "__main__":
    main()