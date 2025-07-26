#!/usr/bin/env python3
"""
Script to add Valencian translations for all recipes (Part 1: Recipes 147-166)
Using La Ribera Alta dialect form of Valencian
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Valencian translations for recipes 147-166 (La Ribera Alta dialect)
VALENCIAN_TRANSLATIONS_PART1 = {
    147: {
        "title": "Pollastre Marengo",
        "description": "Deixa't cautivar per aquest emblemàtic Pollastre Marengo, un plat que narra la història d'una batalla guanyada amb cada mossegada. La sucosa carn de pollastre s'abraça amb una salsa aterciopopelada de tomaca, bolets daurats i herbes aromàtiques, creant una simfonia de sabors que desperta els sentits. Cada cullerada et transporta a la campanya francesa, on la tradició culinària es fusiona amb la passió pels sabors autèntics.",
        "ingredients": "### Per al pollastre:\n- 1 pollastre\n- 30 g de mantega\n- 225 g de bolets\n- 30 g de mantequilla\n\n### Per a la salsa:\n- 1 cebolla\n- 2 tomàtigues\n- 1 got de vi blanc\n- Sal i pebre\n- Herbes aromàtiques",
        "instructions": "1. El pollastre amb la sal i la mantega, es rosteix al forn 20 minuts.\n\n2. **Per a la salsa:** En una cassó es posa la cebolla picada i es sofregeix fins que estiga daurada.\n\n3. S'afegeix la tomaca pelada i picada, deixant-la coure uns minuts.\n\n4. Es tira el vi blanc i es deixa reduir.\n\n5. S'afegeixen els bolets tallats en làmines i es cou tot junt.\n\n6. Es serveix el pollastre amb la salsa per damunt.",
        "category": "Pollastre",
    },
    148: {
        "title": "Pollarda o Pollastre amb Pomes",
        "description": "Experimenta la sublim harmonia entre lo dolç i lo salat en esta exquisita Pollarda amb Pomes. Les pomes reinetes, caramel·litzades per la calor del forn, es fonen amb la tendra carn de pollastre, creant un contrast de textures que delita el paladar. El vi blanc aporta una elegància subtil que eleva cada mossegada, convertint-se en una experiència gastronòmica que evoca la calidesa de la llar i la sofisticació dels grans banquets.",
        "ingredients": "### Per al pollastre:\n- 1 pollarda o pollastre\n- 4 pomes reinetes\n- 1 got de vi blanc\n- 50 g de mantequilla\n- Sal i pebre\n- Herbes aromàtiques",
        "instructions": "1. Es neteja i es salpebra el pollastre.\n\n2. En una cassó es posa la mantequilla i es dora el pollastre per totes bandes.\n\n3. Es pelen les pomes i es tallen en quarters.\n\n4. S'afegeixen les pomes al pollastre i es tira el vi blanc.\n\n5. Es tapa la cassó i es deixa coure a foc lent durant 45 minuts.\n\n6. Es serveix calent amb la salsa que s'ha format.",
        "category": "Pollastre",
    },
    149: {
        "title": "Corona de Xai",
        "description": "Prepara't per a ser el centre d'atenció amb esta espectacular Corona de Xai, una obra mestra culinària que impressiona tant per la seua presentació com pel seu sabor excepcional. La carn de xai, tendra i aromàtica, es realça amb un farcit exòtic d'arròs al curri que desperta els sentits amb cada mossegada. Esta creació no només alimenta el cos, sinó que també nodreix l'ànima amb la satisfacció de compartir alguna cosa verdaderament especial.",
        "ingredients": "### Per a la corona:\n- 1 costillar de xai\n- 200 g d'arròs\n- 1 cullerada de curri\n- 1 cebolla\n- 50 g de mantequilla\n- Sal i pebre\n- Julivert",
        "instructions": "1. Es neteja el costillar de xai i es forma la corona.\n\n2. Es bull l'arròs amb el curri fins que estiga al dent.\n\n3. Es sofregeix la cebolla picada amb la mantequilla.\n\n4. Es mescla l'arròs amb la cebolla i es farceix el centre de la corona.\n\n5. Es rosteix al forn a 180°C durant 30-40 minuts.\n\n6. Es serveix decorat amb julivert.",
        "category": "Carns",
    },
    150: {
        "title": "Arengades Rostides en Vi",
        "description": "Submergeix-te en els sabors profunds de la mar amb estes Arengades Rostides en Vi, on la frescor de l'oceà es troba amb l'elegància del vi negre. Les arengades, pescades en el seu punt perfecte, absorbeixen els matisos complexos del vi, creant una experiència gastronòmica que evoca les costes mediterrànies. Les verdures saltejades i els bolets afegeixen textures contrastants que fan de cada mossegada una xicoteta celebració.",
        "ingredients": "### Per a les arengades:\n- 6 arengades\n- 1 got de vi negre\n- 1 cebolla\n- 200 g de bolets\n- 2 pastanagues\n- Oli d'oliva\n- Sal i pebre",
        "instructions": "1. Es netegen les arengades i es salpebren.\n\n2. En una paella es posa oli i es dauren les arengades.\n\n3. Es retiren i en el mateix oli es sofregeix la cebolla picada.\n\n4. S'afegeixen els bolets i les pastanagues tallades.\n\n5. Es tira el vi negre i es deixa reduir.\n\n6. Es tornen a posar les arengades i es rosteixen al forn 15 minuts.",
        "category": "Peix",
    },
    151: {
        "title": "Mus de Pollastre",
        "description": "Descobreix l'refinada elegància d'aquest Mus de Pollastre, un paté que eleva l'art dels aperitius a noves alçades. La textura sedosa i cremosa es fon en el paladar, alliberant els sabors intensos del pollastre enriquit amb xerès i conyac. És més que una entrada; és una invitació a gaudir dels placers culinaris més sofisticats, perfecte per a aquells moments especials que mereixen ser celebrats.",
        "ingredients": "### Per al mus:\n- 400 g de pit de pollastre\n- 100 ml de xerès\n- 50 ml de conyac\n- 200 ml de nata\n- 3 ous\n- Sal i pebre\n- Nou moscada",
        "instructions": "1. Es bull el pit de pollastre en aigua amb sal.\n\n2. Es pica finament la carn de pollastre.\n\n3. Es mescla amb el xerès, el conyac i la nata.\n\n4. S'afegeixen els ous batuts i els condiments.\n\n5. Es posa en motles i es cou al bany maria 30 minuts.\n\n6. Es deixa refredar abans de servir.",
        "category": "Altres",
    },
    152: {
        "title": "Ous al Curri",
        "description": "Embarca't en un viatge sensorial cap a Orient amb aquests Ous al Curri, on les espècies exòtiques dancen en perfecta harmonia amb la cremositat de l'ou. La poma aporta una dolçor subtil que equilibra el picant del curri, mentre que l'arròs aromàtic serveix com a llenç per a aquesta obra mestra de sabors. Cada cullerada és una explosió de contrastos que desperta emocions i transporta l'ànima a terres llunyanes.",
        "ingredients": "### Per als ous:\n- 6 ous\n- 1 poma\n- 1 cullerada de curri\n- 200 g d'arròs\n- 1 cebolla\n- Oli d'oliva\n- Sal",
        "instructions": "1. Es bullen els ous durant 10 minuts i es pelen.\n\n2. Es bull l'arròs amb sal fins que estiga al dent.\n\n3. Es sofregeix la cebolla picada amb oli.\n\n4. S'afegeix la poma pelada i picada.\n\n5. Es tira el curri i es mescla bé.\n\n6. S'afegeixen els ous tallats per la meitat i es serveix amb l'arròs.",
        "category": "Altres",
    },
    153: {
        "title": "Rosada amb Tomaca",
        "description": "Deixa't seduir per la simplicitat elegant d'aquesta Rosada amb Tomaca, on la frescor de la mar es vesteix de gala amb una salsa de tomaca que canta al mediterrani. La textura ferma i delicada del peix es complementa perfectament amb els sabors intensos de l'all, el julivert i el xerès, creant una simfonia d'aromes que evoquen les cuines tradicionals espanyoles. És comfort food que alimenta tant el cos com l'esperit.",
        "ingredients": "### Per a la rosada:\n- 1 kg de rosada\n- 4 tomàtigues\n- 3 alls\n- Julivert\n- 1 got de xerès\n- Oli d'oliva\n- Sal i pebre",
        "instructions": "1. Es neteja la rosada i es talla en trossos.\n\n2. Es sofregeix l'all picat amb oli d'oliva.\n\n3. S'afegeix la tomaca pelada i picada.\n\n4. Es deixa coure fins que estiga espessa.\n\n5. S'afegeix la rosada i el xerès.\n\n6. Es cou 15 minuts i es serveix amb julivert picat.",
        "category": "Peix",
    },
    154: {
        "title": "Llenguado Farcit de Gambes i Bolets",
        "description": "Prepara't per a una experiència gastronòmica de luxe amb aquest Llenguado Farcit de Gambes i Bolets, on l'aristocràcia de la mar es troba amb l'elegància de la terra. El llenguado, rei dels peixos plans, abraça delicadament el farcit de gambes i bolets, creant textures contrastants que exploten de sabor en cada mossegada. El vi blanc aporta una sofisticació que converteix cada sopar en una ocasió especial.",
        "ingredients": "### Per al llenguado:\n- 2 llenguados\n- 200 g de gambes\n- 150 g de bolets\n- 1 got de vi blanc\n- 100 ml de nata\n- Mantequilla\n- Sal i pebre",
        "instructions": "1. Es netegen els llenguados i es fan talls per al farcit.\n\n2. Es pelen les gambes i es piquen.\n\n3. Es sofregeixen els bolets picats amb mantequilla.\n\n4. Es mesclen les gambes amb els bolets.\n\n5. Es farceixen els llenguados i es lliguen.\n\n6. Es rosteixen al forn amb vi blanc i nata 20 minuts.",
        "category": "Peix",
    },
    155: {
        "title": "Filet Estrogonoff",
        "description": "Viatja a les estepes russes amb aquest autèntic Filet Estrogonoff, un plat que conta històries de noblesa i tradició en cada mossegada. Les tires de vedella, tendres i sucoses, es banyen en una salsa cremosa que abraça el paladar amb la seua textura aterciopopelada. Els bolets i cebes afegeixen profunditat de sabor, mentre que la nata agra proporciona aquell toc distintiu que fa d'aquest plat una experiència inoblidable.",
        "ingredients": "### Per al filet:\n- 600 g de filet de vedella\n- 200 g de bolets\n- 2 cebes\n- 200 ml de nata agra\n- Mantequilla\n- Farina\n- Sal i pebre",
        "instructions": "1. Es talla el filet en tires fines.\n\n2. Es sofregeix la ceba picada amb mantequilla.\n\n3. S'afegeixen els bolets tallats.\n\n4. Es daura la carn en una altra paella.\n\n5. Es mescla tot amb la nata agra.\n\n6. Es cou uns minuts i es serveix calent.",
        "category": "Carns",
    },
    156: {
        "title": "Canelons en Salsa de Formatge",
        "description": "Deixa't conquistar per aquests Canelons en Salsa de Formatge, on la pasta italiana es vesteix de festa amb un farcit que celebra la diversitat de sabors. Les bolets, el salmó, els pebrots i els pèsols creen una simfonia de textures i colors que deliten tant la vista com el paladar. La beixamel daurada i el formatge gruyere gratinat formen una corona daurada que promet moments de pur plaer gastronòmic.",
        "ingredients": "### Per als canelons:\n- 12 planxes de canelons\n- 200 g de salmó\n- 150 g de bolets\n- 1 pebrot\n- 100 g de pèsols\n- 500 ml de beixamel\n- Formatge gruyere\n- Oli d'oliva",
        "instructions": "1. Es bullen les planxes de canelons.\n\n2. Es sofregeixen els bolets i el pebrot.\n\n3. S'afegeix el salmó desmicolat i els pèsols.\n\n4. Es farceixen els canelons amb la mescla.\n\n5. Es col·loquen en una font amb beixamel.\n\n6. Es gratinen amb formatge al forn.",
        "category": "Altres",
    },
    157: {
        "title": "Pollastre a la Basca",
        "description": "Submergeix-te en la passió del País Basc amb aquest Pollastre a la Basca, on cada ingredient conta una història de tradició i sabor. El pollastre s'impregna dels sabors intensos del salichó, els pebrots dolços i l'arròs, creant una harmonia de textures que evoca les muntanyes verdes i les valls fèrtils del nord d'Espanya. És més que un plat; és un abraç culinari que reconforta l'ànima.",
        "ingredients": "### Per al pollastre:\n- 1 pollastre\n- 200 g de salichó\n- 2 pebrots rojos\n- 300 g d'arròs\n- 1 cebolla\n- Oli d'oliva\n- Sal i pebre",
        "instructions": "1. Es talla el pollastre en trossos.\n\n2. Es sofregeix la ceba picada amb oli.\n\n3. S'afegeixen els pebrots tallats en tires.\n\n4. Es dora el pollastre i el salichó.\n\n5. S'afegeix l'arròs i es cou amb brou.\n\n6. Es deixa reposar uns minuts abans de servir.",
        "category": "Pollastre",
    },
    158: {
        "title": "Pizza Napolitana",
        "description": "Transporta la teua cuina directament a Nàpols amb aquesta Pizza Napolitana autèntica, on cada mossegada és un viatge als carrers empedrats d'Itàlia. La massa, treballada amb amor i paciència, es converteix en el llenç perfecte per al formatge cremós, la tomaca madura i el pernil de York. Cada ingredient parla de tradició familiar i de la passió italiana per convertir ingredients simples en experiències extraordinàries.",
        "ingredients": "### Per a la pizza:\n- 300 g de farina\n- 1 sobre de llevat\n- Tomaca triturat\n- Formatge mozzarella\n- Pernil de York\n- Oli d'oliva\n- Sal",
        "instructions": "1. Es fa la massa amb farina, llevat i aigua.\n\n2. Es deixa llevar durant 1 hora.\n\n3. S'estén la massa en forma rodona.\n\n4. S'unten amb tomaca triturat.\n\n5. S'afegeix el formatge i el pernil.\n\n6. Es cou al forn molt calent durant 10 minuts.",
        "category": "Altres",
    },
    159: {
        "title": "Puding de Peix",
        "description": "Descobreix l'elegància rústica d'aquest Puding de Peix, on la humilitat del peix es transforma en una experiència gastronòmica refinada. La textura suau i cremosa es contrasta amb els sabors intensos de la tomaca i les herbes fresques, creant un plat que reconforta i satisfà. És cuina d'àvia elevada a art, perfecta per a aquells moments quan l'ànima necessita ser alimentada amb carinyo.",
        "ingredients": "### Per al puding:\n- 500 g de peix blanc\n- 3 ous\n- 100 ml de llet\n- 1 tomaca\n- Julivert\n- Mantequilla\n- Sal i pebre",
        "instructions": "1. Es bull el peix i es desmicola.\n\n2. Es baten els ous amb la llet.\n\n3. Es sofregeix la tomaca picada.\n\n4. Es mescla tot amb el peix.\n\n5. Es posa en un motle engreixat.\n\n6. Es cou al bany maria 30 minuts.",
        "category": "Peix",
    },
    160: {
        "title": "Peix al Forn amb Vi",
        "description": "Experimenta la puresa dels sabors mediterranis amb aquest Peix al Forn amb Vi, on la simplicitat es converteix en elegància. El peix, banyat en vi blanc i herbes aromàtiques, es cou lentament fins a aconseguir una textura que es desfà en la boca. Cada mossegada és una celebració de la frescor de la mar i la tradició culinària que converteix ingredients simples en moments memorables.",
        "ingredients": "### Per al peix:\n- 1 kg de peix blanc\n- 1 got de vi blanc\n- 2 llimones\n- Herbes aromàtiques\n- Oli d'oliva\n- Sal i pebre",
        "instructions": "1. Es neteja el peix i es col·loca en una font.\n\n2. Es reguega amb oli d'oliva i suc de llimona.\n\n3. S'afegeix el vi blanc i les herbes.\n\n4. Es salpebra al gust.\n\n5. Es rosteix al forn a 180°C durant 25 minuts.\n\n6. Es serveix amb la salsa que s'ha format.",
        "category": "Peix",
    },
    161: {
        "title": "Calamarins en la seua Tinta Dana-Ona",
        "description": "Submergeix-te en les profunditats de l'oceà amb aquests Calamarins en la seua Tinta Dana-Ona, on la mar revela els seus secrets més foscos i saborosos. La tinta natural crea una salsa intensa i misteriosa que abraça els tendres calamarins, mentre que el sofregit de ceba i tomaca aporta la calidesa de la cuina tradicional. És un plat que desperta emocions primitives i connecta amb les arrels més profundes de la gastronomia costanera.",
        "ingredients": "### Per als calamarins:\n- 1 kg de calamarins\n- Tinta de calamar\n- 1 ceba\n- 2 tomàtigues\n- All\n- Oli d'oliva\n- Sal i pebre",
        "instructions": "1. Es netegen els calamarins i es tallen en anells.\n\n2. Es sofregeix la ceba picada amb oli.\n\n3. S'afegeix l'all i la tomaca pelada.\n\n4. Es posen els calamarins i la tinta.\n\n5. Es cou a foc lent durant 20 minuts.\n\n6. Es serveix calent amb pa.",
        "category": "Peix",
    },
    162: {
        "title": "Pintxo Dana-Ona",
        "description": "Deixa't sorprendre per la simplicitat genial d'aquests Pintxos Dana-Ona, xicotetes joies gastronòmiques que concentren grans sabors en cada mossegada. Les mandonguilles, sucoses i aromàtiques, es coronen amb pebrot dolç, creant un contrast de textures i colors que alegra tant la vista com el paladar. Són perfectes per a compartir, despertant converses i somriures en cada trobada social.",
        "ingredients": "### Per als pintxos:\n- 300 g de carn picada\n- 1 ou\n- Julivert\n- 1 pebrot roig\n- Farina\n- Oli per a fregir\n- Sal i pebre",
        "instructions": "1. Es mescla la carn picada amb l'ou i el julivert.\n\n2. Es fan boletes xicotetes.\n\n3. S'arrebossen amb farina i es fregeixen.\n\n4. Es talla el pebrot en quadradets.\n\n5. Es munten els pintxos amb palillos.\n\n6. Es serveixen calents com a aperitiu.",
        "category": "Altres",
    },
    163: {
        "title": "Peix al Forn amb Salsa Holandesa",
        "description": "Eleva la teua taula amb aquest sofisticat Peix al Forn amb Salsa Holandesa, on l'aristocràcia culinària francesa es troba amb la frescor de la mar. Els filets de llenguado, enrollats amb maestria, es banyen en una salsa holandesa aterciopopelada que acaricia el paladar amb la seua riquesa cremosa. Les gambetes afegeixen un toc de luxe que converteix cada sopar en una celebració dels placers gastronòmics més refinats.",
        "ingredients": "### Per al peix:\n- 4 filets de llenguado\n- 200 g de gambetes\n- 3 rovells d'ou\n- 100 g de mantequilla\n- Suc de llimona\n- Sal i pebre blanc",
        "instructions": "1. Es netegen els filets i es enrollen amb les gambetes.\n\n2. Es rosteixen al forn 15 minuts.\n\n3. Per a la salsa: es baten els rovells amb suc de llimona.\n\n4. S'afegeix la mantequilla desfeta a poc a poc.\n\n5. Es bateja fins que espessisca.\n\n6. Es serveix el peix amb la salsa calenta.",
        "category": "Peix",
    },
    164: {
        "title": "Budín de Lluç",
        "description": "Redescobreix la cuina d'antany amb aquest Budín de Lluç, on la tradició familiar es converteix en art culinari. El lluç, cuit amb paciència i amor, es transforma en una textura sedosa que es desfà en la boca, mentre que la tomaca i les herbes aporten frescor i color. És un plat que evoca records de cuines plenes d'aromes i mans expertes que sabien transformar ingredients simples en tresors gastronòmics.",
        "ingredients": "### Per al budín:\n- 600 g de lluç\n- 4 ous\n- 100 ml de llet\n- 1 tomaca\n- Julivert\n- Mantequilla\n- Sal i nou moscada",
        "instructions": "1. Es bull el lluç i es desmicola.\n\n2. Es baten els ous amb la llet.\n\n3. Es sofregeix la tomaca picada.\n\n4. Es mescla tot amb el lluç i el julivert.\n\n5. Es posa en un motle i es cou al bany maria.\n\n6. Es deixa refredar abans de desmotllar.",
        "category": "Peix",
    },
    165: {
        "title": "Carxofes Farcides",
        "description": "Descobreix l'elegància vegetal d'aquestes Carxofes Farcides, on la natura ofereix el seu millor regal transformat en una experiència gastronòmica sublim. Cada fulla tendra abraça un farcit aromàtic de carns i espècies, mentre que la beixamel daurada i el formatge gratinat creen una corona de sabors que desperta els sentits. És la prova que la cuina vegetariana pot ser tan satisfactòria com emocional.",
        "ingredients": "### Per a les carxofes:\n- 6 carxofes\n- 200 g de carn picada\n- 1 ceba\n- 300 ml de beixamel\n- Formatge ratllat\n- Oli d'oliva\n- Sal i pebre",
        "instructions": "1. Es netegen les carxofes i es bulen.\n\n2. Es treu el centre i es farceixen.\n\n3. Es sofregeix la ceba i la carn.\n\n4. Es farceixen les carxofes amb la mescla.\n\n5. Es col·loquen en una font amb beixamel.\n\n6. Es gratinen amb formatge al forn.",
        "category": "Verdures",
    },
    166: {
        "title": "Soufflé d'Espàrrecs",
        "description": "Experimenta la màgia de la cuina francesa amb aquest Soufflé d'Espàrrecs, on la lleugeresa de l'aire es combina amb la intensitat del sabor. Els espàrrecs, nobles verdures de primavera, s'eleven literalment gràcies a la tècnica del soufflé, creant una textura esponjosa que contrasta amb el seu sabor terrós i profund. Cada cullerada és una carícia al paladar que demostra que la cuina pot ser tant ciència com art.",
        "ingredients": "### Per al soufflé:\n- 500 g d'espàrrecs\n- 4 ous\n- 200 ml de beixamel\n- 50 g de formatge\n- Mantequilla\n- Sal i pebre",
        "instructions": "1. Es bullen els espàrrecs i es triteren.\n\n2. Es mesclen amb la beixamel i el formatge.\n\n3. S'afegeixen els rovells d'ou.\n\n4. Es munten els clars a punt de neu.\n\n5. Es mesclen amb cura amb la preparació.\n\n6. Es cou al forn 20 minuts sense obrir.",
        "category": "Verdures",
    },
}


def insert_valencian_translations():
    """Insert Valencian translations for recipes 147-166"""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🔶 Adding Valencian translations (Part 1: Recipes 147-166)...")

    for recipe_id, translation in VALENCIAN_TRANSLATIONS_PART1.items():
        cursor.execute(
            """INSERT OR REPLACE INTO recipe_translations
               (recipe_id, language, title, description, ingredients, instructions, category)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                recipe_id,
                "va",
                translation["title"],
                translation["description"],
                translation["ingredients"],
                translation["instructions"],
                translation["category"],
            ),
        )
        print(
            f"✓ Added Valencian translation for recipe {recipe_id}: {translation['title']}"
        )

    conn.commit()
    conn.close()
    print(
        f"\n✅ Successfully added {len(VALENCIAN_TRANSLATIONS_PART1)} Valencian translations!"
    )


if __name__ == "__main__":
    insert_valencian_translations()
