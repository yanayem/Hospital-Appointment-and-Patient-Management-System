from accounts.models import UserProfile

def doctor_context(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return {}
    try:
        doctor = UserProfile.objects.get(id=user_id, user_type="doctor")
        return {"doctor": doctor}
    except UserProfile.DoesNotExist:
        return {}
