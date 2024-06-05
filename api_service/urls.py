from api_service.views import *
from django.urls import path

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', UserLogin.as_view()),
    path('search/', UserSearchView.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    path('edit-profile/', UserEditProfile.as_view()),
    path('friend-request/', FriendRequestView.as_view()),
    path('friend-request/<int:pk>/', FriendRequestView.as_view()),
    path('friends/', FriendListView.as_view()),
    path('pending-requests/', PendingRequestsView.as_view()),
]