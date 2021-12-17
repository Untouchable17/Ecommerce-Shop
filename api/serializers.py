from rest_framework import serializers

from shop_app.models import Category, Product, Comments


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор модели с категориями """

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с товарами """

    category = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Product
        fields = [
            'category', 'title', 'slug', 'price',
        ]


class CommentSerializer(serializers.ModelSerializer):
    """ Вывод полей в комментариях указанного товара (ProductDetailSerializer) """
    class Meta:
        model = Comments
        fields = ("author", "comment", "star_count", "dislikes", "likes")


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для добавления комментария """

    class Meta:
        model = Comments
        fields = ["product", "author", "star_count", "comment"]


class ProductDetailSerializer(serializers.ModelSerializer):
    """ Вывод конкретного товара """

    category = serializers.SlugRelatedField(slug_field="title", read_only=True)
    comment = CommentSerializer(many=True)

    class Meta:
        model = Product
        exclude = ("available", "created_at", "updated_at",)
