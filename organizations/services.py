from .models import Organization , Membership

def Create_Org(*,user,name,type):
    organization = Organization.objects.create(
        name = name,
        type = type,
    )
    membership = Membership.objects.create(
        user = user,
        organization = organization,
        role = 'owner',
    )

    return organization