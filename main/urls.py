from django.urls import path#url()
from . import views
from .views import (post_list_view, post_detail_view, post_create_view, post_update_view, post_delete_view, 
user_posts, following_view, follower_view, feed_list_view, search_view, search_filter_view, comment_delete_view,
top_all, top_week, top_day, top_month, top_year, conversation_view, message_view, about_view)
from django.conf import settings
from django.conf.urls.static import static




app_name = 'main'  
#call upon the function from view and links it to url path
# views. = function based views
# as_view() = class based views
urlpatterns = [
    path("home/", post_list_view.as_view(), name="home"),
    path("", about_view.as_view(), name="about"),
    path("feed/", feed_list_view.as_view(), name="feed"), #follow feed
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("post/create/", post_create_view.as_view(), name="post-create"),
    path("post/<int:pk>/", post_detail_view.as_view(), name='post-detail'),  #specifies the url for individual posts
    path("comment/<int:pk>/delete", comment_delete_view.as_view(), name='comment-delete'), 
    path("post/<int:pk>/update", post_update_view.as_view(), name='post-update'),
    path("post/<int:pk>/delete", post_delete_view.as_view(), name='post-delete'),
    path("profile/", views.profile, name= "profile"),
    path("user/<str:username>/following/", following_view.as_view(), name= "following"),
    path("user/<str:username>/followers/", follower_view.as_view(), name= "followers"),
    path("user/<str:username>", user_posts.as_view(), name="user-posts"), #profile view
    path("upvote", views.upvote, name='upvote-post'), 
    path("search/", search_view.as_view(), name='search'),
    path("search/filter/", search_filter_view.as_view(), name="search-filter"),
    path("top/all/", top_all.as_view(), name="top-all"),
    path("top/week/", top_week.as_view(), name="top-week"),
    path("top/day/", top_day.as_view(), name="top-day"),
    path("top/month/", top_week.as_view(), name="top-month"),
    path("top/year/", top_week.as_view(), name="top-year"),
    path("messages/", conversation_view.as_view(), name="conversation"),
    path("messages/<str:username>/", message_view.as_view(), name="message"),
    path("contact/", views.contact, name="contact"),
    path("contact/done/", views.contact_done, name="contact-done"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)