#!/usr/bin/env python3
"""
Script to update the remaining 40 recipe descriptions with gastronomic and emotional tone.
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Enhanced descriptions for the remaining recipes with gastronomic and emotional tone
REMAINING_DESCRIPTIONS = {
    180: (
        "Sumérgete en la delicadeza suprema de esta Tarta Teresa Ferri, una obra de arte culinaria que "
        "combina la textura crujiente de las galletas trituradas con la sedosa suavidad de la crema de leche "
        "condensada. Cada bocado es una caricia al paladar que evoca tardes de domingo en cocinas llenas de "
        "amor, donde las manos expertas transforman ingredientes simples en momentos de pura felicidad. La "
        "cocción lenta en horno flojo permite que los sabores se fundan en perfecta armonía, creando una "
        "experiencia que trasciende lo dulce para convertirse en un abrazo gastronómico."
    ),
    181: (
        "Descubre la nostalgia hecha postre en esta Tarta de Manzana Lolita, donde la tradición familiar se "
        "convierte en pura magia culinaria. Los panecillos empapados en leche azucarada crean una base "
        "melosa que abraza las capas de manzana caramelizada, mientras que el azúcar se transforma en notas "
        "cristalinas que danzan en el paladar. Cada capa cuenta una historia de generaciones que supieron "
        "encontrar la belleza en la simplicidad, convirtiendo este postre en un viaje emocional hacia los "
        "recuerdos más dulces de la infancia."
    ),
    182: (
        "Déjate envolver por la sofisticación parisina de este Moka, un postre que es pura elegancia en cada "
        "cucharada. El café intenso se funde con la mantequilla cremosa y las claras montadas, creando una "
        "sinfonía de texturas que despiertan los sentidos más refinados. Las galletas empapadas en café "
        "aportan una base aromática que contrasta con la ligereza etérea del mousse, mientras que cada capa "
        "revela nuevos matices que evocan cafeterías bohemias y tardes de lluvia. Es la perfecta culminación "
        "para cenas íntimas y momentos de contemplación."
    ),
    183: (
        "Experimenta la simplicidad sublime de este Flan de Coco en su versión más pura, donde la esencia "
        "tropical se concentra en cada cremosa cucharada. El coco rallado libera sus aceites naturales "
        "durante la cocción, creando una textura sedosa que se derrite en la boca como una caricia tropical. "
        "La cocción rápida en olla permite que los sabores se intensifiquen, convirtiendo este humilde "
        "postre en una explosión de sensaciones que transportan a playas paradisíacas y atardeceres dorados."
    ),
    184: (
        "Redescubre la alegría de la infancia con estas Galletas Rellenas, pequeños tesoros gastronómicos "
        "que despiertan sonrisas en cada bocado. La mermelada frutal se esconde entre las capas de bizcocho "
        "esponjoso, mientras que el baño de leche azucarada las envuelve en dulzura cremosa. El coco rallado "
        "que las corona añade una textura crujiente que contrasta con la suavidad interior, creando un juego "
        "de sensaciones que evoca meriendas familiares y risas compartidas alrededor de la mesa."
    ),
    185: (
        "Sumérgete en la esencia misma de la repostería con esta Crema Pastelera, la base fundamental que ha "
        "dado vida a miles de dulces sueños. La leche se transforma en seda líquida cuando se funde con las "
        "yemas doradas, mientras que el azúcar aporta esa dulzura que acaricia el alma. El toque de cacao "
        "despierta los sentidos con su profundidad aromática, convirtiendo esta crema en el alma de tartas y "
        "postres que han alimentado generaciones de golosos. Es la prueba de que la perfección reside en la "
        "simplicidad ejecutada con maestría."
    ),
    186: (
        "Déjate cautivar por la elegancia rústica de estas Manzanas Asadas, donde la fruta se convierte en "
        "una joya gastronómica que celebra los sabores del otoño. La mantequilla derretida se mezcla con el "
        "azúcar caramelizado, creando un relleno que se funde con la pulpa de la manzana durante la cocción. "
        "El jerez aporta notas complejas que elevan el postre a nuevas alturas, mientras que la salsa de "
        "maicena envuelve cada porción en una caricia dorada que promete momentos de puro confort."
    ),
    187: (
        "Refréscate con la cremosidad tropical de este Helado de Coco casero, donde cada cucharada es un "
        "escape a paraísos lejanos. El coco se funde con la leche creando una base sedosa que se espesa "
        "lentamente, concentrando los sabores hasta lograr una intensidad que despierta los sentidos. La "
        "textura cremosa que se logra con la cocción paciente contrasta con la frescura helada, creando un "
        "postre que es tanto refugio como celebración, perfecto para esos días cuando el alma necesita un "
        "toque de dulzura tropical."
    ),
    188: (
        "Indúlgate con la decadencia pura de esta Crema de Chocolate, donde el cacao se convierte en "
        "protagonista de una sinfonía de sensaciones. La mantequilla cremosa se funde con el chocolate, "
        "creando una base rica que se alivia con las claras montadas, logrando una textura que flota en el "
        "paladar como una nube de placer. Servida en vasitos individuales y coronada con nata, cada porción "
        "es una pequeña obra de arte que promete momentos de pura indulgencia y satisfacción."
    ),
    189: (
        "Descubre el arte de la decoración pastelera con este Chocolate para Adorno, donde la técnica del "
        "baño maría se convierte en ritual de perfección. El chocolate se derrite lentamente, fundiéndose "
        "con la mantequilla hasta alcanzar una consistencia sedosa que se adhiere perfectamente a cualquier "
        "creación. La yema de huevo aporta brillo y suavidad, convirtiendo este chocolate en el toque final "
        "que transforma pasteles simples en obras maestras dignas de las mejores pastelerías."
    ),
    190: (
        "Transporta tu cocina a las calles de París con estas Crepes auténticas, donde la simplicidad "
        "francesa se convierte en elegancia gastronómica. La masa fina se extiende dorada en la sartén, "
        "creando una textura delicada que abraza la mermelada frutal con suavidad sedosa. Cada crepe es un "
        "lienzo en blanco que permite que los sabores de la mermelada se expresen en toda su intensidad, "
        "mientras que el calor del servicio despierta los aromas que evocan cafeterías parisinas y domingos "
        "perezosos."
    ),
    191: (
        "Sumérgete en la tradición del hogar con este Puding de Manzana, donde cada capa cuenta una historia "
        "de amor culinario. El molde caramelizado crea una base dorada que se funde con las capas alternadas "
        "de manzana tierna y pan empapado en natillas. La cocción lenta en horno permite que todos los "
        "sabores se integren en perfecta armonía, creando un postre que es abrazo, recuerdo y celebración, "
        "perfecto para esos momentos cuando el alma necesita ser consolada con dulzura casera."
    ),
    192: (
        "Déjate seducir por la sofisticación cítrica de esta Tarta de Naranja Donat, una creación elaborada "
        "que eleva la naranja a categoría de arte culinario. La pasta quebrada crujiente contrasta con el "
        "relleno de naranjas cocidas, mientras que la crema de leche aromatizada envuelve cada bocado en "
        "suavidad cremosa. Los cítricos liberan sus aceites esenciales durante la cocción, creando una "
        "explosión de frescura que despierta los sentidos y transporta a huertos mediterráneos bañados por "
        "el sol."
    ),
    193: (
        "Experimenta la dulzura tropical de esta Tarta de Piña, donde la fruta exótica se convierte en "
        "protagonista de una sinfonía de sabores. El caldo natural de la piña se transforma en una crema "
        "sedosa que abraza cada porción con su dulzura característica, mientras que la base mantecosa aporta "
        "el contraste perfecto. Cada bocado es un viaje a islas paradisíacas donde la piña madura bajo el "
        "sol tropical, convirtiendo este postre en una celebración de los sabores más puros y naturales."
    ),
    194: (
        "Conecta con las raíces de la repostería casera a través de esta Tarta de Bicarbonato Pepica, donde "
        "la simplicidad se convierte en elegancia rústica. El aceite se funde con el azúcar creando una "
        "textura húmeda y esponjosa, mientras que la canela y la ralladura de limón aportan esas notas "
        "aromáticas que convierten cada bocado en un abrazo familiar. Es la prueba de que los postres más "
        "memorables nacen de ingredientes humildes pero trabajados con amor y paciencia."
    ),
    195: (
        "Viaja a los Alpes austriacos con esta Tarta de Manzana Tirol, donde la tradición centroeuropea se "
        "expresa en cada delicioso bocado. La masa de mantequilla se deshace en el paladar, revelando un "
        "relleno aromático de manzana rallada que se perfuma con canela y se enriquece con el toque "
        "sofisticado del coñac. Las pasas aportan notas dulces concentradas que contrastan con la acidez de "
        "la manzana, creando una sinfonía de sabores que evoca cabañas alpinas y tardes de invierno junto al "
        "fuego."
    ),
    196: (
        "Descubre la elegancia de lo salado con esta Tarta de Bacon y Queso, donde el contraste de sabores "
        "crea una experiencia gastronómica única. El bacon frito aporta esa textura crujiente y sabor "
        "ahumado que se equilibra perfectamente con la cremosidad del queso, mientras que la base de pasta "
        "quebrada sostiene esta sinfonía de sabores. Los huevos batidos ligan todos los ingredientes en una "
        "mezcla sedosa que se transforma en el horno, creando un plato que es tanto comfort food como "
        "sofisticación culinaria."
    ),
    197: (
        "Sorprende tus sentidos con esta Tarta de Mermelada, Fresa y Nata, donde la frescura frutal se "
        "encuentra con la cremosidad láctea. La masa única hecha con cerveza y aceite aporta una textura "
        "esponjosa que abraza la mermelada de fresas, mientras que la nata fría corona cada porción con su "
        "dulzura etérea. El contraste entre la calidez de la tarta y la frescura de la nata crea una "
        "experiencia sensorial que celebra los sabores del verano y la alegría de los postres compartidos."
    ),
    198: (
        "Déjate refrescar por la elegancia tropical de esta Tarta de Piña y Nata, un postre frío que es pura "
        "sofisticación en cada cucharada. La piña aporta su dulzura natural que se equilibra con la "
        "cremosidad de la nata, mientras que la cola de pescado proporciona esa textura sedosa que se "
        "desliza suavemente por el paladar. Servida congelada, cada porción es un escape refrescante que "
        "transporta a veranos eternos y momentos de pura felicidad."
    ),
    199: (
        "Sumérgete en la riqueza aromática de esta Tarta de Nuez, donde los frutos secos se convierten en "
        "protagonistas de una sinfonía de texturas. Las nueces trituradas se funden con la mantequilla "
        "creando una base rica y aromática, mientras que el merengue de café corona la creación con su "
        "dulzura aérea. La cocción en horno permite que todos los sabores se integren, creando un postre que "
        "es tanto elegancia como sustancia, perfecto para esos momentos cuando se busca la satisfacción "
        "profunda de los sabores auténticos."
    ),
}


def update_recipe_description(recipe_id, new_description):
    """Update a single recipe description"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE recipes SET description = ? WHERE id = ?", (new_description, recipe_id)
    )
    conn.commit()
    conn.close()


def main():
    """Main function to update remaining descriptions"""
    print("🍽️ Updating remaining recipe descriptions (Part 1/2)...")
    print("=" * 60)

    updated_count = 0

    # Update descriptions for the first 20 remaining recipes
    for recipe_id, new_description in REMAINING_DESCRIPTIONS.items():
        print(f"📝 Updating recipe ID {recipe_id}")
        update_recipe_description(recipe_id, new_description)
        updated_count += 1

    print("=" * 60)
    print(f"✅ Updated {updated_count} additional recipe descriptions successfully!")
    print("🎉 Part 1 complete - continuing with remaining recipes...")


if __name__ == "__main__":
    main()
