import requests

url = "https://trades-on-floor-and-otc-transactions.p.rapidapi.com/transactions/transactions-end-of-day/2020/2/4"

querystring = {"offset":"0","limit":"50","securityId":"1159029"}

headers = {
    'accept-language': "he-IL",
    'x-rapidapi-key': "d671270166msh8611bce22eed547p1ca53fjsna6de0b074846",
    'x-rapidapi-host': "trades-on-floor-and-otc-transactions.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)