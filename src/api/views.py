from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.services.slogan_service import SloganService
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_kana_from_slogan(request):
    try:
        slogan = request.GET.get('slogan_sentence', None)

        slogan_service = SloganService()
        kana_sentence = slogan_service.get_kana(slogan)
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return Response({'message': f"{e.__class__.__name__}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'message':'success get kana', 'kana': kana_sentence}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_slogan(request):
    try:
        slogan = request.GET.get('slogan_sentence', None)
        response_limit = request.GET.get('response_limit', None)
        response_limit = int(response_limit)

        slogan_service = SloganService()
        sentence_distances = slogan_service.get_sentence_distance(slogan, response_limit)
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return Response({'message': f"{e.__class__.__name__}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'message':'success check slogan', 'distances': sentence_distances}, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_slogan(request):
    try:
        slogans = request.data['slogan_sentences']
        slogan_service = SloganService()
        with transaction.atomic():
            slogan_service.seva_slogan(slogans)

    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return Response({'message': f"{e.__class__.__name__}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'message':'success insert slogan'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_slogan_list(request):
    try:
        search_head_date = request.GET.get('search_head_date', None)
        search_tail_date = request.GET.get('search_tail_date', None)
        
        slogan_service = SloganService()
        slogan_list = slogan_service.get_slogan_list(search_head_date, search_tail_date)
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return Response({'message': f"{e.__class__.__name__}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'message':'success get slogan list', 'slogans': slogan_list}, status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_slogan(request):
    try:
        slogan_id = request.POST.get('id')
        slogan_service = SloganService()
        slogan_service.delete_slogan_by_id(slogan_id)
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return Response({'message': f"{e.__class__.__name__}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'message':'success delete slogan id:' + str(slogan_id)}, status=status.HTTP_200_OK)
