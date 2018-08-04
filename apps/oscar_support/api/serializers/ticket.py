from rest_framework import serializers

from oscar.core.compat import get_user_model
from oscar.core.loading import get_model

from oscarapi.utils import (
    OscarModelSerializer,
    overridable,
    OscarHyperlinkedModelSerializer
)

Attachment = get_model('oscar_support', 'Attachment')
Basket = get_model('basket', 'Basket')
Line = get_model('order', 'Line')
Message = get_model('oscar_support', 'Message')
Order = get_model('order', 'Order')
Product = get_model('catalogue', 'Product')
Ticket = get_model('oscar_support', 'Ticket')
TicketStatus = get_model('oscar_support', 'TicketStatus')
TicketType = get_model('oscar_support', 'TicketType')


class UserSerializer(serializers.ModelSerializer):
    display_text = serializers.SerializerMethodField('get_display_text')

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'display_text')

    def get_display_text(self, obj):
        if not obj:
            return ''
        full_name = obj.get_full_name()
        if full_name:
            return "{0} <{1}>".format(full_name, obj.email)
        return obj.email


"""
class PartnerSerializer(OscarModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class OptionSerializer(OscarHyperlinkedModelSerializer):
    class Meta:
        model = Option
        fields = overridable('OSCARAPI_OPTION_FIELDS', default=(
            'url', 'id', 'name', 'code', 'type'
        ))
"""


class TicketLinkSerializer(OscarHyperlinkedModelSerializer):
    priority = serializers.StringRelatedField(required=False)

    class Meta:
        model = Ticket
        fields = ['url', 'number', 'subject', 'priority']
        # overridable('OSCARAPI_TICKET_FIELDS', default=())


"""
class ProductAttributeValueSerializer(OscarModelSerializer):
    name = serializers.StringRelatedField(source="attribute")
    value = serializers.StringRelatedField()

    class Meta:
        model = ProductAttributeValue
        fields = overridable('OSCARAPI_PRODUCT_ATTRIBUTE_VALUE_FIELDS', default=('name', 'value',))


class ProductAttributeSerializer(OscarModelSerializer):
    productattributevalue_set = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = overridable('OSCARAPI_PRODUCT_ATTRIBUTE_FIELDS', default=('name', 'productattributevalue_set'))


class ProductImageSerializer(OscarModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class AvailabilitySerializer(serializers.Serializer):
    is_available_to_buy = serializers.BooleanField()
    num_available = serializers.IntegerField(required=False)
    message = serializers.CharField()


class RecommmendedProductSerializer(OscarModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')

    class Meta:
        model = Product
        fields = overridable(
            'OSCARAPI_RECOMMENDED_PRODUCT_FIELDS', default=('url',))
"""


class TicketRelatedLineSerializer(OscarModelSerializer):
    order = serializers.StringRelatedField()
    partner = serializers.StringRelatedField()
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail', read_only=True)

    # status = models.CharField()

    class Meta:
        model = Line
        fields = ['url', 'order', 'partner', 'product', 'status', ]


class TicketRelatedOrderSerializer(OscarModelSerializer):
    basket = serializers.HyperlinkedRelatedField(
        view_name='basket-detail', queryset=Basket.objects)
    owner = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, source='user')

    # TODO: Status doesn't show anything
    # status = models.CharField()

    class Meta:
        model = Order
        fields = ['url', 'number', 'basket', 'owner', 'status', ]


class TicketRelatedProductSerializer(OscarModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'upc', 'title', 'rating']


class TicketAttachmentSerializer(OscarModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, )

    class Meta:
        model = Attachment
        fields = '__all__'


class TicketMessageSerializer(OscarModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True, )

    class Meta:
        model = Message
        fields = '__all__'


class TicketSerializer(OscarModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ticket-detail')
    requester = serializers.StringRelatedField()  # TODO: It need be hyperlinked
    status = serializers.StringRelatedField()
    type = serializers.StringRelatedField()
    assigned_group = serializers.StringRelatedField()
    assignee = serializers.StringRelatedField()
    priority = serializers.StringRelatedField(required=False)
    # parent = serializers.StringRelatedField()
    attachments = TicketAttachmentSerializer(many=True, required=False, )
    related_lines = TicketRelatedLineSerializer(many=True, required=False, )  # TODO: Review it
    related_orders = TicketRelatedOrderSerializer(many=True, required=False, )
    related_products = TicketRelatedProductSerializer(many=True, required=False, )
    messages = TicketMessageSerializer(many=True, required=False, )

    class Meta:
        model = Ticket
        fields = [
            'url',
            'is_internal',
            'type',
            'number',
            'subject',
            'requester',
            'status',
            'body',
            'subticket_id',
            # 'parent',
            'assigned_group',
            'assignee',
            'priority',
            'attachments',
            'related_lines',
            'related_orders',
            'related_products',
            'messages'
        ]
        # overridable('OSCARAPI_PRODUCTDETAIL_FIELDS', default=())


"""
class OptionValueSerializer(serializers.Serializer):
    option = serializers.HyperlinkedRelatedField(
        view_name='option-detail', queryset=Option.objects)
    value = serializers.CharField()


class AddProductSerializer(serializers.Serializer):
    # Serializes and validates an add to basket request.
    quantity = serializers.IntegerField(required=True)
    url = serializers.HyperlinkedRelatedField(
        view_name='product-detail', queryset=Product.objects, required=True)
    options = OptionValueSerializer(many=True, required=False)

    class Meta:
        model = Product
"""


class AddTicketSerializer(serializers.HyperlinkedModelSerializer):
    requester = serializers.StringRelatedField()  # TODO: It need be hyperlinked
    type = serializers.StringRelatedField()
    attachments = TicketAttachmentSerializer(many=True, required=False, )

    class Meta:
        model = Ticket
        fields = [
            'type',
            'subject',
            'requester',
            'body',
            'attachments',
        ]

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)
