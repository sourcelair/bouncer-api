from django.test import TestCase
from .models import IPEntry
from .brain import *


class BrainTests(TestCase):
    def test_is_ip_blacklisted_with_blacklisted_ip(self):
        """is_ip_blacklisted() returns True for ips which are in IPEntry model."""

        blacklisted_ip = "1.2.3.4"
        ip_entry = IPEntry(entry_value=blacklisted_ip)
        self.assertIs(is_ip_blacklisted(blacklisted_ip), True)

    def test_is_ip_blacklisted_with_blacklisted_ip(self):
        """is_ip_blacklisted() returns False for ips which are not in IPEntry model."""

        not_blacklisted_ip = "1.2.3.4"
        self.assertIs(is_ip_blacklisted(not_blacklisted_ip), False)
