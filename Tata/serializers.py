from rest_framework import serializers
from .models import Category
from django.conf import settings



class CategorySerializer(serializers.ModelSerializer):
    # parents = CategorySerializer(many=True, read_only=True)
    

    class Meta:
        model = Category
        fields = ('name', 'id', 'current_sales', 'total_sales', 
                    'color_code', 'progress', 'progress_label', 'parent')
        # read_only_fields = ('color_code', 'progress', 'progress_label')