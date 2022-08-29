from time import sleep
from flask import Flask,jsonify
import json
import googleapiclient.discovery
import googleapiclient.errors
# from pymongo import MongoClient
# import pymongo
from flask_pymongo import PyMongo
import urllib
import database

app = Flask(__name__)

# client = MongoClient('localhost',27017)
# db = client.Videos
# app.config['DEBUG']=True
# app.config['MONGO_URI'] = "mongodb+srv://sartaj16:"+urllib.parse.quote("Sartaj@2000")+"@cluster0.stns21q.mongodb.net/?retryWrites=true&w=majority"
# mongo = PyMongo(app)
# db = mongo.Videos

key = 'AIzaSyB4nXuAM5BZ5RsSSHRUpHsNiEEq19CWGK4'
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = key)
response=[]

def define_request(nextPageToken):
    request = youtube.search().list(
        part="snippet",
        order="date",
        publishedAfter="2022-08-28T00:00:00Z",
        q="cricket",
        pageToken=nextPageToken,
        maxResults=50
    )
    return request

@app.route("/", methods=['POST'])
def main():
    # try:
    #     for video in response['items']:
    #         video_info={}
    #         if video['snippet']:
    #             if video['snippet']['title']:
    #                 video_info['title'] = video['snippet']['title']
    #             if video['snippet']['description']:
    #                 video_info['description'] = video['snippet']['description']
    #             if video['snippet']['description']:
    #                 video_info['publishing_datetime'] = video['snippet']['publishedAt']
    #             if video['snippet']['thumbnails']:
    #                 video_info['thumbnail_urls'] = []
    #                 for key in video['snippet']['thumbnails'].keys():
    #                     video_info['thumbnail_urls'].append(video['snippet']['thumbnails'][key]['url'])
    #             status = database.db.VideosInfo.insert_one(video_info)
    #     return "Success"
    # except Exception as e:
    #     return json.dumps({'error' : str(e)})
    nextPageToken = ''
    while True:
        request = define_request(nextPageToken)
        response = request.execute()
        print(list(response.keys()))
        if 'nextPageToken' not in response.keys():
            break;
        else:
            nextPageToken = response['nextPageToken']
            for video in response['items']:
                video_info={}
                if video['snippet']:
                    if video['snippet']['title']:
                        video_info['title'] = video['snippet']['title']
                    if video['snippet']['description']:
                        video_info['description'] = video['snippet']['description']
                    if video['snippet']['description']:
                        video_info['publishing_datetime'] = video['snippet']['publishedAt']
                    if video['snippet']['thumbnails']:
                        video_info['thumbnail_urls'] = []
                        for key in video['snippet']['thumbnails'].keys():
                            video_info['thumbnail_urls'].append(video['snippet']['thumbnails'][key]['url'])
                    status = database.db.VideosInfo.insert_one(video_info)
            print("While Completed")
    return nextPageToken




# @app.route("/add_video",methods = ['POST'])
# def add_video():


if __name__ == "__main__":
  app.run()