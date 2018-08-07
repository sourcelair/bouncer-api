from django.test import TestCase
from blacklist import models
from django.db.utils import IntegrityError
from rest_framework.response import Response
from hashlib import sha256
from blacklist.brain import (
    is_ip_blacklisted,
    is_email_blacklisted,
    is_email_host_blacklisted,
    is_email_hash_blacklisted,
)


class BaseTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lower_case_blacklisted_ip = "2001:0:3238:dfe1:63::fefb"
        cls.not_blacklisted_ip = "255.254.253.251"
        cls.lower_case_blacklisted_email = "a@spam.com"
        cls.not_blacklisted_email = "a@test.com"
        cls.lower_case_blacklisted_host = "spam.com"
        cls.not_blacklisted_host = "test.com"
        cls.upper_case_blacklisted_email = "B@SPAM.COM"

        ip_entry = models.IPEntry(entry_value=cls.lower_case_blacklisted_ip)
        ip_entry.save()
        email_entry = models.EmailEntry(entry_value=cls.lower_case_blacklisted_email)
        email_entry.save()
        host_entry = models.EmailHostEntry(entry_value=cls.lower_case_blacklisted_host)
        host_entry.save()
        upper_case_email_entry = models.EmailEntry(
            entry_value=cls.upper_case_blacklisted_email
        )
        upper_case_email_entry.save()

    class Meta:
        abstract = True


class BrainTests(BaseTests):
    def test_is_ip_blacklisted_with_lower_case_blacklisted_ip_and_lower_case_query(
        self
    ):
        """
        Test that checking a blacklisted ip correctly returns True.
        """

        self.assertTrue(is_ip_blacklisted(self.lower_case_blacklisted_ip))

    def test_is_ip_blacklisted_with_lower_case_blacklisted_ip_and_upper_case_query(
        self
    ):
        """
        Test that checking a blacklisted ip correctly returns True,
        even if the query is in upper-case and the ip is saved with lower case
        in our database.
        """

        self.assertTrue(is_ip_blacklisted(self.lower_case_blacklisted_ip.upper()))

    def test_is_ip_blacklisted_with_not_blacklisted_ip(self):
        """
        Test that checking a non blacklisted ip correctly returns False.
        """

        self.assertFalse(is_ip_blacklisted(self.not_blacklisted_ip))

    def test_is_email_blacklisted_with_lower_case_blacklisted_email_and_lower_case_query(
        self
    ):
        """
        Test that checking a blacklisted email correctly returns True.
        """

        self.assertTrue(is_email_blacklisted(self.lower_case_blacklisted_email))

    def test_is_email_blacklisted_with_lower_case_blacklisted_email_and_upper_case_query(
        self
    ):
        """
        Test that checking a blacklisted email correctly returns True,
        even if the query is in upper-case and the email is saved with lower case
        in our database.
        """

        self.assertTrue(is_email_blacklisted(self.lower_case_blacklisted_email.upper()))

    def test_is_email_blacklisted_with_not_blacklisted_email(self):
        """
        Test that checking a non blacklisted email correctly returns False.
        """

        self.assertFalse(is_email_blacklisted(self.not_blacklisted_email))

    def test_is_email_blacklisted_with_lower_case_blacklisted_host_and_lower_case_query(
        self
    ):
        """
        Test that checking a blacklisted email correctly returns True,
        even if only the email host is in our database.
        """

        self.assertTrue(is_email_blacklisted(f"a@{self.lower_case_blacklisted_host}"))

    def test_is_email_blacklisted_with_lower_case_blacklisted_host_and_upper_case_query(
        self
    ):
        """
        Test that checking a blacklisted email correctly returns True,
        even if the query is in upper-case and only the email host is saved
        with lower case in our database.
        """

        self.assertTrue(
            is_email_blacklisted(f"a@{self.lower_case_blacklisted_host.upper()}")
        )

    def test_is_email_blacklisted_with_not_blacklisted_host(self):
        """
        Test that checking a non blacklisted email correctly returns False.
        """

        self.assertFalse(is_email_blacklisted(f"a@{self.not_blacklisted_host}"))

    def test_is_email_host_blacklisted_with_lower_case_blacklisted_host_and_lower_case_query(
        self
    ):
        """
        Test that checking a blacklisted email host correctly returns True.
        """

        self.assertTrue(is_email_host_blacklisted(self.lower_case_blacklisted_host))

    def test_is_email_host_blacklisted_with_lower_case_blacklisted_host_and_upper_case_query(
        self
    ):
        """
        Test that checking a blacklisted email host correctly returns True,
        even if the query is in upper-case and the email host is saved with lower case
        in our database.
        """

        self.assertTrue(
            is_email_host_blacklisted(self.lower_case_blacklisted_host.upper())
        )

    def test_is_email_host_blacklisted_with_not_blacklisted_host(self):
        """
        Test that checking a non blacklisted email host correctly returns False.
        """

        self.assertFalse(is_email_host_blacklisted(self.not_blacklisted_host))

    def test_is_email_hash_blacklisted_with_blacklisted_hash(self):
        """
        Test that checking a blacklisted email hash correctly returns True.
        """

        hashed_email = sha256(self.lower_case_blacklisted_email.encode())
        self.assertTrue(is_email_hash_blacklisted(hashed_email.hexdigest()))

    def test_is_email_hash_blacklisted_with_upper_case_blacklisted_hash(self):
        """
        Test that checking a blacklisted email hash correctly returns True,
        even if the query is in upper-case and the email hash is saved with lower case
        in our database.
        """

        hashed_email = sha256(self.lower_case_blacklisted_email.encode())
        self.assertTrue(is_email_hash_blacklisted(hashed_email.hexdigest().upper()))

    def test_is_email_hash_blacklisted_with_not_blacklisted_hash(self):
        """
        Test that checking a non blacklisted email hash correctly returns False.
        """

        hashed_email = sha256(self.not_blacklisted_email.encode())
        self.assertFalse(is_email_hash_blacklisted(hashed_email.hexdigest()))


class ModelTests(BaseTests):
    def test_add_existing_ip_in_database(self):
        """
        Test that checking if correctly we cannot add an existing ip in our database.
        """
        new_ip_entry = models.IPEntry(entry_value=self.lower_case_blacklisted_ip)
        self.assertRaises(IntegrityError, lambda: new_ip_entry.save())

    def test_add_existing_ip_in_database_in_different_case(self):
        """
        Test that checking if correctly we cannot add an existing ip in our database,
        even if it has different case.
        """
        new_ip_entry = models.IPEntry(
            entry_value=self.lower_case_blacklisted_ip.upper()
        )
        self.assertRaises(IntegrityError, lambda: new_ip_entry.save())

    def test_add_existing_email_in_database(self):
        """
        Test that checking if correctly we cannot add an existing email in our database.
        """
        new_email_entry = models.EmailEntry(
            entry_value=self.lower_case_blacklisted_email
        )
        self.assertRaises(IntegrityError, lambda: new_email_entry.save())

    def test_add_existing_email_in_database_in_different_case(self):
        """
        Test that checking if correctly we cannot add an existing email in our database,
        even if it has different case.
        """
        new_email_entry = models.EmailEntry(
            entry_value=self.lower_case_blacklisted_email.upper()
        )
        self.assertRaises(IntegrityError, lambda: new_email_entry.save())

    def test_add_existing_email_host_in_database(self):
        """
        Test that checking if correctly we cannot add an existing email host in our database.
        """
        new_email_host_entry = models.EmailHostEntry(
            entry_value=self.lower_case_blacklisted_host
        )
        self.assertRaises(IntegrityError, lambda: new_email_host_entry.save())

    def test_add_existing_email_host_in_database_in_different_case(self):
        """
        Test that checking if correctly we cannot add an existing email host in our database,
        even if it has different case.
        """
        new_email_host_entry = models.EmailHostEntry(
            entry_value=self.lower_case_blacklisted_host.upper()
        )
        self.assertRaises(IntegrityError, lambda: new_email_host_entry.save())

    def test_email_entry_get_sha256_hash(self):
        """
        Test that checking if an email entry gets a known SHA256 hash after it is saved.
        """
        hashed_email = (
            "ecc15d6405217971226928ec750577080d259357e2d1399af9d81e1ecd368fda"
        )
        self.assertEqual(
            hashed_value,
            models.EmailEntry.objects.get(
                entry_value=self.lower_case_blacklisted_email
            ).hashed_value,
        )

    def test_email_entry_get_sha256_hash(self):
        """
        Test that checking if an email entry gets a known SHA256 hash after it is saved.
        """
        hashed_email = (
            "aa1bcdf211f4e1fc293095588042c1c7906d07de204143ba95797a270e469d97"
        )
        self.assertEqual(
            hashed_email,
            models.EmailEntry.objects.get(
                entry_value=self.upper_case_blacklisted_email
            ).hashed_value,
        )


class RequestViewTests(BaseTests):
    def test_blacklisted_ip(self):
        """
        Test that checking a blacklisted ip correctly returns True.
        """

        correct_response = [
            {"kind": "ip", "value": self.lower_case_blacklisted_ip, "result": True}
        ]
        response = self.client.get(
            "/blacklist/", {"ip": self.lower_case_blacklisted_ip}
        )
        self.assertEqual(response.data, correct_response)

    def test_non_blacklisted_ip(self):
        """
        Test that checking a non blacklisted ip correctly returns False.
        """
        correct_response = [
            {"kind": "ip", "value": self.not_blacklisted_ip, "result": False}
        ]
        response = self.client.get("/blacklist/", {"ip": self.not_blacklisted_ip})
        self.assertEqual(response.data, correct_response)

    def test_blacklisted_email(self):
        """
        Test that checking a blacklisted email correctly returns True.
        """
        correct_response = [
            {
                "kind": "email",
                "value": self.lower_case_blacklisted_email,
                "result": True,
            }
        ]
        response = self.client.get(
            "/blacklist/", {"email": self.lower_case_blacklisted_email}
        )
        self.assertEqual(response.data, correct_response)

    def test_non_blacklisted_email(self):
        """
        Test that checking a non blacklisted email correctly returns False.
        """
        correct_response = [
            {"kind": "email", "value": self.not_blacklisted_email, "result": False}
        ]
        response = self.client.get("/blacklist/", {"email": self.not_blacklisted_email})
        self.assertEqual(response.data, correct_response)

    def test_blacklisted_email_host(self):
        """
        Test that checking a blacklisted email host correctly returns True.
        """
        correct_response = [
            {
                "kind": "email_host",
                "value": self.lower_case_blacklisted_host,
                "result": True,
            }
        ]
        response = self.client.get(
            "/blacklist/", {"email_host": self.lower_case_blacklisted_host}
        )
        self.assertEqual(response.data, correct_response)

    def test_non_blacklisted_email_host(self):
        """
        Test that checking a non blacklisted email host correctly returns False.
        """
        correct_response = [
            {"kind": "email_host", "value": self.not_blacklisted_host, "result": False}
        ]
        response = self.client.get(
            "/blacklist/", {"email_host": self.not_blacklisted_host}
        )
        self.assertEqual(response.data, correct_response)

    def test_two_ips_queries(self):
        """
        Test that checking two ip queries return correctly.
        """
        correct_response = [
            {"kind": "ip", "value": self.lower_case_blacklisted_ip, "result": True},
            {"kind": "ip", "value": self.not_blacklisted_ip, "result": False},
        ]
        response = self.client.get(
            "/blacklist/",
            {"ip": [self.lower_case_blacklisted_ip, self.not_blacklisted_ip]},
        )
        self.assertEqual(response.data, correct_response)

    def test_two_emails_queries(self):
        """
        Test that checking two email queries return correctly.
        """
        correct_response = [
            {
                "kind": "email",
                "value": self.lower_case_blacklisted_email,
                "result": True,
            },
            {"kind": "email", "value": self.not_blacklisted_email, "result": False},
        ]
        response = self.client.get(
            "/blacklist/",
            {"email": [self.lower_case_blacklisted_email, self.not_blacklisted_email]},
        )
        self.assertEqual(response.data, correct_response)

    def test_two_email_hosts_queries(self):
        """
        Test that checking two email host queries return correctly.
        """
        correct_response = [
            {
                "kind": "email_host",
                "value": self.lower_case_blacklisted_host,
                "result": True,
            },
            {"kind": "email_host", "value": self.not_blacklisted_host, "result": False},
        ]
        response = self.client.get(
            "/blacklist/",
            {
                "email_host": [
                    self.lower_case_blacklisted_host,
                    self.not_blacklisted_host,
                ]
            },
        )
        self.assertEqual(response.data, correct_response)
