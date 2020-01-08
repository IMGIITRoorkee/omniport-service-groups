import logging

from rest_framework import status, generics, permissions, response

from groups.models import Group
from groups.utils import rights

logger = logging.getLogger('groups')


class Rights(generics.GenericAPIView):
    """
    This view shows if the current user has the given rights for the given group
    """

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        which = request.query_params.get('which')
        group_slug = request.query_params.get('group')

        user = request.person
        try:
            group = Group.objects.get(slug=group_slug)

            rights_function = getattr(rights, f'has_{which}_rights')
            has_rights = rights_function(user, group)
            response_data = {
                'hasRights': has_rights,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        except AttributeError:
            response_data = {
                'errors': {
                    'which': [
                        'Non-existent right',
                    ],
                },
            }
            logger.error(
                f'The request to check {self.request.person}\'s rights '
                f'for the group \'{group}\' was identified as a bad '
                'request due to an attribute error'
            )
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Group.DoesNotExist:
            response_data = {
                'errors': {
                    'group': [
                        'Non-existent group',
                    ],
                },
            }
            logger.error(
                f'The request to check {self.request.person}\'s rights '
                f'for the group with slug \'{group_slug}\' was identified '
                'as a bad request as the group does not exist'
            )
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
