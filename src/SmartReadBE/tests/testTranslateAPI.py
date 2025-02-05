import unittest
from TranslationModule.TranslationManager import TranslationManager


class TestTranslateAPI(unittest.TestCase):

    def test_translate_30_words_en_fr(self):
        # UT-04: 30WordsEnFrTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """The sun rises in the east, and birds begin to sing as the morning 
        light spreads. Farmers wake up early to tend their crops and prepare for another day 
        of work."""
        expected_phrases = [
            "soleil se lève",
            "oiseaux commencent à chanter",
            "agriculteurs se lèvent tôt",
        ]

        result = translator.translate(input_text, "fr", "en")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_50_words_en_fr(self):
        # UT-05: 50WordsEnFrTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Technology has transformed the way people communicate and work. 
        With the rise of the internet, instant messaging and video conferencing have become 
        essential. Businesses now rely on cloud computing, artificial intelligence, and 
        automation to improve efficiency and stay competitive in an ever-changing digital 
        world."""
        expected_phrases = [
            "messagerie instantanée",
            "intelligence artificielle",
            "monde numérique",
        ]

        result = translator.translate(input_text, "fr", "en")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_70_words_en_fr(self):
        # UT-06: 70WordsEnFrTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """In the modern era, technology shapes the way people interact, work, and learn. 
        The evolution of smartphones, social media, and artificial intelligence has created 
        an interconnected world. Businesses leverage cloud computing and data analytics to 
        optimize decision-making. Automated systems enhance efficiency, reducing human 
        workload. As innovation continues, the role of digital transformation becomes 
        increasingly crucial in every industry."""
        expected_phrases = [
            "téléphones intelligents",
            "transformation numérique",
            "monde interconnecté",
        ]

        result = translator.translate(input_text, "fr", "en")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))
    
    def test_translate_30_words_en_zh(self):
        # UT-07-01: 30WordsEnZhTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """The moon shines brightly at night, illuminating the silent streets. 
        People rest in their homes, preparing for the challenges of the next day."""
        expected_phrases = [
            "月亮明亮",
            "照亮街道",
            "人们在家休息",
        ]

        result = translator.translate(input_text, "zh", "en")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_en_ja(self):
        # UT-07-02: 30WordsEnJaTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """The mountains stand tall in the distance, covered in a blanket of snow. 
        Travelers admire the breathtaking view, feeling at peace with nature."""
        expected_phrases = [
            "山がそびえる",
            "雪に覆われている",
            "旅行者は景色を楽しむ",
        ]

        result = translator.translate(input_text, "ja", "en")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_en_it(self):
        # UT-07-03: 30WordsEnItTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """A warm breeze flows through the city, bringing the scent of blooming flowers. 
        The streets are lively with people enjoying the sunshine and music."""
        expected_phrases = [
            "brezza calda",
            "fiori in fiore",
            "persone che godono del sole",
        ]

        result = translator.translate(input_text, "it", "en")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_zh_en(self):
        # UT-07-04: 30WordsZhEnTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """太阳在早晨的天空升起，温暖的阳光洒满大地。农民们开始他们新的一天，
        而鸟儿在树枝上歌唱。"""
        expected_phrases = [
            "sun rises",
            "warm sunlight",
            "farmers start their day",
        ]

        result = translator.translate(input_text, "en", "zh")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_zh_fr(self):
        # UT-07-05: 30WordsZhFrTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """太阳升起，照亮了沉睡的城市。鸟儿在枝头歌唱，人们开始忙碌的一天。"""
        expected_phrases = [
            "soleil se lève",
            "oiseaux chantent",
            "les gens commencent la journée",
        ]

        result = translator.translate(input_text, "fr", "zh")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))
    
    def test_translate_30_words_zh_ja(self):
        # UT-07-06: 30WordsZhJaTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """太阳升起，温暖的大地。鸟儿歌唱，人们开始他们的工作。"""
        expected_phrases = [
            "太陽が昇る",
            "鳥が歌う",
            "人々が仕事を始める",
        ]

        result = translator.translate(input_text, "ja", "zh")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_zh_it(self):
        # UT-07-07: 30WordsZhItTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """清晨，城市逐渐苏醒，街道上开始热闹起来。商贩摆出新鲜蔬果，人们陆续出门上班。"""
        expected_phrases = [
            "la città si sveglia",
            "frutta e verdura fresca",
            "gente che va al lavoro",
        ]

        result = translator.translate(input_text, "it", "zh")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_fr_en(self):
        # UT-07-08: 30WordsFrEnTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Le vent souffle doucement, portant les parfums des fleurs en pleine floraison. 
        Les rues sont pleines de vie alors que les gens profitent du soleil."""
        expected_phrases = [
            "wind blows softly",
            "scent of blooming flowers",
            "people enjoy the sun",
        ]

        result = translator.translate(input_text, "en", "fr")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_fr_zh(self):
        # UT-07-09: 30WordsFrZhTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Le soleil se lève à l'horizon, illuminant progressivement la ville endormie. 
        Les oiseaux chantent et les gens se préparent pour une nouvelle journée."""
        expected_phrases = [
            "太阳升起",
            "城市渐渐被照亮",
            "鸟儿在歌唱",
        ]

        result = translator.translate(input_text, "zh", "fr")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_fr_ja(self):
        # UT-07-10: 30WordsFrJaTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Les collines verdoyantes s'étendent à perte de vue, accueillant la brise matinale. 
        Les fermiers nourrissent le bétail alors que la journée commence."""
        expected_phrases = [
            "緑豊かな丘が広がる",
            "朝のそよ風",
            "農家は家畜に餌をやる",
        ]

        result = translator.translate(input_text, "ja", "fr")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_fr_it(self):
        # UT-07-11: 30WordsFrItTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Le marché du village s'anime dès l'aube, offrant des produits frais et variés. 
        Les habitants discutent joyeusement tout en faisant leurs achats."""
        expected_phrases = [
            "mercato del villaggio",
            "prodotti freschi",
            "abitanti discutono allegramente",
        ]

        result = translator.translate(input_text, "it", "fr")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_ja_en(self):
        # UT-07-12: 30WordsJaEnTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """夜明けとともに海面が輝き、漁師たちは船を出す準備を始める。 
        浜辺では子供たちが貝を集めて楽しんでいる。"""
        expected_phrases = [
            "ocean glistens at dawn",
            "fishermen prepare their boats",
            "children collecting shells",
        ]

        result = translator.translate(input_text, "en", "ja")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_ja_zh(self):
        # UT-07-13: 30WordsJaZhTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """太陽が昇ると、街の通りは活気に満ち溢れる。 
        人々は新しい一日の始まりに期待を抱いている。"""
        expected_phrases = [
            "太阳升起",
            "街道充满活力",
            "人们对新的一天充满期待",
        ]

        result = translator.translate(input_text, "zh", "ja")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_ja_fr(self):
        # UT-07-14: 30WordsJaFrTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """美しい庭園には色とりどりの花が咲き、穏やかな噴水の音が響いている。 
        観光客は写真を撮りながら散策を楽しむ。"""
        expected_phrases = [
            "jardin magnifique",
            "fleurs colorées",
            "son apaisant de la fontaine",
        ]

        result = translator.translate(input_text, "fr", "ja")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_ja_it(self):
        # UT-07-15: 30WordsJaItTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """遠くに見える山々は朝靄に包まれ、静けさの中に神秘的な雰囲気を醸し出す。 
        ハイカーたちは新鮮な空気を吸いながら山道を歩き始める。"""
        expected_phrases = [
            "montagne in lontananza",
            "avvolte dalla foschia",
            "escursionisti iniziano a camminare",
        ]

        result = translator.translate(input_text, "it", "ja")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_it_en(self):
        # UT-07-16: 30WordsItEnTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Una leggera brezza soffia attraverso i campi, portando il profumo della primavera. 
        Gli agricoltori lavorano diligentemente sotto il cielo azzurro."""
        expected_phrases = [
            "breeze blows through the fields",
            "scent of spring",
            "farmers work diligently",
        ]

        result = translator.translate(input_text, "en", "it")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_it_zh(self):
        # UT-07-17: 30WordsItZhTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """All'alba, le luci della città cominciano a spegnersi mentre il mercato apre i battenti. 
        Le persone acquistano prodotti freschi per la giornata."""
        expected_phrases = [
            "城市的灯光开始熄灭",
            "市场开门营业",
            "人们购买新鲜食材",
        ]

        result = translator.translate(input_text, "zh", "it")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_it_fr(self):
        # UT-07-18: 30WordsItFrTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Nel pomeriggio, una brezza leggera attraversa la piazza, portando il profumo di caffè. 
        I turisti si fermano per godersi il momento al tavolo di un bar."""
        expected_phrases = [
            "une brise légère traverse la place",
            "parfum de café",
            "les touristes profitent du moment",
        ]

        result = translator.translate(input_text, "fr", "it")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))

    def test_translate_30_words_it_ja(self):
        # UT-07-19: 30WordsItJaTranslationTest
        translator = TranslationManager()
        translator.initialize()

        input_text = """Verso sera, le strade si tingono di luci e ombre, mentre la gente torna a casa. 
        Un senso di tranquillità cala sulla città, promettendo una notte serena."""
        expected_phrases = [
            "通りが明かりと影に染まる",
            "人々が家に帰る",
            "穏やかな夜が訪れる",
        ]

        result = translator.translate(input_text, "ja", "it")

        self.assertTrue(all(phrase in result for phrase in expected_phrases))