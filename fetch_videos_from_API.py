from time import sleep
import googleapiclient.discovery
import googleapiclient.errors
import database

key = 'AIzaSyB4nXuAM5BZ5RsSSHRUpHsNiEEq19CWGK4'
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = key)

def define_request(publishedAfter):
    request = youtube.search().list(
        part="snippet",
        order="date",
        publishedAfter=publishedAfter,
        q="cricket",
        maxResults=50
    )
    return request

def store_videos_in_db(response):
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
            database.db.VideosInfo.insert_one(video_info)

def test():
    request = define_request("2022-08-28T00:00:00Z")
    response = request.execute()
    latest_video_datetime = response['items'][0]['snippet']['publishedAt']
    store_videos_in_db(response)
    while True:
        request = define_request(latest_video_datetime)
        response = request.execute()
        store_videos_in_db
        sleep(10)
    
        