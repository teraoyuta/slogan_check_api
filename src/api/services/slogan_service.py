from libraries.sentence_bert import SentenceBertJapanese
from libraries.sentence_congerter import KanjiToHiraganaConverter
from django.core.paginator import Paginator
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

    def get_kana(self, sentence: str):
        hiragana = self.conberter.change_kangi_to_hiragana(sentence)
        return hiragana
        
    def get_sentence_distance(self, sentence: str, limit: int):
        json_data = []
        hiragana = self.conberter.change_kangi_to_hiragana(sentence)
        target_vec = self.sentence_bert_model.encode_sentence(hiragana)
        batch_size = 1000
        paginator = Paginator(Slogans.objects.all(), batch_size)
        for page_idx in range(1, paginator.num_pages + 1):
            slogans_page = paginator.page(page_idx)
            slogan_vecs_dict = self.sentence_bert_model.get_slogans_vec_dict(slogans_page)

            # コサイン類似度による類似度算出
            distance_list = F.cosine_similarity(target_vec, slogan_vecs_dict[self.sentence_bert_model.VECS_KEY]).tolist()
            for slogan, distance in zip(slogan_vecs_dict[self.sentence_bert_model.SENTENCES_KEY], distance_list):
                entry = {
                    "slogan": slogan,
                    "distance": round(distance, 2),
                }
                json_data.append(entry)
        sorted_json_data = sorted(json_data, key=lambda x: x["distance"], reverse=True)
        if (limit is not None):
            sorted_json_data = sorted_json_data[:limit]
        return sorted_json_data
    
    def seva_slogan(self, slogans: list):
        batch_size = 1000
        for i in range(0, len(slogans), batch_size):
            batch = slogans[i:i+batch_size]
            slogan_objects = []
            for slogan in batch:
                hiragana = self.conberter.change_kangi_to_hiragana(slogan)
                vec = self.sentence_bert_model.encode_sentence(hiragana)
                serialized_vec = pickle.dumps(vec)
                slogan_objects.append(Slogans(slogan_sentence=slogan, slogan_kana=hiragana, vector=serialized_vec))
            Slogans.objects.bulk_create(slogan_objects)

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
