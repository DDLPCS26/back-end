from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from .room_creator from RoomCreator

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    Room.objects.all().delete()
    created_rooms = RoomCreator()

    num_rooms = 144
    width = 12
    height = 12
    created_rooms.generate_rooms(width, height, num_rooms)
    user = request.user
    print(f"User: {user}")
    player = user.player
    print(f"Player: {player}")
    player_id = player.id
    print(f"Player ID: {player_id}")
    uuid = player.uuid

    player.current_room = Room.objects.first().id
    room = Room.objects.first()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description,'room_id': room.room_id, 'players':players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()

        ##
        description = nextRoom.description
        if player.hasVisited(nextRoom) and nextRoom.description_b:
            description = nextRoom.description_b
        if not player.hasVisited(nextRoom):
            PlayerVisited.objects.create(player=player, room=room)


        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)


#implementing GET - You will also need to implement a GET rooms API endpoint for clients to fetch all rooms to display a map on the frontend.
@csrf_exempt
@api_view(["GET"])
def rooms(request):
    #user = request.user
    #player = user.player
    #player_id = player.id
    rooms = Room.objects.all()
    room_info = []

    for room in rooms:
        room_info.append(
            {"id": room.id, "title": room.title, "description": room.description, "north": room.n_to, "east": room.e_to, "south": room.s_to, "west": room.w_to, "x": room.x, "y": room.y}
        )
    return JsonResponse({'num_rooms': len(room_data), 'rooms': room_data}, safe=True)
    # return JsonResponse([{
    #     'room_id': room.id,
    #     'north': room.n_to != 0,
    #     'south': room.s_to != 0,
    #     'east': room.e_to != 0,
    #     'west': room.w_to != 0,
    #     'title': room.title,
    #     'y_coor': room.y,
    #     'x_coor': room.x,
    #     'description': room.description,
    #     'players': room.playerNames(player_id)
    # } for  room in rooms], safe=False)


# @csrf_exempt
@api_view(["POST"])
def createworld(request):
    w = World()
    num_rooms = 144
    width = 12
    height = 12
    w.generate_rooms(width, height, num_rooms)
    w.print_rooms()