from deep_translator import GoogleTranslator

def translate_to_english(sentence: str):
    return GoogleTranslator(source='auto', target='english')