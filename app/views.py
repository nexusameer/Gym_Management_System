from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import *
from .forms  import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def service(request):
    plan = MembershipPlan.objects.all()
    context = {'plan': plan}
    return render(request, 'service.html', context)



def add_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_participant')  # Redirect to a view that lists participants
    else:
        form = ParticipantForm()

    return render(request, 'add_participant.html', {'form': form})

def list_participant(request):
    participants = Participant.objects.all()
    participant_data = []

    for participant in participants:
        try:
            membership_purchase = MembershipPurchase.objects.get(participant=participant)
            plan_info = f"{membership_purchase.membership_plan.mname} ({membership_purchase.start_date} to {membership_purchase.end_date})"
        except MembershipPurchase.DoesNotExist:
            plan_info = "No active plan"

        participant_data.append({'participant': participant, 'plan_info': plan_info})

    form = ParticipantListForm()
    context = {'participant_data': participant_data, 'form': form}
    return render(request, 'list_participant.html', context)




def membership_purchase_list(request):
    memberships = MembershipPurchase.objects.all()
    return render(request, 'membership_purchase_list.html', {'memberships': memberships})

def add_membership_purchase(request):
    if request.method == 'POST':
        form = MembershipPurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('membership_purchase_list')  # Redirect to the membership purchase list
    else:
        form = MembershipPurchaseForm()

    return render(request, 'add_membership_purchase.html', {'form': form})






def attendance_list(request):
    attendance_records = AttendanceRecord.objects.select_related('participant').order_by('date')
    return render(request, 'attendance_list.html', {'attendance_records': attendance_records})

def attendance_view(request):
    current_date = timezone.now().date()
    participants = Participant.objects.all()
    expired_membership = False

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            participant_name = form.cleaned_data['participant']
            arrival_time = form.cleaned_data['arrival_time']
            departure_time = form.cleaned_data['departure_time']

            try:
                participant = Participant.objects.get(pname=participant_name)
                attendance_record = AttendanceRecord.objects.create(
                    participant=participant,
                    arrival_time=arrival_time,
                    departure_time=departure_time,
                    date=current_date
                )
                attendance_record.save()
                messages.success(request, 'Attendance recorded successfully.')
            except Participant.DoesNotExist:
                messages.error(request, 'Invalid participant. Please select a valid participant.')
            except Exception as e:
                messages.error(request, f'An error occurred while saving the attendance: {str(e)}')
            return redirect('attendance_list')
        else:
            messages.error(request, 'Form is invalid. Please check the provided data.')
    else:
        form = AttendanceForm()

        # Here, make sure to retrieve the participant based on the circumstances
        participant = None  # You should handle the case where there's no participant

        # Check if the participant has an expired membership
        if participant and participant.membershippurchase.end_date and participant.membershippurchase.end_date < timezone.now().date():
            expired_membership = True

    context = {'form': form, 'current_date': current_date, 'participants': participants, 'expired_membership': expired_membership}
    return render(request, 'attendance.html', context)







