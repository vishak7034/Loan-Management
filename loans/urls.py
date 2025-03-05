from django.urls import path
from .views import RegisterView, LoginView, LoanListCreateView, LoanDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('loans/', LoanListCreateView.as_view(), name='loans'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<str:loan_id>/foreclose/', LoanForeclosureView.as_view(), name='loan_foreclose'),
]
