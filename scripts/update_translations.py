#!/usr/bin/env python3
"""
Script to update English and Chinese translations with gastronomic and emotional tone.
"""

import sqlite3
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "recipes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Enhanced English translations with gastronomic and emotional tone
ENGLISH_TRANSLATIONS = {
    147: (
        "Let yourself be captivated by this emblematic Chicken Marengo, a dish that tells the story of a victorious battle with every bite. "
        "The juicy chicken meat embraces a velvety sauce of tomatoes, golden mushrooms, and aromatic herbs, creating a symphony of flavors that awakens the senses. "
        "Each spoonful transports you to the French countryside, where culinary tradition merges with a passion for authentic flavors."
    ),
    148: (
        "Experience the sublime harmony between sweet and savory in this exquisite Pularda with Apples. "
        "The reinette apples, caramelized by the heat of the oven, meld with the tender chicken meat, creating a contrast of textures that delights the palate. "
        "The white wine provides a subtle elegance that elevates each bite, becoming a gastronomic experience that evokes the warmth of home and the sophistication of grand banquets."
    ),
    149: (
        "Prepare to be the center of attention with this spectacular Crown of Lamb, a culinary masterpiece that impresses as much with its presentation as with its exceptional flavor. "
        "The lamb meat, tender and aromatic, is enhanced with an exotic curry rice filling that awakens the senses with each bite. "
        "This creation not only nourishes the body but also feeds the soul with the satisfaction of sharing something truly special."
    ),
    150: (
        "Immerse yourself in the deep flavors of the sea with these Wine-Roasted Herrings, where the freshness of the ocean meets the elegance of red wine. "
        "The herrings, caught at their perfect point, absorb the complex nuances of the wine, creating a gastronomic experience that evokes Mediterranean coasts. "
        "The sautéed vegetables and mushrooms add contrasting textures that make each bite a small celebration."
    ),
    151: (
        "Discover the refined elegance of this Chicken Mousse, a pâté that elevates the art of appetizers to new heights. "
        "The silky, creamy texture melts on the palate, releasing the intense flavors of chicken enriched with sherry and cognac. "
        "It's more than an appetizer; it's an invitation to enjoy the most sophisticated culinary pleasures, perfect for those special moments that deserve to be celebrated."
    ),
    152: (
        "Embark on a sensory journey to the Orient with these Curried Eggs, where exotic spices dance in perfect harmony with the creaminess of the egg. "
        "The apple provides a subtle sweetness that balances the spiciness of the curry, while the aromatic rice serves as a canvas for this masterpiece of flavors. "
        "Each spoonful is an explosion of contrasts that awakens emotions and transports the soul to distant lands."
    ),
    153: (
        "Let yourself be seduced by the elegant simplicity of this Pink Snapper with Tomatoes, where the freshness of the sea dresses up with a tomato sauce that sings to the Mediterranean. "
        "The firm yet delicate texture of the fish complements perfectly with the intense flavors of garlic, parsley, and sherry, creating a symphony of aromas that evoke traditional Spanish kitchens. "
        "It's comfort food that nourishes both body and spirit."
    ),
    154: (
        "Prepare for a luxury gastronomic experience with this Sole Stuffed with Shrimp and Mushrooms, where the aristocracy of the sea meets the elegance of the land. "
        "The sole, king of flatfish, delicately embraces the shrimp and mushroom filling, creating contrasting textures that explode with flavor in every bite. "
        "The white wine adds sophistication that turns every dinner into a special occasion."
    ),
    155: (
        "Travel to the Russian steppes with this authentic Beef Stroganoff, a dish that tells stories of nobility and tradition in every bite. "
        "The beef strips, tender and juicy, bathe in a creamy sauce that embraces the palate with its velvety texture. "
        "The mushrooms and onions add depth of flavor, while the sour cream provides that distinctive touch that makes this dish an unforgettable experience."
    ),
    156: (
        "Let yourself be conquered by these Cannelloni in Cheese Sauce, where Italian pasta dresses up for a party with a filling that celebrates the diversity of flavors. "
        "The mushrooms, salmon, peppers, and peas create a symphony of textures and colors that delight both the eye and the palate. "
        "The golden béchamel and gratinated gruyere cheese form a golden crown that promises moments of pure gastronomic pleasure."
    ),
    157: (
        "Immerse yourself in the passion of the Basque Country with this Basque-Style Chicken, where each "
        "ingredient tells a story of tradition and flavor. The chicken becomes infused with the intense "
        "flavors of chorizo, sweet peppers, and rice, creating a harmony of textures that evokes the green "
        "mountains and fertile valleys of northern Spain. It's more than a dish; it's a culinary embrace "
        "that comforts the soul."
    ),
    158: (
        "Transport your kitchen directly to Naples with this authentic Neapolitan Pizza, where each bite is "
        "a journey to the cobblestone streets of Italy. The dough, worked with love and patience, becomes "
        "the perfect canvas for creamy cheese, ripe tomatoes, and York ham. Each ingredient speaks of family "
        "tradition and Italian passion for turning simple ingredients into extraordinary experiences."
    ),
    159: (
        "Discover the rustic elegance of this Fish Pudding, where the humility of fish transforms into a "
        "refined gastronomic experience. The smooth, creamy texture contrasts with the intense flavors of "
        "tomatoes and fresh herbs, creating a dish that comforts and satisfies. It's grandmother's cooking "
        "elevated to art, perfect for those moments when the soul needs to be nourished with care."
    ),
    160: (
        "Experience the purity of Mediterranean flavors with this Baked Fish with Wine, where simplicity "
        "becomes elegance. The fish, bathed in white wine and aromatic herbs, cooks slowly until reaching a "
        "texture that melts in your mouth. Each bite is a celebration of sea freshness and culinary "
        "tradition that turns simple ingredients into memorable moments."
    ),
    161: (
        "Dive into the depths of the ocean with these Squid in Ink Dana-Ona Style, where the sea reveals its "
        "darkest and most flavorful secrets. The natural ink creates an intense, mysterious sauce that "
        "embraces the tender squid, while the sautéed onion and tomato base provides the warmth of "
        "traditional cooking. It's a dish that awakens primitive emotions and connects with the deepest "
        "roots of coastal gastronomy."
    ),
    162: (
        "Let yourself be surprised by the ingenious simplicity of these Dana-Ona Skewers, small gastronomic "
        "jewels that concentrate great flavors in each bite. The meatballs, juicy and aromatic, are crowned "
        "with sweet pepper, creating a contrast of textures and colors that delights both the eye and the "
        "palate. They're perfect for sharing, sparking conversations and smiles at every social gathering."
    ),
    163: (
        "Elevate your table with this sophisticated Baked Fish with Hollandaise Sauce, where French culinary "
        "aristocracy meets the freshness of the sea. The sole fillets, expertly rolled, bathe in a velvety "
        "hollandaise sauce that caresses the palate with its creamy richness. The shrimp add a touch of "
        "luxury that turns every dinner into a celebration of the most refined gastronomic pleasures."
    ),
    164: (
        "Rediscover the cooking of yesteryear with this Hake Pudding, where family tradition becomes "
        "culinary art. The hake, cooked with patience and love, transforms into a silky texture that melts "
        "in your mouth, while the tomatoes and herbs provide freshness and color. It's a dish that evokes "
        "memories of kitchens filled with aromas and expert hands that knew how to transform simple "
        "ingredients into gastronomic treasures."
    ),
    165: (
        "Discover the vegetal elegance of these Stuffed Artichokes, where nature offers its best gift "
        "transformed into a sublime gastronomic experience. Each tender leaf embraces an aromatic filling of "
        "meats and spices, while the golden béchamel and gratinated cheese create a crown of flavors that "
        "awakens the senses. It's proof that vegetarian cuisine can be as satisfying as it is emotional."
    ),
    166: (
        "Experience the magic of French cuisine with this Asparagus Soufflé, where the lightness of air "
        "combines with the intensity of flavor. The asparagus, noble spring vegetables, literally rise "
        "thanks to the soufflé technique, creating a spongy texture that contrasts with their earthy, deep "
        "flavor. Each spoonful is a caress to the palate that demonstrates cooking can be both science and "
        "art."
    ),
    167: (
        "Refresh your senses with this colorful Tomato Cocktail, where garden freshness meets the elegance "
        "of the sea. The tomatoes, juicy and aromatic, become the perfect container for an exquisite mixture "
        "of shrimp, tuna, and olives. The mayonnaise and touch of tabasco add creaminess and a spicy point "
        "that awakens the appetite and promises moments of pure gastronomic pleasure."
    ),
    168: (
        "Immerse yourself in charcuterie tradition with this Chicken Pâté, where the humility of chicken "
        "transforms into a luxury gastronomic experience. The sherry and cognac elevate the flavors, "
        "creating a creamy, aromatic pâté that melts in your mouth releasing complex layers of flavor. It's "
        "the perfect appetizer for those special moments when we want to impress with authentic and "
        "sophisticated flavors."
    ),
    169: (
        "Rediscover Italian pizza with this alternative version of Neapolitan Pizza, where sea flavors meet "
        "Italian tradition. The anchovies and mussels provide the essence of the Mediterranean, while the "
        "tomatoes and aromatic herbs create a perfect base for this symphony of marine flavors. Each bite is "
        "a sensory journey that celebrates the diversity of Italian cuisine."
    ),
    170: (
        "Let yourself be seduced by the irresistible creaminess of this Cheesecake, where simplicity becomes "
        "sophistication. The cheese, absolute protagonist, melts with béchamel creating a velvety texture "
        "that caresses the palate. The whipped egg whites provide lightness, while the golden gratin "
        "promises that first crispy bite that gives way to a creamy and satisfying experience."
    ),
    171: (
        "Refresh your soul with this homemade Strawberry Ice Cream, where the natural sweetness of the fruit "
        "combines with the creaminess of cream to create moments of pure happiness. Each spoonful is an "
        "explosion of summer flavor, evoking fields of ripe strawberries under the sun and the satisfaction "
        "of life's simple pleasures. It's more than a dessert; it's an icy caress that awakens smiles and "
        "sweet memories."
    ),
    172: (
        "Connect with family roots through this Aunt Josefina's Baking Soda Cake, where each bite tells the "
        "story of generations of expert hands. The cinnamon awakens the senses with its warm aroma, while "
        "the spongy texture evokes family Sundays and kitchens filled with love. It's a gastronomic treasure "
        "that transcends time, connecting past and present in each sweet bite."
    ),
    173: (
        "Indulge with this decadent Aunt Marita's Chocolate Cake, where passion for cocoa transforms into an "
        "almost sinful experience. The butter and whipped egg whites create a texture that melts in your "
        "mouth, releasing waves of chocolate flavor that awaken the most primitive senses. It's the perfect "
        "dessert for those moments when the soul needs to be consoled with pure pleasure."
    ),
    174: (
        "Revitalize your spirit with this Lemon or Orange Shake, where citrus freshness meets the creaminess "
        "of banana to create a drink that is pure joy in a glass. The bright, vibrant flavors awaken the "
        "senses, while the creamy texture satisfies the soul. It's the perfect drink for those days when you "
        "need a liquid ray of sunshine to brighten your day."
    ),
    175: (
        "Immerse yourself in the tropical creaminess of this Banana Shake, where the natural sweetness of "
        "the fruit combines with condensed milk to create an experience that is pure liquid comfort. Each "
        "sip is a caress that relaxes the soul and awakens childhood memories, when simple flavors had the "
        "power to create moments of perfect happiness."
    ),
    176: (
        "Travel to tropical paradises with this exotic Coconut Shake, where coconut creaminess meets the "
        "sweetness of vanilla ice cream to create a drink that is pure escape. The flavors transport to "
        "white sand beaches and crystal-clear waters, while the creamy texture embraces the palate with its "
        "tropical richness. It's a vacation in a glass that awakens dreams of distant places."
    ),
    177: (
        "Let yourself be seduced by this Chocolate and Cream Cake, where chocolate intensity balances with "
        "cream lightness to create a dessert that is pure seduction. The coffee-soaked cookies provide an "
        "aromatic base that melts with the creamy layers, creating contrasting textures that explode with "
        "flavor in every bite. It's the perfect ending for intimate dinners and special moments."
    ),
    178: (
        "Transport your senses to tropical islands with this Coconut Flan, where coconut creaminess meets "
        "Spanish flan tradition to create a fusion that is pure magic. The golden caramel contrasts with the "
        "coconut whiteness, while the silky texture melts in your mouth releasing flavors that evoke sea "
        "breezes and golden sunsets."
    ),
    179: (
        "Brighten your day with this Pepita's Lemon Cake, where the bright acidity of lemon balances with "
        "meringue sweetness to create a dessert that is pure joy. The crunchy cookie base contrasts with the "
        "filling's creaminess, while the golden meringue crowns this masterpiece with its airy texture. Each "
        "bite is an explosion of freshness that awakens smiles."
    ),
}

# Enhanced Chinese translations with gastronomic and emotional tone
CHINESE_TRANSLATIONS = {
    147: "让这道标志性的马伦戈鸡肉深深打动您，每一口都述说着胜利战役的故事。鲜嫩的鸡肉与丝滑的番茄酱、金黄蘑菇和芳香草本植物相拥，创造出唤醒感官的味觉交响曲。每一勺都将您带到法国乡村，在那里烹饪传统与对正宗味道的热情相融合。",
    148: "在这道精美的鸡肉配苹果中体验甜与咸的崇高和谐。烤箱的热力将雷纳苹果焦糖化，与嫩鸡肉融为一体，创造出令味蕾愉悦的质感对比。白葡萄酒带来微妙的优雅，提升每一口的品味，成为唤起家庭温暖和盛大宴会精致感的美食体验。",
    149: "准备好成为关注焦点，这道壮观的羊肉皇冠，是一件烹饪杰作，其呈现方式和卓越风味同样令人印象深刻。羊肉嫩滑芳香，配以异域咖喱米饭馅料，每一口都唤醒感官。这道创作不仅滋养身体，更以分享真正特别之物的满足感滋养灵魂。",
    150: "沉浸在这道红酒烤鲱鱼的深海风味中，海洋的新鲜与红酒的优雅相遇。鲱鱼在完美时刻被捕获，吸收了红酒的复杂韵味，创造出令人联想到地中海海岸的美食体验。炒制的蔬菜和蘑菇增添了对比鲜明的质感，让每一口都成为小小的庆典。",
    151: "发现这道鸡肉慕斯的精致优雅，这是一道将开胃菜艺术提升到新高度的肉酱。丝滑奶香的质地在味蕾上融化，释放出雪利酒和干邑丰富的浓郁鸡肉风味。这不仅仅是开胃菜；更是享受最精致烹饪乐趣的邀请，完美适合那些值得庆祝的特殊时刻。",
    152: "踏上这道咖喱蛋的东方感官之旅，异域香料与鸡蛋的奶香完美和谐地舞动。苹果提供微妙的甜味，平衡咖喱的辛辣，而芳香的米饭则成为这道风味杰作的画布。每一勺都是对比的爆发，唤醒情感并将灵魂带到遥远的土地。",
    153: "让这道番茄红鲷鱼的优雅简约诱惑您，海洋的新鲜与歌颂地中海的番茄酱盛装打扮。鱼肉紧实而细腻的质地与大蒜、香菜和雪利酒的浓郁风味完美互补，创造出令人联想到传统西班牙厨房的香气交响曲。这是既滋养身体又滋养精神的舒适食物。",
    154: "准备好享受这道虾仁蘑菇酿比目鱼的奢华美食体验，海洋贵族与大地优雅相遇。比目鱼作为扁鱼之王，精致地拥抱着虾仁和蘑菇馅料，创造出每一口都爆发风味的对比质感。白葡萄酒增添的精致感让每一顿晚餐都成为特殊场合。",
    155: "通过这道正宗的牛肉斯特罗加诺夫踏上俄罗斯草原之旅，每一口都诉说着贵族和传统的故事。牛肉条鲜嫩多汁，沐浴在用丝滑质地拥抱味蕾的奶香酱汁中。蘑菇和洋葱增添了风味深度，而酸奶油提供了使这道菜成为难忘体验的独特触感。",
    156: "让这道奶酪汁肉馅面管征服您，意大利面食盛装打扮，配以庆祝风味多样性的馅料。蘑菇、三文鱼、甜椒和豌豆创造出既愉悦视觉又愉悦味蕾的质感和色彩交响曲。金黄的白汁和焗烤的格吕耶尔奶酪形成金色皇冠，承诺纯粹的美食乐趣时刻。",
    157: "沉浸在这道巴斯克风味鸡肉的巴斯克地区激情中，每种食材都诉说着传统和风味的故事。鸡肉浸透了香肠、甜椒和米饭的浓郁风味，创造出令人联想到西班牙北部绿色山脉和肥沃山谷的质感和谐。这不仅仅是一道菜；更是抚慰灵魂的烹饪拥抱。",
    158: (
        "通过这道正宗的那不勒斯披萨将您的厨房直接带到那不勒斯，每一口都是通往意大利鹅卵石街道的旅程。面团经过爱心和耐心制作，成为奶香奶酪、成熟番茄和约克火腿的完美画布。每种食材都诉说着家庭传统和意大利人将简单食材转化为非凡体验的激情。"
    ),
    159: "发现这道鱼肉布丁的乡村优雅，鱼肉的朴实转化为精致的美食体验。光滑奶香的质地与番茄和新鲜香草的浓郁风味形成对比，创造出既舒适又满足的菜肴。这是提升为艺术的祖母烹饪，完美适合灵魂需要被关爱滋养的时刻。",
    160: "通过这道红酒烤鱼体验地中海风味的纯粹，简约成为优雅。鱼肉沐浴在白葡萄酒和芳香草本中，慢慢烹煮直至达到入口即化的质地。每一口都是对海洋新鲜和烹饪传统的庆祝，将简单食材转化为难忘时刻。",
    161: "通过这道达纳-奥纳风味墨鱼汁炖鱿鱼深入海洋深处，大海揭示其最深沉和最美味的秘密。天然墨汁创造出拥抱嫩鱿鱼的浓郁神秘酱汁，而洋葱和番茄的炒制底料提供传统烹饪的温暖。这道菜唤醒原始情感，与沿海美食的最深根源相连。",
    162: "让这些达纳-奥纳肉串的巧妙简约惊艳您，这些小小的美食珍宝在每一口中集中了巨大的风味。肉丸多汁芳香，配以甜椒冠冕，创造出既愉悦视觉又愉悦味蕾的质感和色彩对比。它们完美适合分享，在每次社交聚会中激发对话和笑容。",
    163: "通过这道荷兰汁烤鱼提升您的餐桌，法国烹饪贵族与海洋新鲜相遇。比目鱼片专业地卷制，沐浴在用奶香丰富性抚慰味蕾的丝滑荷兰汁中。虾仁增添奢华触感，让每一顿晚餐都成为最精致美食乐趣的庆典。",
    164: "通过这道鳕鱼布丁重新发现往昔的烹饪，家庭传统成为烹饪艺术。鳕鱼经过耐心和爱心烹制，转化为入口即化的丝滑质地，而番茄和香草提供新鲜和色彩。这道菜唤起充满香气的厨房记忆和知道如何将简单食材转化为美食珍宝的专业双手。",
    165: "发现这道酿朝鲜蓟的蔬菜优雅，大自然提供其最好的礼物，转化为崇高的美食体验。每片嫩叶拥抱着肉类和香料的芳香馅料，而金黄的白汁和焗烤奶酪创造出唤醒感官的风味皇冠。这证明了素食烹饪既可以令人满足又可以充满情感。",
    166: (
        "通过这道芦笋舒芙蕾体验法式烹饪的魔力，空气的轻盈与风味的浓郁相结合。芦笋作为春季贵族蔬菜，通过舒芙蕾技术字面上地升起，创造出与其土地般深沉风味形成对比的海绵质地。每一勺都是对味蕾的抚慰，证明烹饪既可以是科学也可以是艺术。"
    ),
    167: "通过这道色彩缤纷的番茄鸡尾酒刷新您的感官，花园新鲜与海洋优雅相遇。番茄多汁芳香，成为虾仁、金枪鱼和橄榄精美混合的完美容器。蛋黄酱和塔巴斯科酱的点缀增添奶香和辛辣点，唤醒食欲并承诺纯粹美食乐趣的时刻。",
    168: "通过这道鸡肉酱沉浸在熟食传统中，鸡肉的朴实转化为奢华的美食体验。雪利酒和干邑提升风味，创造出入口即化的奶香芳香肉酱，释放复杂的风味层次。这是完美的开胃菜，适合那些我们想要以正宗和精致风味印象深刻的特殊时刻。",
    169: "通过这道那不勒斯披萨的替代版本重新发现意大利披萨，海洋风味与意大利传统相遇。凤尾鱼和贻贝提供地中海的精髓，而番茄和芳香草本为这道海洋风味交响曲创造完美基础。每一口都是庆祝意大利烹饪多样性的感官旅程。",
    170: "让这道芝士蛋糕不可抗拒的奶香诱惑您，简约成为精致。奶酪作为绝对主角，与白汁融合创造出抚慰味蕾的丝滑质地。打发的蛋白提供轻盈感，而金黄的焗烤承诺那第一口酥脆，然后是奶香和满足的体验。",
    171: "通过这道自制草莓冰淇淋刷新您的灵魂，水果的天然甜味与奶油的丰富性结合创造纯粹幸福的时刻。每一勺都是夏日风味的爆发，唤起阳光下成熟草莓田野和生活简单乐趣的满足感。这不仅仅是甜点；更是唤醒笑容和甜蜜回忆的冰凉抚慰。",
    172: "通过这道约瑟菲娜阿姨的小苏打蛋糕与家庭根源连接，每一口都诉说着几代专业双手的故事。肉桂以其温暖香气唤醒感官，而海绵质地唤起家庭星期天和充满爱的厨房。这是超越时间的美食珍宝，在每一口甜蜜中连接过去和现在。",
    173: "通过这道玛丽塔阿姨的颓废巧克力蛋糕纵容自己，对可可的激情转化为几乎罪恶的体验。黄油和打发的蛋白创造出入口即化的质地，释放出唤醒最原始感官的巧克力风味波浪。这是完美的甜点，适合灵魂需要被纯粹乐趣安慰的时刻。",
    174: "通过这道柠檬或橙子奶昔振奋您的精神，柑橘新鲜与香蕉的奶香相遇，创造出杯中纯粹喜悦的饮品。明亮活力的风味唤醒感官，而奶香质地满足灵魂。这是完美的饮品，适合那些需要液体阳光来照亮一天的日子。",
    175: "沉浸在这道香蕉奶昔的热带奶香中，水果的天然甜味与炼乳结合创造出纯粹液体舒适的体验。每一口都是放松灵魂的抚慰，唤起童年记忆，那时简单的风味有创造完美幸福时刻的力量。",
    176: "通过这道异域椰子奶昔前往热带天堂，椰子的奶香与香草冰淇淋的甜味相遇，创造出纯粹逃避的饮品。风味带您前往白沙滩和水晶般清澈的海水，而奶香质地以其热带丰富性拥抱味蕾。这是杯中度假，唤醒对遥远地方的梦想。",
    177: "让这道巧克力奶油蛋糕诱惑您，巧克力的浓郁与奶油的轻盈平衡创造出纯粹诱惑的甜点。浸泡咖啡的饼干提供与奶香层次融合的芳香基础，创造出每一口都爆发风味的对比质感。这是亲密晚餐和特殊时刻的完美结尾。",
    178: "通过这道椰子布丁将您的感官带到热带岛屿，椰子的奶香与西班牙布丁传统相遇，创造出纯粹魔力的融合。金色焦糖与椰子的洁白形成对比，而丝滑质地在口中融化，释放出令人联想到海风和金色夕阳的风味。",
    179: "通过这道佩皮塔的柠檬蛋糕照亮您的一天，柠檬的明亮酸味与蛋白糖的甜味平衡创造出纯粹喜悦的甜点。酥脆的饼干基础与馅料的奶香形成对比，而金黄的蛋白糖以其空气般的质地为这道杰作加冕。每一口都是唤醒笑容的新鲜爆发。",
}


def update_translations():
    """Update English and Chinese translations"""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🌍 Updating English translations...")
    for recipe_id, english_desc in ENGLISH_TRANSLATIONS.items():
        cursor.execute(
            "UPDATE recipe_translations SET description = ? WHERE recipe_id = ? AND language = 'en'",
            (english_desc, recipe_id),
        )
        print(f"Updated English for recipe {recipe_id}")

    print("\n🏮 Updating Chinese translations...")
    for recipe_id, chinese_desc in CHINESE_TRANSLATIONS.items():
        cursor.execute(
            "UPDATE recipe_translations SET description = ? WHERE recipe_id = ? AND language = 'zh'",
            (chinese_desc, recipe_id),
        )
        print(f"Updated Chinese for recipe {recipe_id}")

    conn.commit()
    conn.close()
    print("\n✅ All translations updated successfully!")


if __name__ == "__main__":
    update_translations()
