import requests

def song_and_singer(): #Функция выполняет поиск песен и артистов с похожими именами
	text = input('Enter the some words of name: ')
	url = f"https://shazam.p.rapidapi.com/search"
	querystring = {"term": text, "locale": "en-US", "offset": "0", "limit": "5"}
	response = get_response(url, querystring)
	all_response = response.json()

	key_response = all_response['tracks']['hits']

	for k in key_response:
		print(k['track']['share']['subject'])
		href = k['track']['share']['href']
		print(f'Href to Shazam: {href}\n')

	choice()


def get_response(url, querystring):

	headers = {
		"X-RapidAPI-Key": "65e8946b8fmsh3232f9c5a11906dp1c5ef0jsn87b958a3c09f",
		"X-RapidAPI-Host": "shazam.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	return response


def top_ten_songs(): # Выполняет поиск топ 10 песен исполнителя
	url = "https://shazam.p.rapidapi.com/search"
	singer = input('Enter the name of singer: ')
	querystring = {"term": singer, "locale": "en-US", "offset": "0", "limit": "1"}

	response = get_response(url, querystring)
	all_response = response.json()
	artist_name = all_response['artists']['hits'][0]['artist']['adamid']

	url = "https://shazam.p.rapidapi.com/artists/get-top-songs"
	querystring = {"id": artist_name, "l": "en-US"}

	response = get_response(url, querystring)
	top_songs = response.json()['data']
	artist_name = top_songs[0]['attributes']['artistName']
	print(f'\nGroup: {artist_name}')
	numbers_of_songs = list(range(1, 21))
	for i, v in zip(top_songs, numbers_of_songs):
		name_of_song = i['attributes']['name']
		date_of_relise = i['attributes']['releaseDate']
		print(f'{v}. Name of song: {name_of_song}')
		print(f'Date of relise: {date_of_relise}\n')

	choice()

def list_recomend(): # Предоставляет список из 20 рекомендаций по названию одной песни
	url = "https://shazam.p.rapidapi.com/search"
	song = input('Enter the name of song: ')
	querystring = {"term": song, "locale": "en-US", "offset": "0", "limit": "5"}

	response = get_response(url, querystring)
	resp = response.json()['tracks']['hits']
	for i in range(len(resp)):
		res = resp[i]["track"]["share"]["subject"]
		ans = input(f'Search recommendations for this song? {res}\n yes/no: ')
		if ans == 'yes':
			key_of_the_track = resp[i]['track']['key']
			print(key_of_the_track)
			url = "https://shazam.p.rapidapi.com/songs/list-recommendations"

			querystring = {"key": key_of_the_track, "locale": "en-US"}

			response = get_response(url, querystring)
			if response.json() == {}:
				print("Sorry, we can't create list_recomendation..\n")
				choice()
			recomend_list = response.json()['tracks']

			numbers = list(range(1, 21))
			print(f'Key of the track: {key_of_the_track}\n')
			for num, track in zip(numbers, recomend_list):
				track_share = track['share']['subject']
				print(f'{num}. {track_share}')

			choice()

		else:
			if res == response.json()['tracks']['hits'][-1]['track']['share']['subject']:
				print('Sorry.. We can\'t find your song.. Try again?!')
				list_recomend()
			else:
				continue


def choice():
	print('Select the choice: \n\
		  1. Find song and artist name\n\
		  2. Top 10 songs of specified artist\n\
		  3. List recomendations')
	enter = int(input('Integer: '))
	if enter == 1:
		song_and_singer()
	elif enter == 2:
		top_ten_songs()
	elif enter == 3:
		list_recomend()
	else:
		choice()

choice()