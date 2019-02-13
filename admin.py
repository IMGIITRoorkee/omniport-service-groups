from omniport.admin.site import omnipotence

from groups.models import Group, Membership, Post

omnipotence.register(Group)
omnipotence.register(Membership)
omnipotence.register(Post)
