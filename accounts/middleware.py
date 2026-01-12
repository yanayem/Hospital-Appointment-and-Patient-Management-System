from django.shortcuts import redirect

class RoleSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        user_id = request.session.get("user_id")
        current_role = request.session.get("current_role")
        original_role = request.session.get("user_type")

        if not user_id:
            return self.get_response(request)

        if not current_role:
            request.session["current_role"] = original_role
            current_role = original_role

        # Doctor acting as patient can access patient pages
        if path.startswith("/patients/") and current_role != "patient":
            return redirect("doctor_dashboard") if original_role == "doctor" else redirect("/")

        # Patient or doctor acting as patient cannot access doctor pages
        if path.startswith("/doctors/") and current_role != "doctor":
            return redirect("patient_dashboard")

        return self.get_response(request)
