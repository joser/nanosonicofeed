import webapp2
import time
from feedformatter import Feed
import urllib2
import json
from pprint import pprint
import datetime

SOUNDCLOUD_CLIENTID = "your_soundcloud_clientid"
VIDAS_URI = "http://api.soundcloud.com/playlists/21726859.json?client_id="+SOUNDCLOUD_CLIENTID
ESTAPASANDO_URI = "http://api.soundcloud.com/playlists/22278078.json?client_id="+SOUNDCLOUD_CLIENTID

class VidasEjemplaresHandler(webapp2.RequestHandler):

    def get(self):
        data = get_soundcloud_info(VIDAS_URI)
        rss_feed = create_feed(data) 
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.write(rss_feed)

class EstaPasandoHandler(webapp2.RequestHandler):

    def get(self):
        data = get_soundcloud_info(ESTAPASANDO_URI)
        rss_feed = create_feed(data) 
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.write(rss_feed)

def create_feed(data):
	# Create the feed
	feed = Feed()

	# Set the feed/channel level properties
	feed.feed["title"] = data["title"]
	feed.feed["link"] = data["permalink_url"]
	feed.feed["author"] = data["user"]["username"]
	feed.feed["description"] = data["description"]
	feed.feed["image"] = data["tracks"][0]["artwork_url"]

	# Create an item
	for track in data["tracks"]:
	    item = {} # reset item object
	    pubDate = datetime.datetime.strptime(track["created_at"][:-6], '%Y/%m/%d %H:%M:%S')
	    item["title"] = track["title"]
	    item["enclosure"] = (
	        track["download_url"]+"?client_id="+SOUNDCLOUD_CLIENTID,
	        str(track["original_content_size"]))
	    item["description"] = track["description"]
	    item["guid"] = str(track["id"])
	    item["pubDate"] = pubDate.timetuple()
	    # Add item to feed
	    feed.items.append(item)

	# Print the feed to stdout in various formats
	return feed.format_rss2_string()

def get_soundcloud_info(uri):
    json_data = urllib2.urlopen(uri).read()
    data = json.loads(json_data)
    return data


application = webapp2.WSGIApplication([
    (r'/vidas-ejemplares-de-alaska', VidasEjemplaresHandler),
    (r'/esta-pasando', EstaPasandoHandler)
], debug=True)
