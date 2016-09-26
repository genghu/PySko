import json

import urllib 
import urlparse
import oauth2 as oauth
import pprint

REDIRECT_URI = "http://ccnu.x-in-y.com:8889/redmineCallback"

# Create your consumer with the proper key/secret.
consumer_key="rfszuzHlfUaa5D5n4cLGUwLMV8mWn7HAii1VuxBI" 
consumer_secret="IPuZtbSq4dge35W5hjTvO5B7I5EKvpdjDDKM5Fvo"

consumer = oauth.Consumer(consumer_key, consumer_secret)

# Request token URL for Twitter.
request_token_url = "http://ccnu.x-in-y.com:3000/oauth/request_token"
access_token_url = 'http://ccnu.x-in-y.com:3000/oauth/access_token'
authorize_url = 'http://ccnu.x-in-y.com:3000/oauth/authorize'
userinfo_url = 'http://ccnu.x-in-y.com:3000/oauth/user_info'
currentuser_url = 'http://ccnu.x-in-y.com:3000/oauth/current_user'
test_url = 'http://ccnu.x-in-y.com:3000/oauth/test_url'
uloggedin_url = 'http://ccnu.x-in-y.com:3000/oauth/user_logged_in'


client1 = oauth.Client(consumer)
resp1, content1 = client1.request(request_token_url, "GET")
request_token = dict(urlparse.parse_qsl(content1))
print 'Req token: ',request_token
url = authorize_url+'?oauth_token='+request_token['oauth_token']

print 'Open this and Allow: ', url 

oauth_verifier = raw_input("Enter auth verifier: ")
token = oauth.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client2 = oauth.Client(consumer,token)
resp2, content2 = client2.request(access_token_url, "POST")
access_token = dict(urlparse.parse_qsl(content2))
print 'Acces token: ',access_token
