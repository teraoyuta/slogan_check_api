from pykakasi import kakasi

class KanjiToHiraganaConverter:
    def __init__(self):
        self.kks = kakasi()

    def change_kangi_to_hiragana(self, text: str):
        result = self.kks.convert(text)
        string = ''
        for i in range(len(result)):
            string += result[i]['hira']
        return string