from .models import IPEntry

def is_ip_blacklisted(ip):
	if IPEntry.objects.filter(entry_value=ip):
		return True
	return False