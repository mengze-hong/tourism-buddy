#!/usr/bin/env python3
"""
Tourism Buddy — Survival Phrase Book
Essential travel phrases for common destinations with pronunciation guides.
Supports: Japanese, Thai, Spanish, Mandarin, French, Korean, Italian, German.
"""

from typing import Optional, List, Dict

# Essential phrase categories with English templates
PHRASE_TEMPLATES = [
    # Greetings & Basics
    ("Hello", "greeting"),
    ("Goodbye", "greeting"),
    ("Please", "basic"),
    ("Thank you", "basic"),
    ("Yes", "basic"),
    ("No", "basic"),
    ("Excuse me", "basic"),
    ("I'm sorry", "basic"),
    # Survival
    ("I don't understand", "survival"),
    ("Do you speak English?", "survival"),
    ("How much does this cost?", "shopping"),
    ("Too expensive", "shopping"),
    ("Where is the bathroom?", "navigation"),
    ("Where is...?", "navigation"),
    ("Left / Right / Straight", "navigation"),
    # Food
    ("Water, please", "food"),
    ("The bill, please", "food"),
    ("Delicious!", "food"),
    ("I'm allergic to...", "food"),
    ("No spicy, please", "food"),
    # Emergency
    ("Help!", "emergency"),
    ("I need a doctor", "emergency"),
    ("Call the police", "emergency"),
    ("I'm lost", "emergency"),
    ("Where is the hospital?", "emergency"),
]

# Pre-built phrase books for popular destinations
PHRASE_BOOKS = {
    "japanese": {
        "language": "Japanese",
        "script": "Japanese (Hiragana/Katakana/Kanji)",
        "phrases": {
            "Hello": {"local": "こんにちは", "pronunciation": "Kon-nee-chee-wah", "notes": "Formal, use during daytime"},
            "Goodbye": {"local": "さようなら", "pronunciation": "Sah-yoh-nah-rah", "notes": "Formal; casual: じゃね (jah-neh)"},
            "Please": {"local": "お願いします", "pronunciation": "Oh-neh-gai-shee-mahs", "notes": "Use for requests"},
            "Thank you": {"local": "ありがとうございます", "pronunciation": "Ah-ree-gah-toh go-zai-mahs", "notes": "Casual: ありがとう"},
            "Yes": {"local": "はい", "pronunciation": "Hai", "notes": ""},
            "No": {"local": "いいえ", "pronunciation": "Ee-eh", "notes": "Japanese rarely say no directly"},
            "Excuse me": {"local": "すみません", "pronunciation": "Sue-mee-mah-sen", "notes": "Also means 'sorry' in some contexts"},
            "I'm sorry": {"local": "ごめんなさい", "pronunciation": "Go-men-nah-sai", "notes": "For apologies"},
            "I don't understand": {"local": "わかりません", "pronunciation": "Wah-kah-ree-mah-sen", "notes": ""},
            "Do you speak English?": {"local": "英語を話せますか？", "pronunciation": "Ei-go oh hah-nah-seh-mahs-kah?", "notes": ""},
            "How much does this cost?": {"local": "いくらですか？", "pronunciation": "Ee-koo-rah des-kah?", "notes": "Point at the item"},
            "Too expensive": {"local": "高すぎます", "pronunciation": "Tah-kah-sue-gee-mahs", "notes": "Bargaining uncommon in Japan"},
            "Where is the bathroom?": {"local": "トイレはどこですか？", "pronunciation": "Toy-reh wah doh-koh des-kah?", "notes": ""},
            "Water, please": {"local": "お水をください", "pronunciation": "Oh-mee-zoo oh koo-dah-sai", "notes": "Free water at restaurants"},
            "The bill, please": {"local": "お会計をお願いします", "pronunciation": "Oh-kai-kei oh oh-neh-gai-shee-mahs", "notes": "No tipping in Japan!"},
            "Delicious!": {"local": "おいしい！", "pronunciation": "Oi-shee!", "notes": "Chefs love hearing this"},
            "No spicy, please": {"local": "辛くないでください", "pronunciation": "Kah-rah-koo nai-deh koo-dah-sai", "notes": ""},
            "Help!": {"local": "助けて！", "pronunciation": "Tah-sue-keh-teh!", "notes": "Emergency"},
            "I need a doctor": {"local": "医者が必要です", "pronunciation": "Ee-shah gah hee-tsoo-yoh des", "notes": ""},
            "Call the police": {"local": "警察を呼んでください", "pronunciation": "Kei-sah-tsoo oh yon-deh koo-dah-sai", "notes": "Police: 110"},
            "I'm lost": {"local": "道に迷いました", "pronunciation": "Mee-chee nee mah-yoi-mah-shee-tah", "notes": "Show your hotel card"},
            "Where is the hospital?": {"local": "病院はどこですか？", "pronunciation": "Byoh-een wah doh-koh des-kah?", "notes": "Ambulance: 119"},
        },
    },
    "thai": {
        "language": "Thai",
        "script": "Thai Script",
        "phrases": {
            "Hello": {"local": "สวัสดี", "pronunciation": "Sah-wah-dee (+ krap/ka)", "notes": "Add ครับ (krap, male) or ค่ะ (ka, female)"},
            "Goodbye": {"local": "ลาก่อน", "pronunciation": "Lah-gorn", "notes": "Or just สวัสดี again"},
            "Please": {"local": "กรุณา", "pronunciation": "Gah-roo-nah", "notes": ""},
            "Thank you": {"local": "ขอบคุณ", "pronunciation": "Kop-kun (+ krap/ka)", "notes": "Always add polite particle"},
            "Yes": {"local": "ใช่", "pronunciation": "Chai", "notes": ""},
            "No": {"local": "ไม่", "pronunciation": "Mai", "notes": ""},
            "Excuse me": {"local": "ขอโทษ", "pronunciation": "Kor-toht", "notes": "Also means sorry"},
            "I don't understand": {"local": "ไม่เข้าใจ", "pronunciation": "Mai kao jai", "notes": ""},
            "Do you speak English?": {"local": "คุณพูดภาษาอังกฤษได้ไหม", "pronunciation": "Kun poot pah-sah ang-grit dai mai?", "notes": ""},
            "How much does this cost?": {"local": "เท่าไหร่", "pronunciation": "Tao-rai?", "notes": "Essential for markets"},
            "Too expensive": {"local": "แพงไป", "pronunciation": "Paeng bpai", "notes": "Then offer 50-70%"},
            "Where is the bathroom?": {"local": "ห้องน้ำอยู่ที่ไหน", "pronunciation": "Hong-nam yoo tee-nai?", "notes": ""},
            "Water, please": {"local": "น้ำเปล่า", "pronunciation": "Nam plao", "notes": "Specify: cold = yen"},
            "The bill, please": {"local": "เช็คบิล", "pronunciation": "Check bin", "notes": ""},
            "Delicious!": {"local": "อร่อย", "pronunciation": "Ah-roi!", "notes": "Thai people love food compliments"},
            "No spicy, please": {"local": "ไม่เผ็ด", "pronunciation": "Mai pet", "notes": "VERY useful in Thailand"},
            "Where is...?": {"local": "...อยู่ที่ไหน", "pronunciation": "...yoo tee-nai?", "notes": "Point + ask"},
            "Help!": {"local": "ช่วยด้วย!", "pronunciation": "Chuay duay!", "notes": "Emergency"},
            "I need a doctor": {"local": "ต้องการหมอ", "pronunciation": "Dtong gahn mor", "notes": ""},
            "Call the police": {"local": "เรียกตำรวจ", "pronunciation": "Riak dtam-ruat", "notes": "Police: 191"},
            "I'm lost": {"local": "ฉันหลงทาง", "pronunciation": "Chan long tahng", "notes": "Show hotel card/map"},
            "Where is the hospital?": {"local": "โรงพยาบาลอยู่ที่ไหน", "pronunciation": "Rohng-pah-yah-bahn yoo tee-nai?", "notes": "Ambulance: 1669"},
        },
    },
    "spanish": {
        "language": "Spanish",
        "script": "Latin",
        "phrases": {
            "Hello": {"local": "Hola", "pronunciation": "Oh-lah", "notes": "Universal, any time of day"},
            "Goodbye": {"local": "Adios", "pronunciation": "Ah-dee-ohs", "notes": "Casual: Chao!"},
            "Please": {"local": "Por favor", "pronunciation": "Por fah-vor", "notes": ""},
            "Thank you": {"local": "Gracias", "pronunciation": "Grah-see-ahs", "notes": "Muchas gracias = thank you very much"},
            "Yes": {"local": "Si", "pronunciation": "See", "notes": ""},
            "No": {"local": "No", "pronunciation": "No", "notes": ""},
            "Excuse me": {"local": "Disculpe", "pronunciation": "Dees-kool-peh", "notes": "For attention; Perdon for sorry"},
            "I'm sorry": {"local": "Lo siento", "pronunciation": "Loh see-en-toh", "notes": ""},
            "I don't understand": {"local": "No entiendo", "pronunciation": "No en-tee-en-doh", "notes": ""},
            "Do you speak English?": {"local": "Habla ingles?", "pronunciation": "Ah-blah een-glehs?", "notes": ""},
            "How much does this cost?": {"local": "Cuanto cuesta?", "pronunciation": "Kwahn-toh kwes-tah?", "notes": ""},
            "Too expensive": {"local": "Muy caro", "pronunciation": "Moo-ee kah-roh", "notes": ""},
            "Where is the bathroom?": {"local": "Donde esta el bano?", "pronunciation": "Don-deh es-tah el bah-nyoh?", "notes": ""},
            "Where is...?": {"local": "Donde esta...?", "pronunciation": "Don-deh es-tah?", "notes": ""},
            "Water, please": {"local": "Agua, por favor", "pronunciation": "Ah-gwah, por fah-vor", "notes": "con/sin gas = with/without bubbles"},
            "The bill, please": {"local": "La cuenta, por favor", "pronunciation": "Lah kwen-tah, por fah-vor", "notes": ""},
            "Delicious!": {"local": "Delicioso!", "pronunciation": "Deh-lee-see-oh-soh!", "notes": "Riquisimo! is more enthusiastic"},
            "No spicy, please": {"local": "Sin picante, por favor", "pronunciation": "Seen pee-kahn-teh, por fah-vor", "notes": ""},
            "Help!": {"local": "Ayuda!", "pronunciation": "Ah-yoo-dah!", "notes": "Emergency"},
            "I need a doctor": {"local": "Necesito un medico", "pronunciation": "Neh-seh-see-toh oon meh-dee-koh", "notes": ""},
            "Call the police": {"local": "Llame a la policia", "pronunciation": "Yah-meh ah lah poh-lee-see-ah", "notes": "Emergency: 112 (Europe) / 911 (Americas)"},
            "I'm lost": {"local": "Estoy perdido/a", "pronunciation": "Es-toy per-dee-doh/dah", "notes": "-o (male) / -a (female)"},
            "Where is the hospital?": {"local": "Donde esta el hospital?", "pronunciation": "Don-deh es-tah el os-pee-tahl?", "notes": ""},
        },
    },
    "mandarin": {
        "language": "Mandarin Chinese",
        "script": "Simplified Chinese",
        "phrases": {
            "Hello": {"local": "你好", "pronunciation": "Nee how", "notes": "Universal greeting"},
            "Goodbye": {"local": "再见", "pronunciation": "Zai jee-en", "notes": ""},
            "Please": {"local": "请", "pronunciation": "Ching", "notes": ""},
            "Thank you": {"local": "谢谢", "pronunciation": "Shieh shieh", "notes": ""},
            "Yes": {"local": "是 / 对", "pronunciation": "Shih / Dway", "notes": "Context dependent"},
            "No": {"local": "不是 / 不要", "pronunciation": "Boo shih / Boo yao", "notes": "不要 = don't want"},
            "Excuse me": {"local": "不好意思", "pronunciation": "Boo how ee sih", "notes": "For getting attention"},
            "I'm sorry": {"local": "对不起", "pronunciation": "Dway boo chee", "notes": "For apologies"},
            "I don't understand": {"local": "我听不懂", "pronunciation": "Woh ting boo dong", "notes": ""},
            "Do you speak English?": {"local": "你会说英语吗？", "pronunciation": "Nee hway shwo ying-yoo mah?", "notes": ""},
            "How much does this cost?": {"local": "多少钱？", "pronunciation": "Dwoh shaow chee-en?", "notes": "Essential for shopping"},
            "Too expensive": {"local": "太贵了", "pronunciation": "Tai gway luh", "notes": "Then offer 50-60%"},
            "Where is the bathroom?": {"local": "厕所在哪里？", "pronunciation": "Tse-swoh zai nah-lee?", "notes": ""},
            "Where is...?": {"local": "...在哪里？", "pronunciation": "...zai nah-lee?", "notes": ""},
            "Water, please": {"local": "请给我水", "pronunciation": "Ching gay woh shway", "notes": "Hot water: 热水 (ruh shway)"},
            "The bill, please": {"local": "买单", "pronunciation": "Mai dan", "notes": "Or gesture writing in air"},
            "Delicious!": {"local": "好吃！", "pronunciation": "How chih!", "notes": "Locals love hearing this"},
            "No spicy, please": {"local": "不要辣", "pronunciation": "Boo yao lah", "notes": "Very important in Sichuan!"},
            "Help!": {"local": "救命！", "pronunciation": "Jiou ming!", "notes": "Emergency"},
            "I need a doctor": {"local": "我需要看医生", "pronunciation": "Woh shoo yao kan ee sheng", "notes": ""},
            "Call the police": {"local": "叫警察", "pronunciation": "Jiao jing-cha", "notes": "Police: 110"},
            "I'm lost": {"local": "我迷路了", "pronunciation": "Woh mee loo luh", "notes": "Show hotel card/map app"},
            "Where is the hospital?": {"local": "医院在哪里？", "pronunciation": "Ee-ywan zai nah-lee?", "notes": "Ambulance: 120"},
        },
    },
    "french": {
        "language": "French",
        "script": "Latin",
        "phrases": {
            "Hello": {"local": "Bonjour", "pronunciation": "Bon-zhoor", "notes": "ALWAYS greet before asking anything"},
            "Goodbye": {"local": "Au revoir", "pronunciation": "Oh reh-vwahr", "notes": ""},
            "Please": {"local": "S'il vous plait", "pronunciation": "Seel voo pleh", "notes": ""},
            "Thank you": {"local": "Merci", "pronunciation": "Mair-see", "notes": "Merci beaucoup = thank you very much"},
            "Yes": {"local": "Oui", "pronunciation": "Wee", "notes": ""},
            "No": {"local": "Non", "pronunciation": "Non", "notes": ""},
            "Excuse me": {"local": "Excusez-moi", "pronunciation": "Ex-koo-zay mwah", "notes": ""},
            "I'm sorry": {"local": "Je suis desole(e)", "pronunciation": "Zhuh swee day-zoh-lay", "notes": ""},
            "I don't understand": {"local": "Je ne comprends pas", "pronunciation": "Zhuh nuh kom-pron pah", "notes": ""},
            "Do you speak English?": {"local": "Parlez-vous anglais?", "pronunciation": "Par-lay voo on-gleh?", "notes": "Always try French first!"},
            "How much does this cost?": {"local": "Combien?", "pronunciation": "Kom-bee-en?", "notes": ""},
            "Too expensive": {"local": "Trop cher", "pronunciation": "Troh shair", "notes": ""},
            "Where is the bathroom?": {"local": "Ou sont les toilettes?", "pronunciation": "Oo son lay twah-let?", "notes": ""},
            "Where is...?": {"local": "Ou est...?", "pronunciation": "Oo eh...?", "notes": ""},
            "Water, please": {"local": "De l'eau, s'il vous plait", "pronunciation": "Duh loh, seel voo pleh", "notes": "Tap water: une carafe d'eau"},
            "The bill, please": {"local": "L'addition, s'il vous plait", "pronunciation": "Lah-dee-see-on, seel voo pleh", "notes": ""},
            "Delicious!": {"local": "Delicieux!", "pronunciation": "Day-lee-see-uh!", "notes": ""},
            "No spicy, please": {"local": "Pas epice, s'il vous plait", "pronunciation": "Pah ay-pee-say, seel voo pleh", "notes": ""},
            "Help!": {"local": "Au secours!", "pronunciation": "Oh suh-koor!", "notes": "Emergency"},
            "I need a doctor": {"local": "J'ai besoin d'un medecin", "pronunciation": "Zhay buh-zwan duhn med-san", "notes": ""},
            "Call the police": {"local": "Appelez la police", "pronunciation": "Ah-play lah poh-lees", "notes": "Emergency: 112 / Police: 17"},
            "I'm lost": {"local": "Je suis perdu(e)", "pronunciation": "Zhuh swee pair-doo", "notes": "Add -e if female"},
            "Where is the hospital?": {"local": "Ou est l'hopital?", "pronunciation": "Oo eh loh-pee-tahl?", "notes": "SAMU (ambulance): 15"},
        },
    },
    "korean": {
        "language": "Korean",
        "script": "Hangul",
        "phrases": {
            "Hello": {"local": "안녕하세요", "pronunciation": "An-nyeong-ha-seh-yo", "notes": "Universal polite greeting"},
            "Goodbye": {"local": "안녕히 가세요", "pronunciation": "An-nyeong-hee ga-seh-yo", "notes": "To someone leaving"},
            "Please": {"local": "주세요", "pronunciation": "Joo-seh-yo", "notes": "Add after what you want"},
            "Thank you": {"local": "감사합니다", "pronunciation": "Gam-sa-ham-nee-da", "notes": "Formal; casual: 고마워"},
            "Yes": {"local": "네", "pronunciation": "Neh", "notes": ""},
            "No": {"local": "아니요", "pronunciation": "Ah-nee-yo", "notes": ""},
            "Excuse me": {"local": "실례합니다", "pronunciation": "Shil-leh-ham-nee-da", "notes": ""},
            "I'm sorry": {"local": "죄송합니다", "pronunciation": "Jweh-song-ham-nee-da", "notes": ""},
            "I don't understand": {"local": "이해를 못해요", "pronunciation": "Ee-heh-reul mo-teh-yo", "notes": ""},
            "Do you speak English?": {"local": "영어 하세요?", "pronunciation": "Young-uh ha-seh-yo?", "notes": ""},
            "How much does this cost?": {"local": "이거 얼마예요?", "pronunciation": "Ee-guh ul-ma-yeh-yo?", "notes": "Point at item"},
            "Too expensive": {"local": "너무 비싸요", "pronunciation": "Nuh-moo bee-ssa-yo", "notes": ""},
            "Where is the bathroom?": {"local": "화장실 어디예요?", "pronunciation": "Hwa-jang-shil uh-dee-yeh-yo?", "notes": ""},
            "Water, please": {"local": "물 주세요", "pronunciation": "Mul joo-seh-yo", "notes": "Free water at restaurants"},
            "The bill, please": {"local": "계산해 주세요", "pronunciation": "Gyeh-san-heh joo-seh-yo", "notes": ""},
            "Delicious!": {"local": "맛있어요!", "pronunciation": "Ma-shee-ssuh-yo!", "notes": ""},
            "Help!": {"local": "도와주세요!", "pronunciation": "Do-wa-joo-seh-yo!", "notes": "Emergency"},
            "I need a doctor": {"local": "의사가 필요해요", "pronunciation": "Eui-sa-ga pil-yo-heh-yo", "notes": ""},
            "Call the police": {"local": "경찰을 불러주세요", "pronunciation": "Kyung-chal-eul bool-luh-joo-seh-yo", "notes": "Police: 112"},
            "I'm lost": {"local": "길을 잃었어요", "pronunciation": "Gil-eul il-uh-ssuh-yo", "notes": "Show map on phone"},
            "Where is the hospital?": {"local": "병원이 어디예요?", "pronunciation": "Byung-won-ee uh-dee-yeh-yo?", "notes": "Ambulance: 119"},
        },
    },
    "italian": {
        "language": "Italian",
        "script": "Latin",
        "phrases": {
            "Hello": {"local": "Ciao / Buongiorno", "pronunciation": "Chow / Bwon-jor-no", "notes": "Ciao = informal; Buongiorno = formal"},
            "Goodbye": {"local": "Arrivederci", "pronunciation": "Ah-ree-veh-dair-chee", "notes": "Ciao also works informally"},
            "Please": {"local": "Per favore", "pronunciation": "Pair fah-vor-eh", "notes": ""},
            "Thank you": {"local": "Grazie", "pronunciation": "Grah-tsee-eh", "notes": "Mille grazie = thanks a lot"},
            "Yes": {"local": "Si", "pronunciation": "See", "notes": ""},
            "No": {"local": "No", "pronunciation": "No", "notes": ""},
            "Excuse me": {"local": "Scusi", "pronunciation": "Skoo-zee", "notes": "Formal; Scusa = informal"},
            "I don't understand": {"local": "Non capisco", "pronunciation": "Non kah-pee-skoh", "notes": ""},
            "How much does this cost?": {"local": "Quanto costa?", "pronunciation": "Kwahn-toh kos-tah?", "notes": ""},
            "Where is the bathroom?": {"local": "Dov'e il bagno?", "pronunciation": "Doh-veh eel bahn-yoh?", "notes": ""},
            "Water, please": {"local": "Acqua, per favore", "pronunciation": "Ah-kwah, pair fah-vor-eh", "notes": "Naturale/frizzante = still/sparkling"},
            "The bill, please": {"local": "Il conto, per favore", "pronunciation": "Eel kon-toh, pair fah-vor-eh", "notes": ""},
            "Delicious!": {"local": "Delizioso!", "pronunciation": "Deh-lee-tsee-oh-zoh!", "notes": "Buonissimo! is more common"},
            "Help!": {"local": "Aiuto!", "pronunciation": "Ah-yoo-toh!", "notes": "Emergency"},
            "I need a doctor": {"local": "Ho bisogno di un medico", "pronunciation": "Oh bee-zohn-yoh dee oon meh-dee-koh", "notes": ""},
            "Call the police": {"local": "Chiami la polizia", "pronunciation": "Kee-ah-mee lah poh-lee-tsee-ah", "notes": "Emergency: 112 / Carabinieri: 112"},
            "I'm lost": {"local": "Mi sono perso/a", "pronunciation": "Mee soh-noh pair-soh/sah", "notes": "-o (male) / -a (female)"},
            "Where is the hospital?": {"local": "Dov'e l'ospedale?", "pronunciation": "Doh-veh los-peh-dah-leh?", "notes": "Ambulance: 118"},
        },
    },
    "german": {
        "language": "German",
        "script": "Latin",
        "phrases": {
            "Hello": {"local": "Hallo / Guten Tag", "pronunciation": "Hah-loh / Goo-ten Tahg", "notes": "Guten Tag = more formal"},
            "Goodbye": {"local": "Auf Wiedersehen", "pronunciation": "Owf vee-der-zay-en", "notes": "Casual: Tschuss (choose)"},
            "Please": {"local": "Bitte", "pronunciation": "Bit-teh", "notes": "Also means 'you're welcome'"},
            "Thank you": {"local": "Danke", "pronunciation": "Dahn-keh", "notes": "Vielen Dank = many thanks"},
            "Yes": {"local": "Ja", "pronunciation": "Yah", "notes": ""},
            "No": {"local": "Nein", "pronunciation": "Nine", "notes": ""},
            "Excuse me": {"local": "Entschuldigung", "pronunciation": "Ent-shool-dee-goong", "notes": "Also means sorry"},
            "I don't understand": {"local": "Ich verstehe nicht", "pronunciation": "Ikh fer-shtay-uh nikht", "notes": ""},
            "Do you speak English?": {"local": "Sprechen Sie Englisch?", "pronunciation": "Shpreh-khen zee eng-lish?", "notes": "Most Germans speak English"},
            "How much does this cost?": {"local": "Was kostet das?", "pronunciation": "Vahs kos-tet dahs?", "notes": ""},
            "Where is the bathroom?": {"local": "Wo ist die Toilette?", "pronunciation": "Voh ist dee toy-let-teh?", "notes": ""},
            "Water, please": {"local": "Wasser, bitte", "pronunciation": "Vah-ser, bit-teh", "notes": "Still/sparkling: Stilles/mit Gas"},
            "The bill, please": {"local": "Die Rechnung, bitte", "pronunciation": "Dee rekh-noong, bit-teh", "notes": ""},
            "Delicious!": {"local": "Lecker!", "pronunciation": "Lek-er!", "notes": ""},
            "Help!": {"local": "Hilfe!", "pronunciation": "Hil-feh!", "notes": "Emergency"},
            "I need a doctor": {"local": "Ich brauche einen Arzt", "pronunciation": "Ikh brow-kheh eye-nen artst", "notes": ""},
            "Call the police": {"local": "Rufen Sie die Polizei", "pronunciation": "Roo-fen zee dee poh-lee-tsai", "notes": "Emergency: 112 / Police: 110"},
            "I'm lost": {"local": "Ich habe mich verlaufen", "pronunciation": "Ikh hah-beh mikh fer-low-fen", "notes": ""},
            "Where is the hospital?": {"local": "Wo ist das Krankenhaus?", "pronunciation": "Voh ist dahs krahn-ken-house?", "notes": "Ambulance: 112"},
        },
    },
}

# Map common destination names to language keys
DESTINATION_LANGUAGE_MAP = {
    "japan": "japanese", "tokyo": "japanese", "osaka": "japanese", "kyoto": "japanese",
    "thailand": "thai", "bangkok": "thai", "phuket": "thai", "chiang mai": "thai",
    "spain": "spanish", "madrid": "spanish", "barcelona": "spanish",
    "mexico": "spanish", "colombia": "spanish", "argentina": "spanish", "peru": "spanish",
    "china": "mandarin", "beijing": "mandarin", "shanghai": "mandarin", "guangzhou": "mandarin",
    "taiwan": "mandarin", "taipei": "mandarin",
    "france": "french", "paris": "french", "lyon": "french", "nice": "french",
    "korea": "korean", "seoul": "korean", "busan": "korean",
    "italy": "italian", "rome": "italian", "milan": "italian", "florence": "italian", "venice": "italian",
    "germany": "german", "berlin": "german", "munich": "german", "hamburg": "german",
    "austria": "german", "vienna": "german", "switzerland": "german", "zurich": "german",
}


def get_language_for_destination(destination: str) -> Optional[str]:
    """Try to auto-detect the language key from a destination name."""
    dest_lower = destination.lower().strip()
    for keyword, lang in DESTINATION_LANGUAGE_MAP.items():
        if keyword in dest_lower:
            return lang
    return None


def get_available_languages() -> List[str]:
    """Return list of available language keys."""
    return sorted(PHRASE_BOOKS.keys())


def get_phrase_book(language_key: str) -> str:
    """Get formatted phrase book for a language.

    Args:
        language_key: Language identifier (case-insensitive).
                     Use get_available_languages() to see options.

    Returns:
        Formatted markdown table of phrases.
    """
    # Case-insensitive lookup
    language_key = language_key.lower().strip()

    if language_key not in PHRASE_BOOKS:
        available = ", ".join(sorted(PHRASE_BOOKS.keys()))
        return f"Language '{language_key}' not found. Available: {available}"

    book = PHRASE_BOOKS[language_key]
    lines = [
        f"# Survival Phrases — {book['language']}",
        f"Script: {book['script']}",
        "",
    ]

    # Group phrases by category for better readability
    categories = {
        "Greetings & Basics": ["Hello", "Goodbye", "Please", "Thank you", "Yes", "No", "Excuse me", "I'm sorry"],
        "Survival": ["I don't understand", "Do you speak English?"],
        "Shopping": ["How much does this cost?", "Too expensive"],
        "Navigation": ["Where is the bathroom?", "Where is...?"],
        "Food & Drinks": ["Water, please", "The bill, please", "Delicious!", "No spicy, please"],
        "Emergency": ["Help!", "I need a doctor", "Call the police", "I'm lost", "Where is the hospital?"],
    }

    for cat_name, phrase_keys in categories.items():
        has_phrases = any(k in book["phrases"] for k in phrase_keys)
        if not has_phrases:
            continue

        lines.append(f"\n### {cat_name}")
        lines.append("")

        for key in phrase_keys:
            if key not in book["phrases"]:
                continue
            data = book["phrases"][key]
            lines.append(f"**{key}**")
            lines.append(f"  {data['local']}  —  _{data['pronunciation']}_")
            if data.get("notes"):
                lines.append(f"  Note: {data['notes']}")
            lines.append("")

    return "\n".join(lines)


def get_emergency_phrases(language_key: str) -> str:
    """Get emergency-only phrases for quick reference.

    Args:
        language_key: Language identifier (case-insensitive).

    Returns:
        Formatted emergency phrase card.
    """
    language_key = language_key.lower().strip()

    if language_key not in PHRASE_BOOKS:
        available = ", ".join(sorted(PHRASE_BOOKS.keys()))
        return f"Language '{language_key}' not available. Options: {available}"

    book = PHRASE_BOOKS[language_key]
    emergency_keys = ["Help!", "I need a doctor", "Call the police", "Where is the hospital?", "I'm lost"]

    lines = [
        f"EMERGENCY PHRASES — {book['language']}",
        "=" * 50,
        "",
    ]

    found_any = False
    for key in emergency_keys:
        if key in book["phrases"]:
            found_any = True
            p = book["phrases"][key]
            lines.append(f"  {key}")
            lines.append(f"    {p['local']}")
            lines.append(f"    Say: {p['pronunciation']}")
            if p.get("notes"):
                lines.append(f"    ({p['notes']})")
            lines.append("")

    if not found_any:
        lines.append("  (No emergency phrases available for this language)")

    return "\n".join(lines)


def get_quick_card(language_key: str) -> str:
    """Get a compact quick-reference card for the top 10 most useful phrases."""
    language_key = language_key.lower().strip()

    if language_key not in PHRASE_BOOKS:
        available = ", ".join(sorted(PHRASE_BOOKS.keys()))
        return f"Language '{language_key}' not available. Options: {available}"

    book = PHRASE_BOOKS[language_key]
    top_phrases = [
        "Hello", "Thank you", "Please", "Excuse me",
        "How much does this cost?", "Where is the bathroom?",
        "Water, please", "The bill, please", "Help!", "I don't understand",
    ]

    lines = [
        f"QUICK CARD — {book['language']}",
        "-" * 40,
    ]

    for key in top_phrases:
        if key in book["phrases"]:
            p = book["phrases"][key]
            lines.append(f"  {key:<25} {p['pronunciation']}")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    langs = get_available_languages()
    if len(sys.argv) < 2:
        print("Tourism Buddy — Phrase Book")
        print(f"Available languages: {', '.join(langs)}\n")
        print("Usage:")
        print("  python phrase_book.py <language>            full phrase book")
        print("  python phrase_book.py <language> quick      top-10 quick card")
        print("  python phrase_book.py <language> emergency  emergency phrases only")
        print("  python phrase_book.py auto <destination>    auto-detect by city\n")
        print("Example:  python phrase_book.py japanese quick")
        sys.exit(0)

    if sys.argv[1] == "auto" and len(sys.argv) >= 3:
        dest = " ".join(sys.argv[2:])
        lang = get_language_for_destination(dest)
        if not lang:
            print(f"No language match for '{dest}'. Available: {', '.join(langs)}")
            sys.exit(1)
        print(f"[auto-detected: {lang} for '{dest}']\n")
        print(get_quick_card(lang))
        sys.exit(0)

    lang = sys.argv[1].lower()
    mode = sys.argv[2].lower() if len(sys.argv) > 2 else "full"

    if mode == "quick":
        print(get_quick_card(lang))
    elif mode == "emergency":
        print(get_emergency_phrases(lang))
    else:
        print(get_phrase_book(lang))
