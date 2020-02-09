from django.urls import include, path
from rest_framework import routers

from groups.views.generics.contact_information import (
    ContactInformationViewSet,
)
from groups.views.generics.location_information import (
    LocationInformationViewSet,
)
from groups.views.generics.social_link import (
    SocialLinkViewSet,
)
from groups.views.group import GroupViewSet
from groups.views.membership import MembershipViewSet
from groups.views.post import PostViewSet
from groups.views.rights import Rights

app_name = 'groups'

router = routers.SimpleRouter()
router.register(
    'group',
    GroupViewSet,
    basename='group'
)
router.register(
    'post',
    PostViewSet,
    basename='post'
)
router.register(
    'membership',
    MembershipViewSet,
    basename='membership'
)
router.register(
    'contact_information',
    ContactInformationViewSet,
    basename='contact_information'
)
router.register(
    'location_information',
    LocationInformationViewSet,
    basename='location_information'
)
router.register(
    'social_link',
    SocialLinkViewSet,
    basename='social_information'
)

urlpatterns = [
    path('rights/', Rights.as_view(), name='rights'),
    path('', include(router.urls)),
]
