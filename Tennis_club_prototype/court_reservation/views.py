from django.shortcuts import render, redirect
from .models import Court
from .forms import ReservationForm

# def reserve_court(request):
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.user = request.user  # Set the logged-in user
#             reservation.save()
#             return redirect('success_page')  # Redirect to a success page or another view
#     else:
#         form = ReservationForm()
    
#     courts = Court.objects.filter(available=True)  # Optionally filter available courts
#     return render(request, 'reserve_court.html', {'form': form, 'courts': courts})
