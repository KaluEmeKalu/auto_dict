import os.path


class Word(object):
    def __init__(self, word="Gadget", definition="A thing that does something",
                 example='a computer is a gadget.', origin="Anglo Saxon",
                 part_of_speech="noun", syllables="Ga*dget",
                 synonyms="thing, jawn", antonyms="void, lack",
                 other_usages="used to mean tech device", pronunciation="gaaa*jett",
                 tags="tech, science, short_words", audio=None):
        self.word = word
        self.definition = definition
        self.example = example
        self.origin = origin
        self.part_of_speech = part_of_speech
        self.syllables = syllables
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.other_usages = other_usages
        self.pronunciation = pronunciation
        self.tags = tags
        self.audio = audio

    def anki_header(self):
        text = "Front\tBack\tExample\tOrigin\tUsage\t"
        text += "Part of speech\tSyllables\t"
        text += "Synonyms\tAntonyms\t"
        text += "Other usages\tPronunciation\tTags\n\n"
        return text



    def make_string(self):
        word = self
        entry = "{w.word}\t{w.definition}\t".format(w=word)
        entry += "{w.example}\t".format(w=word)
        entry += "{w.origin}\t".format(w=word)
        entry += "{w.part_of_speech}\t".format(w=word)
        entry += "{w.syllables}\t".format(w=word)
        entry += "{w.synonyms}\t".format(w=word)
        entry += "{w.antonyms}\t".format(w=word)
        entry += "{w.other_usages}\t".format(w=word)
        entry += "{w.pronunciation}\t".format(w=word)
        entry += "{w.tags}\n".format(w=word)
        entry += "\n"
        return entry


class MakeAnkiExportString(object): 

    def __init__(self, word_objs_list):
        """
        word_objs_list must be a list of 
        instances of the Word class above
        """

        self.word_objs_list = word_objs_list

    def make(self):

        text = self.word_objs_list[0].anki_header()
        
        for word in self.word_objs_list:
            text += word.make_string()
        return text

        
word = Word()
word2 = Word(definition="A thign to put to see better", word='glasses')
wordlist= [word, word2]