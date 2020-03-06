from django.contrib.auth.models import User
from adventure.models import Player, Room
from util.sample_generator import World


#Room.objects.all().delete()
world = World()
world.generate_rooms(12, 12, 144)

cache = {}

for row in w.grid:
    for r in row:
            room = Room(title = r.name, description = f'Welcome to the {j.name} room with id {r.id}', x = r.x, y = r.y)
            room.save()
            cache[(r.x, r.y)] = room
            if (r.e_to.x, r.e_to.y) in cache:
                room.connectRooms(cache[(r.e_to.x, r.e_to.y)], 'e')
                cache[(r.e_to.x, r.e_to.y)].connectRooms(room, 'w')
    if r.w_to != None:
        if (r.w_to.x, r.w_to.y) in cache:
            room.connectRooms(cache[(r.w_to.x, r.w_to.y)], 'w')
            cache[(r.w_to.x, r.w_to.y)].connectRooms(room, 'e')
    if r.s_to != None:
        if (r.s_to.x, r.s_to.y) in cache:
            room.connectRooms(cache[(r.s_to.x, r.s_to.y)], 's')
            cache[(r.s_to.x, r.s_to.y)].connectRooms(room, 'n')
    if r.n_to != None:
        if (r.n_to.x, r.n_to.y) in cache:
            room.connectRooms(cache[(r.n_to.x, r.n_to.y)], 'n')
            cache[(r.n_to.x, r.n_to.y)].connectRooms(room, 's')


# r_outside = Room(title="Outside Cave Entrance",
#               description="North of you, the cave mount beckons")

# r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
# passages run north and east.""")

# r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
# into the darkness. Ahead to the north, a light flickers in
# the distance, but there is no way across the chasm.""")

# r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
# to north. The smell of gold permeates the air.""")

# r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
# chamber! Sadly, it has already been completely emptied by
# earlier adventurers. The only exit is to the south.""")

# r_outside.save()
# r_foyer.save()
# r_overlook.save()
# r_narrow.save()
# r_treasure.save()

# Link rooms together
# r_outside.connectRooms(r_foyer, "n")
# r_foyer.connectRooms(r_outside, "s")

# r_foyer.connectRooms(r_overlook, "n")
# r_overlook.connectRooms(r_foyer, "s")

# r_foyer.connectRooms(r_narrow, "e")
# r_narrow.connectRooms(r_foyer, "w")

# r_narrow.connectRooms(r_treasure, "n")
# r_treasure.connectRooms(r_narrow, "s")

players = Player.objects.all()
first_room = world.grid[0][0]
for p in players:
    p.currentRoom = first_room.id
    p.save()

