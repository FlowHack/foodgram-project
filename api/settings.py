from rest_framework import status
from rest_framework.response import Response

RESPONSE_SUCCESS = Response({'success': 'true'})
RESPONSE_400_EXIST = Response(
    {'success': 'false', 'error': 'Такой объект уже имеется'}, 
    status=status.HTTP_400_BAD_REQUEST
)
RESPONSE_400_NOT_EXISTS = Response(
    {'success': 'false', 'error': 'Нет такого объекта'}, 
    status=status.HTTP_400_BAD_REQUEST
)
RESPONSE_404_NOT_AUTHOR = Response(
    {'success': 'false', 'error': 'Нет такого автора'}, 
    status=status.HTTP_404_NOT_FOUND
)
RESPONSE_400_CANT_SUBSCRIBE_YOURSELF = Response(
    {'success': 'false', 'error': 'Нельзя подписаться на себя'}, 
    status=status.HTTP_400_BAD_REQUEST
)
