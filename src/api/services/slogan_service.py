from libraries.sentence_bert import SentenceBertJapanese
from libraries.sentence_congerter import KanjiToHiraganaConverter
from api.constants import AI_MODEL_NAME
from api.models import Slogans
import torch.nn.functional as F

class SloganService:
    def __init__(self):
        self.sentence_bert_model = SentenceBertJapanese(AI_MODEL_NAME)
        self.conberter = KanjiToHiraganaConverter()
        
    def get_sentence_distance(self, sentence:str):
        hiragana = self.conberter.change_kangi_to_hiragana(sentence)

        all_slogans = Slogans.objects.all()
        vector_list = [[float(value) for value in slogan.vector.split(',')] for slogan in all_slogans]
        slogan_list = [slogan.slogan_sentence for slogan in all_slogans]
        vecs = self.sentence_bert_model.vec_from_list(vector_list)

        target_vec = self.sentence_bert_model.encode_sentence(hiragana)

        # コサイン類似度による類似度算出
        distance_list = F.cosine_similarity(target_vec, vecs).tolist()

        json_data = []
        # name_listとage_listをzipして辞書のリストを作成する
        for slogan, distance in zip(slogan_list, distance_list):
            entry = {
                "slogan": slogan,
                "distance": round(distance, 2),
            }
            json_data.append(entry)
        sorted_json_data = sorted(json_data, key=lambda x: x['distance'], reverse=True)
        return sorted_json_data
    
    def seva_slogan(self, slogan:str):
        hiragana = self.conberter.change_kangi_to_hiragana(slogan)
        vec = self.sentence_bert_model.encode_sentence(hiragana)
        vec_string = self.sentence_bert_model.get_vec_string(vec)
        new_slogan = Slogans(slogan_sentence=slogan, slogan_kana=hiragana, vector=vec_string)
        new_slogan.save()

    def get_slogan_list(self):
        all_slogans = Slogans.objects.all()
        json_data = []
        for slogan in all_slogans:
            entry = {
                "id": slogan.id,
                "slogan": slogan.slogan_sentence,
            }
            json_data.append(entry)
        return json_data
    
    def delete_slogan_by_id(self, id):
        Slogans.objects.filter(id=id).delete()
