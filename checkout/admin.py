from django.contrib import admin
from django import forms
from .models import Order, OrderLineItem


class OrderAdminForm(forms.ModelForm):
    """
    Custom form for Order admin to override the country field.
    django-countries CountryField returns BlankChoiceIterator which
    doesn't have __len__, causing admin rendering to fail.
    """
    country = forms.ChoiceField(required=True)

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Materialize the country choices to avoid BlankChoiceIterator issues
        country_field = Order._meta.get_field('country')
        self.fields['country'].choices = list(country_field.choices)


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid',)

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)