#import sys
#import database
#sys.path.append('/home/netcamo/css/module4/Assignment/database')
from flask import Flask, jsonify, request, Response
from flask_mongoengine import MongoEngine
from database.db import initialize_db
from database.models import  Photo,Album
from flask import request, jsonify
from bson.objectid import ObjectId
#from database.db import initialize_db
#from database.models import Photo, Album
import json
import os
import urllib
import base64
import codecs


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://mongo/flask-database'
    }
db = initialize_db(app)

def object_list_as_id_list(obj_list):
    return list( map(lambda obj: str(obj.id), obj_list  ))
def str_list_to_objectid(str_list):
    return list(map(lambda str_item: ObjectId(str_item),str_list ))

if __name__ == '__main__':
        app.run()




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@app.route('/listPhoto', methods=['POST'])
def add_photo():
    posted_image =request.files['file']
    posted_data=request.form.to_dict() #"use request.form to obtain the associated immutable dict and convert it into dict"
    default_album=Album.objects(name="Default")
    if (len(default_album)==0) :
        default_album=Album(name="Default").save()    
        print("Saved")

    albums=["Default"]; 
    albums_id=[]
    for album in albums:
        albums_id.append(str(Album.objects(name=album)[0].id))
   

    print(f"{bcolors.FAIL}START COMMENT{bcolors.ENDC}")
    print(albums_id)
    print(f"{bcolors.WARNING}END COMMENT{bcolors.ENDC}")
    
    photo = Photo(**posted_data, image_file=posted_image)
    if "tags" in posted_data.keys():
        photo.tags=list(map(str.strip, json.loads( posted_data['tags'])))

    photo.albums=str_list_to_objectid(albums_id)
    print(photo.tags)
    photo.save()
    output = {'message': "Photo successfully created", 'id': str(photo.id)}
    status_code = 201
    return output,status_code 
    
    


@app.route('/listPhoto/<photo_id>', methods=['GET', 'PUT', 'DELETE'])
def get_photo_by_id(photo_id):
    if request.method == "GET":
        photo = Photo.objects.get(id=photo_id)
        "Get the photo with photo_id from the db"
        if photo:
            ## Photos should be encoded with base64 and decoded using UTF-8 in all GET requests with an image before sending the image as shown below
            base64_data = codecs.encode(photo.image_file.read(), 'base64')
            image = base64_data.decode('utf-8')
            ##########
            output = {"name": photo.name, "location":photo.location ,
            "tags":photo.tags,"albums" : photo.albums , "file" : image} 
            status_code = 200
            return output, status_code
    elif request.method == "PUT":
        photo=Photo.objects(id=photo_id)
        body = request.get_json()
        # if "albums" in keys:
        #     # print(f"{bcolors.FAIL}START COMMENT{bcolors.ENDC}")
        #     # print(body["albums"])
        #     # print(f"{bcolors.WARNING}END COMMENT{bcolors.ENDC}")
        #     albums=["Default"]
        #     for al in body["albums"]:
        #         if(len(Album.objects(name=al))==0):
        #             Album(name=al).save()
        #         albums.append(al)
        #     albums_id=[]
        #     for album in albums:
        #         albums_id.append(str(Album.objects(name=album)[0].id))
        #     body["albums"]=str_list_to_objectid(albums_id)
        #     print(body["albums"])
        
        # photo.albums
        #body["albums"]=  # ALBUM duzelt
        
        albums=["Default"]; 
        albums_id=[]
        for album in albums:
            albums_id.append(str(Album.objects(name=album)[0].id))
        print(Album.objects(name=album)[0].id)
        body["albums"]=str_list_to_objectid(albums_id)
        Photo.objects.get(id=photo_id).update(**body)
        output = {'message': "Photo successfully updated", 'id': str(photo_id)}
        status_code = 200
        return output,status_code 
        
    elif request.method == "DELETE":
        photo = Photo.objects.get_or_404(id=photo_id)
        photo.delete()
        output = {'message': "Photo successfully deleted", 'id': str(photo_id)}
        status_code = 200
        return output,status_code 
        

@app.route('/listPhotos', methods=['GET'])
def get_photos():
    
    tag =request.args.get("tag") #"Get the tag from query parameters" 
    albumName =request.args.get("albumName") #"Get albumname from query parameters"
    if albumName is not None:
        albums=Album.objects(name=albumName)
        photo_objects=Photo.objects(albums__in=albums)
        photo_objects=[]
        photo_objects.append(Photo.objects()[0])
        photo_objects.append(Photo.objects()[1])
        
        
    elif tag is not None:
        photo_objects=Photo.objects(tags=tag)
    else:
        photo_objects=Photo.objects
        
    photos = []
    for photo in photo_objects:
        base64_data = codecs.encode(photo.image_file.read(), 'base64')
        image = base64_data.decode('utf-8')
        photos.append({'name': photo.name , 'location': photo.location, 
         "albums": photo.albums , "id" : object_list_as_id_list ([photo]) , 
         "file" : image
         })
    return jsonify(photos), 200







@app.route('/listAlbum', methods=['POST'])
def add_album():
    posted_data=request.form.to_dict() #"use request.form to obtain the associated immutable dict and convert it into dict"
    print(f"{bcolors.FAIL}START COMMENT{bcolors.ENDC}")
    print(posted_data)
    print(f"{bcolors.WARNING}END COMMENT{bcolors.ENDC}")
    
        
    album = Album(**posted_data)
    album.save()
    output = {'message': "Album successfully created", 'id': str(album.id)}
    status_code = 201
    return output,status_code 
    return "Got it" , 201

@app.route('/listAlbum/<album_id>', methods=['GET', 'PUT', 'DELETE'])
def get_album_by_id(album_id):
    if request.method == "GET":
        album = Album.objects.get(id=album_id)
        
        if album:
            print(f"{bcolors.FAIL}START COMMENT{bcolors.ENDC}")
            output = {"id": str(album_id), "name": album.name }
            status_code = 200
            return output, status_code

    elif request.method == "PUT":
        album=Album.objects(id=album_id)
        body = request.get_json()
        print(f"{bcolors.FAIL}START COMMENT{bcolors.ENDC}")
        album.name=body['name']
        print({"name": album.name})
        print(f"{bcolors.WARNING}END COMMENT{bcolors.ENDC}")
        keys = body.keys()
    
        Album.objects.get(id=album_id).update(**body)
        output = {'message': "Album successfully updated", 'id': str(album_id)}
        status_code = 200
        return output,status_code 
        
    elif request.method == "DELETE":
        album = Album.objects.get_or_404(id=album_id)
        album.delete()
        output = {'message': "Album successfully deleted", 'id': str(album_id)}
        status_code = 200
        return output,status_code 
        