from unittest import TestCase
from kundocase.forum.spamcheck import all_users_from_domain_are_spam
from kundocase.forum.spamcheck import known_spammers_are_spam
from kundocase.forum.spamcheck import long_texts_are_spam
from kundocase.forum.spamcheck import some_usernames_are_spam
from kundocase.forum.spamcheck import words_in_text_are_spam

class SpamTest(TestCase):
    def setUp(self):
        class TestObj(object):
            user_email="valid.email@gmail.com"
            user_name="Valid User"
            content="Not too long"
        class Empty(object):
            pass
        self.testobj=TestObj
        self.empty=Empty

    def test_domain_spam(self):
        self.assertFalse(all_users_from_domain_are_spam(self.testobj, ["evil.com"]))
        self.assertFalse(all_users_from_domain_are_spam(self.empty, ["evil.com"]))
        self.assertTrue(all_users_from_domain_are_spam(self.testobj, ["gmail.com"]))
    
    def test_known_spammer(self):
        class Spammer:
            user_email="albertvictor@payinapp.com"
        self.assertFalse(known_spammers_are_spam(self.testobj))
        self.assertFalse(known_spammers_are_spam(self.empty))
        self.assertTrue(known_spammers_are_spam(Spammer))
        
    def test_long_text_spam(self):
        class LongText:
            content="spam!"*50
        self.assertFalse(long_texts_are_spam(self.testobj))
        self.assertFalse(long_texts_are_spam(self.empty))
        self.assertTrue(long_texts_are_spam(LongText,200))
    
    def test_bad_user_spam(self):
        self.assertFalse(some_usernames_are_spam(self.testobj, ["evil user"]))
        self.assertFalse(some_usernames_are_spam(self.empty, ["evil user"]))
        self.assertTrue(some_usernames_are_spam(self.testobj, ["Valid User"]))
    
    def test_bad_word_spam(self):
        self.assertFalse(words_in_text_are_spam(self.testobj, ["wordNotPresent"]))
        self.assertFalse(words_in_text_are_spam(self.empty, ["wordNotPresent"]))
        self.assertTrue(words_in_text_are_spam(self.testobj, ["too"]))
