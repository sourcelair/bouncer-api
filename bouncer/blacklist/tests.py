from django.test import TestCase
from blacklist import models
from blacklist.brain import is_ip_blacklisted, is_email_blacklisted


class BrainTests(TestCase):
    def test_is_ip_blacklisted_with_blacklisted_ip(self):
        """
        is_ip_blacklisted() returns True for ips which are in IPEntry model.
        """

        blacklisted_ip = "1.2.3.4"
        ip_entry = models.IPEntry(entry_value=blacklisted_ip)
        ip_entry.save()
        self.assertIs(is_ip_blacklisted(blacklisted_ip), True)

    def test_is_ip_blacklisted_with_not_blacklisted_ip(self):
        """
        is_ip_blacklisted() returns False for ips which are not in IPEntry model.
        """

        not_blacklisted_ip = "1.2.3.4"
        self.assertIs(is_ip_blacklisted(not_blacklisted_ip), False)

    def test_is_email_blacklisted_with_blacklisted_email(self):
        """
        is_email_blacklisted() returns True for emails which are in EmailEntry model.
        """

        blacklisted_email = "a@spam.com"
        email_entry = models.EmailEntry(entry_value=blacklisted_email)
        email_entry.save()
        self.assertIs(is_email_blacklisted(blacklisted_email), True)

    def test_is_email_blacklisted_with_not_blacklisted_email(self):
        """
        is_email_blacklisted() returns False for emails which are not in EmailEntry model.
        """

        not_blacklisted_email = "a@test.com"
        self.assertIs(is_email_blacklisted(not_blacklisted_email), False)

    def test_is_email_blacklisted_with_blacklisted_host(self):
        """
        is_email_blacklisted() returns True for emails whose host is in
        EmailHostEntry model.
        """

        blacklisted_host = "spam.com"
        host_entry = models.EmailHostEntry(entry_value=blacklisted_host)
        host_entry.save()
        self.assertIs(is_email_blacklisted("a@" + blacklisted_host), True)

    def test_is_email_blacklisted_with_not_blacklisted_host(self):
        """
        is_email_blacklisted() returns False for emails whose host is not in
        EmailHostEntry model.
        """

        not_blacklisted_host = "test.com"
        self.assertIs(is_email_blacklisted("a@" + not_blacklisted_host), False)
