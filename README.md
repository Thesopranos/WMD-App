# WMD-App  
#### Description  
A collaborative streaming platform where users can create rooms to watch movies, series, and videos together in real-time. Enjoy synchronized playback, text and voice chat, friend management, and profile customization. Open-source and built with Django and React. Watch together, anytime, anywhere!  

#### Features  
**User Profile Management**: Create and manage user profiles.  
**Followers System**: Follow users.  
**Text and Voice Chat**: Communicate through text and voice chat.  
**Watch Rooms**: Create rooms to watch videos together on platforms like Netflix and YouTube.  
  
#### Technologies Used  
Frontend: React  
Backend: Django  
Database: PostgreSQL  
  
#### Models  
##### User Model Information  
The CustomUser model includes the following fields:  
**Nickname**: A user's nickname (max 30 characters).  
**Name**: The user's first name (max 30 characters).  
**Surname**: The user's last name (max 30 characters).  
**Bio**: A short biography of the user (max 500 characters).  
**Birth Date**: The user's date of birth.  
**Location**: The user's location (max 30 characters).  
**Email**: The user's email address (unique).  
**Phone**: The user's phone number (max 15 characters).  
**Avatar**: The user's profile picture (image upload).  
**Obstruct List**: A many-to-many relationship to other users, allowing users to block others.  
**Followers**: A many-to-many relationship to other users, representing users who follow this user.  
**Following**: A many-to-many relationship to other users, representing users that this user is following.  
**Created At**: The timestamp when the user profile was created.  
**Updated At**: The timestamp when the user profile was last updated.  
**Is Active**: A boolean field indicating if the user account is active (default: True).  

##### User Model Functions
The CustomUser model includes the following methods:
  
###### String Representation:  
**\_\_str\_\_(self)**: Returns the username of the user.  
  
###### Get Methods:
**get_absolute_url(self)**: Returns the absolute URL for the user detail page.  
**get_followers(self) -> list**: Returns a list of users who follow this user.  
**get_followings(self) -> list**: Returns a list of users this user is following.  
**get_obstruct_list(self) -> list**: Returns a list of users who are obstructed by this user.  
**get_followers_count(self) -> int**: Returns the number of followers this user has.  
**get_followings_count(self) -> int**: Returns the number of users this user is following.  
**get_obstruct_count(self) -> int**: Returns the number of users in the obstruct list.  
  
######Reaction Methods:  
**follow(self, user)**: Allows the user to follow another user if they are not already following and not obstructing them.  
**unfollow(self, user)**: Allows the user to unfollow another user.  
**obstruct(self, user)**: Allows the user to obstruct another user. If the user is following or being followed by the obstructed user, the respective follow relationship will be removed.  
**unobstruct(self, user)**: Allows the user to remove a user from the obstruct list.  

######Check Methods:  
**is_following(self, user) -> bool**: Checks if the user is following another user.  
**is_followed_by(self, user) -> bool**: Checks if the user is followed by another user.  
**is_obstructing(self, user) -> bool**: Checks if the user is obstructing another user.  
These methods enable users to interact with each other, such as following, unfollowing, and managing the obstruct list, while also providing convenient ways to check relationships and get related data.  
