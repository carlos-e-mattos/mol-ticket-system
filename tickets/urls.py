from django.urls import path

from . import views

urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('tickets/novo/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/editar/', views.TicketUpdateView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/excluir/', views.TicketDeleteView.as_view(), name='ticket-delete'),
]
