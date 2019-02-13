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
    base_name='group'
)
router.register(
    'post',
    PostViewSet,
    base_name='post'
)
router.register(
    'membership',
    MembershipViewSet,
    base_name='membership'
)
router.register(
    'contact_information',
    ContactInformationViewSet,
    base_name='contact_information'
)
router.register(
    'location_information',
    LocationInformationViewSet,
    base_name='location_information'
)
router.register(
    'social_link',
    SocialLinkViewSet,
    base_name='social_information'
)

urlpatterns = [
    path('rights/', Rights.as_view(), name='rights'),
    path('', include(router.urls)),
]
