from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, redirect
from eventos.forms import RegistroUsuarioForm, EventoForm
from eventos.models import Evento


class ListaEventosView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/lista_eventos.html'

    context_object_name = 'eventos'

    def get_queryset(self):
        if self.request.user.rol == 'admin':
            return Evento.objects.all()
        return Evento.objects.filter(estado=True)


class DetalleEventoView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'eventos/detalle_evento.html'
    context_object_name = 'evento'


class InscribirEventoView(View):
    def post(self, request, *args, **kwargs):
        evento = get_object_or_404(Evento, pk=kwargs['pk'])
        if request.user.is_authenticated:
            if request.user not in evento.inscritos.all() and evento.inscritos.count() < evento.cupos:
                evento.inscritos.add(request.user)
                messages.success(request, f'Se ha inscrito exitosamente en el evento {evento.nombre}.')
            else:
                messages.error(request,
                               'No se pudo realizar la inscripción. El evento puede estar lleno o ya estás inscrito.')
        else:
            messages.error(request, 'Debes iniciar sesión para inscribirte en este evento.')

        return redirect('detalle_evento', pk=evento.pk)

    def get(self, request, *args, **kwargs):
        # No se debería acceder a esta vista por GET, redirigir a detalle_evento
        evento = get_object_or_404(Evento, pk=kwargs['pk'])
        return redirect('detalle_evento', pk=evento.pk)


class CrearEventoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/eventos_form.html'
    success_url = reverse_lazy('lista_eventos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasar el usuario actual al formulario
        return kwargs
    def test_func(self):
        return self.request.user.rol == 'admin' or self.request.user.rol == 'normal'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'El evento se ha creado correctamente')
        return response


class MisEventosView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/lista_eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        return self.request.user.eventos_inscritos.all()


class CustomLoginView(LoginView):
    template_name = 'registro/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Sesión iniciada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos. Por favor, ingrese nuevamente.')
        return super().form_invalid(form)


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente.')
        response = redirect('login')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'registro/registro.html'
    success_url = reverse_lazy('lista_eventos')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Se ha registrado exitosamente.")
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class EliminarEventoView(View):
    def post(self, request, pk, *args, **kwargs):
        evento = get_object_or_404(Evento, pk=pk)
        if request.user.rol == 'admin':
            evento.delete()
            messages.success(request, 'El evento ha sido eliminado exitosamente.')
            return redirect('lista_eventos')
        return redirect('detalle_evento', pk=pk)

@login_required
def perfil(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Manejar cambio de contraseña
        password_form = PasswordChangeForm(user=user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión después del cambio de contraseña
            messages.success(request, 'Perfil y contraseña actualizados con éxito')
            return redirect('perfil')
        else:
            for field, errors in password_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'registro/perfil.html', {'password_form': password_form})