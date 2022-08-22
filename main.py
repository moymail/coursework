import json
import requests


class VK:
    url = 'https://api.vk.com/method/'
    version = '5.131'
    with open('vk_token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()

    def __init__(self, vk_id):
        self.vk_id = vk_id

    def photos_get(self):
        photos_url = self.url + 'photos.get'
        photos_params = {'access_token': self.vk_token,
                         'v': self.version,
                         'count': count,
                         'user_id': self.vk_id,
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
    ya_url = "https://cloud-api.yandex.net/v1/disk/resources/"

    def __init__(self, token):
        self.token = token
        self.ya_folder_name = input('Введите название папки ')

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}

    def add_photo_folder(self, folder_name):
        headers = self.get_headers()
        params = {'path': folder_name}
        response = requests.put(self.ya_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'\nПапка {folder_name} создана\n')
            return folder_name
        elif response.status_code == 409:
            print(f'\nПапка {folder_name} уже существует.\n')
            return folder_name
        elif response.status_code >= 400:
            print(f'Ошибка {response.status_code}')
        return folder_name

    def get_vk_photo(self, file):
        vk_photo_file = []
        for value in file:
            vk_photo_file.append(dict([('file_name', value), ('size', file[value][1])]))
        with open('vk_photo.json', 'w') as f:
            json.dump(vk_photo_file, f)
        return vk_photo_file

    def upload_photo(self, file):
        upload_url = self.ya_url + "upload"
        self.add_photo_folder(self.ya_folder_name)
        headers = self.get_headers()
        progress_bar = 1
        for photo in file:
            params = {'url': file[photo][0], 'path': f'{self.ya_folder_name}/{photo}.jpg'}
            response = requests.post(upload_url, headers=headers, params=params)
            print(f'Загрузка {progress_bar} фото из {len(file)}, код ответа: {response.status_code}')
            progress_bar += 1
            if response.status_code >= 400:
                print(f'Ошибка загрузки! Код ошибки: {response.status_code}')
            else:
                print('Загрузка завершена')
        return


if __name__ == '__main__':
    user_id = VK(str(input('id пользователя VK: ')))
    count = int(input('Введите количество фото: '))
    with open('yandex_token.txt', 'r') as file_object_1:
        ya_token = file_object_1.read().strip()
    ya_disk = YaDisk(ya_token)
    ya_disk.upload_photo(user_id.photos_get())
