#Hello world jr82 
#Byjr082to views
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.utils import timezone
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import DetoxSession, Badge, UserBadge, UserProfile, DailyCheckIn, User
from .forms import CustomUserCreationForm
from django.contrib import messages
from datetime import date, timedelta
from .utils import award_brave_start_badge
from .forms import ProductiveNoteForm
from .models import ProductiveNote
print("Testing stash flow")


class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  
        return response



def home(request):
    return render(request, 'home.html')

def dashboard(request):

    quotes = [
        ("“The only way to do great work is to love what you do.”", " By Steve Jobs"),
        ("“Success is not final, failure is not fatal: It is the courage to continue that counts.”", "Winston Churchill"),
        ("“The future depends on what we do in the present.”", "Mahatma Gandhi"),
        ("“It does not matter how slowly you go as long as you do not stop.”", "Confucius"),
        ("“Believe you can and you're halfway there.”", "Theodore Roosevelt"),
        ("“You are never too old to set another goal or to dream a new dream.”", "C.S. Lewis")
    ]
    
  
    quote, author = random.choice(quotes)
    
    return render(request, 'tracker/dashboard.html', {'quote': quote, 'author': author})

@login_required
def dashboard(request):
    profile = request.user.userprofile
    today = timezone.now().date()
    today_checkin, _ = DailyCheckIn.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'checked_in': False}
    )

    active_session = DetoxSession.objects.filter(user=request.user, end_time__isnull=True).first()
    badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    notes = ProductiveNote.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        if 'check_in' in request.POST and not today_checkin.checked_in:
            today_checkin.checked_in = True
            today_checkin.save()
            profile.update_streak()

        if 'note_submit' in request.POST:
            form = ProductiveNoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.user = request.user
                note.save()
                return redirect('dashboard')
    else:
        form = ProductiveNoteForm()

    context = {
        'profile': profile,
        'today_checkin': today_checkin,
        'active_session': active_session,
        'badges': badges,
        'form': form,
        'notes': notes,
        'total_detox_time': profile.total_detox_time,
        'current_streak': profile.current_streak,
        'longest_streak': profile.longest_streak,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def dashboard(request):
    profile = request.user.userprofile
    notes = ProductiveNote.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ProductiveNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('dashboard')  
    else:
        form = ProductiveNoteForm()

    return render(request, 'dashboard.html', {
        'profile': profile,
        'total_detox_time': profile.total_detox_time,
        'form': form,
        'notes': notes,
    })


@login_required
def start_session(request):
    if request.method == 'POST':
        # Check for existing active session
        if not DetoxSession.objects.filter(user=request.user, is_active=True).exists():
            session = DetoxSession.objects.create(user=request.user)
            award_brave_start_badge(request.user)
            messages.success(request, "Ghost session started! 👻")
        else:
            messages.warning(request, "You already have an active session")
        return redirect('dashboard')

@login_required
def end_session(request):
    if request.method == 'POST':
        session = DetoxSession.objects.filter(user=request.user, is_active=True).first()
        
        if session:
            session.end_time = timezone.now()
            session.save()  # Triggers duration calc and detox time update
            
            minutes = int(session.duration or 0)
            messages.success(request, f"Great job! You detoxed for {minutes} minutes. 🎉")
        else:
            messages.error(request, "No active session found.")

        return redirect('dashboard')


@login_required
def check_in(request):
    if request.method == 'POST':
        today = timezone.now().date()
        checkin, _ = DailyCheckIn.objects.get_or_create(user=request.user, date=today)
        if not checkin.checked_in:
            checkin.checked_in = True
            checkin.save()


            profile = request.user.userprofile
            profile.update_streak()

            if profile.current_streak >= 3:
                badge, _ = Badge.objects.get_or_create(
                    name='3-Day Streak',
                    defaults={
                        'description': 'Completed a 3-day streak without Instagram!',
                        'image': 'badge-3day.png',
                        'criteria': '3_day_streak'
                    }
                )
                UserBadge.objects.get_or_create(user=request.user, badge=badge)

    return redirect('dashboard')



def award_badges(user):
    profile = user.userprofile
    badges = []


    if DetoxSession.objects.filter(user=user).count() == 1:
        badge, _ = Badge.objects.get_or_create(
            name='First Timer',
            defaults={
                'description': 'Completed first session',
                'icon': 'badge-first.png',
                'criteria': 'first_session'
            }
        )
        badges.append(badge)


    if profile.current_streak >= 3:
        badge, _ = Badge.objects.get_or_create(
            name='3-Day Streak',
            defaults={
                'description': '3 day streak',
                'icon': 'badge-3day.png',
                'criteria': '3_day_streak'
            }
        )
        badges.append(badge)

    for badge in badges:
        UserBadge.objects.get_or_create(user=user, badge=badge)


from django.utils import timezone
from .models import DailyCheckIn

@login_required
def mark_detox_day(request):
    user_profile = request.user.userprofile
    today = timezone.now().date()

    # Check if already checked in today
    if user_profile.last_checkin_date == today:
        messages.info(request, "Already checked in today!")
        return redirect('dashboard')

    # If yesterday was also checked in, increment streak
    yesterday = today - timedelta(days=1)
    if user_profile.last_checkin_date == yesterday:
        user_profile.current_streak += 1
    else:
        user_profile.current_streak = 1  # reset streak

    # Update longest streak if needed
    if user_profile.current_streak > user_profile.longest_streak:
        user_profile.longest_streak = user_profile.current_streak

    # Save last checkin date
    user_profile.last_checkin_date = today
    user_profile.save()

    messages.success(request, "Check-in successful! Keep going!")
    return redirect('dashboard')
