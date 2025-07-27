#!/usr/bin/env python3
"""
Sistema para expandir las instrucciones originales en español
para que coincidan con el nivel de detalle de las traducciones.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_database


def expand_spanish_instructions():
    """Expandir las instrucciones originales en español para que coincidan con las traducciones."""

    print("🔄 Expandiendo instrucciones en español para mayor detalle...")

    # Inicializar base de datos
    init_database()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener todas las recetas
    cursor.execute("SELECT id, title, instructions FROM recipes")
    recipes = cursor.fetchall()

    updated_count = 0

    for recipe in recipes:
        recipe_id, title, original_instructions = recipe

        # Generar instrucciones expandidas específicas para cada receta
        expanded_instructions = get_expanded_spanish_instructions(
            title, original_instructions
        )

        if expanded_instructions != original_instructions:
            # Actualizar las instrucciones originales
            cursor.execute(
                "UPDATE recipes SET instructions = ? WHERE id = ?",
                (expanded_instructions, recipe_id),
            )

            updated_count += 1
            print(f"   ✅ {title}")

    conn.commit()
    conn.close()

    print(
        f"\n✅ {updated_count} recetas actualizadas con instrucciones expandidas en español!"
    )


def get_expanded_spanish_instructions(title, original_instructions):
    """Generar instrucciones expandidas específicas para cada receta."""

    # Instrucciones expandidas para recetas específicas
    if "Alcachofas Rellenas" in title:
        return """1. Limpiar las alcachofas y cortar la parte más dura de las hojas.

2. Cocer las alcachofas en agua salada durante unos 25 minutos hasta que estén tiernas.

3. Mezclar la carne magra, el jamón y las especias para hacer un picadillo.

4. Enfriar las alcachofas y abrirlas por la mitad, quitar el corazón y rellenar con el picadillo.

5. Preparar la salsa bechamel: derretir mantequilla, añadir harina y luego agregar leche gradualmente mientras se remueve constantemente.

6. Colocar las alcachofas en una fuente, cubrir con salsa bechamel y esparcir queso rallado por encima.

7. Precalentar el horno a 180°C y hornear durante unos 20 minutos hasta que la superficie esté dorada.

8. Servir caliente."""

    elif "Batido de Coco" in title:
        return """1. Poner el coco rallado y la leche condensada en un recipiente.

2. Utilizando una batidora o túrmix, batir durante tres minutos hasta que los ingredientes estén bien mezclados.

3. Añadir cubitos de hielo y volver a batir para hacer la mezcla más refrescante.

4. Servir en vasos altos, bien frío.

5. Si se desea, decorar con coco rallado y un poco de canela por encima."""

    elif "Corona de Cordero" in title:
        return """1. Limpiar las chuletas de cordero y quitar la grasa.

2. Mezclar todos los ingredientes del relleno: pan, cebolla picada, perejil y especias.

3. Atar las chuletas con cuerda formando una corona, dejando el relleno en el centro.

4. Sazonar la corona por fuera con sal y pimienta.

5. Batir la harina y el huevo y colocar sobre la corona.

6. Precalentar el horno a 200°C y cocinar durante 45 minutos, dando la vuelta ocasionalmente.

7. Los últimos 10 minutos bajar la temperatura a 180°C.

8. Una vez cocinado, dejar reposar 5 minutos antes de cortar."""

    elif "Pollo Marengo" in title:
        return """1. Cortar el pollo en trozos y sazonar con sal y especias.

2. Poner una sartén al fuego y freír el pollo con mantequilla hasta que tome color dorado.

3. Añadir la cebolla y el ajo y hacer un sofrito.

4. Incorporar los tomates y cocinar durante 5 minutos.

5. Agregar vino y un poco de caldo hasta cubrir el pollo.

6. Cocinar a fuego lento durante 30 minutos, bien tapado.

7. Al final añadir perejil picado y zumo de limón.

8. Servir con arroz o patatas hervidas."""

    elif "Tarta de Queso" in title:
        return """1. Precalentar el horno a 160°C.

2. Mezclar el queso, el azúcar y los huevos hasta obtener una crema suave.

3. Añadir la harina y la levadura y volver a mezclar.

4. Incorporar la leche poco a poco mientras se remueve constantemente.

5. Untar un molde con mantequilla y verter la mezcla.

6. Hornear al baño maría durante 60 minutos.

7. Apagar y no sacar del horno hasta que se enfríe.

8. Dejar una hora en la nevera antes de servir."""

    elif "Crema de Chocolate" in title:
        return """1. Poner la leche a calentar a fuego lento.

2. Trocear el chocolate en pedazos pequeños y derretir con la leche caliente.

3. Batir las yemas de huevo con azúcar hasta que estén blancas y cremosas.

4. Añadir el chocolate caliente poco a poco mientras se remueve constantemente.

5. Volver al fuego lento y cocinar durante 10 minutos, removiendo siempre.

6. Repartir en recipientes pequeños y dejar enfriar.

7. Guardar en la nevera al menos 2 horas.

8. Si se desea, decorar con nata montada y azúcar por encima."""

    elif "Crepes" in title:
        return """1. Mezclar la harina, los huevos y una pizca de sal en un bol.

2. Añadir la leche poco a poco mientras se bate para evitar grumos.

3. Dejar reposar la masa durante 30 minutos.

4. Calentar una sartén antiadherente con un poco de mantequilla.

5. Verter una pequeña cantidad de masa y extender por toda la sartén.

6. Cocinar hasta que los bordes se doren, luego dar la vuelta.

7. Cocinar el otro lado durante 1-2 minutos.

8. Servir caliente con el relleno deseado."""

    elif "Manzanas Asadas" in title:
        return """1. Precalentar el horno a 180°C.

2. Lavar las manzanas y quitar el corazón con un descorazonador.

3. Mezclar azúcar, canela y mantequilla en un bol pequeño.

4. Rellenar el hueco de las manzanas con la mezcla de azúcar.

5. Colocar las manzanas en una fuente de horno.

6. Añadir un poco de agua en el fondo de la fuente.

7. Hornear durante 25-30 minutos hasta que estén tiernas.

8. Servir caliente, opcionalmente con helado de vainilla."""

    elif "Flan de Coco" in title:
        return """1. Preparar el caramelo: calentar azúcar en una sartén hasta que se dore.

2. Verter el caramelo líquido en el molde y distribuir por las paredes.

3. Calentar la leche con el coco rallado a fuego lento.

4. Batir los huevos con azúcar hasta que estén bien mezclados.

5. Añadir la leche de coco tibia a los huevos batidos.

6. Colar la mezcla y verter en el molde caramelizado.

7. Hornear al baño maría a 160°C durante 45 minutos.

8. Enfriar completamente antes de desmoldar."""

    elif "Helado de Fresa" in title:
        return """1. Lavar y quitar las hojas de las fresas.

2. Triturar las fresas con un poco de azúcar hasta obtener un puré.

3. Calentar la leche con la nata en un cazo.

4. Batir las yemas con azúcar hasta que blanqueen.

5. Añadir la leche caliente a las yemas batidas, removiendo constantemente.

6. Cocinar a fuego lento hasta que espese, sin que hierva.

7. Mezclar con el puré de fresas y dejar enfriar.

8. Congelar en una heladera o removiendo cada hora durante 4 horas."""

    else:
        # Para recetas sin instrucciones específicas, expandir las existentes
        return expand_generic_instructions(original_instructions)


def expand_generic_instructions(instructions):
    """Expandir instrucciones genéricas añadiendo más detalle."""

    if not instructions or len(instructions.strip()) < 50:
        return instructions

    # Expandir instrucciones básicas comunes
    expanded = instructions

    # Expansiones comunes
    expansions = {
        "Se cuecen": "Se cuecen en agua salada durante el tiempo necesario hasta que estén tiernas",
        "Se fríe": "Se fríe en aceite caliente hasta que tome color dorado",
        "Se mezcla": "Se mezcla cuidadosamente hasta obtener una preparación homogénea",
        "Se añade": "Se añade gradualmente mientras se remueve constantemente",
        "Se sirve": "Se sirve inmediatamente mientras esté caliente",
        "al horno": "al horno precalentado a temperatura media",
        "hasta que": "hasta que esté en su punto óptimo",
        "se gratina": "se gratina en el horno hasta que la superficie esté dorada",
        "se bate": "se bate enérgicamente hasta obtener la consistencia deseada",
    }

    for basic, detailed in expansions.items():
        expanded = expanded.replace(basic, detailed)

    return expanded


if __name__ == "__main__":
    expand_spanish_instructions()
