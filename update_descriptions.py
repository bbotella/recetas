#!/usr/bin/env python3
"""
Script to rewrite recipe descriptions with a more gastronomic and emotional tone.
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'recipes.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Enhanced descriptions with gastronomic and emotional tone
NEW_DESCRIPTIONS = {
    147: "Déjate cautivar por este emblemático Pollo Marengo, un plato que narra la historia de una batalla ganada con cada bocado. La jugosa carne de pollo se abraza con una salsa aterciopelada de tomate, champiñones dorados y hierbas aromáticas, creando una sinfonía de sabores que despierta los sentidos. Cada cucharada te transporta a la campiña francesa, donde la tradición culinaria se fusiona con la pasión por los sabores auténticos.",
    
    148: "Experimenta la sublime armonía entre lo dulce y lo salado en esta exquisita Pularda con Manzanas. Las manzanas reinetas, caramelizadas por el calor del horno, se funden con la tierna carne de pollo, creando un contraste de texturas que deleita el paladar. El vino blanco aporta una elegancia sutil que eleva cada bocado, convirtiéndose en una experiencia gastronómica que evoca la calidez del hogar y la sofisticación de los grandes banquetes.",
    
    149: "Prepárate para ser el centro de atención con esta espectacular Corona de Cordero, una obra maestra culinaria que impresiona tanto por su presentación como por su sabor excepcional. La carne de cordero, tierna y aromática, se realza con un relleno exótico de arroz al curry que despierta los sentidos con cada bocado. Esta creación no solo alimenta el cuerpo, sino que también nutre el alma con la satisfacción de compartir algo verdaderamente especial.",
    
    150: "Sumérgete en los sabores profundos del mar con estos Arenques Asados en Vino, donde la frescura del océano se encuentra con la elegancia del vino tinto. Los arenques, pescados en su punto perfecto, absorben los matices complejos del vino, creando una experiencia gastronómica que evoca las costas mediterráneas. Las verduras salteadas y los champiñones añaden texturas contrastantes que hacen de cada bocado una pequeña celebración.",
    
    151: "Descubre la refinada elegancia de este Mus de Pollo, un paté que eleva el arte de los aperitivos a nuevas alturas. La textura sedosa y cremosa se derrite en el paladar, liberando los sabores intensos del pollo enriquecido con jerez y coñac. Es más que una entrada; es una invitación a disfrutar de los placeres culinarios más sofisticados, perfecto para esos momentos especiales que merecen ser celebrados.",
    
    152: "Embárcate en un viaje sensorial hacia Oriente con estos Huevos al Curry, donde las especias exóticas danzan en perfecta armonía con la cremosidad del huevo. La manzana aporta una dulzura sutil que equilibra el picante del curry, mientras que el arroz aromático sirve como lienzo para esta obra maestra de sabores. Cada cucharada es una explosión de contrastes que despierta emociones y transporta el alma a tierras lejanas.",
    
    153: "Déjate seducir por la simplicidad elegante de esta Rosada con Tomate, donde la frescura del mar se viste de gala con una salsa de tomate que canta al mediterráneo. La textura firme y delicada del pescado se complementa perfectamente con los sabores intensos del ajo, perejil y jerez, creando una sinfonía de aromas que evocan las cocinas tradicionales españolas. Es comfort food que alimenta tanto el cuerpo como el espíritu.",
    
    154: "Prepárate para una experiencia gastronómica de lujo con este Lenguado Relleno de Gambas y Champiñones, donde la aristocracia del mar se encuentra con la elegancia de la tierra. El lenguado, rey de los pescados planos, abraza delicadamente el relleno de gambas y champiñones, creando texturas contrastantes que explotan de sabor en cada bocado. El vino blanco aporta una sofisticación que convierte cada cena en una ocasión especial.",
    
    155: "Viaja a las estepas rusas con este auténtico Filete Estrogonoff, un plato que cuenta historias de nobleza y tradición en cada bocado. Las tiras de ternera, tiernas y jugosas, se bañan en una salsa cremosa que abraza el paladar con su textura aterciopelada. Los champiñones y cebollas añaden profundidad de sabor, mientras que la crema agria proporciona ese toque distintivo que hace de este plato una experiencia inolvidable.",
    
    156: "Déjate conquistar por estos Canelones en Salsa de Queso, donde la pasta italiana se viste de fiesta con un relleno que celebra la diversidad de sabores. Las setas, el salmón, los pimientos y guisantes crean una sinfonía de texturas y colores que deleitan tanto la vista como el paladar. La bechamel dorada y el queso gruyere gratinado forman una corona dorada que promete momentos de puro placer gastronómico.",
    
    157: "Sumérgete en la pasión del País Vasco con este Pollo a la Vasca, donde cada ingrediente cuenta una historia de tradición y sabor. El pollo se impregna de los sabores intensos del salchichón, los pimientos dulces y el arroz, creando una armonía de texturas que evoca las montañas verdes y los valles fértiles del norte de España. Es más que un plato; es un abrazo culinario que reconforta el alma.",
    
    158: "Transporta tu cocina directamente a Nápoles con esta Pizza Napolitana auténtica, donde cada mordisco es un viaje a las calles empedradas de Italia. La masa, trabajada con amor y paciencia, se convierte en el lienzo perfecto para el queso cremoso, el tomate maduro y el jamón de York. Cada ingrediente habla de tradición familiar y de la pasión italiana por convertir ingredientes simples en experiencias extraordinarias.",
    
    159: "Descubre la elegancia rústica de este Puding de Pescado, donde la humildad del pescado se transforma en una experiencia gastronómica refinada. La textura suave y cremosa se contrasta con los sabores intensos del tomate y las hierbas frescas, creando un plato que reconforta y satisface. Es cocina de abuela elevada a arte, perfecta para esos momentos cuando el alma necesita ser alimentada con cariño.",
    
    160: "Experimenta la pureza de los sabores mediterráneos con este Pescado al Horno con Vino, donde la simplicidad se convierte en elegancia. El pescado, bañado en vino blanco y aromáticas hierbas, se cocina lentamente hasta alcanzar una textura que se deshace en la boca. Cada bocado es una celebración de la frescura del mar y la tradición culinaria que convierte ingredientes simples en momentos memorables.",
    
    161: "Sumérgete en las profundidades del océano con estos Calamares en su Tinta Dana-Ona, donde el mar revela sus secretos más oscuros y sabrosos. La tinta natural crea una salsa intensa y misteriosa que abraza los tiernos chipirones, mientras que el sofrito de cebolla y tomate aporta la calidez de la cocina tradicional. Es un plato que despierta emociones primitivas y conecta con las raíces más profundas de la gastronomía costera.",
    
    162: "Déjate sorprender por la simplicidad genial de estos Pinchitos Dana-Ona, pequeñas joyas gastronómicas que concentran grandes sabores en cada bocado. Las albóndigas, jugosas y aromáticas, se coronan con pimiento dulce, creando un contraste de texturas y colores que alegra tanto la vista como el paladar. Son perfectos para compartir, despertando conversaciones y sonrisas en cada encuentro social.",
    
    163: "Eleva tu mesa con este sofisticado Pescado al Horno con Salsa Holandesa, donde la aristocracia culinaria francesa se encuentra con la frescura del mar. Los filetes de lenguado, enrollados con maestría, se bañan en una salsa holandesa aterciopelada que acaricia el paladar con su riqueza cremosa. Los camarones añaden un toque de lujo que convierte cada cena en una celebración de los placeres gastronómicos más refinados.",
    
    164: "Redescubre la cocina de antaño con este Budín de Merluza, donde la tradición familiar se convierte en arte culinario. La merluza, cocida con paciencia y amor, se transforma en una textura sedosa que se derrite en la boca, mientras que el tomate y las hierbas aportan frescura y color. Es un plato que evoca recuerdos de cocinas llenas de aromas y manos expertas que sabían transformar ingredientes simples en tesoros gastronómicos.",
    
    165: "Descubre la elegancia vegetal de estas Alcachofas Rellenas, donde la naturaleza ofrece su mejor regalo transformado en una experiencia gastronómica sublime. Cada hoja tierna abraza un relleno aromático de carnes y especias, mientras que la bechamel dorada y el queso gratinado crean una corona de sabores que despierta los sentidos. Es la prueba de que la cocina vegetariana puede ser tan satisfactoria como emocional.",
    
    166: "Experimenta la magia de la cocina francesa con este Soufflé de Espárragos, donde la ligereza del aire se combina con la intensidad del sabor. Los espárragos, nobles verduras de primavera, se elevan literalmente gracias a la técnica del soufflé, creando una textura esponjosa que contrasta con su sabor terroso y profundo. Cada cucharada es una caricia al paladar que demuestra que la cocina puede ser tanto ciencia como arte.",
    
    167: "Refresca tus sentidos con este colorido Cocktail de Tomate, donde la frescura del huerto se encuentra con la elegancia del mar. Los tomates, jugosos y aromáticos, se convierten en el recipiente perfecto para una mezcla exquisita de gambas, atún y aceitunas. La mayonesa y el toque de tabasco añaden cremosidad y un punto picante que despierta el apetito y promete momentos de puro placer gastronómico.",
    
    168: "Sumérgete en la tradición charcutera con este Paté de Pollo, donde la humildad del pollo se transforma en una experiencia gastronómica de lujo. El jerez y el coñac elevan los sabores, creando un paté cremoso y aromático que se derrite en la boca liberando capas complejas de sabor. Es el aperitivo perfecto para esos momentos especiales cuando queremos impresionar con sabores auténticos y sofisticados.",
    
    169: "Redescubre la pizza italiana con esta versión alternativa de la Pizza Napolitana, donde los sabores del mar se encuentran con la tradición italiana. Las anchoas y mejillones aportan la esencia del Mediterráneo, mientras que el tomate y las hierbas aromáticas crean una base perfecta para esta sinfonía de sabores marinos. Cada bocado es un viaje sensorial que celebra la diversidad de la cocina italiana.",
    
    170: "Déjate seducir por la cremosidad irresistible de esta Tarta de Queso, donde la simplicidad se convierte en sofisticación. El queso, protagonista absoluto, se funde con la bechamel creando una textura aterciopelada que acaricia el paladar. Las claras montadas aportan ligereza, mientras que el gratinado dorado promete ese primer bocado crujiente que da paso a una experiencia cremosa y satisfactoria.",
    
    171: "Refresca tu alma con este Helado de Fresa casero, donde la dulzura natural de la fruta se combina con la cremosidad de la nata para crear momentos de pura felicidad. Cada cucharada es una explosión de sabor a verano, evocando campos de fresas maduras bajo el sol y la satisfacción de los placeres simples de la vida. Es más que un postre; es una caricia helada que despierta sonrisas y recuerdos dulces.",
    
    172: "Conecta con las raíces familiares a través de esta Tarta de Bicarbonato de la Tía Josefina, donde cada bocado cuenta la historia de generaciones de manos expertas. La canela despierta los sentidos con su aroma cálido, mientras que la textura esponjosa evoca domingos familiares y cocinas llenas de amor. Es un tesoro gastronómico que trasciende el tiempo, conectando pasado y presente en cada dulce mordisco.",
    
    173: "Indúlgate con esta decadente Tarta de Chocolate de la Tía Marita, donde la pasión por el cacao se transforma en una experiencia casi pecaminosa. La mantequilla y las claras montadas crean una textura que se derrite en la boca, liberando ondas de sabor a chocolate que despiertan los sentidos más primitivos. Es el postre perfecto para esos momentos cuando el alma necesita ser consolada con puro placer.",
    
    174: "Revitaliza tu espíritu con este Batido de Limón o Naranja, donde la frescura cítrica se encuentra con la cremosidad del plátano para crear una bebida que es pura alegría en vaso. Los sabores brillantes y vibrantes despiertan los sentidos, mientras que la textura cremosa satisface el alma. Es la bebida perfecta para esos días cuando necesitas un rayo de sol líquido para iluminar tu día.",
    
    175: "Sumérgete en la cremosidad tropical de este Batido de Plátano, donde la dulzura natural de la fruta se combina con la leche condensada para crear una experiencia que es puro confort líquido. Cada sorbo es una caricia que relaja el alma y despierta recuerdos de infancia, cuando los sabores simples tenían el poder de crear momentos de felicidad perfecta.",
    
    176: "Viaja a paraísos tropicales con este exótico Batido de Coco, donde la cremosidad del coco se encuentra con la dulzura del helado de vainilla para crear una bebida que es pura evasión. Los sabores transportan a playas de arena blanca y aguas cristalinas, mientras que la textura cremosa abraza el paladar con su riqueza tropical. Es una vacación en vaso que despierta sueños de lugares lejanos.",
    
    177: "Déjate seducir por esta Tarta de Chocolate y Nata, donde la intensidad del chocolate se equilibra con la ligereza de la nata para crear un postre que es pura seducción. Las galletas empapadas en café aportan una base aromática que se funde con las capas cremosas, creando texturas contrastantes que explotan de sabor en cada bocado. Es el final perfecto para cenas íntimas y momentos especiales.",
    
    178: "Transporta tus sentidos a islas tropicales con este Flan de Coco, donde la cremosidad del coco se encuentra con la tradición del flan español para crear una fusión que es pura magia. El caramelo dorado contrasta con la blancura del coco, mientras que la textura sedosa se derrite en la boca liberando sabores que evocan brisas marinas y atardeceres dorados.",
    
    179: "Ilumina tu día con esta Tarta de Limón de Pepita, donde la acidez brillante del limón se equilibra con la dulzura del merengue para crear un postre que es pura alegría. La base crujiente de galletas contrasta con la cremosidad del relleno, mientras que el merengue dorado corona esta obra maestra con su textura aérea. Cada bocado es una explosión de frescura que despierta sonrisas."
}

def get_all_recipes():
    """Get all recipes from database"""
    conn = get_db_connection()
    recipes = conn.execute("SELECT * FROM recipes ORDER BY id").fetchall()
    conn.close()
    return recipes

def update_recipe_description(recipe_id, new_description):
    """Update a single recipe description"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE recipes SET description = ? WHERE id = ?",
        (new_description, recipe_id)
    )
    conn.commit()
    conn.close()

def main():
    """Main function to update all descriptions"""
    print("🍽️ Updating recipe descriptions with gastronomic and emotional tone...")
    print("=" * 60)
    
    # Get all recipes
    recipes = get_all_recipes()
    updated_count = 0
    
    # Update descriptions for recipes we have new descriptions for
    for recipe in recipes:
        if recipe['id'] in NEW_DESCRIPTIONS:
            print(f"📝 Updating: {recipe['title']}")
            update_recipe_description(recipe['id'], NEW_DESCRIPTIONS[recipe['id']])
            updated_count += 1
    
    print("=" * 60)
    print(f"✅ Updated {updated_count} recipe descriptions successfully!")
    print("🎉 All descriptions now have a more gastronomic and emotional tone!")

if __name__ == "__main__":
    main()