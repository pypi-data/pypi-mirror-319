from deep_translator import GoogleTranslator
import random

def translate(times,original):
    temp=original
    languages =list(GoogleTranslator().get_supported_languages(as_dict=True).values())
    for i in range(times):
        random.shuffle(languages)
        transltor=GoogleTranslator(source='auto', target=languages[0])
        temp=transltor.translate(temp)
        if i==times-1:
            temp=GoogleTranslator(source='auto', target='en').translate(temp)
            return temp