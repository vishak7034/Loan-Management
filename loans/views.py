from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Loan, CustomUser
from .serializers import LoanSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Loan
from rest_framework.exceptions import NotFound
from django.db import transaction

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    def post(self, request):
        user = CustomUser.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoanForeclosureView(generics.GenericAPIView):
    def post(self, request, loan_id):
        # Fetch the loan based on loan_id
        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            raise NotFound("Loan not found")

        # Get amount paid and foreclosure discount from the request
        amount_paid = request.data.get('amount_paid')
        foreclosure_discount = request.data.get('foreclosure_discount', 0)

        if amount_paid is None or amount_paid <= 0:
            return Response({"message": "Amount paid must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the final settlement amount
        final_settlement_amount = amount_paid - foreclosure_discount

        # Ensure that the loan amount is fully settled
        if final_settlement_amount < loan.amount:
            return Response({"message": "Final settlement amount is less than the loan amount."}, status=status.HTTP_400_BAD_REQUEST)

        # Start a transaction to ensure data integrity
        with transaction.atomic():
            # Update loan details
            loan.amount = final_settlement_amount
            loan.status = "CLOSED"
            loan.save()

        # Return a successful response
        return Response({
            "message": "Loan foreclosed successfully.",
            "data": {
                "loan_id": loan.id,
                "amount_paid": amount_paid,
                "foreclosure_discount": foreclosure_discount,
                "final_settlement_amount": final_settlement_amount,
                "status": loan.status
            }
        })
