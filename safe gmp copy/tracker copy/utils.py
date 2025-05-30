from .models import Badge

def award_brave_start_badge(user):
    if not Badge.objects.filter(user=user, name="Brave Start").exists():
        Badge.objects.create(
            user=user,
            name="Brave Start",
            description="Awarded for starting your digital detox journey!"
        )
