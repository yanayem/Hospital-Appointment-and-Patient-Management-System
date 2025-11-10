from accounts.models import UserProfile

def patient_context(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return {}
    try:
        patient = UserProfile.objects.get(id=user_id, user_type="patient")
        return {"patient": patient}
    except UserProfile.DoesNotExist:
        return {}
