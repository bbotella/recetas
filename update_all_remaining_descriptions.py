#!/usr/bin/env python3
"""
Script to update all 40 remaining recipe descriptions with gastronomic and emotional tone.
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'recipes.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Enhanced descriptions for all 40 remaining recipes with gastronomic and emotional tone
REMAINING_DESCRIPTIONS = {
    180: "Sumérgete en la delicadeza suprema de esta Tarta Teresa Ferri, una obra de arte culinaria que combina la textura crujiente de las galletas trituradas con la sedosa suavidad de la crema de leche condensada. Cada bocado es una caricia al paladar que evoca tardes de domingo en cocinas llenas de amor, donde las manos expertas transforman ingredientes simples en momentos de pura felicidad. La cocción lenta en horno flojo permite que los sabores se fundan en perfecta armonía, creando una experiencia que trasciende lo dulce para convertirse en un abrazo gastronómico.",
    
    181: "Descubre la nostalgia hecha postre en esta Tarta de Manzana Lolita, donde la tradición familiar se convierte en pura magia culinaria. Los panecillos empapados en leche azucarada crean una base melosa que abraza las capas de manzana caramelizada, mientras que el azúcar se transforma en notas cristalinas que danzan en el paladar. Cada capa cuenta una historia de generaciones que supieron encontrar la belleza en la simplicidad, convirtiendo este postre en un viaje emocional hacia los recuerdos más dulces de la infancia.",
    
    182: "Déjate envolver por la sofisticación parisina de este Moka, un postre que es pura elegancia en cada cucharada. El café intenso se funde con la mantequilla cremosa y las claras montadas, creando una sinfonía de texturas que despiertan los sentidos más refinados. Las galletas empapadas en café aportan una base aromática que contrasta con la ligereza etérea del mousse, mientras que cada capa revela nuevos matices que evocan cafeterías bohemias y tardes de lluvia. Es la perfecta culminación para cenas íntimas y momentos de contemplación.",
    
    183: "Experimenta la simplicidad sublime de este Flan de Coco en su versión más pura, donde la esencia tropical se concentra en cada cremosa cucharada. El coco rallado libera sus aceites naturales durante la cocción, creando una textura sedosa que se derrite en la boca como una caricia tropical. La cocción rápida en olla permite que los sabores se intensifiquen, convirtiendo este humilde postre en una explosión de sensaciones que transportan a playas paradisíacas y atardeceres dorados.",
    
    184: "Redescubre la alegría de la infancia con estas Galletas Rellenas, pequeños tesoros gastronómicos que despiertan sonrisas en cada bocado. La mermelada frutal se esconde entre las capas de bizcocho esponjoso, mientras que el baño de leche azucarada las envuelve en dulzura cremosa. El coco rallado que las corona añade una textura crujiente que contrasta con la suavidad interior, creando un juego de sensaciones que evoca meriendas familiares y risas compartidas alrededor de la mesa.",
    
    185: "Sumérgete en la esencia misma de la repostería con esta Crema Pastelera, la base fundamental que ha dado vida a miles de dulces sueños. La leche se transforma en seda líquida cuando se funde con las yemas doradas, mientras que el azúcar aporta esa dulzura que acaricia el alma. El toque de cacao despierta los sentidos con su profundidad aromática, convirtiendo esta crema en el alma de tartas y postres que han alimentado generaciones de golosos. Es la prueba de que la perfección reside en la simplicidad ejecutada con maestría.",
    
    186: "Déjate cautivar por la elegancia rústica de estas Manzanas Asadas, donde la fruta se convierte en una joya gastronómica que celebra los sabores del otoño. La mantequilla derretida se mezcla con el azúcar caramelizado, creando un relleno que se funde con la pulpa de la manzana durante la cocción. El jerez aporta notas complejas que elevan el postre a nuevas alturas, mientras que la salsa de maicena envuelve cada porción en una caricia dorada que promete momentos de puro confort.",
    
    187: "Refréscate con la cremosidad tropical de este Helado de Coco casero, donde cada cucharada es un escape a paraísos lejanos. El coco se funde con la leche creando una base sedosa que se espesa lentamente, concentrando los sabores hasta lograr una intensidad que despierta los sentidos. La textura cremosa que se logra con la cocción paciente contrasta con la frescura helada, creando un postre que es tanto refugio como celebración, perfecto para esos días cuando el alma necesita un toque de dulzura tropical.",
    
    188: "Indúlgate con la decadencia pura de esta Crema de Chocolate, donde el cacao se convierte en protagonista de una sinfonía de sensaciones. La mantequilla cremosa se funde con el chocolate, creando una base rica que se alivia con las claras montadas, logrando una textura que flota en el paladar como una nube de placer. Servida en vasitos individuales y coronada con nata, cada porción es una pequeña obra de arte que promete momentos de pura indulgencia y satisfacción.",
    
    189: "Descubre el arte de la decoración pastelera con este Chocolate para Adorno, donde la técnica del baño maría se convierte en ritual de perfección. El chocolate se derrite lentamente, fundiéndose con la mantequilla hasta alcanzar una consistencia sedosa que se adhiere perfectamente a cualquier creación. La yema de huevo aporta brillo y suavidad, convirtiendo este chocolate en el toque final que transforma pasteles simples en obras maestras dignas de las mejores pastelerías.",
    
    190: "Transporta tu cocina a las calles de París con estas Crepes auténticas, donde la simplicidad francesa se convierte en elegancia gastronómica. La masa fina se extiende dorada en la sartén, creando una textura delicada que abraza la mermelada frutal con suavidad sedosa. Cada crepe es un lienzo en blanco que permite que los sabores de la mermelada se expresen en toda su intensidad, mientras que el calor del servicio despierta los aromas que evocan cafeterías parisinas y domingos perezosos.",
    
    191: "Sumérgete en la tradición del hogar con este Puding de Manzana, donde cada capa cuenta una historia de amor culinario. El molde caramelizado crea una base dorada que se funde con las capas alternadas de manzana tierna y pan empapado en natillas. La cocción lenta en horno permite que todos los sabores se integren en perfecta armonía, creando un postre que es abrazo, recuerdo y celebración, perfecto para esos momentos cuando el alma necesita ser consolada con dulzura casera.",
    
    192: "Déjate seducir por la sofisticación cítrica de esta Tarta de Naranja Donat, una creación elaborada que eleva la naranja a categoría de arte culinario. La pasta quebrada crujiente contrasta con el relleno de naranjas cocidas, mientras que la crema de leche aromatizada envuelve cada bocado en suavidad cremosa. Los cítricos liberan sus aceites esenciales durante la cocción, creando una explosión de frescura que despierta los sentidos y transporta a huertos mediterráneos bañados por el sol.",
    
    193: "Experimenta la dulzura tropical de esta Tarta de Piña, donde la fruta exótica se convierte en protagonista de una sinfonía de sabores. El caldo natural de la piña se transforma en una crema sedosa que abraza cada porción con su dulzura característica, mientras que la base mantecosa aporta el contraste perfecto. Cada bocado es un viaje a islas paradisíacas donde la piña madura bajo el sol tropical, convirtiendo este postre en una celebración de los sabores más puros y naturales.",
    
    194: "Conecta con las raíces de la repostería casera a través de esta Tarta de Bicarbonato Pepica, donde la simplicidad se convierte en elegancia rústica. El aceite se funde con el azúcar creando una textura húmeda y esponjosa, mientras que la canela y la ralladura de limón aportan esas notas aromáticas que convierten cada bocado en un abrazo familiar. Es la prueba de que los postres más memorables nacen de ingredientes humildes pero trabajados con amor y paciencia.",
    
    195: "Viaja a los Alpes austriacos con esta Tarta de Manzana Tirol, donde la tradición centroeuropea se expresa en cada delicioso bocado. La masa de mantequilla se deshace en el paladar, revelando un relleno aromático de manzana rallada que se perfuma con canela y se enriquece con el toque sofisticado del coñac. Las pasas aportan notas dulces concentradas que contrastan con la acidez de la manzana, creando una sinfonía de sabores que evoca cabañas alpinas y tardes de invierno junto al fuego.",
    
    196: "Descubre la elegancia de lo salado con esta Tarta de Bacon y Queso, donde el contraste de sabores crea una experiencia gastronómica única. El bacon frito aporta esa textura crujiente y sabor ahumado que se equilibra perfectamente con la cremosidad del queso, mientras que la base de pasta quebrada sostiene esta sinfonía de sabores. Los huevos batidos ligan todos los ingredientes en una mezcla sedosa que se transforma en el horno, creando un plato que es tanto comfort food como sofisticación culinaria.",
    
    197: "Sorprende tus sentidos con esta Tarta de Mermelada, Fresa y Nata, donde la frescura frutal se encuentra con la cremosidad láctea. La masa única hecha con cerveza y aceite aporta una textura esponjosa que abraza la mermelada de fresas, mientras que la nata fría corona cada porción con su dulzura etérea. El contraste entre la calidez de la tarta y la frescura de la nata crea una experiencia sensorial que celebra los sabores del verano y la alegría de los postres compartidos.",
    
    198: "Déjate refrescar por la elegancia tropical de esta Tarta de Piña y Nata, un postre frío que es pura sofisticación en cada cucharada. La piña aporta su dulzura natural que se equilibra con la cremosidad de la nata, mientras que la cola de pescado proporciona esa textura sedosa que se desliza suavemente por el paladar. Servida congelada, cada porción es un escape refrescante que transporta a veranos eternos y momentos de pura felicidad.",
    
    199: "Sumérgete en la riqueza aromática de esta Tarta de Nuez, donde los frutos secos se convierten en protagonistas de una sinfonía de texturas. Las nueces trituradas se funden con la mantequilla creando una base rica y aromática, mientras que el merengue de café corona la creación con su dulzura aérea. La cocción en horno permite que todos los sabores se integren, creando un postre que es tanto elegancia como sustancia, perfecto para esos momentos cuando se busca la satisfacción profunda de los sabores auténticos.",
    
    200: "Refréscate con la dulzura tropical de este Helado de Plátano, donde la fruta madura se convierte en protagonista de una sinfonía helada. La leche concentrada envuelve los plátanos en cremosidad láctea, mientras que el toque de limón aporta esa acidez que realza los sabores naturales. Cortado en cachitos para servir, cada porción es una pequeña celebración de la simplicidad hecha arte, perfecta para esos momentos cuando el alma necesita ser consolada con dulzura pura y refrescante.",
    
    201: "Descubre la genialidad de la repostería práctica con esta Tarta de Yogurt, donde la simplicidad se convierte en sabiduría culinaria. El yogurt actúa como medida universal, creando una textura esponjosa que se perfuma con ralladura de limón y se eleva con la levadura Royal. Cada bocado es una explosión de frescura láctea que demuestra que los postres más satisfactorios nacen de la combinación inteligente de ingredientes cotidianos transformados en pura magia gastronómica.",
    
    202: "Sumérgete en la versatilidad de la repostería clásica con este Bizcocho y Tortada, donde la tradición se adapta a los gustos personales. La clara montada aporta esa ligereza etérea que hace que cada bocado se deshaga en el paladar, mientras que en su variante tortada, la almendra molida sustituye a la harina creando una textura rica y aromática. Es la prueba de que los postres básicos pueden ser la base de infinitas posibilidades creativas.",
    
    203: "Déjate cautivar por la acidez refrescante de esta Tarta de Limón Carmela, donde los cítricos se convierten en protagonistas de una sinfonía de contrastes. La pasta de mantequilla y manteca crea una base rica que contrasta con la intensidad de la crema de limón, mientras que el gratinado final aporta esa textura dorada que promete el primer bocado crujiente. Cada porción es una explosión de frescura que despierta los sentidos y transporta a huertos mediterráneos bañados por el sol.",
    
    204: "Experimenta la elegancia de lo frío con esta Tarta de Carlota, donde los sabores del café se encuentran con la sofisticación del coñac. La carlota triturada se funde con las galletas empapadas, creando una base aromática que se corona con coco rallado. El contraste entre la intensidad del café y la dulzura del coco crea una experiencia sensorial que evoca salones elegantes y tardes de invierno junto al fuego.",
    
    205: "Redescubre la cremosidad del queso en esta Tarta de Queso alternativa, donde los quesitos se transforman en protagonistas de una sinfonía láctea. La base de galletas molidas y mantequilla aporta esa textura crujiente que contrasta con la suavidad del relleno, mientras que la mezcla de quesitos, leche y huevos se transforma en el horno en una crema sedosa que abraza el paladar con su dulzura característica.",
    
    206: "Déjate seducir por los sabores mediterráneos de este Lomo a la Naranja con Olla, donde la carne se transforma en una experiencia gastronómica única. El lomo dorado se impregna de los jugos cítricos de la naranja, mientras que el jerez aporta notas complejas que elevan el plato a nuevas alturas. El orégano perfuma cada bocado con su aroma característico, creando un guiso que es tanto comfort food como sofisticación culinaria.",
    
    207: "Sumérgete en la creatividad culinaria con estas Tortillas de Pisos, donde cada capa cuenta una historia de sabores diferentes. Las tortillas se apilan como pisos de un edificio gastronómico, separadas por capas de tomate frito perfumado con curry que aporta ese toque exótico. Cada bocado es una aventura sensorial que demuestra que la comida puede ser tanto arte como sustancia, perfecta para esos momentos cuando se busca sorprender y deleitar.",
    
    208: "Descubre la elegancia de la charcutería casera con este Trufado María Teresa, donde el magro picado se convierte en una experiencia gastronómica refinada. Las lechugas aportan frescura que contrasta con la riqueza de los huevos y especias, mientras que las trufas elevan el plato a categoría de lujo. La cocción al baño maría permite que todos los sabores se integren lentamente, creando una terrina que es tanto arte como tradición.",
    
    209: "Experimenta la sofisticación de la carne rellena con este Lomo Relleno, donde cada corte revela una sorpresa gastronómica. El lomo abierto como un libro abraza el relleno de huevos duros y jamón, mientras que la mantequilla dorada crea una superficie crujiente que contrasta con la jugosidad interior. La leche y naranja aportan notas dulces que equilibran los sabores salados, creando un plato que es tanto elegancia como sustancia.",
    
    210: "Sumérgete en la tradición cinegética con este Faisán a la Cazuela, donde la caza se convierte en protagonista de una experiencia gastronómica única. El faisán se cocina lentamente rodeado de lomo fino y cebolla, absorbiendo todos los sabores del guiso, mientras que la nata sin montar corona el plato con su cremosidad característica. Es la prueba de que los platos tradicionales pueden ser tanto rústicos como sofisticados.",
    
    211: "Viaja a Bélgica con este Faisán a la Belga, donde la caza se encuentra con la tradición culinaria europea. Las endivias aportan ese toque amargo característico que contrasta con la riqueza de la carne, mientras que las zanahorias y cebolla crean una base aromática que se intensifica durante el estofado. Servido sobre un lecho de endivias cocidas, cada bocado es una celebración de los sabores auténticos y la cocina tradicional.",
    
    212: "Déjate reconfortar con estas Espinacas a la Crema, donde las verduras se convierten en protagonistas de una sinfonía de sabores. La cebolla y ajos aportan esa base aromática que realza el sabor terroso de las espinacas, mientras que la bechamel las envuelve en cremosidad sedosa. El gratinado final crea una superficie dorada que promete el primer bocado crujiente, convirtiendo este plato en comfort food elevado a arte culinario.",
    
    213: "Experimenta la frescura primaveral con estos Guisantes con Jamón, donde la verdura tierna se encuentra con la intensidad del jamón curado. El jamón, cebolla, perejil y ajo crean una base aromática que se intensifica con la cocción en caldo, mientras que el cogollo de lechuga aporta frescura y textura. Es la prueba de que los platos simples pueden ser tanto nutritivos como deliciosos cuando se preparan con amor y respeto por los ingredientes.",
    
    214: "Descubre la elegancia italiana con esta Ternera a la Italiana, donde la carne se transforma en una experiencia gastronómica refinada. Las chuletas rebozadas con harina se doran hasta alcanzar una textura crujiente que contrasta con la jugosidad interior, mientras que el jamón aporta notas salinas que se equilibran con el jerez y caldo. Cada bocado es una celebración de la simplicidad italiana hecha arte culinario.",
    
    215: "Sumérgete en la sofisticación de lo salado con esta Tarta de Cebolla, donde la humilde cebolla se convierte en protagonista de una sinfonía de sabores. La cebolla pochada lentamente desarrolla una dulzura natural que se equilibra con la cremosidad de la nata y la intensidad del queso gruyere. La base de pasta quebrada aporta esa textura crujiente que contrasta con la suavidad del relleno, creando un plato que es tanto elegancia como comfort food.",
    
    216: "Redescubre la alegría de los sabores marineros con estos Emparedados de Merluza, donde el pescado se viste de fiesta con jamón y queso. La merluza fresca se funde con el jamón y queso creando una combinación que explota de sabor en cada bocado, mientras que el rebozado crujiente aporta esa textura que contrasta con la suavidad interior. Fritos en abundante aceite, cada emparedado es una pequeña celebración de los sabores del mar.",
    
    217: "Déjate seducir por la simplicidad sofisticada de este Pollo con Mostaza, donde el ave se transforma en una experiencia gastronómica única. El adobo de mostaza y mantequilla penetra en cada fibra de la carne, mientras que la cocción al horno permite que los sabores se concentren. La nata final corona el plato con su cremosidad característica, creando un contraste de texturas que convierte cada bocado en una caricia al paladar.",
    
    218: "Experimenta la elegancia dorada de esta Merluza a la Bechamel, donde el pescado se viste de gala con una salsa que es pura sofisticación. Los filetes rebozados y fritos crean una base crujiente que contrasta con la cremosidad de la bechamel de tomate, mientras que el queso y especias aportan notas complejas que elevan el plato a nuevas alturas. El gratinado final promete ese primer bocado dorado que da paso a una experiencia sensorial completa.",
    
    219: "Sumérgete en la versatilidad gastronómica de este Pastel de Patata, donde el humilde tubérculo se convierte en lienzo para infinitas posibilidades. El puré de patata cremoso abraza rellenos variados que van desde las espinacas frescas hasta el atún con tomate o el magro con jamón, mientras que la cocción al horno crea una superficie dorada que promete momentos de puro confort. Es la prueba de que los ingredientes simples pueden ser la base de creaciones extraordinarias."
}

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
    """Main function to update all remaining descriptions"""
    print("🍽️ Updating all 40 remaining recipe descriptions...")
    print("=" * 60)
    
    updated_count = 0
    
    # Update descriptions for all remaining recipes
    for recipe_id, new_description in REMAINING_DESCRIPTIONS.items():
        print(f"📝 Updating recipe ID {recipe_id}")
        update_recipe_description(recipe_id, new_description)
        updated_count += 1
    
    print("=" * 60)
    print(f"✅ Updated {updated_count} additional recipe descriptions successfully!")
    print("🎉 All remaining recipes now have gastronomic and emotional descriptions!")

if __name__ == "__main__":
    main()