from django.http import HttpResponse, JsonResponse
from user_1.models import User_register, p_detail
from user_1.serializers import p_detail_Serializer
from rest_framework.renderers import JSONRenderer


# Geting all properties data
def p_detail_api(request):
    data = p_detail.objects.all()
    data = p_detail_Serializer(data, many=True)
    data = JSONRenderer().render(data.data)
    return HttpResponse(data)


def specific_property(request, property_id):
    data = p_detail.objects.get(pk=property_id)
    data = p_detail_Serializer(data)
    data = JSONRenderer().render(data.data)
    return HttpResponse(data)


def user_wise_property(request, saller_id):
    user_id = User_register.objects.get(user_id=saller_id)
    data = p_detail.objects.filter(seller_id=user_id)
    data = p_detail_Serializer(data, many=True)
    data = JSONRenderer().render(data.data)
    return HttpResponse(data)
