from unittest import mock

from django.conf.global_settings import PASSWORD_HASHERS
from django.contrib.auth.hashers import get_hasher
from django.core import mail
from django.test import TestCase, override_settings

from hafizhlab.accounts.models import User


class UserTestCase(TestCase):
    """
    From Django's tests.auth_tests.test_models.AbstractUserTestCase
    with additional get_full_name() and get_short_name() test.
    """

    def test_email_user(self):
        # valid send_mail parameters
        kwargs = {
            "fail_silently": False,
            "auth_user": None,
            "auth_password": None,
            "connection": None,
            "html_message": None,
        }
        user = User(email='foo@bar.com')
        user.email_user(
            subject="Subject here",
            message="This is a message",
            from_email="from@domain.com",
            **kwargs
        )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, "Subject here")
        self.assertEqual(message.body, "This is a message")
        self.assertEqual(message.from_email, "from@domain.com")
        self.assertEqual(message.to, [user.email])

    def test_last_login_default(self):
        user1 = User.objects.create(username='user1')
        self.assertIsNone(user1.last_login)

        user2 = User.objects.create_user(username='user2')
        self.assertIsNone(user2.last_login)

    def test_user_clean_normalize_email(self):
        user = User(username='user', password='foo', email='foo@BAR.com')
        user.clean()
        self.assertEqual(user.email, 'foo@bar.com')

    def test_user_double_save(self):
        """
        Calling user.save() twice should trigger password_changed() once.
        """
        user = User.objects.create_user(username='user', password='foo')
        user.set_password('bar')
        with mock.patch('django.contrib.auth.password_validation.password_changed') as pw_changed:
            user.save()
            self.assertEqual(pw_changed.call_count, 1)
            user.save()
            self.assertEqual(pw_changed.call_count, 1)

    @override_settings(PASSWORD_HASHERS=PASSWORD_HASHERS)
    def test_check_password_upgrade(self):
        """
        password_changed() shouldn't be called if User.check_password()
        triggers a hash iteration upgrade.
        """
        user = User.objects.create_user(username='user', password='foo')
        initial_password = user.password
        self.assertTrue(user.check_password('foo'))
        hasher = get_hasher('default')
        self.assertEqual('pbkdf2_sha256', hasher.algorithm)

        old_iterations = hasher.iterations
        try:
            # Upgrade the password iterations
            hasher.iterations = old_iterations + 1
            with mock.patch('django.contrib.auth.password_validation.password_changed') as pw_changed:
                user.check_password('foo')
                self.assertEqual(pw_changed.call_count, 0)
            self.assertNotEqual(initial_password, user.password)
        finally:
            hasher.iterations = old_iterations

    def test_get_full_name(self):
        user = User(full_name='John Doe')
        self.assertEqual(user.get_full_name(), 'John Doe')

    def test_get_short_name_with_nickname(self):
        user = User(full_name='John Doe', nickname='Jade')
        self.assertEqual(user.get_short_name(), 'Jade')

    def test_get_full_name_without_nickname(self):
        user = User(full_name='John Doe')
        self.assertEqual(user.get_short_name(), 'John')

    def test_get_short_name_none(self):
        user = User()
        self.assertEqual(user.get_short_name(), None)
