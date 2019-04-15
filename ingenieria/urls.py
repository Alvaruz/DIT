from django.urls import path
from django.contrib.auth import views as auth_views
from ingenieria.views import *
from . import views
#  DocumentoListView.as_view()

urlpatterns = [
    path('index/', views.index, name='index'),
    path('panel/', views.panel, name='panel'),

    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='login.html'), name='logout'),

    path('documento/listar/', DocumentoListView.as_view(),
         name='documento_list'),
    path('documento/nuevo/', DocumentoAddView.as_view(),
         name='documento_add'),
    path('documento/editar/<int:pk>/', DocumentoEditView.as_view(),
         name='documento_edit'),
    path('documento/eliminar/<int:pk>/', DocumentoDeleteView.as_view(),
         name='documento_delete'),

    path('informe/listar/', InformeListView.as_view(),
         name='informe_list'),
    path('informe/nuevo/', InformeAddView.as_view(),
         name='informe_add'),
    path('informe/editar/<int:pk>/', InformeEditView.as_view(),
         name='informe_edit'),
    path('informe/eliminar/<int:pk>/', InformeDeleteView.as_view(),
         name='informe_delete'),

    path('graficas/', views.graficas, name='graficas'),
    path('tablas/', views.tablas, name='tablas'),
    path('espacios_reservados/', views.tabla_espacios, name='tabla_espacios'),
    path('calles/', views.tabla_calles, name='tabla_calles'),
    path('recurrentes/', views.tabla_recurrentes, name='tabla_recurrentes'),
    path('GIS/', views.gis, name='gis'),

    path('sin_privilegios/', HomeSinPrivilegios.as_view(), name='sin_privilegios'),
]


#  Add Django site authentication urls (for login, logout, password management)
# urlpatterns += [
#     path('cuentas/', include('django.contrib.auth.urls')),
# ]


# urlpatterns += [

# ]