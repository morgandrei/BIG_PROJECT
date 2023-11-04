from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView

from newsletter.forms import NewsletterForm, MessageForm, ClientForm
from newsletter.models import Newsletter, Message, Client, Log
from newsletter.services import get_random_blog_article



class UserQuerysetMixin:
    """Ограничивает список просматриваемых пользователем объектов, принадлежащими только текущему пользователю,
     и сохраняет доступ для персонала"""

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class StaffUserObjectMixin:
    """Ограничивает доступ пользователя к чужим объектам, и сохраняет доступ для персонала"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class UserObjectMixin:
    """Ограничивает доступ пользователя к чужим объектам"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class UserFormMixin:
    """Присваивает объект пользователю который его создал"""

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LoginRequiredMessageMixin(LoginRequiredMixin):
    """Ограничение доступа только для авторизованных пользователей, вывод соответствующего информационного сообщения"""

    def handle_no_permission(self):
        messages.error(self.request, 'Для доступа к этой странице необходимо авторизоваться')
        return super().handle_no_permission()


def index(request):

    return render(request, 'newsletter/index.html', context=
    {
        'all_newsletter': Newsletter.objects.count(),
        'active_newsletter': Newsletter.objects.filter(is_active=True).count(),
        'clients': Client.objects.all().values('email').distinct().count(),
        'blog_list': get_random_blog_article()
    }
                  )


class ContactsView(TemplateView):
    template_name = 'newsletter/clients_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            print(f'You have new message from {name}({email}): {message}')
        context_data['object_list'] = Client.objects.all()

        return context_data


class NewsletterCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    permission_required = 'newsletter.add_newsletter'
    success_url = reverse_lazy('newsletter:newsletter_list')

    def get_form(self, form_class=None):
        """Формирование полей 'clients' и 'message' в форме, принадлежащих текущему пользователю"""
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)

        return form


class NewsletterUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    permission_required = 'newsletter.change_newsletter'

    def get_success_url(self):
        return reverse('newsletter:newsletter_detail', args=[self.kwargs.get('pk')])


class NewsletterListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Newsletter
    permission_required = 'newsletter.view_newsletter'


class NewsletterDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Newsletter
    permission_required = 'newsletter.view_newsletter'


class NewsletterDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Newsletter
    permission_required = 'newsletter.delete_newsletter'
    success_url = reverse_lazy('newsletter:newsletter_list')


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'newsletter.add_message'
    success_url = reverse_lazy('newsletter:message_list')


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'newsletter.change_message'

    def get_success_url(self):
        return reverse('newsletter:message_detail', args=[self.kwargs.get('pk')])


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Message
    permission_required = 'newsletter.view_message'


class MessageDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Message
    permission_required = 'newsletter.delete_message'
    success_url = reverse_lazy('newsletter:message_list')


class MessageDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Message
    permission_required = 'newsletter.view_message'


class ClientCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'newsletter.add_client'
    success_url = reverse_lazy('newsletter:client_list')


class ClientUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'newsletter.change_client'

    def get_success_url(self):
        return reverse('newsletter:client_detail', args=[self.kwargs.get('pk')])


class ClientListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Client
    permission_required = 'newsletter.view_client'


class ClientDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Client
    permission_required = 'newsletter.view_client'


class ClientDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Client
    permission_required = 'newsletter.delete_client'
    success_url = reverse_lazy('newsletter:client_list')


@login_required
@permission_required('newsletter.change_activity')
def toggle_activity(request, pk):
    """Отключение рассылок"""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.user.is_staff:
        if newsletter.is_active:
            newsletter.is_active = False
            newsletter.status = newsletter.STATUS_CHOICES[2]
            newsletter.save()
        else:
            newsletter.is_active = True
            newsletter.status = newsletter.STATUS_CHOICES[1]
            newsletter.save()
        return redirect('newsletter:newsletter_list')


class LogListView(LoginRequiredMessageMixin, ListView):
    model = Log

    def get_queryset(self):
        """Получает список логов рассылок принадлежащих только текущему пользователю, и всех логов для персонала"""
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(newsletter__user=self.request.user)


@login_required
def get_newsletter_log(request, pk):
    """Получение логов принадлежащих конкретной рассылке"""
    newsletter_log = Log.objects.filter(newsletter_id=pk)
    newsletter = newsletter_log.first().newsletter
    context = {
        'object_list': newsletter_log,
        'name': newsletter.name
    }
    return render(request, 'newsletter/newsletter_logs.html', context=context)
