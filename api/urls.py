from django.urls import path
from api.views import MyTokenObtainPairView, get_schools,UserView,UserDetail, LogoutView,UpdateActiveUserView, StudentView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('active/<int:user_id>/', UpdateActiveUserView.as_view(), name='deactive'),
    path('users/', UserView.as_view(), name='users'),
    path('students/', StudentView.as_view(), name='students'),
    path('user-detail/<int:id>', UserDetail.as_view(), name='user-detail'),
    path('schools/', get_schools, name='schools'),
] 

