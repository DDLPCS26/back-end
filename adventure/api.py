from .world_creator import World
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    Room.objects.all().delete()
    created_rooms = World()
    num_rooms = 144
    width = 12
    height = 12
    created_rooms.generate_rooms(width, height, num_rooms)

    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid

    player.current_room = Room.objects.first().id
    room = Room.objects.first()
    players = room.playerNames(player_id)

    return JsonResponse({
        'uuid': uuid, 
        'name':player.user.username, 
        'title':room.title, 
        'description':room.description, 
        'players':players}, safe=True)


@api_view(["POST"])
def move(request):
    dirs={
        "n": "north", 
        "s": "south", 
        "e": "east", 
        "w": "west"}

    reverse_dirs = {"n": "south", 
        "s": "north", 
        "e": "west", 
        "w": "east"}

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

        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)

        return JsonResponse({
            'name':player.user.username, 
            'title':nextRoom.title, 
            'description':nextRoom.description, 
            'players':players, 
            'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)

        return JsonResponse({
            'name':player.user.username, 
            'title':room.title, 
            'description':room.description, 
            'players':players, 
            'error_msg':"You cannot move that way."}, safe=True)

@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)


#implementing GET - You will also need to implement a GET rooms API endpoint for clients to fetch all rooms to display a map on the frontend.
@csrf_exempt
@api_view(["GET"])
def rooms(request):
    rooms = Room.objects.all()
    room_data = []

    for room in rooms:
        room_data.append(
            {"id": room.id, 
            "title": room.title, 
            "description": room.description, 
            "north": room.n_to, 
            "east": room.e_to, 
            "south": room.s_to, 
            "west": room.w_to, 
            "x": room.x_coor, 
            "y": room.y_coor}
        )
    return JsonResponse({
        'num_rooms': len(room_data), 
        'rooms': room_data}, safe=True)