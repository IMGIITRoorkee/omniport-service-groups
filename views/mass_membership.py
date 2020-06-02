import swapper
from rest_framework import status
from rest_framework import response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from formula_one.enums.active_status import ActiveStatus

from groups.models import Membership, Group
from groups.permissions.admin import HasAdminRights, has_admin_rights as _has_admin_rights
from groups.serializers.membership import MembershipSerializer
from groups.utils.membership_notifications import send_mass_membership_notifications


Student = swapper.load_model('kernel', 'Student')

class MassMembershipUpdate(APIView):
    """
    APIView for mass addition, deletion or update of Membership objects
    """

    permission_classes = [
        permissions.IsAuthenticated,
        HasAdminRights,
    ]

    queryset = Membership.objects.all()

    @staticmethod
    def get_object(person_id):
        return Membership.objects.get(person=person_id)

    def put(self, request):
        """

        :param request:
        :return:
        """
        person = request.person
        group = request.data.get('group')
        try:
            group = Group.objects.get(pk=group)
            if not _has_admin_rights(person, group):
                raise PermissionDenied
        except Group.DoesNotExist:
            pass
        method = request.data.get('method')
        enrolment_nos = request.data.get('enrolment_nos')
        if method == 'delete':
            person_ids = []
            for enrolment_no in enrolment_nos:
                student = Student.objects.get(enrolment_number=enrolment_no)
                person = student.person.id
                try:
                    membership = self.get_object(person)
                    membership.delete()
                    person_ids.append(person)
                except Membership.DoesNotExist:
                    pass
            send_mass_membership_notifications(group.name, 'remove', person_ids)
            return response.Response(
                status=status.HTTP_204_NO_CONTENT
            )
        elif method == 'edit':
            person_ids = []
            data = {}
            data['group'] = request.data.get('group')
            data['designation'] = request.data.get('designation', None)
            data['post'] = request.data.get('post', None)
            data['has_admin_rights'] = request.data.get('has_admin_rights', None)
            data['has_edit_rights'] = request.data.get('has_edit_rights', None)
            data['start_date'] = request.data.get('start_date', None)
            data['end_date'] = request.data.get('end_date', None)
            for enrolment_no in enrolment_nos:
                try:
                    student = Student.objects.get(enrolment_number=enrolment_no)
                    data['person'] = student.person.id
                    try:
                        membership = self.get_object(data['person'])
                        serializer = MembershipSerializer(membership, data=data)
                        if serializer.is_valid():
                            serializer.save()
                        person_ids.append(student.person.id)
                    except Membership.DoesNotExist:
                        pass
                except Student.DoesNotExist:
                    return  response.Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data="Student matching query does not exist"
                    )
            send_mass_membership_notifications(group.name, 'edit', person_ids)
            return response.Response(
                status=status.HTTP_200_OK,
                data="The members have been update if existing"
            )

    def post(self, request):
        """
        Check if user has a permission to create new memberships and
        create new members from given enrolment numbers
        :param request: the request being processed
        :return:
        """

        person = request.person
        group = request.data.get('group')
        try:
            group = Group.objects.get(pk=group)
            if not _has_admin_rights(person, group):
                raise PermissionDenied
        except Group.DoesNotExist:
            pass
        data = {}
        enrolment_nos = request.data.get('enrolment_nos')
        data['group'] = request.data.get('group')
        data['designation'] = request.data.get('designation')
        data['post'] = request.data.get('post')
        data['has_admin_rights'] = request.data.get('has_admin_rights')
        data['has_edit_rights'] = request.data.get('has_edit_rights')
        data['start_date'] = request.data.get('start_date')
        data['end_date'] = request.data.get('end_date')
        person_ids = []
        for enrolment_no in enrolment_nos:
            try:
                student = Student.objects.get(enrolment_number=enrolment_no)
                data['person'] = student.person.id
            except Student.DoesNotExist:
                return response.Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="Student matching query does not exist"
                )
            serializer = MembershipSerializer(data=data)
            if serializer.is_valid():
                person_ids.append(data['person'])
                serializer.save()
            else:
                return response.Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=""
                )
        send_mass_membership_notifications(group.name, 'add', person_ids)
        return response.Response(
            status=status.HTTP_201_CREATED
        )
