#!/usr/bin/env python3
"""
Script to update Flask-Babel .po files with real translations from JSON files.
"""

from pathlib import Path

# Interface translations that we need in .po files
INTERFACE_TRANSLATIONS = {
    "es": {
        "Aunt Carmen's Recipes": "Recetas de la Tía Carmen",
        "Home": "Inicio",
        "Categories": "Categorías",
        "Language": "Idioma",
        "Search Recipes": "Buscar Recetas",
        "Search by name, ingredients or description...": "Buscar por nombre, ingredientes o descripción...",
        "All categories": "Todas las categorías",
        "Search": "Buscar",
        "Search results": "Resultados de búsqueda",
        "for": "para",
        "in": "en",
        "All Recipes": "Todas las Recetas",
        "Clear search": "Limpiar búsqueda",
        "View Recipe": "Ver Receta",
        "No recipes found matching your search.": "No se encontraron recetas que coincidan con tu búsqueda.",
        "View all recipes": "Ver todas las recetas",
        "Search tip": "Consejo de búsqueda",
        "You can search by recipe name, specific ingredients or dish type.": (
            "Puedes buscar por nombre de receta, ingredientes específicos o tipo de plato."
        ),
        "Ingredients": "Ingredientes",
        "Instructions": "Instrucciones",
        "Preparation": "Preparación",
        "Category": "Categoría",
        "Back to recipes": "Volver a las recetas",
        "Print recipe": "Imprimir receta",
        "Share recipe": "Compartir receta",
        "Related recipes": "Recetas relacionadas",
        "Recipe not found": "Receta no encontrada",
        "The requested recipe could not be found.": "No se pudo encontrar la receta solicitada.",
        "minutes": "minutos",
        "servings": "porciones",
        "Difficulty": "Dificultad",
        "Easy": "Fácil",
        "Medium": "Medio",
        "Hard": "Difícil",
        "Traditional family recipes": "Recetas familiares tradicionales",
        "Discover the traditional flavors of family cooking": (
            "Descubre los sabores tradicionales de la cocina familiar"
        ),
        "Preserving family culinary traditions": (
            "Preservando las tradiciones culinarias familiares"
        ),
    },
    "en": {
        "Aunt Carmen's Recipes": "Aunt Carmen's Recipes",
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
        "You can search by recipe name, specific ingredients or dish type.": (
            "You can search by recipe name, specific ingredients or dish type."
        ),
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
        "Hard": "Hard",
        "Traditional family recipes": "Traditional family recipes",
        "Discover the traditional flavors of family cooking": (
            "Discover the traditional flavors of family cooking"
        ),
        "Preserving family culinary traditions": (
            "Preserving family culinary traditions"
        ),
    },
    "zh": {
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
        "You can search by recipe name, specific ingredients or dish type.": "您可以按食谱名称、特定配料或菜肴类型搜索。",
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
        "Hard": "困难",
        "Traditional family recipes": "传统家庭食谱",
        "Discover the traditional flavors of family cooking": "探索家庭烹饪的传统风味",
        "Preserving family culinary traditions": "保护家庭烹饪传统",
    },
    "ca": {
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
        "You can search by recipe name, specific ingredients or dish type.": (
            "Pots cercar per nom de recepta, ingredients específics o tipus de plat."
        ),
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
        "Hard": "Difícil",
        "Traditional family recipes": "Receptes tradicionals familiars",
        "Discover the traditional flavors of family cooking": (
            "Descobreix els sabors tradicionals de la cuina familiar"
        ),
        "Preserving family culinary traditions": (
            "Preservant les tradicions culinàries familiars"
        ),
    },
    "eu": {
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
        "You can search by recipe name, specific ingredients or dish type.": (
            "Errezeta izenez, osagai zehatzez edo plater motaz bilatu dezakezu."
        ),
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
        "Hard": "Zaila",
        "Traditional family recipes": "Familia-errezetak tradizionalak",
        "Discover the traditional flavors of family cooking": (
            "Aurkitu familia-sukaldaritzaren zapore tradizionalak"
        ),
        "Preserving family culinary traditions": (
            "Familiaren kultura-tradizio kulinarioak mantenduz"
        ),
    },
}


def update_po_file(language_code, translations):
    """Update a .po file with proper translations"""
    po_path = Path(f"translations/{language_code}/LC_MESSAGES/messages.po")

    if not po_path.parent.exists():
        po_path.parent.mkdir(parents=True, exist_ok=True)

    # Create proper .po file content
    po_content = f"""# {language_code} translations for Recetas de la Tía Carmen
msgid ""
msgstr ""
"Project-Id-Version: Recetas de la Tía Carmen 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2024-01-01 00:00+0000\\n"
"PO-Revision-Date: 2024-01-01 00:00+0000\\n"
"Last-Translator: AI Translation System\\n"
"Language: {language_code}\\n"
"Language-Team: {language_code}\\n"
"Plural-Forms: nplurals=2; plural=(n != 1)\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

"""

    # Add all translations
    for msgid, msgstr in translations.items():
        # Escape quotes properly
        escaped_msgid = msgid.replace('"', '\\"')
        escaped_msgstr = msgstr.replace('"', '\\"')

        po_content += f'msgid "{escaped_msgid}"\n'
        po_content += f'msgstr "{escaped_msgstr}"\n\n'

    # Write the file
    with open(po_path, "w", encoding="utf-8") as f:
        f.write(po_content)

    print(f"✅ Updated {po_path} with {len(translations)} translations")


def main():
    """Main function to update all .po files with real translations"""
    print("🔄 Updating Flask-Babel .po files with real translations...")

    # Update each language
    for lang_code, translations in INTERFACE_TRANSLATIONS.items():
        update_po_file(lang_code, translations)

    print("\n✅ All .po files updated successfully!")
    print("Next step: Compile .po files to .mo files")


if __name__ == "__main__":
    main()
