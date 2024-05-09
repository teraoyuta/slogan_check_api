from libraries.sentence_bert import SentenceBertJapanese
from libraries.sentence_congerter import KanjiToHiraganaConverter
import api.constants as constants
from api.models import Slogans
import torch.nn.functional as F
import pickle
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SloganService:
    def __init__(self):
        self.sentence_bert_model = SentenceBertJapanese(constants.AI_MODEL_NAME)
        self.conberter = KanjiToHiraganaConverter()
        
    def get_sentence_distance(self, sentence: str, limit: int):
        hiragana = self.conberter.change_kangi_to_hiragana(sentence)

        all_slogans = Slogans.objects.all()
        # vector_list = [slogan.vector for slogan in all_slogans]
        slogan_list = [slogan.slogan_sentence for slogan in all_slogans]
        vecs = self.sentence_bert_model.vec_from_binary(all_slogans)

        target_vec = self.sentence_bert_model.encode_sentence(hiragana)

        # コサイン類似度による類似度算出
        distance_list = F.cosine_similarity(target_vec, vecs).tolist()
        logger.info(target_vec)
        logger.info(vecs)
        logger.info(distance_list)
        json_data = []
        for slogan, distance in zip(slogan_list, distance_list):
            entry = {
                "slogan": slogan,
                "distance": round(distance, 2),
            }
            json_data.append(entry)
        sorted_json_data = sorted(json_data, key=lambda x: x['distance'], reverse=True)
        if (limit is not None):
            sorted_json_data = sorted_json_data[:limit]
        return sorted_json_data
    
    def seva_slogan(self, slogans: list):
        for slogan in slogans:
            hiragana = self.conberter.change_kangi_to_hiragana(slogan)
            vec = self.sentence_bert_model.encode_sentence(hiragana)
            serialized_vec = pickle.dumps(vec)
            new_slogan = Slogans(slogan_sentence=slogan, slogan_kana=hiragana, vector=serialized_vec)
            new_slogan.save()

    def get_slogan_list(self, search_head_date: datetime = None, search_tail_date: datetime = None):
        all_slogans = Slogans.objects.all()
        if search_head_date:
            head_date = datetime.strptime(search_head_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            all_slogans = all_slogans.filter(created_at__gte=head_date)

        if search_tail_date:
            tail_date = datetime.strptime(search_tail_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            all_slogans = all_slogans.filter(created_at__lte=tail_date)
            
        json_data = []
        for slogan in all_slogans:
            entry = {
                "id": slogan.id,
                "slogan": slogan.slogan_sentence,
                "created_at": slogan.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            json_data.append(entry)
        return json_data
    
    def delete_slogan_by_id(self, id: int):
        Slogans.objects.filter(id=id).delete()
