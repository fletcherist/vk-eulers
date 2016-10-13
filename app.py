import vk_api
from config import login, password, target_id
import pprint

vk_session = vk_api.VkApi(login, password)

try:
    vk_session.authorization()
except vk_api.AuthorizationError as error_msg:
    print(error_msg)

vk = vk_session.get_api()

response = vk.users.get(user_id = target_id)
print('Analyzing: %s' % response[0]['first_name'] + ' ' + response[0]['last_name'])
print('\n')

# response = vk.friends.get(user_id = target_id)
# print(response)

# print(friends)
photos_request = vk.photos.getAll(
	owner_id = target_id,
	photo_sizes = 0,
	count = 200
)
photos = photos_request['items']
count = photos_request['count']

# photo_id = photos[0]['id']
photo = photos[0]

likers = {}
def get_likes (owner_id, item_id):
	likes = vk.likes.getList(
		type = 'photo',
		owner_id = owner_id,
		item_id = item_id
	)
	print ('found %s likes' % likes['count'])
	return likes['items']

def analyze_likes (likes):
	for like in likes:
		if (like not in likers):
			likers[like] = 1
		else:
			likers[like] = likers[like] + 1	

likes = get_likes(photo['owner_id'], photo['id'])
analyze_likes(likes)
pprint.pprint(likers)

# for photo in photos:
# 	print(photo['id'])
# print(len(photos))
# print(photos)