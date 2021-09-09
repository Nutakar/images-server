'''Testing functions from flask_server'''

import json
import base64
from io import BytesIO
from PIL import Image
import pytest
import requests

@pytest.fixture()
def generate_image():

    '''generate an image called "blue.jpg" for each test'''

    # create an image, encode to base64
    img = Image.new('RGB', (60, 30), color='blue')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    new_img_str = img_str.decode('ascii')

    # add an image to /images
    headers = {'content-Type' : 'application/json'}
    url = 'http://localhost:8000/image'
    payload = [{'name' : 'blue.jpg', 'img_base64' : new_img_str}]
    add_response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    add_response_body = add_response.content.decode('ascii')
    return (add_response,
            add_response_body,
            img_str)


def test_show_image(generate_image):

    '''tests func show_image from flask_server'''

    get_response = requests.get('http://localhost:8000/images/blue.jpg')
    check_base64 = base64.b64encode(get_response.content)
    img_str = generate_image[2]
    requests.delete('http://localhost:8000/image/blue.jpg')

    assert check_base64 == img_str
    assert get_response.status_code == 200


def test_show_all_images_info(generate_image):

    '''tests func show_all_images_info from flask_server'''

    get_all_request = requests.get('http://localhost:8000/image')
    get_all_request_content = get_all_request.content.decode('ascii')
    requests.delete('http://localhost:8000/image/blue.jpg')

    assert "blue.jpg" in get_all_request_content
    assert get_all_request.status_code == 200


def test_delete_image(generate_image):

    '''tests func delete_image from flask_server'''

    del_response = requests.delete("http://localhost:8000/image/blue.jpg")
    del_response_body = del_response.content.decode('ascii')
    get_response = requests.get('http://localhost:8000/images/blue.jpg')

    assert del_response.status_code == 200
    assert get_response.status_code == 404
    assert del_response_body == '{"success":"image deleted"}\n'


def test_create_from_base64(generate_image):

    '''tests func create_from_base64 from flask_server'''

    # get an image and compare it to the start image
    get_response = requests.get('http://localhost:8000/images/blue.jpg')
    check_base64 = base64.b64encode(get_response.content)
    requests.delete('http://localhost:8000/image/blue.jpg')

    add_response = generate_image[0]
    add_response_body = generate_image[1]
    img_str = generate_image[2]

    assert add_response.status_code == 200
    assert get_response.status_code == 200
    assert check_base64 == img_str
    assert add_response_body == '{"success":"image created"}\n'
