import re
# import string
import json
import os
from adaletCleaning import utils


class Cleaning:

    def __init__(self,
                 text: str,
                 removeStops: bool = True,
                 isConvertTRChars: bool = False,
                 removeSpecialChars: bool = False,
                 isLowerCase: bool = True,
                 keepAlphaNumChars: bool = True,
                 removeNumbers: bool = True,
                 removeConsonants: bool = False,
                 removeVowels: bool = False,
                 removePuncts: bool = True,
                 removeCityDistricts: bool = True,
                 isOnlySpecificChars: bool = False,
                 isReplaceAbbr: bool = True):

        self.__text = text
        self.__removeStops = removeStops
        self.__isConvertTRChars = isConvertTRChars
        self.__removeSpecialChars = removeSpecialChars
        self.__isLowerCase = isLowerCase
        self.__keepAlphaNumChars = keepAlphaNumChars
        self.__removeNumbers = removeNumbers
        self.__removeConsonants = removeConsonants
        self.__removeVowels = removeVowels
        self.__removePuncts = removePuncts
        self.__removeCityDistricts = removeCityDistricts
        self.__isOnlySpecificChars = isOnlySpecificChars
        self.__isReplaceAbbr = isReplaceAbbr

        current_dir = os.path.dirname(__file__)

        trChar_path = os.path.join(current_dir, "resources", "trCharToReplace.json")
        punct_path = os.path.join(current_dir, "resources", "punctuations.txt")
        params_path = os.path.join(current_dir, "resources", "cleaningParams.txt")
        stops_path = os.path.join(current_dir, "resources", "stopwords.txt")
        abbr_path = os.path.join(current_dir, "resources", "abbreviations.json")
        allowed_path = os.path.join(current_dir, "resources", "allowedChars.txt")

        with open(trChar_path, "r", encoding="utf-8") as file:
            self.__TRCHARTOREPLACE = json.load(file)

        _, _, self.__cityDistrictNames = utils.getCityDistrictNames()

        # string.punctuations characters are : !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        with open(punct_path, "r", encoding="utf-8") as file:
            self.__PUNCTUATIONS = file.read()

        with open(params_path, "r", encoding="utf-8") as file:
            partOfFile = file.read()

            charactersToKeepStart = partOfFile.find("<CHARACTERS_TO_KEEP>") + len("<CHARACTERS_TO_KEEP>")
            charactersToKeepEnd = partOfFile.find("</CHARACTERS_TO_KEEP>")
            charactersAndNumbersToKeepStart = partOfFile.find("<CHARACTERSANDNUMBERS_TO_KEEP>") + len(
                "<CHARACTERSANDNUMBERS_TO_KEEP>")
            charactersAndNumbersToKeepEnd = partOfFile.find("</CHARACTERSANDNUMBERS_TO_KEEP>")
            specialCharactersStart = partOfFile.find("<SPECIAL_CHARACTERS>") + len("<SPECIAL_CHARACTERS>")
            specialCharactersEnd = partOfFile.find("</SPECIAL_CHARACTERS>")

            characterTokens = partOfFile[charactersToKeepStart:charactersToKeepEnd]
            self.__CHARACTERSTOKEEP = re.compile(r'[{}]'.format(characterTokens))
            characterAndNumbersTokens = partOfFile[charactersAndNumbersToKeepStart:charactersAndNumbersToKeepEnd]
            self.__CHARACTERSANDNUMBERSTOKEEP = re.compile(r'[{}]'.format(characterAndNumbersTokens))
            specialCharacters = partOfFile[specialCharactersStart:specialCharactersEnd]
            self.__SPECIALCHARACTERS = re.compile(r'[{}]'.format(specialCharacters))

        with open(stops_path, "r", encoding="utf-8") as file:
            self.__STOPWORDS = file.read().split("\n")

        with open(abbr_path, "r", encoding="utf-8") as file:
            self.__ABBREVIATIONS = json.load(file)

        with open(allowed_path, "r") as file:
            self.__ALLOWEDCHARS = file.read()

    def __convertTRChars(self):

        try:
            if isinstance(self.__text, str):
                for key, value in self.__TRCHARTOREPLACE.items():
                    self.__text = self.__text.replace(key, value)

            elif isinstance(self.__text, list):
                for key, value in self.__TRCHARTOREPLACE.items():
                    for i in range(len(self.__text)):
                        if isinstance(self.__text[i], str):
                            self.__text[i] = self.__text[i].replace(key, value)

        except Exception as e:
            print("Error: ", e)

    def __lowercase(self):

        try:
            if isinstance(self.__text, str):
                self.__text = utils.turkish_lower(self.__text)
                self.__cleanSpaces()

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = utils.turkish_lower(self.__text[i])
                self.__cleanSpaces()

        except Exception as e:
            print("Error: ", e)

    def __removeCityDistrictNames(self):

        try:
            if isinstance(self.__text, str):
                self.__text = utils.turkish_lower(self.__text)
                self.__text = ' '.join(word for word in self.__text.split() if word not in self.__cityDistrictNames)

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = utils.turkish_lower(self.__text[i])
                        self.__text[i] = ' '.join(
                            word for word in self.__text[i].split() if word not in self.__cityDistrictNames)

        except Exception as e:
            print("Error: ", e)

    def __removePunctuations(self):

        try:
            if isinstance(self.__text, str):
                self.__text = self.__text.translate(str.maketrans(self.__PUNCTUATIONS, ' ' * len(self.__PUNCTUATIONS)))
                self.__cleanSpaces()

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = self.__text[i].translate(
                            str.maketrans(self.__PUNCTUATIONS, ' ' * len(self.__PUNCTUATIONS)))
                self.__cleanSpaces()

        except Exception as e:
            print("Error: ", e)

    def __keepAlphaNumericCharacters(self, removeNumbers):

        try:
            if isinstance(self.__text, str):
                if not removeNumbers:
                    pattern = re.compile(self.__CHARACTERSANDNUMBERSTOKEEP)
                else:
                    pattern = re.compile(self.__CHARACTERSTOKEEP)
                self.__text = re.sub(pattern, ' ', self.__text)
                self.__cleanSpaces()

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        if not removeNumbers:
                            pattern = re.compile(self.__CHARACTERSANDNUMBERSTOKEEP)
                        else:
                            pattern = re.compile(self.__CHARACTERSTOKEEP)
                        self.__text[i] = re.sub(pattern, ' ', self.__text[i])
                self.__cleanSpaces()

        except Exception as e:
            print("Error: ", e)

    def __removeSpecialCharacters(self):

        try:
            if isinstance(self.__text, str):
                pattern = re.compile(self.__SPECIALCHARACTERS)
                self.__text = re.sub(pattern, ' ', self.__text)
                self.__cleanSpaces()

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        pattern = re.compile(self.__SPECIALCHARACTERS)
                        self.__text[i] = re.sub(pattern, ' ', self.__text[i])
                self.__cleanSpaces()

        except Exception as e:
            print("Error: ", e)

    def __removeStopwords(self):

        try:
            if isinstance(self.__text, str):
                self.__text = utils.turkish_lower(self.__text)
                self.__text = ' '.join(word for word in self.__text.split() if word not in self.__STOPWORDS)

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = utils.turkish_lower(self.__text[i])
                        self.__text[i] = ' '.join(
                            word for word in self.__text[i].split() if word not in self.__STOPWORDS)


        except Exception as e:
            print("Error: ", e)

    def __removeSingleCharacters(self):

        try:
            if isinstance(self.__text, str):
                self.__text = ' '.join([w for w in self.__text.split() if len(w) > 1])

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = ' '.join([w for w in self.__text[i].split() if len(w) > 1])

        except Exception as e:
            print("Error: ", e)

    def __removeConsecutiveConsonants(self):

        try:
            if isinstance(self.__text, str):
                result = []
                for word in self.__text.strip().split(" "):
                    if isinstance(word, str):
                        # if there are more than 3 consecutive consonants for a text
                        if len(utils.consonantConsecutiveList(word, 3)) == 0:
                            result.append(word)
                if len(result) > 0:
                    self.__text = ' '.join(result)

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        result = []
                        for word in self.__text[i].strip().split(" "):
                            if isinstance(word, str):
                                # if there are more than 3 consecutive consonants for a text
                                if len(utils.consonantConsecutiveList(word, 3)) == 0:
                                    result.append(word)
                        if len(result) > 0:
                            self.__text[i] = ' '.join(result)

        except Exception as e:
            print("Error: ", e)

    def __removeConsecutiveVowels(self):
        try:
            if isinstance(self.__text, str):
                result = []
                for word in self.__text.strip().split(" "):
                    if isinstance(word, str):
                        # if there are more than 2 consecutive vowels for a text
                        if len(utils.vowelConsecutiveList(word, 2)) == 0:
                            result.append(word)
                if len(result) > 0:
                    self.__text = ' '.join(result)

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        result = []
                        for word in self.__text[i].strip().split(" "):
                            if isinstance(word, str):
                                # if there are more than 3 consecutive consonants for a text
                                if len(utils.vowelConsecutiveList(word, 2)) == 0:
                                    result.append(word)
                        if len(result) > 0:
                            self.__text[i] = ' '.join(result)

        except Exception as e:
            print("Error: ", e)

    def __cleanSpaces(self):

        try:
            # return str(rawText).replace("\'", "").replace('"', "").replace("\t", "").replace("\n", "")
            if isinstance(self.__text, str):
                # text = re.sub(r'\s+', ' ', text).strip()
                self.__text = re.sub(r'\s+', ' ', self.__text).replace("'", " ").replace('"', " ").strip()

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = re.sub(r'\s+', ' ', self.__text[i]).replace("'", " ").replace('"', " ").strip()

        except Exception as e:
            print("Error: ", e)

    def __replaceAbbreviations(self):

        try:
            if isinstance(self.__text, str):
                self.__text = utils.turkish_lower(self.__text)
                self.__removePunctuations()
                for abbr, full_form in self.__ABBREVIATIONS.items():
                    self.__text = re.sub(r'\b{}\b'.format(re.escape(abbr)), full_form, self.__text)
                self.__cleanSpaces()

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = utils.turkish_lower(self.__text[i])
                        self.__removePunctuations()
                        for abbr, full_form in self.__ABBREVIATIONS.items():
                            self.__text[i] = re.sub(r'\b{}\b'.format(re.escape(abbr)), full_form, self.__text[i])
                self.__cleanSpaces()

        except Exception as e:
            print("Error: ", e)

    #: if requested allowCharacters params, then merge all unwanted punctuations and finally remove allowedchars from them
    def __allowOnlySpecificCharacters(self, removeSpecialChars):

        try:
            charactersForReplace = self.__PUNCTUATIONS
            if removeSpecialChars == True:
                charactersForReplace += self.__SPECIALCHARACTERS.pattern
            if len(self.__ALLOWEDCHARS.strip()) > 0:
                uniqueCharacters = ''.join(set(charactersForReplace) - set(self.__ALLOWEDCHARS))
            else:
                uniqueCharacters = ''.join(set(charactersForReplace))

            if isinstance(self.__text, str):
                self.__text = self.__text.translate(str.maketrans(uniqueCharacters, ' ' * len(uniqueCharacters)))
                self.__cleanSpaces()

            elif isinstance(self.__text, list):
                for i in range(len(self.__text)):
                    if isinstance(self.__text[i], str):
                        self.__text[i] = self.__text[i].translate(
                            str.maketrans(uniqueCharacters, ' ' * len(uniqueCharacters)))
                self.__cleanSpaces()

        except Exception as e:
            print("Error: ", e)

    def clean(self):

        if self.__text is not None:

            self.__cleanSpaces()

            if self.__isLowerCase:
                self.__lowercase()

            if self.__isOnlySpecificChars:
                self.__allowOnlySpecificCharacters(self.__removeSpecialChars)
            else:
                if self.__removePuncts:
                    self.__removePunctuations()
                if self.__removeSpecialChars:
                    self.__removeSpecialCharacters()

            if self.__removeCityDistricts:
                self.__removeCityDistrictNames()

            if self.__removeStops:
                self.__removeStopwords()

            if self.__isReplaceAbbr:
                self.__replaceAbbreviations()

            if self.__isConvertTRChars:
                self.__convertTRChars()

            if self.__keepAlphaNumChars:
                self.__keepAlphaNumericCharacters(self.__removeNumbers)

            self.__removeSingleCharacters()

            if self.__removeConsonants:
                self.__removeConsecutiveConsonants()

            if self.__removeVowels:
                self.__removeConsecutiveVowels()

        return self.__text



