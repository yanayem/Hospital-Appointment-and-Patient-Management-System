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

        # 🔁 AUTO SWITCH doctor → patient for booking
        if path.startswith("/patients/book-appointment/"):
            if original_role == "doctor" and current_role != "patient":
                request.session["current_role"] = "patient"
                request.session["user_type"] = "patient"

        # 🚫 Patient accessing doctor area
        if path.startswith("/doctors/") and request.session.get("current_role") != "doctor":
            return redirect("patient_dashboard")

        return self.get_response(request)
