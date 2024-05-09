from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.services.slogan_service import SloganService
import logging
import json

logger = logging.getLogger(__name__)

@api_view(['GET'])
def check_slogan(request):
    slogan_kana = request.GET.get('slogan_sentence', None)
    slogan_service = SloganService()
    sentence_distances = slogan_service.get_sentence_distance(slogan_kana)
    return Response({'message':'success check slogan', 'distances': sentence_distances})

@api_view(['POST'])
def save_slogan(request):
    try:
        slogans = request.data['sentences']
        slogan_service = SloganService()
        slogan_service.seva_slogan(slogans)
        return Response({'message':'success insert slogan'})
    except:
        logger.error('error')
        return Response({'message':'error'})

@api_view(['GET'])
def get_slogan_list(request):
    select_head_date = request.GET.get('select_head_date', None)
    select_tail_date = request.GET.get('select_tail_date', None)
    
    slogan_service = SloganService()
    slogan_list = slogan_service.get_slogan_list(select_head_date, select_tail_date)
    return Response({'message':'success get slogan list', 'slogans': slogan_list})

@api_view(['POST'])
def delete_slogan(request):
    slogan_id = request.POST.get('id')
    slogan_service = SloganService()
    slogan_service.delete_slogan_by_id(slogan_id)
    return Response({'message':'success delete slogan id:' + str(slogan_id)})
