from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message
from datetime import date, time


class MessageModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", email="alice@test.com", password="pass123")
        self.receiver = User.objects.create_user(username="bob", email="bob@test.com", password="pass123")

        self.message = Message.objects.create(
            from_who=self.sender,
            to_who=self.receiver,
            message="Hello Bob!",
            date=date(2025, 8, 20),
            time=time(14, 30)
        )

    def test_message_str(self):
        """__str__ should return the message text"""
        self.assertEqual(str(self.message), "Hello Bob!")

    def test_message_sender_and_receiver(self):
        """Check that sender and receiver are correct"""
        self.assertEqual(self.message.from_who.username, "alice")
        self.assertEqual(self.message.to_who.username, "bob")

    def test_message_default_seen_status(self):
        """By default, has_been_seen should be False"""
        self.assertFalse(self.message.has_been_seen)

    def test_message_can_mark_as_seen(self):
        """Update has_been_seen to True"""
        self.message.has_been_seen = True
        self.message.save()
        self.assertTrue(Message.objects.get(id=self.message.id).has_been_seen)