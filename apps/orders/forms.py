from django import forms
from apps.orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("name", "surname", "email", "phone", "is_delivery", "address", "pay_choice")

    def save(self, commit=True):
        """
        Default save method inside the form.
        `commit=True` saves to the database immediately.
        You can override it to add extra logic before saving.
        """
        instance = super().save(commit=False)  # get the unsaved instance

        # Example: custom logic before saving
        if not instance.is_delivery:
            instance.address = ""  # clear address if no delivery

        if instance.pay_choice == "cod":
            instance.is_completed = True

        if commit:
            instance.save()  # actually save to DB

        return instance