import requests

# GET--------------------------------------------------------------------------------
# URL = 'http://localhost:8000/api/v1/reviews?page=1&limit=2'
# HEADERS = {'accept': 'application/json'}
# QUERYSET = {'page': 2, 'limit': 1}

# response = requests.get(URL, headers=HEADERS, params=QUERYSET)

# if response.status_code == 200:
#    print(response.headers)

#    if response.headers.get('content-type') == 'application/json':
#        reviews = response.json()
#        for review in reviews:
#            print(
#                f'score: {review.get("score")} - movie: {review.get("movie").get("title")} - review: {review.get("review")}')

##POST----------------------------------------------------------------
# URL = 'http://localhost:8000/api/v1/reviews'
# BODY={
#    'user_id': 1,
#    'movie_id':1,
#    'review': 'Peliculaintermedia donde ...........................................................................................',
#    'score': 3
# }
# response = requests.post(URL, json=BODY)
# if response.status_code==200:
#    print('Reseña creada de forma exitosa')
#    print(response.json()['id'])
# else:
#    print(response.content)

# PUT
# REVIEW_ID = 11
# URL = f'http://localhost:8000/api/v1/reviews/{REVIEW_ID}'
# BODY = {
#    'user_id': 1,
#    'movie_id': 1,
#    'review': 'Pelicula buena donde ...........................................................................................',
#    'score': 5
# }
# response = requests.put(URL, json=BODY)

# if response.status_code == 200:
#    print('Reseña modificada de forma exitosa')
#    print(response.json()['id'])
# else:
#    print(response.content)


##DELETE
# REVIEW_ID = 11
# URL = f'http://localhost:8000/api/v1/reviews/{REVIEW_ID}'

# response= requests.delete(URL)

# if response.status_code == 200:
#    print('Reseña borrada de forma exitosa')
#    print(response.json())
# else:
#    print(response.content)

# cookies
URL = 'http://localhost:8000/api/v1/users/'
USER = {
    "username": "User",
    "password": "Pass1234"
}

response = requests.post(URL + 'login', json=USER)

if response.status_code == 200:
    print(response.json())

    print(response.cookies)
    print(response.cookies.get_dict())

    user_id = response.cookies.get_dict().get('user_id')

    cookies = {'user_id': user_id}
    response = requests.get(URL + 'reviews', cookies=cookies)

    if response.status_code == 200:
        for review in response.json():
            print(f'{review.get("review")} - {review.get("score")}')
