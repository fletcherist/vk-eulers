import vk_api
from config import login, password, target_id
import pprint
import time
from math import ceil 

vk_session = vk_api.VkApi(login, password)

try:
    vk_session.authorization()
except vk_api.AuthorizationError as error_msg:
    print(error_msg)

vk = vk_session.get_api()



def get_user(target_id):
	response = vk.users.get(user_id = target_id)
	user = response[0]
	return user

def print_user(user):
	print_string = 'Analyzing: %s' % user['first_name'] + ' ' + user['last_name']
	print(print_string)
	print('-' * len(print_string))

def get_photos(target_id):
	photos_request = vk.photos.getAll(
		owner_id = target_id,
		photo_sizes = 0,
		count = 200
	)
	return {
		'photos': photos_request['items'],
		'count': photos_request['count']
	}

def get_friends():
	response = vk.friends.get(user_id = target_id)
	print(response)
	# print(friends)

def get_likes(owner_id, item_id):
	likes = vk.likes.getList(
		type = 'photo',
		owner_id = owner_id,
		item_id = item_id
	)
	# print ('found %s likes' % likes['count'])
	return likes['items']

def analyze_likes(likes):
	for like in likes:
		if (like not in likers):
			likers[like] = 1
		else:
			likers[like] = likers[like] + 1	

def sort_likers():
	# ??? how it works
	# fucking magic
	sorted_likers = [(k,v) for v,k in sorted(
	    	[(v,k) for k,v in likers.items()]
		)
	]
	return sorted_likers

def print_all_this_shit(sorted_likers):
	for i in range(0, 5):
		# the last element
		# + range counter
		range_counter = 5 - i
		maxlikers = len(sorted_likers) - 1 - range_counter
		if maxlikers < 6:
			break
		user_id = sorted_likers[maxlikers][0]
		count = sorted_likers[maxlikers][1]
		percent  = ceil(count / (len(photos) / 100))
		print('id%s - shows interest of equal  %s percent' %(user_id, percent))



user = get_user(target_id)
print_user(user)

user_photos = get_photos(target_id)
photos = user_photos['photos']
count = user_photos['count']

likers = {}
sorted_likers = {}

for index, photo in enumerate(photos):
	print('Analyzing photo %s of %s' % (index, len(photos)))
	likes = get_likes(photo['owner_id'], photo['id'])
	analyze_likes(likes)
	sorted_likers = sort_likers()
	print_all_this_shit(sorted_likers)

	# to avoid too many requests
	# need a small latency between them
	time.sleep(.3)
