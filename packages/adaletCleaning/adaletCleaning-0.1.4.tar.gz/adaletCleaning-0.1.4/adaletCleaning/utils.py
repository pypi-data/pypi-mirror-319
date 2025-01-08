import re
import xml.etree.ElementTree as elemTree
import os

def consonantConsecutiveList(word, count):
    consonant_list = re.split(r"[aeıioöuü]+", word, flags=re.I)
    return [y for y in consonant_list if len(y) > count]


def vowelConsecutiveList(word, count):
    consonant_list = re.split(r"[bcdfghjklmnprstvyz]+", word, flags=re.I)
    return [y for y in consonant_list if len(y) > count]


def turkish_lower(text):
    text = text.replace("T.C.", " tc ")
    text = re.sub(r'İ', 'i', text)
    text = re.sub(r'I', 'ı', text)
    text = text.lower()
    return text


def turkish_upper(text):
    text = re.sub(r'i', 'İ', text)
    text = text.upper()
    return text



#: read a xml file and parse its roots
def getCityDistrictNames():
    current_dir = os.path.dirname(__file__)  # Geçerli dosyanın bulunduğu dizin

    il_ilceler_path = os.path.join(current_dir, "resources", "il_ilceler.xml")

    tree = elemTree.parse(il_ilceler_path)
    root = tree.getroot()

    cityNames = []
    districtNames = []
    cityDistrictNames = []

    try:
        for city in root.findall('CITY'):
            cityName = turkish_lower(str(city.attrib['cityname']))
            cityNames.append(cityName)
            for district in city.findall('DISTRICT'):
                districtName = turkish_lower(district.find('DISTNAME').text)
                if len(districtName.split('/')) > 1:
                    districtName = districtName.split('/')[0].strip()
                if len(districtName.split(' ')) > 1:
                    districtName = districtName.split(' ')[1].strip()
                districtNames.append(districtName)

                cityDistrictNames.append(cityName)
                cityDistrictNames.append(districtName)

    except Exception as e:
        print(e)

    return list(set(cityNames)), list(set(districtNames)), list(set(cityDistrictNames))

