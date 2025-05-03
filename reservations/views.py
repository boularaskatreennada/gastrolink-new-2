from django.shortcuts import render
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from reservations.forms import ReservationForm 
from restaurant.decorators import waiter_required
from restaurant.models import Server
from .models import Reservation,Table # ReservationStatus, 
from django.db.models import Q
from datetime import datetime, time

@waiter_required
def reserved_tables(request):
    server = get_object_or_404(Server, user=request.user)
    restaurant = server.restaurant

    reservations = Reservation.objects.filter(table__restaurant=restaurant)

    # Get filters from GET
    filter_date = request.GET.get('filterDate')
    filter_time = request.GET.get('filterTime')
    filter_status = request.GET.get('filterStatus')
    filter_table = request.GET.get('filterTable')
    search = request.GET.get('search')
    clear = request.GET.get('clear')

    if clear:
        # Redirect to clear filters
        return redirect('reservedTables')  

    if filter_date:
        try:
            date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            reservations = reservations.filter(datetime__date=date_obj)
        except ValueError:
            pass  

    if filter_time:
        
        if filter_time == 'Lunch':
            reservations = reservations.filter(datetime__time__gte=time(11, 0), datetime__time__lt=time(15, 0))
        elif filter_time == 'Dinner':
            reservations = reservations.filter(datetime__time__gte=time(17, 0), datetime__time__lt=time(22, 0))

    if filter_status:
        reservations = reservations.filter(status__iexact=filter_status)

    if filter_table:
        try:
            table_num = int(filter_table)
            reservations = reservations.filter(table__id=table_num)
        except ValueError:
            pass

    if search:
        reservations = reservations.filter(
            Q(client__name__icontains=search) |
            Q(table__id__icontains=search)
        )

    return render(request, 'waiter/reservedTables.html', {
        'reservations': reservations,
        'restaurant': restaurant,
    })

@waiter_required
def update_reservation(request, pk):
    
     #  Identify waiter → his restaurant
    serveur     = get_object_or_404(Server, user=request.user)
    restaurant  = serveur.restaurant

    # Fetch the reservation, only if it belongs to this restaurant
    reservation = get_object_or_404(
        Reservation, 
        pk=pk,
        table__restaurant=restaurant
    )

    # Limit the table choices to this restaurant
    tables_qs = Table.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        # Bind form to POST + instance
        form = ReservationForm(request.POST, instance=reservation)
        #  Override the queryset for the table field
        form.fields['table'].queryset = tables_qs

        if form.is_valid():
            form.save()
            messages.success(request, "Réservation mise à jour avec succès.")
            return redirect('reservations:list')
    else:
        #  On GET, show a form pre-filled with existing data
        form = ReservationForm(instance=reservation)
        form.fields['table'].queryset = tables_qs

    return render(request, 'waiter/editReservation.html', {
        'form': form,
        'reservation': reservation,
        'restaurant': restaurant,
    })
    
@waiter_required
def update_status(request, pk):
    reservation =Reservation.objects.get(Reservation, id=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(ReservationStatus.choices):
            reservation.status = new_status
            reservation.save()
    return redirect('reservedTables')

@waiter_required
def cancel_reservation(request,pk):
    server = get_object_or_404(Server, user=request.user)
    reservation = get_object_or_404(
        Reservation,
        id=pk,
        table__restaurant=server.restaurant
    )
    
    if request.method == 'POST':
        reservation.status = Reservation.Status.CANCELLED
        reservation.save()
    
    return redirect('reserved_tables')
