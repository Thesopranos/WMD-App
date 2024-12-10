from django.db import models
from django.conf import settings
from django.urls import reverse

class Room(models.Model):
	"""
		Room model.

		Fields:

			name: str, unique, max_length=100, required

			room_code: str, unique, max_length=10, required

			created_by: CustomUser object, required

			created_at: datetime object, auto_now_add, required

			participants: list of CustomUser objects, not required

			obstructed_users: list of CustomUser objects, not required

			managers: list of CustomUser objects, not required

			is_private: bool default=False, required

			password: str max_length=100, not required

		Methods:

			get_absolute_url: str

			get_participants: list

			get_managers: list

			get_obstructed_users: list

			get_participants_count: int

			get_managers_count: int

			get_obstructed_users_count: int

			add_participant: bool

			add_manager: bool

			add_obstructed_user: bool

			remove_participant: bool

			remove_manager: bool
			remove_obstructed_user: bool

			change_password: None

			make_private: None

			make_public: None

			delete_room: None

			is_participant: bool

			is_manager: bool

			is_obstructed: bool

			is_private: bool

			is_password_correct: bool

			is_created_by: bool

			is_accessible: bool

			is_editable: bool

			is_deletable: bool

	"""

	name = models.CharField(max_length=100, unique=True, blank=False)
	room_code = models.CharField(max_length=10, unique=True, blank=False)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_rooms', blank=False)
	created_at = models.DateTimeField(auto_now_add=True, blank=False)
	participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rooms', blank=True)
	obsturcted_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='obstructed_rooms', blank=True)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='managed_rooms', blank=True)
	is_private = models.BooleanField(default=False, blank=False)
	password = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.name

	# !! == GET METHODS ==
	# ? == Get absolute url ==
	def get_absolute_url(self):
		return reverse('room-detail', args=[str(self.id)])

	# ? == Get participants ==
	def get_participants(self) -> list:
		return self.participants.all()

	# ? == Get managers ==
	def get_managers(self) -> list:
		return self.managers.all()

	# ? == Get obstructed users ==
	def get_obstructed_users(self) -> list:
		return self.obsturcted_users.all()

	# ? == Get participants count ==
	def get_participants_count(self) -> int:
		return self.participants.count()

	# ? == Get managers count ==
	def get_managers_count(self) -> int:
		return self.managers.count()

	# ? == Get obstructed users count ==
	def get_obstructed_users_count(self) -> int:
		return self.obsturcted_users.count()

	# !! == REACTION METHODS ==
	# ? == Add participant ==
	def add_participant(self, user) -> bool:
		if not self.is_participant(user) and not self.is_obstructed(user):
			self.participants.add(user)
			return True
		return False

	# ? == Add manager ==
	def add_manager(self, user)	-> bool:
		if not self.is_manager(user) and not self.is_obstructed(user) and self.is_participant(user):
			self.managers.add(user)
			return True
		return False

	# ? == Add obstructed user ==
	def add_obstructed_user(self, user) -> bool:
		if not self.is_obstructed(user) and not self.is_created_by(user):
			self.obsturcted_users.add(user)
			self.participants.remove(user)
			self.managers.remove(user)
			return True
		return False

	# ? == Remove participant ==
	def remove_participant(self, user) -> bool:
		if self.is_participant(user):
			self.participants.remove(user)
			self.managers.remove(user)
			return True
		return False

	# ? == Remove manager ==
	def remove_manager(self, user) -> bool:
		if self.is_manager(user):
			self.managers.remove(user)
			return True
		return False

	# ? == Remove obstructed user ==
	def remove_obstructed_user(self, user) -> bool:
		if self.is_obstructed(user):
			self.obsturcted_users.remove(user)
			return True
		return False

	# ? == Change password ==
	def change_password(self, password):
		self.password = password

	# ? == Make private ==
	def make_private(self):
		self.is_private = True

	# ? == Make public ==
	def make_public(self):
		self.is_private = False

	# ? == Delete room ==
	def delete_room(self):
		self.delete()

	# !! == CHECK METHODS ==
	# ? == Is participant ==
	def is_participant(self, user) -> bool:
		return user in self.participants.all()

	# ? == Is manager ==
	def is_manager(self, user) -> bool:
		return user in self.managers.all()

	# ? == Is obstructed ==
	def is_obstructed(self, user) -> bool:
		return user in self.obsturcted_users.all()

	# ? == Is private ==
	def is_private(self) -> bool:
		return self.is_private

	# ? == Is password correct ==
	def is_password_correct(self, password) -> bool:
		return self.password == password

	# ? == Is created by ==
	def is_created_by(self, user) -> bool:
		return self.created_by == user

	# ? == Is accessible ==
	def is_accessible(self, user) -> bool:
		return (self.is_participant(user) or self.is_manager(user) or self.is_created_by(user)) and not self.is_obstructed(user)

	# ? == Is editable ==
	def is_editable(self, user) -> bool:
		return self.is_manager(user) or self.is_created_by(user)

	# ? == Is deletable ==
	def is_deletable(self, user) -> bool:
		return self.is_created_by(user)
