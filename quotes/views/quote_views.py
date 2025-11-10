# from django.views.generic import TemplateView, CreateView, ListView, DetailView
# from django.shortcuts import redirect
# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from quotes.models.quote_models import QuoteRequest
# from quotes.forms.quote_forms import QuoteRequestForm
# from products.models.product_models import Product, FabricOption, ColorOption
# from django.utils.translation import gettext_lazy as _


# class QuoteCalculatorView(TemplateView):
#     template_name = 'quotes/calculator.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         context['fabric_options'] = FabricOption.objects.all()
#         context['color_options'] = ColorOption.objects.all()
#         return context


# class QuoteRequestCreateView(CreateView):
#     model = QuoteRequest
#     form_class = QuoteRequestForm
#     template_name = 'quotes/request_form.html'
#     success_url = reverse_lazy('quotes:success')

#     def form_valid(self, form):
#         # Set user if authenticated
#         if self.request.user.is_authenticated:
#             form.instance.user = self.request.user
        
#         # Calculate the price
#         response = super().form_valid(form)
#         self.object.calculate_price()
        
#         # Send notification email (implementation depends on email setup)
#         # send_quote_notification(self.object)
        
#         messages.success(self.request, _('Your quote request has been submitted successfully!'))
#         return response


# class QuoteSuccessView(TemplateView):
#     template_name = 'quotes/success.html'


# class QuoteListView(LoginRequiredMixin, ListView):
#     model = QuoteRequest
#     template_name = 'quotes/list.html'
#     context_object_name = 'quotes'
#     paginate_by = 10

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return QuoteRequest.objects.all()
#         return QuoteRequest.objects.filter(user=self.request.user)


# class QuoteDetailView(LoginRequiredMixin, DetailView):
#     model = QuoteRequest
#     template_name = 'quotes/detail.html'
#     context_object_name = 'quote'

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return QuoteRequest.objects.all()
#         return QuoteRequest.objects.filter(user=self.request.user)

# quotes/views/quote_views.py
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from quotes.models.quote_models import QuoteRequest
from quotes.forms.quote_forms import QuoteRequestForm
from products.models.product_models import Product, FabricOption, ColorOption
from quotes.services.email_service import send_quote_notification, send_quote_confirmation
import logging
logger = logging.getLogger(__name__)

class QuoteCalculatorView(TemplateView):
    template_name = 'quotes/calculator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['fabric_options'] = FabricOption.objects.all()
        context['color_options'] = ColorOption.objects.all()
        return context


class QuoteRequestCreateView(CreateView):
    model = QuoteRequest
    form_class = QuoteRequestForm
    template_name = 'quotes/request_form.html'
    
    def get_success_url(self):
        return reverse_lazy('quotes:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # تعيين المستخدم إذا كان مسجلاً
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            # استخدام الجلسة للمستخدمين غير المسجلين
            if not self.request.session.session_key:
                self.request.session.create()
            form.instance.session_key = self.request.session.session_key
        
        response = super().form_valid(form)
        self.object.calculate_price()
        
        # حفظ معرف الاقتباس في الجلسة
        if 'user_quotes' not in self.request.session:
            self.request.session['user_quotes'] = []
        
        user_quotes = self.request.session['user_quotes']
        if self.object.pk not in user_quotes:
            user_quotes.append(self.object.pk)
            self.request.session['user_quotes'] = user_quotes
            self.request.session.modified = True
        
        # إرسال الإشعارات بالبريد الإلكتروني مع تصحيح مفصل
        try:
            logger.info(f"Attempting to send emails for quote {self.object.quote_id}")
            
            # إرسال إشعار للموقع
            notification_sent = send_quote_notification(self.object)
            
            # إرسال تأكيد للعميل
            confirmation_sent = send_quote_confirmation(self.object)
            
            if notification_sent and confirmation_sent:
                messages.success(self.request, _('Your quote request has been submitted successfully! Confirmation emails have been sent.'))
                logger.info(f"All emails sent successfully for quote {self.object.quote_id}")
            elif notification_sent:
                messages.success(self.request, _('Quote submitted successfully! Confirmation email to customer may be delayed.'))
                logger.warning(f"Only notification email sent for quote {self.object.quote_id}")
            elif confirmation_sent:
                messages.success(self.request, _('Quote submitted successfully! Internal notification may be delayed.'))
                logger.warning(f"Only confirmation email sent for quote {self.object.quote_id}")
            else:
                messages.success(self.request, _('Quote submitted successfully! Email notifications failed but your request is saved.'))
                logger.error(f"All emails failed for quote {self.object.quote_id}")
                
        except Exception as e:
            logger.error(f"Email sending failed completely: {e}")
            messages.success(self.request, _('Quote submitted successfully! There was an issue with email notifications.'))
        
        return response


class QuoteSuccessView(TemplateView):
    template_name = 'quotes/success.html'


class QuoteListView(ListView):
    model = QuoteRequest
    template_name = 'quotes/list.html'
    context_object_name = 'quotes'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # للمستخدمين المسجلين: عرض جميع طلباتهم
            return QuoteRequest.objects.filter(user=self.request.user)
        else:
            # للمستخدمين غير المسجلين: عرض طلبات الجلسة الحالية فقط
            if self.request.session.session_key:
                return QuoteRequest.objects.filter(session_key=self.request.session.session_key)
            else:
                return QuoteRequest.objects.none()


class QuoteDetailView(DetailView):
    model = QuoteRequest
    template_name = 'quotes/detail.html'
    context_object_name = 'quote'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # للمستخدمين المسجلين: يمكنهم رؤية جميع طلباتهم
            return QuoteRequest.objects.filter(user=self.request.user)
        else:
            # للمستخدمين غير المسجلين: يمكنهم رؤية طلبات جلستهم فقط
            if self.request.session.session_key:
                return QuoteRequest.objects.filter(
                    session_key=self.request.session.session_key,
                    pk=self.kwargs['pk']
                )
            else:
                return QuoteRequest.objects.none()

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except QuoteRequest.DoesNotExist:
            messages.error(request, _('Quote request not found or access denied.'))
            return redirect('quotes:list')