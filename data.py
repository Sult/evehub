from django.contrib.auth.models import User

# add test users
user = User.objects.create_superuser("ghitzarai", "some@email.com", "1234")
user.save()
user.create_related()

user = User.objects.create_superuser("slippu", "some@email.com", "1234")
user.save()
user.create_related()


#set initial data
print "Adding misc"
execfile("populate/misc.py")

print "Adding all skills"
execfile("populate/skills.py")
