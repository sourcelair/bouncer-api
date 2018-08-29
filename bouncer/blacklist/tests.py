from django.test import TestCase
from blacklist import models
from django.db.utils import IntegrityError
from hashlib import sha256
from rest_framework.test import APIClient
from authentication.models import AuthToken
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
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

        unauthorized_user = User(username="unauthorized_user")
        unauthorized_user.save()
        unauthorized_token = AuthToken(user=unauthorized_user)
        unauthorized_token.save()
        authorized_user = User(username="authorized_user")
        authorized_user.save()
        content_type = ContentType.objects.get_for_model(models.IPEntry)
        view_ip_permission = Permission.objects.get(
            content_type=content_type, codename="view_ipentry"
        )
        add_ip_permission = Permission.objects.get(
            content_type=content_type, codename="add_ipentry"
        )
        content_type = ContentType.objects.get_for_model(models.EmailEntry)
        view_email_permission = Permission.objects.get(
            content_type=content_type, codename="view_emailentry"
        )
        add_email_permission = Permission.objects.get(
            content_type=content_type, codename="add_emailentry"
        )
        content_type = ContentType.objects.get_for_model(models.EmailHostEntry)
        view_emailhost_permission = Permission.objects.get(
            content_type=content_type, codename="view_emailhostentry"
        )
        add_emailhost_permission = Permission.objects.get(
            content_type=content_type, codename="add_emailhostentry"
        )
        authorized_user.user_permissions.add(
            view_ip_permission,
            view_email_permission,
            view_emailhost_permission,
            add_ip_permission,
            add_email_permission,
            add_emailhost_permission,
        )
        authorized_token = AuthToken(user=authorized_user)
        authorized_token.save()
        one_permission_user = User(username="user_with_one_permission")
        one_permission_user.save()
        one_permission_user.user_permissions.add(view_ip_permission)
        one_permission_token = AuthToken(user=one_permission_user)
        one_permission_token.save()
        cls.authenticated_client = APIClient()
        cls.authenticated_client.credentials(
            HTTP_AUTHORIZATION=f"Token {unauthorized_token.key}"
        )
        cls.authorized_client = APIClient()
        cls.authorized_client.credentials(
            HTTP_AUTHORIZATION=f"Token {authorized_token.key}"
        )
        cls.unauthenticated_client = APIClient()
        cls.one_permission_client = APIClient()
        cls.one_permission_client.credentials(
            HTTP_AUTHORIZATION=f"Token {one_permission_token}"
        )

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


class GetRequestViewTests(BaseTests):
    def test_blacklisted_ip_with_authorized_client(self):
        """
        Test that checking a blacklisted ip correctly returns True.
        """

        correct_response = [
            {"kind": "ip", "value": self.lower_case_blacklisted_ip, "result": True}
        ]
        response = self.authorized_client.get(
            "/blacklist/", {"ip": self.lower_case_blacklisted_ip}
        )
        self.assertEqual(response.data, correct_response)

    def test_non_blacklisted_ip_with_authorized_client(self):
        """
        Test that checking a non blacklisted ip correctly returns False.
        """
        correct_response = [
            {"kind": "ip", "value": self.not_blacklisted_ip, "result": False}
        ]
        response = self.authorized_client.get(
            "/blacklist/", {"ip": self.not_blacklisted_ip}
        )
        self.assertEqual(response.data, correct_response)

    def test_blacklisted_email_with_authorized_client(self):
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
        response = self.authorized_client.get(
            "/blacklist/", {"email": self.lower_case_blacklisted_email}
        )
        self.assertEqual(response.data, correct_response)

    def test_non_blacklisted_email_with_authorized_client(self):
        """
        Test that checking a non blacklisted email correctly returns False.
        """
        correct_response = [
            {"kind": "email", "value": self.not_blacklisted_email, "result": False}
        ]
        response = self.authorized_client.get(
            "/blacklist/", {"email": self.not_blacklisted_email}
        )
        self.assertEqual(response.data, correct_response)

    def test_blacklisted_email_host_with_authorized_client(self):
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
        response = self.authorized_client.get(
            "/blacklist/", {"email_host": self.lower_case_blacklisted_host}
        )
        self.assertEqual(response.data, correct_response)

    def test_non_blacklisted_email_host_with_authorized_client(self):
        """
        Test that checking a non blacklisted email host correctly returns False.
        """
        correct_response = [
            {"kind": "email_host", "value": self.not_blacklisted_host, "result": False}
        ]
        response = self.authorized_client.get(
            "/blacklist/", {"email_host": self.not_blacklisted_host}
        )
        self.assertEqual(response.data, correct_response)

    def test_two_ips_queries_with_authorized_client(self):
        """
        Test that checking two ip queries return correctly.
        """
        correct_response = [
            {"kind": "ip", "value": self.lower_case_blacklisted_ip, "result": True},
            {"kind": "ip", "value": self.not_blacklisted_ip, "result": False},
        ]
        response = self.authorized_client.get(
            "/blacklist/",
            {"ip": [self.lower_case_blacklisted_ip, self.not_blacklisted_ip]},
        )
        self.assertEqual(response.data, correct_response)

    def test_two_emails_queries_with_authorized_client(self):
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
        response = self.authorized_client.get(
            "/blacklist/",
            {"email": [self.lower_case_blacklisted_email, self.not_blacklisted_email]},
        )
        self.assertEqual(response.data, correct_response)

    def test_two_email_hosts_queries_with_authorized_client(self):
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
        response = self.authorized_client.get(
            "/blacklist/",
            {
                "email_host": [
                    self.lower_case_blacklisted_host,
                    self.not_blacklisted_host,
                ]
            },
        )
        self.assertEqual(response.data, correct_response)

    def test_query_with_unauthenticated_client(self):
        """
        Test that checking a query correctly returns status code 401.
        """
        response = self.unauthenticated_client.get(
            "/blacklist/",
            {
                "ip": self.lower_case_blacklisted_ip,
                "email": self.lower_case_blacklisted_email,
                "email_host": self.lower_case_blacklisted_host,
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_query_with_authenticated_client(self):
        """
        Test that checking a query correctly returns status code 403.
        """
        response = self.authenticated_client.get(
            "/blacklist/",
            {
                "ip": self.lower_case_blacklisted_ip,
                "email": self.lower_case_blacklisted_email,
                "email_host": self.lower_case_blacklisted_host,
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_query_with_one_permission_client(self):
        """
        Test that checking a query correctly returns status code 200
        when request for ip entry, but when requests for all entries returns status code 401.
        """
        response = self.one_permission_client.get(
            "/blacklist/", {"ip": self.lower_case_blacklisted_ip}
        )
        self.assertEqual(response.status_code, 200)

        response = self.one_permission_client.get(
            "/blacklist/",
            {
                "ip": self.lower_case_blacklisted_ip,
                "email": self.lower_case_blacklisted_email,
                "email_host": self.lower_case_blacklisted_host,
            },
        )
        self.assertEqual(response.status_code, 403)


class PostRequestViewSetTests(BaseTests):
    def test_add_ip_with_authorized_client(self):
        """
        Test that checking a blacklisted ip correctly returns status code 200.
        """
        response = self.authorized_client.post(
            "/blacklist/add/",
            [{"kind": "ip", "value": self.not_blacklisted_ip}],
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_add_email_with_authorized_client(self):
        """
        Test that checking a blacklisted email correctly returns status code 200.
        """
        response = self.authorized_client.post(
            "/blacklist/add/",
            [{"kind": "email", "value": self.not_blacklisted_email}],
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_add_email_host_with_authorized_client(self):
        """
        Test that checking a blacklisted email host correctly returns status code 200.
        """
        response = self.authorized_client.post(
            "/blacklist/add/",
            [{"kind": "email_host", "value": self.not_blacklisted_host}],
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_add_with_unauthenticated_client(self):
        """
        Test that checking a query correctly returns status code 401.
        """
        response = self.unauthenticated_client.post(
            "/blacklist/add/",
            [
                {"kind": "ip", "value": self.not_blacklisted_ip},
                {"kind": "email", "value": self.not_blacklisted_email},
                {"kind": "email_host", "value": self.not_blacklisted_host},
            ],
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_add_with_authenticated_client(self):
        """
        Test that checking a query correctly returns status code 403.
        """
        response = self.authenticated_client.post(
            "/blacklist/add/",
            [
                {"kind": "ip", "value": self.not_blacklisted_ip},
                {"kind": "email", "value": self.not_blacklisted_email},
                {"kind": "email_host", "value": self.not_blacklisted_host},
            ],
            format="json",
        )
        self.assertEqual(response.status_code, 403)
