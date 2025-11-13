def get_client_ip(request):
    # If using reverse proxy/load balancer (e.g., Nginx, Cloudflare)
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Could contain multiple IPs, take the first one
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        # Fallback to remote address
        ip = request.META.get("REMOTE_ADDR")
    return ip