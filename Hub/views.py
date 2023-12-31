from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import FilamentForm, PrinterForm, PartsForm, AddProjectForm, RegisterForm
from .models import Filament, Printer, Parts, Project, PrintingQue
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):

    def get(self, request):
        return render(request, 'base.html')


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
        return render(request, 'register.html', {'form':form})

class LoginView(View):
    def get(self, request):
        return render(request, 'base.html', {'page': 'login'})

    def post(self, request):
        login_value = request.POST['login']
        password = request.POST['password']

        user = authenticate(request, username=login_value, password=password)

        if user is not None:
            # Użytkownik poprawnie uwierzytelniony, możesz zalogować
            login(request, user)
            return redirect('printer_list')
        else:
            error_message = "Niepoprawny login lub hasło"

        return render(request, 'base.html', {'page': 'login', 'error_message': error_message})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class PrinterList(View):

    def get(self, request):
        printers = Printer.objects.all()
        return render(request, 'printer_list.html', {'printers': printers})

class AddPrinter(View):

    def get(self, request):
        form = PrinterForm()
        return render(request, 'add_printer.html', {'form': form})

    def post(self, request):
        form = PrinterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('printer_list')
        return render(request, 'add_printer.html', {'form': form})


class DeletePrinter(View):
    def post(self, request, printer_id):
        printer = Printer.objects.get(id=printer_id)
        printer.delete()
        return redirect('printer_list')

class PrinterDetail(View):
    def get(self, request, printer_id):
        printer = get_object_or_404(Printer, id=printer_id)
        return render(request, 'printer_detail.html', {'printer': printer})

class EditPrinter(View):

    def get(self, request, printer_id):
        printer = get_object_or_404(Printer, id=printer_id)
        form = PrinterForm(instance=printer)
        return render(request, 'edit_printer.html', {'form': form, 'printer': printer})

    def post(self, request, printer_id):
        printer = get_object_or_404(Printer, id=printer_id)
        form = PrinterForm(request.POST, instance=printer)
        if form.is_valid():
            form.save()
            return redirect('printer_list')
        return render(request, 'edit_printer.html', {'form': form, 'printer': printer})


class ProjectListView(View):

    def get(self, request):
        projects = Project.objects.all()
        return render(request, 'project_list.html', {'projects': projects})


    def post(self, request):
        print("Próba dodania projektu do kolejki")
        project_id = request.POST.get('project_id')
        print("ID projektu:", project_id)

        try:
            project = Project.objects.get(id=project_id)
            order = PrintingQue.objects.count() + 1
            printing_que = PrintingQue(project=project, order=order, user=request.user)
            printing_que.save()
            print("Projekt dodany do kolejki")
            print(request.user)
        except Project.DoesNotExist:
            print("Projekt o podanym ID nie istnieje")

        return redirect('project')



class AddProject(LoginRequiredMixin, View):

    def get(self, request):
        form = AddProjectForm()
        filaments = Filament.objects.all()
        return render(request, 'add_project.html', {'form': form, 'filaments': filaments})


    def post(self, request):
        form = AddProjectForm(request.POST, request.FILES)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.user = request.user  # Przypisanie zalogowanego użytkownika
            new_project.save()
            return redirect('project')
        return render(request, 'add_project.html', {'form': form})

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "Dodawanie projektów dostępne tylko dla zalogowanych użytkowników.")
            return redirect('login')
        return super().dispatch(*args, **kwargs)


class DeleteProject(View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return redirect('project')

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return redirect('project')


class FilamentList(View):
    def get(self, request):
        search_name = request.GET.get('search_name', '')
        search_producer = request.GET.get('search_producer', '')
        search_material = request.GET.get('search_material', '')
        search_colour = request.GET.get('search_colour', '')
        search_weight = request.GET.get('search_weight', '')


        filaments = Filament.objects.filter(
            name__icontains=search_name,
            producer__icontains=search_producer,
            material__icontains=search_material,
            colour__icontains=search_colour,
            weight__icontains=search_weight
        )

        return render(request, 'filament_list.html', {'filaments': filaments})

class AddFilament(View):
    def get(self, request):
        form = FilamentForm()
        return render(request, 'add_filament.html', {'form': form})

    def post(self, request):
        form = FilamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('filament')
        return render(request, 'add_filament.html', {'form': form})

class PartsList(View):
    def get(self, request):
        parts = Parts.objects.all()
        return render(request, 'parts.html', {'parts': parts})


class AddParts(View):
    def get(self, request):
        form = PartsForm()
        printers = Printer.objects.all()
        return render(request, 'add_parts.html', {'form': form, 'printers': printers})

    def post(self, request):
        form = PartsForm(request.POST)
        if form.is_valid():
            part = form.save()
            selected_printers = form.cleaned_data.get('printers')
            if selected_printers:
                part.printers.set(selected_printers)
            return redirect('parts')
        return render(request, 'add_parts.html', {'form': form})

class DeletePart(View):
    def post(self, request, part_id):
        part = get_object_or_404(Parts, id=part_id)
        part.delete()
        return redirect('parts')

class DeleteFilament(View):
    def post(self, request, filament_id):
        filament = Filament.objects.get(id=filament_id)
        filament.delete()
        return redirect('filament')

class EditFilament(View):
    def get(self, request, filament_id):
        filament = get_object_or_404(Filament, id=filament_id)
        form = FilamentForm(instance=filament)
        return render(request, 'edit_filament.html', {'form': form, 'filament': filament})

    def post(self, request, filament_id):
        filament = get_object_or_404(Filament, id=filament_id)
        form = FilamentForm(request.POST, instance=filament)
        if form.is_valid():
            form.save()
            return redirect('filament')
        return render(request, 'edit_filament.html', {'form': form, 'filament': filament})


class PrintingView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        printing_list = PrintingQue.objects.filter(user=user)
        return render(request, 'printing_list.html', {'printing_list': printing_list})

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "Kolejka Wydruków dostępna jest tylko dla zalogowanych użytkowników.")
            return redirect('login')
        return super().dispatch(*args, **kwargs)


class MoveProjectUpView(View):
    def post(self, request, item_id):
        item = get_object_or_404(PrintingQue, id=item_id)

        if item.order > 1:
            prev_items = PrintingQue.objects.filter(order=item.order - 1)

            if prev_items.exists():
                prev_item = prev_items.first()

                current_order = item.order
                item.order = prev_item.order
                prev_item.order = current_order

                item.save()
                prev_item.save()

        return redirect('printing_list')


class MoveProjectDownView(View):
    def post(self, request, item_id):
        item = get_object_or_404(PrintingQue, id=item_id)

        if item.order < PrintingQue.objects.count():
            next_items = PrintingQue.objects.filter(order=item.order + 1)

            if next_items.exists():
                next_item = next_items.first()

                current_order = item.order
                item.order = next_item.order
                next_item.order = current_order

                item.save()
                next_item.save()

        return redirect('printing_list')


class RemoveFromPrintingQueueView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        try:
            printing_que = PrintingQue.objects.filter(project=project, user=request.user).order_by('order').first()
            if printing_que:
                printing_que.delete()
                print("Projekt usunięty z kolejki wydruków")
            else:
                print("Projekt nie istnieje w kolejce wydruków")
        except PrintingQue.DoesNotExist:
            print("Projekt nie istnieje w kolejce wydruków")

        return redirect('printing_list')