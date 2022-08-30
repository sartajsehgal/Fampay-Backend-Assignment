from flask import Flask,jsonify,request
from flask_pymongo import pymongo
import fetch_videos_from_API
import threading
import database

app = Flask(__name__)

@app.route("/get_videos", methods=['GET'])

def get_videos():

    videos_info = database.db.VideosInfo

    offset = int(request.args['offset'])
    limit = int(request.args['limit'])

    starting_id = videos_info.find().sort('_id',pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']

    videos = videos_info.find({'_id' : {'$gte': last_id}}).sort('_id',pymongo.ASCENDING).limit(limit)

    all_videos = []

    for video in videos:
        video_dict={}
        if 'title' in video.keys():
            video_dict['title']=video['title']
        if 'description' in video.keys():
            video_dict['description']=video['description']
        if 'publishing_datetime' in video.keys():
            video_dict['publishing_datetime']=video['publishing_datetime']
        if 'thumbnail_urls' in video.keys():
            video_dict['thumbnail_urls']=video['thumbnail_urls']
        all_videos.append(video_dict)

    next_url = '/get_videos?limit=' + str(limit) + '&offset=' + str(offset + limit)
    prev_url = '/get_videos?limit=' + str(limit) + '&offset=' + str(min(0, offset - limit))

    return jsonify({'result': all_videos, 'prev_url': prev_url, 'next_url': next_url})


@app.route("/search_videos", methods=['GET'])

def search_videos():

    videos_info = database.db.VideosInfo

    query = request.args['query']

    videos = videos_info.find({'$or': [{'title': {'$eq': query}}, {'description' : {'$eq':query}}]})

    all_videos = []

    for video in videos:
        video_dict={}
        if 'title' in video.keys():
            video_dict['title']=video['title']
        if 'description' in video.keys():
            video_dict['description']=video['description']
        if 'publishing_datetime' in video.keys():
            video_dict['publishing_datetime']=video['publishing_datetime']
        if 'thumbnail_urls' in video.keys():
            video_dict['thumbnail_urls']=video['thumbnail_urls']
        all_videos.append(video_dict)

    return jsonify({'result': all_videos})


if __name__ == "__main__":
    # x = threading.Thread(target=fetch_videos_from_API.test)
    # x.start()
    app.run(ost="0.0.0.0", port=5000)
