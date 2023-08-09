
from django.contrib import admin
from django.urls import path, reverse
from Hub import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginView.as_view(), name= 'login'),
    path('printer/', views.PrinterList.as_view(), name= 'printer_list'),
    path('addPrinter/', views.AddPrinter.as_view(), name= 'add_printer'),
    path('project/', views.ProjectListView.as_view(), name= 'project'),
    path('addProject/', views.AddProject.as_view(), name= 'add_project'),
    path('filament/', views.FilamentList.as_view(), name= 'filament'),
    path('addFilament/', views.AddFilament.as_view(), name= 'add_filament'),
    path('parts/', views.PartsList.as_view(), name='parts'),
    path('addParts/', views.AddParts.as_view(), name='add_parts'),
    path('delete_filament/<int:filament_id>/', views.DeleteFilament.as_view(), name='delete_filament'),
    path('edit_filament/<int:filament_id>/', views.EditFilament.as_view(), name='edit_filament'),
    path('delete_printer/<int:printer_id>/', views.DeletePrinter.as_view(), name='delete_printer'),
    path('edit_printer/<int:printer_id>/', views.EditPrinter.as_view(), name='edit_printer'),
    path('delete_part/<int:part_id>/', views.DeletePart.as_view(), name='delete_part'),
    path('printer_detail/<int:printer_id>/', views.PrinterDetail.as_view(), name='printer_detail'),
    path('printing/', views.PrintingView.as_view(), name= 'printing_list'),
    path('move_up/<int:item_id>/', views.MoveProjectUpView.as_view(), name='move_up'),
    path('move_down/<int:item_id>/', views.MoveProjectDownView.as_view(), name='move_down'),
    path('delete_project/<int:project_id>/', views.DeleteProject.as_view(), name='delete_project'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('remove_from_queue/<int:project_id>/', views.RemoveFromPrintingQueueView.as_view(), name='remove_from_queue'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)