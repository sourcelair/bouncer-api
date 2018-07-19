from .models import IPEntry


def is_ip_blacklisted(ip):
    """Checks if ip is in IPEntry model."""

    if IPEntry.objects.filter(entry_value=ip):
        return True
    return False
