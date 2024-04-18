from django.shortcuts import render
from seller.models import Food
from .models import Cart
# Create your views here.
def order_detail(request, pk):
    food = Food.objects.get(pk=pk) # 하나의 오브젝트를 가져온다
    context = {
        'object':food
    }
    return render(request, 'order/order_detail.html')
from django.http import JsonResponse

def modify_cart(request):
    # A사용자가 카트에 담은 음식에 대해서 수량을 조정하는 내용
    # 응답 : 새로운 변경된 수량, 전체 카트에 음식 수량 응답
    # 어떤 사용자 ? 선택한 유저
    user = request.user 
    # 어떤 음식 ?
    food_id = request.POST['foodId']
    food = Food.objects.get(pk=food_id)
    # 카트 정보
    cart, creaeted = Cart.objects.get_or_create(food=food, user = user)
    # 수량 업데이트 
    cart.amount += int(request.POST['amountChange'])
    if cart.amount>0:
        cart.save()
    # user 가 카트에 담은 전체 음식 (개별개수 amount) 개수
    # "내"가 주문한 전체 음식 개수
    # Question - Choice
    # 이 문제에 대한 초이스
    totalQuantity = user.cart_set.aggregate(totalcount=Sum('amount'))['totalcount']
    # Json
    context = {
        'newQuantity' : cart.amount,
        'totalQuantity' : cart.amount,
        'message':'성공',
        'success':True
    }
    return JsonResponse(context)