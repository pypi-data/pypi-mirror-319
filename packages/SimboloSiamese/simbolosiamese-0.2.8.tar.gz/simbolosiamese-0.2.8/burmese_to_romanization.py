# This function converts Burmese text to Romanized Burmese.
# pip install SimboloSiamese
# pip install myanmartools
from Siamese import BurmeseConverter
from myanmartools import ZawgyiDetector

def burmese_to_romanization(text):
        # It first detects whether the input text is in Zawgyi or Unicode encoding using the ZawgyiDetector
        detector = ZawgyiDetector()
        score = detector.get_zawgyi_probability(text)

        # If the text is Zawgyi (score >= 0.5), it converts it to Unicode and then romanizes it.
        if score >= 0.5:
            converter = BurmeseConverter() # The BurmeseConverter class is used for both conversions (Zawgyi to Unicode and Unicode to Romanized Burmese).
            zawgyi_text = text
            try:
                unicode_output = converter.zawgyi_to_unicode(zawgyi_text)
                romanized_output = converter.burmese_to_romanization(unicode_output)
                return ("Romanized Output:", romanized_output)
            except Exception as e:
                return (f"Error in Zawgyi to Unicode conversion: {e}")

        else:  # If the text is already in Unicode, it directly romanizes the text.
            try:
                converter = BurmeseConverter()
                romanized_output = converter.burmese_to_romanization(text)
                return ("Romanized Output:", romanized_output)
            except Exception as e:
                return(f"Error in Burmese Romanization: {e}")

text = "မင္း ကလဲကြာ"
print(burmese_to_romanization(text))