from django.urls import path
from .views import CreateQuestion, CreateTestimony, get_api_key, get_api_key_discord_bot, update_invite


urlpatterns = [
    path("new/key/", get_api_key, name="app_api_key_gen"),
    path("new/question/", CreateQuestion.as_view(), name="question_create"),
    path("new/testimony/", CreateTestimony.as_view(), name="testimony_create"),
    path("new/discord/", get_api_key_discord_bot, name="discord_api_key_gen"),
    path("api/invite/update/", update_invite, name='update_discord_invite'),
]