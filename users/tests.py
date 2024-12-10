from django.test import TestCase
from .models import CustomUser

class CustomUserTestCase(TestCase):
	"""
		Custom user model test case.

		Fields:
			user1, user2, user3, user4, user5, user6, user7

		Methods:

			- setUp

			- follow_all_users

			- follow_from_all_users

			- test_user_count

			- test_followings_count

			- test_followers_count

			- test_obstructing_count

			- test_follow

			- test_unfollow

			- test_following_list

			- test_followers_list

			- test_obstruct

			- test_unobstruct

	"""
	# !! == Setup ==
	def setUp(self):
		self.user1 = CustomUser.objects.create_user(username='ali', email='ali@example.com', password='12345')
		self.user2 = CustomUser.objects.create_user(username='veli', email='veli@example.com', password='67890')
		self.user3 = CustomUser.objects.create_user(username='mehmet', email='mehmet@example.com', password='67dskf890')
		self.user4 = CustomUser.objects.create_user(username='orhan', email='orhan@example.com', password='6789ss0')
		self.user5 = CustomUser.objects.create_user(username='abuzer', email='abuzer@example.com', password='6789asd0')
		self.user6 = CustomUser.objects.create_user(username='haluk', email='haluk@example.com', password='67dd89asd0')
		self.user7 = CustomUser.objects.create_user(username='guray', email='guray@example.com', password='6dd7dd89asd0')
		self.follow_all_users(self.user1)

	# !! == Helper methods ==
	# ? == Follow all users ==
	def follow_all_users(self, user):
		for current_user in CustomUser.objects.all():
			user.follow(current_user)

	# ? == Follow from all users ==
	def follow_from_all_users(self, user):
		for current_user in CustomUser.objects.all():
			current_user.follow(user)

	# !! == Tests ==
	# ? == User count ==
	def test_user_count(self):
		self.assertEqual(CustomUser.objects.count(), 7)

	# ? == User followings count ==
	def test_followings_count(self):
		self.assertEqual(self.user1.get_followings_count(), 6)
		self.assertEqual(self.user2.get_followings_count(), 0)

	# ? == User followers count ==
	def test_followers_count(self):
		self.assertEqual(self.user1.get_followers_count(), 0)
		self.assertEqual(self.user2.get_followers_count(), 1)

	# ? == User obstruct count ==
	def test_obstructing_count(self):
		self.user3.obstruct(self.user2)
		self.assertEqual(self.user3.get_obstruct_count(), 1)
		self.assertEqual(self.user2.get_obstruct_count(), 0)

	# ? == User follow ==
	def test_follow(self):
		self.user3.follow(self.user2)
		self.assertTrue(self.user3.is_following(self.user2))
		self.assertFalse(self.user2.is_following(self.user3))

	# ? == User unfollow ==
	def test_unfollow(self):
		self.user3.follow(self.user2)
		self.assertTrue(self.user3.is_following(self.user2))
		self.user3.unfollow(self.user2)
		self.assertFalse(self.user3.is_following(self.user2))

	# ? == User following all ==
	def test_following(self):
		self.assertEqual(self.user1.get_followings_count(), 6)
		for current_user in CustomUser.objects.all():
			if current_user != self.user1:
				self.assertTrue(self.user1.is_following(current_user))

	# ? == User following list ==
	def test_following_list(self):
		self.follow_all_users(self.user1)
		for current_user in CustomUser.objects.all():
			if current_user != self.user1:
				self.assertTrue(self.user1.is_following(current_user))

	# ? == User followers list ==
	def test_followers_list(self):
		self.follow_from_all_users(self.user1)
		for current_user in CustomUser.objects.all():
			if current_user != self.user1:
				self.assertTrue(current_user.is_following(self.user1))

	# ? == User obstruct ==
	def test_obstruct(self):
		self.user3.obstruct(self.user2)
		self.assertTrue(self.user3.is_obstructing(self.user2))
		self.assertFalse(self.user2.is_obstructing(self.user3))

	# ? == User unobstruct ==
	def test_unobstruct(self):
		self.user3.obstruct(self.user2)
		self.assertTrue(self.user3.is_obstructing(self.user2))
		self.assertFalse(self.user2.is_obstructing(self.user3))
		self.user3.unobstruct(self.user2)
		self.assertFalse(self.user3.is_obstructing(self.user2))
		self.assertFalse(self.user2.is_obstructing(self.user3))
