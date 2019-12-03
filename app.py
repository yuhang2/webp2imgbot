from bottle import Bottle, request, response
from helpers import send_image, send_chat_action
application = Bottle()

@application.route('/', method='POST')
def message_handler():
    if "message" not in request.json.keys():
        return '{}'
    message = request.json['message']
    chat_id = message['chat']['id']
    sticker_file_id = None
    convert_png = False
    message_id = 0
    if 'sticker' in message.keys() and 'emoji' not in message['sticker'].keys() and (message['sticker']['width'] != 512 and message['sticker']['height'] != 512):
        sticker_file_id = message['sticker']['file_id']
        message_id = message['message_id']
    if 'reply_to_message' in message.keys() and \
        "text" in message.keys() and \
        "@autowebp2imgbot" in message["text"].lower() and \
        'sticker' in message['reply_to_message'].keys():
        sticker_file_id = message['reply_to_message']['sticker']['file_id']
        message_id = message['reply_to_message']['message_id']
        if "png" in message["text"].lower():
            convert_png = True
    if sticker_file_id is not None:
        send_chat_action(chat_id,'upload_photo')
        send_image(chat_id,message_id,sticker_file_id,convert_png)
    response.type = 'application/json'
    response.status = 200
    return '{}'

application.run(server="paste")
