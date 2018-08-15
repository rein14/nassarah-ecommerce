from django.views.generic import RedirectView, TemplateView


class CouponView(TemplateView):
    """
    This is the home page and will typically live at /
    """
    template_name = 'coupon.html'