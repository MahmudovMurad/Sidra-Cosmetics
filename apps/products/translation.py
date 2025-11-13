from modeltranslation.translator import TranslationOptions, register

from .models import Product, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", )


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "description", "price", "discount")