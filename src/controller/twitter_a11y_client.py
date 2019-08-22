import datetime as dt
import arrow

import requests

API_ROOT = 'https://image-description-backend.herokuapp.com'

pending_requests = {}

def request_alt_for_tweet(tweet):
    created_at = arrow.get(tweet['created_at'], "ddd MMM DD H:m:s Z YYYY", locale='en')
    data = {
        "tweetId": tweet['id_str'],
        "authorId": tweet['user']['id_str'],
        "postText": tweet['full_text'], 
        "time": created_at.isoformat()
    }
    imgs = 0
    imageUrls = []
    print(tweet)
    if "extended_entities" in tweet and "media" in tweet["extended_entities"]:
        print(tweet["extended_entities"]["media"])
        for z in tweet["extended_entities"]["media"]:
            if z["type"] == "photo":
                data["imageUrl"+str(imgs)] = z["media_url"]
                imageUrls.append(z["media_url"])
                if "ext_alt_text" in z and z["ext_alt_text"] != None:
                    data["alt"+str(imgs)]
                imgs += 1
    if not imgs:
        return []
    if tweet['id_str'] not in pending_requests:
        pending_requests[tweet['id_str']] = (data)
    print("requesting data from twitter A11y!", tweet['id_str'])
    r = requests.post(API_ROOT + '/create', data = data)
    response = r.json()
    image_descriptions = [response[u] for u in imageUrls]
    return image_descriptions