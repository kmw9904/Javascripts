from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from finlife.models import DepositProducts,DepositOptions
from mypjt import settings
from .serializers import DepositProductsSerializer,DepositOptionsSerializer
from rest_framework import status
# Create your views here.
from pprint import pprint

from finlife import serializers


api_key = settings.API_KEY
BASE_URL = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"


# requests 모듈을 활용하여 정기 예금 상품 목록 데이터를
# 가져와 정기 예금 상품 목록과 옵션 목록을 DB에 저장
@api_view(['GET'])
def save_deposit_products(request):
    URL = BASE_URL
    params = {
        'auth':api_key,
        'topFinGrpNo':'020000',
        'pageNo':1
    }
    response = requests.get(URL,params=params).json()
    for product_li in response.get('result').get('baseList'):
        fin_prdt_cd = product_li.get('fin_prdt_cd')
        kor_co_nm = product_li.get('kor_co_nm')
        fin_prdt_nm = product_li.get('fin_prdt_nm')
        etc_note = product_li.get('etc_note')
        join_deny = product_li.get('join_deny')
        join_member = product_li.get('join_member')
        join_way = product_li.get('join_way')
        spcl_cnd = product_li.get('spcl_cnd')


        if DepositProducts.objects.filter(
            fin_prdt_cd=fin_prdt_cd,
            kor_co_nm=kor_co_nm,
            fin_prdt_nm=fin_prdt_nm,
            etc_note=etc_note,
            join_deny=join_deny,
            join_member=join_member,
            join_way=join_way,
            spcl_cnd=spcl_cnd).exists():
            continue
        save_product_data = {
            'fin_prdt_cd':fin_prdt_cd,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'etc_note':etc_note,
            'join_deny':join_deny,
            'join_member':join_member,
            'join_way':join_way,
            'spcl_cnd':spcl_cnd
        }
        serializer = DepositProductsSerializer(data=save_product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option_li in response.get('result').get('optionList'):
        
        fin_prdt_cd = option_li.get('fin_prdt_cd')
        intr_rate_type_nm = option_li.get('intr_rate_type_nm')
        intr_rate = option_li.get('intr_rate')
        intr_rate2 = option_li.get('intr_rate2')
        save_trm = option_li.get('save_trm')

        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)

        if not intr_rate :
            intr_rate = -1

        if DepositOptions.objects.filter(
            fin_prdt_cd=fin_prdt_cd,
            intr_rate_type_nm=intr_rate_type_nm,
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
            save_trm=save_trm).exists():
            continue

        save_option_data = {
            "product":product.pk,
            'fin_prdt_cd':fin_prdt_cd,
            'intr_rate_type_nm':intr_rate_type_nm,
            'intr_rate':intr_rate,
            'intr_rate2':intr_rate2,
            'save_trm':save_trm,
        }
        serializer = DepositOptionsSerializer(data=save_option_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    return JsonResponse({'message':'저장완료'})

# GET : 전체 정기 예금 상품 목록 반환
# POST : 상품 데이터 저장
@api_view(['GET','POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            Response(serializer.data, status=status.HTTP_201_CREATED)


# 특정 상품의 옵션 리스트 반환
@api_view(['GET'])
def deposit_product_options(request,fin_product_cd):
    if request.method == 'GET':
        product = DepositOptions.objects.filter(fin_prdt_cd=fin_product_cd)
        serializer = DepositOptionsSerializer(product, many=True)
        return Response(serializer.data)

# 가입 기간에 상관 없이 금리가 가장 높은 상품과
# 해당 상품의 옵션 리스트 출력
@api_view(['GET'])
def top_rate(request):
    
    if request.method == "GET":
        highest_value_product_option = DepositOptions.objects.order_by('-intr_rate2').first()
        highest_value_product = highest_value_product_option.product
        option_serializer = DepositOptionsSerializer(highest_value_product_option)
        product_serializer = DepositProductsSerializer(highest_value_product)

        return Response({
            "option": option_serializer.data,
            "product": product_serializer.data
        })
    return Response({"error": "No options found"}, status=404)

