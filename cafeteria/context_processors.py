# cafeteria/context_processors.py
from .models import Order

def canteen_load(request):
    pending_orders = Order.objects.filter(status__in=["Pending", "Preparing"]).count()
    if pending_orders < 10:
        return {"load_label": "Low", "load_color": "#28a745"}
    elif pending_orders < 20:
        return {"load_label": "Moderate", "load_color": "#ff9800"}
    else:
        return {"load_label": "High", "load_color": "#dc3545"}