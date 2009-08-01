from pybird import Birdie, Account, Status

Birdie.login("username", "password")
Birdie.format("json")
obj = Birdie(Status.show.k3057366428)

print obj.text