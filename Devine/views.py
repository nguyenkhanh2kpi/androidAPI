from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import filters
from .models import *
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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

