from blacklist import models


def is_ip_blacklisted(ip):
    """
    Checks if ip is in IPEntry model.
    """
    print(ip)
    if models.IPEntry.objects.filter(entry_value__iexact=ip):
        return True
    return False


def is_email_blacklisted(email):
    """
    Checks if email is in EmailEntry model or host is in HostEntry model.
    """

    if models.EmailEntry.objects.filter(entry_value__iexact=email):
        return True
    host = email.split("@")[1]
    return is_email_host_blacklisted(host)


def is_email_host_blacklisted(host):
    """
    Checks if email host is in EmailHostEntry model.
    """

    if models.EmailHostEntry.objects.filter(entry_value__iexact=host):
        return True
    return False
