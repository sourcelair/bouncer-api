from blacklist import models


def is_ip_blacklisted(ip):
    """
    Checks if ip is in IPEntry model.
    """

    return models.IPEntry.objects.filter(lower_case_entry_value=ip.lower()).exists()


def is_email_blacklisted(email):
    """
    Checks if email is in EmailEntry model or host is in EmailHostEntry model.
    """

    if models.EmailEntry.objects.filter(lower_case_entry_value=email.lower()).exists():
        return True
    host = email.split("@")[1]
    return is_email_host_blacklisted(host)


def is_email_host_blacklisted(host):
    """
    Checks if email host is in EmailHostEntry model.
    """

    return models.EmailHostEntry.objects.filter(
        lower_case_entry_value=host.lower()
    ).exists()


def is_email_hash_blacklisted(email_hash):
    """
    Checks if email hashed value is in EmailEntry model
    """

    return models.EmailEntry.objects.filter(hashed_value=email_hash.lower()).exists()
