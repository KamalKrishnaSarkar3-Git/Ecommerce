def cart_count(request):
    if request.user.is_authenticated:
        try:
            return {'cart_count': request.user.cart.total_items()}
        except Exception:
            return {'cart_count': 0}
    return {'cart_count': 0}