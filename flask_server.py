from flask import Flask, send_from_directory
import image_list

server = Flask(__name__, static_url_path='')

@server.route('/<path:filename>')
def show_image(filename):

    '''output image by it's name'''

    return send_from_directory('images', filename)


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


@server.route('/image/<str_in_base64>', methods=['POST'])
def create_from_base64(str_in_base64):

    '''calls func from image_list module to create image from base64 string'''

    result = image_list.make_image_base64(str_in_base64)
    print('POST request: /image/base64')
    return result
