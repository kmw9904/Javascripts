from django.urls import path
from . import views


app_name='finlife'
urlpatterns = [
    # 정기 예금 상품 목록 DB에 저장
    path('save-deposit-products/', views.save_deposit_products),
    # 전체 정기 예금 상품 목록 출력 & 데이터 삽입
    path('deposit-products/', views.deposit_products),
    # 특정 상품의 옵션 리스트 출력
    path('deposit-product-options/<str:fin_product_cd>/', views.deposit_product_options),
    # 가입 기간에 상관 없이 최고 금리가 가장 높은 금융상품과
    # 해당 상품의 옵션 리스트 출력
    path('deposit-products/top_rate/', views.top_rate),

]
