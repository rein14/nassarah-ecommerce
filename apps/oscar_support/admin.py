from django.contrib import admin
from oscar.core.loading import get_model

Attachment = get_model('oscar_support', 'Attachment')
Line = get_model('order', 'Line')
Message = get_model('oscar_support', 'Message')
Priority = get_model("oscar_support", "Priority")
Product = get_model('catalogue', 'Product')
RelatedOrder = get_model("oscar_support", "RelatedOrder")
RelatedOrderLine = get_model("oscar_support", "RelatedOrderLine")
RelatedProduct = get_model("oscar_support", "RelatedProduct")
Ticket = get_model('oscar_support', 'Ticket')
TicketStatus = get_model('oscar_support', 'TicketStatus')
TicketType = get_model('oscar_support', 'TicketType')


class AttacmentInlineAdmin(admin.TabularInline):
    model = Attachment
    fields = ['user', 'file']


class LinesInlineAdmin(admin.TabularInline):
    model = Ticket.related_lines.through
    fields = ['line']


class OrderInlineAdmin(admin.TabularInline):
    model = Ticket.related_orders.through
    fields = ['order']


class ProductInlineAdmin(admin.TabularInline):
    model = Ticket.related_products.through
    fields = ['product']


class MessageInlineAdmin(admin.TabularInline):
    model = Message
    fields = ['user', 'type', 'text']


class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fields = ['name', 'slug']
    readonly_fields = ['slug']


class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fields = ['name', 'slug']
    readonly_fields = ['slug']


class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'comment']
    fields = ['name', 'slug', 'comment']
    readonly_fields = ['slug']


class TicketAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_updated'
    inlines = [
        AttacmentInlineAdmin,
        LinesInlineAdmin,
        OrderInlineAdmin,
        ProductInlineAdmin,
        MessageInlineAdmin
    ]
    list_display = ['number', 'is_internal', 'requester', 'type', 'assignee', 'priority', 'status']
    list_filter = ['is_internal', 'requester', 'type', 'assignee', 'priority', 'status']
    raw_id_fields = ['related_lines', 'related_orders', 'related_products']
    readonly_fields = ['date_created', 'date_updated']
    search_fields = [
        'is_internal',
        'requester__username',
        'type__name',
        'assignee__username',
        'priority__name',
        'status__name'
    ]


class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_updated'
    list_display = ['user', 'type', 'ticket', 'text']
    list_filter = ['user', 'type', 'ticket']
    readonly_fields = ['date_created', 'date_updated']
    search_fields = ['user__username', 'type', 'ticket__number']


class RelatedOrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_updated'
    list_display = ['user', 'ticket', 'order']
    list_filter = ['user', 'ticket', ]
    readonly_fields = ['date_created', 'date_updated']
    search_fields = ['user__username', 'ticket__number', ]


class RelatedOrderLineAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_updated'
    list_display = ['user', 'ticket', 'line']
    list_filter = ['user', 'ticket', ]
    readonly_fields = ['date_created', 'date_updated']
    search_fields = ['user__username', 'ticket__number', ]


class RelatedProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_updated'
    list_display = ['user', 'ticket', 'product']
    list_filter = ['user', 'ticket', ]
    readonly_fields = ['date_created', 'date_updated']
    search_fields = ['user__username', 'ticket__number', ]


class AttachmentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_updated'
    list_display = ['user', 'ticket', 'file']
    list_filter = ['user', 'ticket', ]
    readonly_fields = ['date_created', 'date_updated']
    search_fields = ['user__username', 'ticket__number', ]


admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(TicketStatus, TicketStatusAdmin)
admin.site.register(Priority, PriorityAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(RelatedOrder, RelatedOrderAdmin)
admin.site.register(RelatedOrderLine, RelatedOrderLineAdmin)
admin.site.register(RelatedProduct, RelatedProductAdmin)
admin.site.register(Attachment, AttachmentAdmin)
