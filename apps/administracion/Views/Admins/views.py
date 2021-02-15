import datetime

from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.administracion.models import Profile
from apps.administracion.Views.Admins.forms import ProfileForm, UserFormNew, ProfileUpdateForm
from apps.administracion.functions import actualizar_datos, actualizar_precios

class AdministratorList(ListView):
    template_name = 'administracion/specific/Admins/list.html'
    model = Profile

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Administradores'
        context['title_table'] = 'Lista de Administradores'
        context['table_id'] = 'Admins'
        context['table_fields'] = [
            'Usuario',
            'Sueldo Mensual',
            'Dinero en posesión',
            'Acciones',
        ]
        context['add_button_name'] = 'Nuevo Administrador'
        context['administradores'] = Profile.objects.all().count()
        return context

class AdministratorCreate(CreateView):
    model = User
    template_name = 'administracion/specific/Admins/create.html'
    form_class = UserCreationForm
    second_form_class = ProfileForm
    thirth_form_class = UserFormNew
    success_url = reverse_lazy('administracion:administradores')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.thirth_form_class(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save(commit=False)
            form3.save(commit=False)
            user.is_staff = False
            user.is_active = True
            user.is_superuser = True
            user.date_joined = datetime.datetime.now()
            user.first_name = form3.instance.first_name
            user.last_name = form3.instance.last_name
            user.save()
            profile = form2.save(commit=False)
            profile.user = user
            profile.rol = 'Administrador'
            profile.amount = 0
            profile.sueldo = 0
            profile.save()
            actualizar_datos()
            actualizar_precios()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(AdministratorCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.thirth_form_class(self.request.GET)
        context['title'] = 'Nuevo Administrador'
        context['action_button'] = 'Agregar Nuevo Administrador'
        return context

class AdministratorDelete(DeleteView):
    model = Profile
    template_name = 'administracion/specific/Admins/delete.html'
    success_url = reverse_lazy('administracion:administradores')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        user = User.objects.get(pk=self.object.user.id)
        self.object.delete()
        user.delete()
        actualizar_datos()
        actualizar_precios()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar administrador'
        return context

class AdministratorUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('administracion:administradores')
    template_name = 'administracion/specific/Admins/update.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        actualizar_datos()
        actualizar_precios()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Sueldo'
        context['action_button'] = 'Guardar Cambios'
        return context
