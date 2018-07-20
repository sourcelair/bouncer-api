from blacklist import models


def is_ip_blacklisted(ip):
    """
    Checks if ip is in IPEntry model.
    """

    if models.IPEntry.objects.filter(entry_value=ip):
        return True
    return False


def is_email_blacklisted(email):
    """
    Checks if email is in EmailEntry model host is in HostEntry model.
    """

    if models.EmailEntry.objects.filter(entry_value=email):
        return True
    host = email.split("@")[1]
    if models.EmailHostEntry.objects.filter(entry_value=host):
        return True
    return False
