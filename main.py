import json
import requests



class VK:
    url = 'https://api.vk.com/method/'
    version = '5.131'
    with open('vk_token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()

    def __init__(self, id):
        self.id = id

    def photos_get(self):
        photos_url = self.url + 'photos.get'
        photos_params = {'access_token': self.vk_token,
                         'v': self.version,
                         'count': count,
                         'user_id': self.id,
                         'album_id': 'profile',
                         'extended': 1
                         }
        result = requests.get(photos_url, photos_params).json()
        photo_dict = {}
        for photo in result['response']['items']:
            if str(photo['likes']['count']) not in photo_dict:
                photo_dict[str(photo['likes']['count'])] = [photo['sizes'][-1]['url']]
                photo_dict[str(photo['likes']['count'])].append(photo['sizes'][-1]['type'])
            else:
                photo_dict[f"{photo['likes']['count']}_{photo['date']}"] = [photo['sizes'][-1]['url']]
                photo_dict[f"{photo['likes']['count']}_{photo['date']}"].append(photo['sizes'][-1]['type'])
        return photo_dict


class YaDisk:
    with open('yandex_token.txt', 'r') as file_object_1:
        token = file_object_1.read().strip()

    def __init__(self, token):
        self.token = token

    def headers(self):
        return {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}

    def vk_photo(self, file):
        vk_photo_file = []
        for value in file:
            vk_photo_file.append(dict([('file_name', value), ('size', file[value][1])]))
        with open('vk_photo.json', 'w') as f:
            json.dump(vk_photo_file, f)
        return vk_photo_file

    def photo_folder(self):
        folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.headers()
        params = {'path': 'vk_photo'}
        response = requests.put(folder_url, headers=headers, params=params)
        return response.json()

    def upload(self, file):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.photo_folder()
        headers = self.headers()
        progress_bar = 1
        for photo in file:
            params = {'url': file[photo][0], 'path': f'photos/{photo}.jpg'}
            response = requests.post(upload_url, headers=headers, params=params)
            print(f'Загрузка {progress_bar} фото из {len(file)}, код ответа: {response.status_code}')
            progress_bar += 1
            if response.status_code >= 400:
                print(f'Ошибка загрузки! Код ошибки: {response.status_code}')
            else:
                print('Загрузка завершена')
        return self.photo_folder(file)


#
if __name__ == '__main__':
    vk_id = VK(str(input('id пользователя VK: ')))
    count = int(input('Введите количество фото: '))
    yadisk = YaDisk(YaDisk.token)
    print(yadisk.upload(vk_id.photos_get()))


