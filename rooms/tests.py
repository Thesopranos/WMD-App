from django.test import TestCase
from .models import Room
from users.models import CustomUser

# Create your tests here.
class RoomTestCase(TestCase):
	"""
		Room model test case.

		Fields:

			user1, user2, user3, user4, user5, user6, user7, user8

			room1, room2, room3, room4, room5, room6, room7

		Methods:

			- setUp

			- test_room_count

			- test_participants_count

			- test_managers_count

			- test_obstructed_users_count

			- test_add_participant

			- test_add_manager

			- test_add_obstructed_user

			- test_remove_participant

			- test_remove_manager

			- test_remove_obstructed_user

			- test_change_password

			- test_is_participant

			- test_is_manager

			- test_is_obstructed

			- test_is_created_by

			- test_managers

			- test_obstructed_users

			- test_participants_list

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
		self.user8 = CustomUser.objects.create_user(username='gu2ray', email='gu2ray@example.com', password='6dd37dd89asd0')

		self.room1 = Room.objects.create(name='room1', room_code='room1', created_by=self.user1)
		self.room2 = Room.objects.create(name='room2', room_code='room2', created_by=self.user2)
		self.room3 = Room.objects.create(name='room3', room_code='room3', created_by=self.user3)
		self.room4 = Room.objects.create(name='room4', room_code='room4', created_by=self.user4)
		self.room5 = Room.objects.create(name='room5', room_code='room5', created_by=self.user5)
		self.room6 = Room.objects.create(name='room6', room_code='room6', created_by=self.user6)
		self.room7 = Room.objects.create(name='room7', room_code='room7', created_by=self.user7)

		self.room1.add_participant(self.user2)
		self.room1.add_participant(self.user3)
		self.room1.add_participant(self.user4)
		self.room1.add_participant(self.user5)
		self.room1.add_participant(self.user6)
		self.room1.add_participant(self.user7)
		self.room1.add_participant(self.user8)

		self.room1.add_manager(self.user2)
		self.room1.add_manager(self.user3)
		self.room1.add_manager(self.user4)

		self.room1.add_obstructed_user(self.user3)
		self.room1.add_obstructed_user(self.user5)
		self.room1.add_obstructed_user(self.user7)

	# !! == Tests ==
	# ? == Room count ==
	def test_room_count(self):
		self.assertEqual(Room.objects.count(), 7)

	# ? == Room participants count ==
	def test_participants_count(self):
		self.assertEqual(self.room1.get_participants_count(), 4)
		self.assertEqual(self.room2.get_participants_count(), 0)

	# ? == Room managers count ==
	def test_managers_count(self):
		self.assertEqual(self.room1.get_managers_count(), 2)
		self.assertEqual(self.room2.get_managers_count(), 0)

	# ? == Room obstructed users count ==
	def test_obstructed_users_count(self):
		self.room1.add_obstructed_user(self.user2)
		self.assertEqual(self.room1.get_obstructed_users_count(), 4)
		self.assertEqual(self.room2.get_obstructed_users_count(), 0)

	# ? == Room add participant ==
	def test_add_participant(self):
		self.room1.add_participant(self.user1)
		self.assertTrue(self.room1.is_participant(self.user1))
		self.assertFalse(self.room1.is_obstructed(self.user1))

	# ? == Room add manager ==
	def test_add_manager(self):
		self.room1.add_manager(self.user6)
		self.assertTrue(self.room1.is_manager(self.user6))
		self.assertFalse(self.room1.is_obstructed(self.user6))

	# ? == Room add obstructed user ==
	def test_add_obstructed_user(self):
		self.room1.add_obstructed_user(self.user2)
		self.assertTrue(self.room1.is_obstructed(self.user2))
		self.assertFalse(self.room1.is_created_by(self.user2))

	# ? == Room remove participant ==
	def test_remove_participant(self):
		self.room1.remove_participant(self.user2)
		self.assertFalse(self.room1.is_participant(self.user2))

	# ? == Room remove manager ==
	def test_remove_manager(self):
		self.room1.remove_manager(self.user2)
		self.assertFalse(self.room1.is_manager(self.user2))

	# ? == Room remove obstructed user ==
	def test_remove_obstructed_user(self):
		self.room1.remove_obstructed_user(self.user2)
		self.assertFalse(self.room1.is_obstructed(self.user2))

	# ? == Room change password ==
	def test_change_password(self):
		self.room1.change_password('new_password')
		self.assertEqual(self.room1.password, 'new_password')

	# ? == Room is participant ==
	def test_is_participant(self):
		self.assertTrue(self.room1.is_participant(self.user2))
		self.assertFalse(self.room2.is_participant(self.user1))

	# ? == Room is manager ==
	def test_is_manager(self):
		self.assertTrue(self.room1.is_manager(self.user2))
		self.assertFalse(self.room2.is_manager(self.user1))

	# ? == Room is obstructed ==
	def test_is_obstructed(self):
		self.room1.add_obstructed_user(self.user2)
		self.assertTrue(self.room1.is_obstructed(self.user2))
		self.assertFalse(self.room2.is_obstructed(self.user1))

	# ? == Room is created by ==
	def test_is_created_by(self):
		self.assertTrue(self.room1.is_created_by(self.user1))
		self.assertFalse(self.room2.is_created_by(self.user1))

	# ? == Room managers ==
	def test_managers(self):
		self.assertEqual(self.room1.get_managers_count(), 2)
		self.assertTrue(self.room1.is_manager(self.user2))
		self.assertFalse(self.room1.is_manager(self.user3))
		self.assertTrue(self.room1.is_manager(self.user4))
		self.assertFalse(self.room1.is_manager(self.user5))
		self.assertFalse(self.room1.is_manager(self.user6))
		self.assertFalse(self.room1.is_manager(self.user7))

	# ? == Room obstructed users ==
	def test_obstructed_users(self):
		self.room1.add_obstructed_user(self.user2)
		self.assertEqual(self.room1.get_obstructed_users_count(), 4)
		self.assertTrue(self.room1.is_obstructed(self.user2))
		self.assertFalse(self.room1.is_created_by(self.user2))
		self.assertFalse(self.room1.is_manager(self.user2))
		self.assertFalse(self.room1.is_participant(self.user2))

	# ? == Room participants list ==
	def test_participants_list(self):
		self.room1.add_participant(self.user8)
		self.assertEqual(self.room1.get_participants_count() , 4)
