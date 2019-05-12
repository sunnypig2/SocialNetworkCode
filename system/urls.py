from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_site, name='login'),
    path('logout/', views.logout_site, name='logout'),
    path('demo/<int:eventpage>/<int:peoplepage>', views.demo, name='demo'),
    path('search/', views.search, name='search'),
    path('relationextraction', views.relationextraction, name='relationextraction'),
    path('fileUpload', views.fileUpload, name='fileUpload'),
    path('peoplenews/<str:name>', views.peoplenews, name='peoplenews'),
    path('sin_analysis/<str:name>', views.sin_analysis, name='sin_analysis'),
    path('all_analysis/<str:name>', views.all_analysis, name='all_analysis'),
    path('gn/<str:name>', views.gn, name='gn'),
    path('newgn', views.newgn, name='newgn'),
    path('allgn', views.allgn, name='allgn'),

    path('recommendation/<str:name>', views.recommendation, name='recommendation'),

    path('media_focus/<str:media>/<str:account>', views.media_focus, name='media_focus'),
    path('person_contrast/<str:name>/<str:contrast>', views.person_contrast, name='person_contrast'),
    path('friend_circle/<str:name>', views.friend_circle, name='friend_circle'),

    path('gn_part/<str:name>', views.gn_part, name='gn_part'),
    path('all_gn', views.all_gn, name='all_gn'),

    path('param_gender/<str:name>', views.param_gender, name='param_gender'),
    # path('gn_part/<str:name>', views.gn_part, name='gn_part'),

    path('person_tweet/<int:id_tweet>/<str:name>', views.person_tweet, name='person_tweet'),
    path('person_event/<str:event>/<str:name>', views.person_event, name='person_event'),
    path('sensitiveinfo/<str:event>', views.sensitiveinfo, name='sensitiveinfo'),
    path('sensitive_develop/<str:event>', views.sensitive_develop, name='sensitive_develop'),
    path('tweet_analysis/<int:id_tweet>', views.tweet_analysis, name='tweet_analysis'),

]
