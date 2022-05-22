from unicodedata import category
from rest_framework import viewsets, status
from .serializers import CategorySerializer
from .models import Category
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def populate_data(self, data):
        body = data
        progress = (int(body['current_sales']) /int(body['total_sales'])) *100
        print(progress)
        body['progress'] = int(progress)
        body['color_code'] = 'YELLOW'
        body['progress_label'] = 'Off Track'
        
        if progress >66: 
            body['color_code'] = 'GREEN'
            body['progress_label'] = 'On Track'
        elif progress <=33:
            body['color_code'] = 'RED'
            body['progress_label'] = 'At Risk'

        return body


    def populate_children(self, children, level):
        if level == 0: return None
        queryset = Category.objects.all()
        data = []

        for child in children:
            category = get_object_or_404(queryset, pk=int(child.pk))
            serializer = CategorySerializer(category)
            children = category.children.all()
            obj = {}
            obj.update(serializer.data)
            level -= 1
            obj['children'] = self.populate_children(children, level)
            level += 1
            data.append(obj)
        
        return data


    @action(methods=['get'], detail=True)
    def retrieve_category_with_level(self, request, *args, **kwargs):
        level = int(kwargs['level'])
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=int(kwargs['pk']))
        serializer = CategorySerializer(category)
        children = category.children.all()
        obj = {}
        obj.update(serializer.data)
        obj['children'] = self.populate_children(children, level)

        return Response(obj, status=status.HTTP_200_OK)
    

    @action(methods=['get'], detail=True)
    def retrieve_parents(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        parent = serializer.data['parent']
        obj = {}
        obj.update(serializer.data)

        parents = []
        def populate_parents(parent):
            if parent:
                queryset = Category.objects.all()
                category = get_object_or_404(queryset, pk=int(parent))
                serializer = CategorySerializer(category)
                parent = serializer.data['parent']
                parents.append(serializer.data)
                obj['parents'] = populate_parents(parent)
        populate_parents(parent)
        obj['parents'] = parents

        return Response(obj, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        serializer = CategorySerializer(data=self.populate_data(request.data))
        request.data._mutable = False
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Category Saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        obj = Category.objects.get(id=pk)
        request.data._mutable = True
        serializer = CategorySerializer(obj, data=self.populate_data(request.data))
        request.data._mutable = False
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Category Updated'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        category = get_object_or_404(Category, id=pk)
        category.delete()
        return Response({'msg': 'Category Deleted'}, status=status.HTTP_200_OK)


    @action(methods=['delete'], detail=True)
    def delete_parent_without_child(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        children = category.children.all()
        for child in children:
            child.parent = None
            child.save()
        return Response({'msg': 'Category deleted without child'}, status=status.HTTP_200_OK)


