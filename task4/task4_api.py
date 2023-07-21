from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()  #automatically loads the environment variable file.
# Only if it is named as .env in the same directory as your python script.

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#The Spotify API allows you to query data like an artist's songs, albums, 
#various artists, albums and their top songs, etc.

#SPOTIFY API also allows you to control a specific user's spotify player and retrieve info about a user's top songs, etc.
#For getting this user specific information, one has to authenticate as user which is a quite
#complicated process and requires some special priviledges. (USER AUTHENTICATION)

#However, retrieving globally available info about artists, songs, albums, etc is done by authenticating
#as a client. (CLIENT AUTHENTICATION). We'll be doing this...

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    #We are concatenating client_id and client_secret in the specific format and encoding
    #it into a base64 object. This obj is converted into a string which is then concatenated with 
    #the URL to get CLIENT AUTHORIZED.


    url = "https://accounts.spotify.com/api/token" #this is available in the documentation.
    #This is the URL where POST request should be send to get client auth token.

    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    #This is also specified in the official documentation. This should be the header of our
    # POST request. Treat this like a rule.

    data = {"grant_type":"client_credentials"} #this should be the data to be send in the POST req.
    # Again, this is as per the documentation.

    result = requests.post(url, headers=headers, data=data)
    result_dict = result.json()
    token = result_dict["access_token"]
    return token   #Here you'll have the client auth token!!

#Now in every HTTP request to the API, THE header must be the following(containing client auth token)
def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

#Now in spotify api, we need every artits's id to search his/her tracks, albums, etc. Here we're defining this function which will give us an artist's id from his name.
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search" #the documentation that this the URL where we should send GET req.
    
    headers = get_auth_header(token)  #every HTTP req should include this header.
    
    query = f"?q={artist_name}&type=artist&limit=1" #it can be possible that there are multiple artists of the same name or no artists with the given name.
    #so we are just selecting the top result by limit=1

    query_url = url + query #standard rule as per doc.
    result = requests.get(query_url, headers=headers)
    result_dict = result.json()["artists"]["items"] #this will give us info. about 1 artist with that name.
    # To know more, print result.text to see the entire JSON response.

    if len(result_dict) == 0:
        print("No artist with this name exists!")
        return None

    return result_dict[0] #After viewing the response, you'll realise that this is 

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=IN"  #this URL, when hit with an HTTP GET req, returns top 10 songs of the artist
    #specified and country name passed as parameter.
    
    headers = get_auth_header(token)

    song_res = requests.get(url, headers=headers)
    song_dict = song_res.json()["tracks"]
    return song_dict

token_rec =  get_token()
artist_res = search_for_artist(token_rec, "The Weeknd")
artist_id = artist_res["id"]
songs = get_songs_by_artist(token_rec, artist_id)

for index, song in enumerate(songs):
    print(f"{index + 1}. {song['name']}")


