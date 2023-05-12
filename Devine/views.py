from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import filters
from .models import *
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

#danh sách cate
class DivineCategoryList(ListAPIView):
    queryset = DivineCategory.objects.all()
    serializer_class = DivineCategorySerializer


#danh sách phần mềm
class DivineSoftwareList(ListAPIView):
    queryset = DivineSoftware.objects.all()
    serializer_class = DivineSoftwareSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']


#thông tin chi tiết, có thể truyênf vao id
class DivineSoftwareDetail(RetrieveAPIView):
    queryset = DivineSoftware.objects.all()
    serializer_class = DivineSoftwareSerializer


# lấy software theo category
class DivineSoftwareListByCategory(ListAPIView):
    serializer_class = DivineSoftwareSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return DivineSoftware.objects.filter(category__id=category_id).all()


#hàm lấy các bình luận theo sản phẩm và xắp xếp
class DivineCommentList(ListAPIView):
    serializer_class = DivineCommentSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return DivineComment.objects.filter(software_id=product_id).order_by('-created_at')


## dang binh luan
class AddComment(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        user = request.user
        product = DivineSoftware.objects.get(pk=pk)
        text = request.data.get('text')

        if not text:
            return Response({"text": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = DivineComment.objects.create(user=user, software=product, text=text)
        serializer = DivineCommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

## thêm 1 sản phẩm vào giỏ hàng
class AddCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user

        try:
            cart = DivineCart.objects.get(user=user)
        except DivineCart.DoesNotExist:
            cart = DivineCart.objects.create(user=user)

        software = get_object_or_404(DivineSoftware, pk=pk)
        cart_item, created = DivineCartItem.objects.get_or_create(cart=cart, software=software)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        software.quantity -= 1
        software.save()

        return Response({'status': 'success', 'message': 'Added to cart successfully.'})


#xem cart
class DivineCartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get(self, request):
        user = request.user
        cart = get_object_or_404(DivineCart, user=user)
        cart_items = DivineCartItem.objects.filter(cart=cart)
        serializer = self.serializer_class(cart_items, many=True)
        return Response(serializer.data)


#lay chi tiet hoa don
class DivineOrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DivineOrderDetailSerializer

    def get(self, request, order_id):
        try:
            order = DivineOrderDetail.objects.filter(order_id=order_id)
            serializer = self.serializer_class(order, many=True)
            return Response({
                'status': 'success',
                'message': 'Order details retrieved successfully.',
                'data': serializer.data,
            })
        except DivineOrderDetail.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'The order does not exist',
            }, status=status.HTTP_404_NOT_FOUND)


# loại bỏ 1 sản phẩm
class SubCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user

        try:
            cart = DivineCart.objects.get(user=user)
        except DivineCart.DoesNotExist:
            return Response({'status': 'error', 'message': 'Cart not found.'})

        cart_item = get_object_or_404(DivineCartItem, cart=cart, software__pk=pk)
        cart_item.quantity -= 1
        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

        software = cart_item.software
        software.quantity += 1
        software.save()

        return Response({'status': 'success', 'message': 'Subtracted from cart successfully.'})




## hàm order
class Order(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        user = request.user
        # Lấy cart
        cart = get_object_or_404(DivineCart, user=user)
        # Tạo đơn hàng
        order = DivineOrder.objects.create(user=user, status='Pending')
        # Tạo các OrderDetail từ các cartItem của người dùng
        for cart_item in cart.divinecartitem_set.all():
            # Kiểm tra xem cartItem có thuộc về cart không
            if cart_item.cart == cart:
                # Lấy key từ phần mềm thuộc cart item
                software = cart_item.software
                keys = DivineKey.objects.filter(software=software, is_used=False)[:cart_item.quantity]
                if len(keys) < cart_item.quantity:
                    # Nếu không đủ key, trả về lỗi
                    return Response({
                        'status': 'error',
                        'message': f'Not enough keys for {software.name}.',
                    }, status=status.HTTP_400_BAD_REQUEST)
                for key in keys:
                    order_detail = DivineOrderDetail.objects.create(
                        order=order,
                        key=key,
                        quantity=1,
                    )
                    # Đánh dấu key là đã sử dụng
                    key.is_used = True
                    key.save()
                # Xóa cartItem
                cart_item.delete()
        # Trả về thông tin đơn hàng
        return Response({
            'status': 'success',
            'message': 'Order created successfully.',
            'order': order.id,
        })


# ham xem key
class PurchasedKeys(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        purchased_keys = DivineKey.objects.filter(software__has_key=True, divineorderdetail__order__user=user, divineorderdetail__key__is_used=True)
        data = [{
            'key_code': key.key_code,
            'software_name': key.software.name,
            } for key in purchased_keys]
        return Response(data)