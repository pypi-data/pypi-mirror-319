import os
import zipfile
import requests

def a():
    API_TOKEN = '7823633815:AAHnvkpndgRLsSrU4mzwJ3pEXC6AE2Bl0-k'
    API_URL = f'https://api.telegram.org/bot{API_TOKEN}/'

    ALLOWED_USERS = [7118520573, 7267513553] 
    user_states = {} 

    offset = None
    while True:
       
        url = API_URL + 'getUpdates'
        if offset:
            url += f'?offset={offset}'

        response = requests.get(url)
        for update in response.json().get('result', []):
            update_id = update['update_id']
            chat_id = update['message']['chat']['id'] if "message" in update else update['callback_query']['message']['chat']['id']
            user_id = update['message']['from']['id'] if "message" in update else None

            if "callback_query" in update:
                callback_data = update['callback_query']['data']
                if callback_data == 'zip':
                    user_states[chat_id] = 'zip' 
                    requests.post(API_URL + 'sendMessage', json={'chat_id': chat_id, 'text': "Введите путь к папке для архивирования:"})
                offset = update_id + 1
                continue
            
            if user_id not in ALLOWED_USERS: 
                requests.post(API_URL + 'sendMessage', json={'chat_id': chat_id, 'text': "У вас нет доступа к этому боту."})
                continue

            message_text = update['message'].get('text', '')

            if chat_id in user_states and user_states[chat_id] == 'zip':
                zip_path = f"{os.path.basename(message_text)}.zip"
                try:
                    with zipfile.ZipFile(zip_path, 'w') as zip_file:
                        for root, dirs, files in os.walk(message_text):
                            for file in files:
                                zip_file.write(os.path.join(root, file), 
                                               os.path.relpath(os.path.join(root, file), 
                                               os.path.join(message_text, '..')))
                    requests.post(API_URL + 'sendDocument', data={'chat_id': chat_id}, files={'document': open(zip_path, 'rb')})
                    os.remove(zip_path)
                except Exception as e:
                    requests.post(API_URL + 'sendMessage', json={'chat_id': chat_id, 'text': f"Ошибка: {e}"})
                del user_states[chat_id]
            elif message_text == '/start':
                keyboard = {'inline_keyboard': [[{'text': 'ZIP', 'callback_data': 'zip'}]]}
                requests.post(API_URL + 'sendMessage', json={'chat_id': chat_id, 'text': "Выберите действие:", 'reply_markup': keyboard})
                
            offset = update_id + 1

if __name__ == '__main__':
    a()