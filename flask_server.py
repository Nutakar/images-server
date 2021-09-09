from flask import Flask, send_from_directory, request
import image_list

server = Flask(__name__, static_url_path='')

@server.route('/images/<filename>')
def show_image(filename):

    '''output image by it's name'''

    print(f'GET request: /images/{filename}')
    return send_from_directory('/images', filename)


@server.route('/image', methods=['GET'])
def show_all_images_info():

    '''cals func to output info about all images in JSON'''

    result = image_list.get_list_of_files()
    print('GET request: /image')
    return result


@server.route('/image/<name>', methods=['DELETE'])
def delete_image(name):

    '''calls func from image_list module to delete image by it's name'''

    result = image_list.remove(name)
    print(f'DELETE request: /image/{name}')
    return result


@server.route('/image', methods=['POST'])
def create_from_base64():

    '''calls func from image_list module to create image from base64 string'''
    request_data = request.get_json()
    for dict in request_data:
        name = dict['name']
        str_in_base64 = dict['img_base64']

    result = image_list.make_image_base64(name, str_in_base64)
    print('POST request: /image/base64')
    return result
