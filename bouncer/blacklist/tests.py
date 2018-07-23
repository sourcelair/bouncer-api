from django.test import TestCase
from blacklist import models
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
)


class BrainTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BrainTests, cls).setUpClass()
        cls.lower_case_blacklisted_ip = "2001:0:3238:dfe1:63::fefb"
        cls.upper_case_blacklisted_ip = "2001:0:3238:DFE1:63::FEFB"
        cls.not_blacklisted_ip = "255.254.253.251"
        cls.lower_case_blacklisted_email = "a@spam.com"
        cls.upper_case_blacklisted_email = "A@SPAM.COM"
        cls.not_blacklisted_email = "a@test.com"
        cls.lower_case_blacklisted_host = "spam.com"
        cls.upper_case_blacklisted_host = "SPAM.COM"
        cls.not_blacklisted_host = "test.com"

        ip_entry = models.IPEntry(entry_value=cls.lower_case_blacklisted_ip)
        ip_entry.save()
        email_entry = models.EmailEntry(entry_value=cls.lower_case_blacklisted_email)
        email_entry.save()
        host_entry = models.EmailHostEntry(entry_value=cls.lower_case_blacklisted_host)
        host_entry.save()

    def test_is_ip_blacklisted_with_lower_case_blacklisted_ip_and_lower_case_query(
        self
    ):
        """
        is_ip_blacklisted() returns True for ips which are in IPEntry model.
        """

        self.assertTrue(is_ip_blacklisted(self.lower_case_blacklisted_ip))

    def test_is_ip_blacklisted_with_lower_case_blacklisted_ip_and_upper_case_query(
        self
    ):
        """
        is_ip_blacklisted() returns True for ips which are in IPEntry model.
        """

        self.assertTrue(is_ip_blacklisted(self.upper_case_blacklisted_ip))

    def test_is_ip_blacklisted_with_not_blacklisted_ip(self):
        """
        is_ip_blacklisted() returns False for ips which are not in IPEntry model.
        """

        self.assertFalse(is_ip_blacklisted(self.not_blacklisted_ip))

    def test_is_email_blacklisted_with_lower_case_blacklisted_email_and_lower_case_query(
        self
    ):
        """
        is_email_blacklisted() returns True for emails which are in EmailEntry model.
        """

        self.assertTrue(is_email_blacklisted(self.lower_case_blacklisted_email))

    def test_is_email_blacklisted_with_lower_case_blacklisted_email_and_upper_case_query(
        self
    ):
        """
        is_email_blacklisted() returns True for emails which are in EmailEntry model.
        """

        self.assertTrue(is_email_blacklisted(self.upper_case_blacklisted_email))

    def test_is_email_blacklisted_with_not_blacklisted_email(self):
        """
        is_email_blacklisted() returns False for emails which are not in EmailEntry model.
        """

        self.assertFalse(is_email_blacklisted(self.not_blacklisted_email))

    def test_is_email_blacklisted_with_lower_case_blacklisted_host_and_lower_case_query(
        self
    ):
        """
        is_email_blacklisted() returns True for emails whose host is in
        EmailHostEntry model.
        """

        self.assertTrue(is_email_blacklisted(f"a@{self.lower_case_blacklisted_host}"))

    def test_is_email_blacklisted_with_lower_case_blacklisted_host_and_upper_case_query(
        self
    ):
        """
        is_email_blacklisted() returns True for emails whose host is in
        EmailHostEntry model.
        """

        self.assertTrue(is_email_blacklisted(f"a@{self.upper_case_blacklisted_host}"))

    def test_is_email_blacklisted_with_not_blacklisted_host(self):
        """
        is_email_blacklisted() returns False for emails whose host is not in
        EmailHostEntry model.
        """

        self.assertFalse(is_email_blacklisted(f"a@{self.not_blacklisted_host}"))

    def test_is_email_host_blacklisted_with_lower_case_blacklisted_host_and_lower_case_query(
        self
    ):
        """
        is_email_host_blacklisted() returns True for hosts which are in
        EmailHostEntry model.
        """

        self.assertTrue(is_email_host_blacklisted(self.lower_case_blacklisted_host))

    def test_is_email_host_blacklisted_with_lower_case_blacklisted_host_and_upper_case_query(
        self
    ):
        """
        is_email_host_blacklisted() returns True for hosts which are in
        EmailHostEntry model.
        """

        self.assertTrue(is_email_host_blacklisted(self.upper_case_blacklisted_host))

    def test_is_email_host_blacklisted_with_not_blacklisted_host(self):
        """
        is_email_host_blacklisted() returns False for hosts which are not in
        EmailHostEntry model.
        """

        self.assertFalse(is_email_host_blacklisted(self.not_blacklisted_host))
