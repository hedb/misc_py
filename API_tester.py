
import urllib.request



# url = 'https://api.dialogflow.com/v1/intents?v=20150910'
url = 'https://api.dialogflow.com/v1/query?v=20150910'

I    "timezone": "America/New_York"
  }
data = data.encode('ascii')

req = urllib.request.Request(url, data, headers)
response = urllib.request.urlopen(req)
http_status = response.getcode()
data = response.read()  # a `bytes` object
text = data.decode('utf-8', errors='ignore')
print(text)