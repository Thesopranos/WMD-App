from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    """
        Custom user model.

        Fields:
            nickname: str, max_length=30, unique, required

            name: str, max_length=30, required

            surname: str, max_length=30, required

            bio: str, max_length=500, not required

            birth_date: date, required

            location: str, max_length=30, not required

            email: email, unique, required

            phone: str, max_length=15, not required

            avatar: image, upload_to='avatars/', not required

            obstruct_list: list, related_name='obstructed_by', symmetrical=False, not required

            created_at: datetime, auto_now_add, required

            updated_at: datetime, auto_now, not required

            is_active: bool, default=True, not required

            followers: list, related_name='user_following', symmetrical=False, not required

            following: list, related_name='user_followers', symmetrical=False, not required


        Methods:

            get_absolute_url: str

            get_followers: list

            get_followings: list

            get_obstruct_list: list

            follow: bool

            unfollow: bool

            obstruct: bool

            unobstruct: bool

            is_following: bool

            is_followed_by: bool

            is_obstructing: bool

            get_followers_count: int

            get_followings_count: int

            get_obstruct_count: int

    """

    nickname = models.CharField(max_length=30, blank=True, unique=True)
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    obstruct_list = models.ManyToManyField('self', related_name='obstructed_by', symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)

    followers = models.ManyToManyField(
        'self',
        related_name='user_following',
        symmetrical=False,
        blank=True
    )

    following = models.ManyToManyField(
        'self',
        related_name='user_followers',
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.username

    # !! == GET METHODS ==
    # ? == Get absolute url ==
    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    # ? == Get followers ==
    def get_followers(self) -> list:
        return self.followers.all()

    # ? == Get followings ==
    def get_followings(self) -> list:
        return self.following.all()

    # ? == Get obstruct list ==
    def get_obstruct_list(self) -> list:
        return self.obstruct_list.all()

    # ? == Get followers count ==
    def get_followers_count(self) -> int:
        return self.followers.count()

    # ? == Get followings count ==
    def get_followings_count(self) -> int:
        return self.following.count()

    # ? == Get obstruct count ==
    def get_obstruct_count(self) -> int:
        return self.obstruct_list.count()


    # !! == REACTION METHODS ==
    # ? == Follow user ==
    def follow(self, user) -> bool:
        if not self.is_following(user) and self != user and not self.is_obstructing(user):
            self.following.add(user)
            user.followers.add(self)
            return True
        return False

    # ? == Unfollow user ==
    def unfollow(self, user) -> bool:
        if self.is_following(user) and self != user and not self.is_obstructing(user):
            self.following.remove(user)
            user.followers.remove(self)
            return True
        return False

    # ? == Obstruct user ==
    def obstruct(self, user) -> bool:
        if not self.is_obstructing(user) and self != user:
            self.obstruct_list.add(user)
            if self.is_following(user):
                self.unfollow(user)
            if self.is_followed_by(user):
                user.unfollow(self)
            return True
        return False

    # ? == Unobstruct user ==
    def unobstruct(self, user):
        if self.is_obstructing(user) and self != user:
            self.obstruct_list.remove(user)
            user.obstruct_list.remove(self)
            return True
        return False

    # !! == CHECK METHODS ==
    # ? == Check if user is following ==
    def is_following(self, user) -> bool:
        return self.following.filter(id=user.id).exists()

    # ? == Check if user is followed by ==
    def is_followed_by(self, user) -> bool:
        return self.followers.filter(id=user.id).exists()

    # ? == Check if user is obstructing ==
    def is_obstructing(self, user) -> bool:
        return self.obstruct_list.filter(id=user.id).exists()
