from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

db = client.eulers

users = db.users
photos = db.photos

def add_user(name, surname, vkID):
	potential = users.find_one({'vkID': vkID})
	if not potential:
		users.insert_one({
			'name': name,
			'surname': surname,
			'vkID': vkID,
			'is_finished_photos': False
		})

def get_user(vkID):
	return users.find_one({'vkID': vkID})

def add_like_on_photo (userVKID, targetVKID):
	potential = photos.find_one({
		'userVKID': userVKID,
		'targetVKID': targetVKID
	})
	if not potential:
		photos.insert_one({
			'userVKID': userVKID,
			'targetVKID': targetVKID,
			'count': 1
		})
	# if already exists
	else:
		if is_finished_photos(targetVKID) == True:
			return False

		photo = photos.update_one({
			'userVKID': userVKID,
			'targetVKID': targetVKID,
		}, {
			'$inc': {
				'count': 1
			}
		})



def is_finished_photos (vkID):
	user = get_user(vkID)
	if not user:
		return False

	return user['is_finished_photos']


def set_is_finished_photos (targetVKID, flag):
	users.update_one({'vkID': targetVKID}, {
		'$set': {
			'is_finished_photos': flag
			}
		}
	)


