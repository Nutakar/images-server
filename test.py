import requests
import json
from PIL import Image
import base64
from io import BytesIO
import pytest

@pytest.fixture()
def generate_image():
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
    add_response = requests.post(url=url, data = json.dumps(payload), headers=headers)
    add_response_body = add_response.content.decode('ascii')
    return (
            add_response, 
            add_response_body, 
            img_str)


def test_delete_info(generate_image):

    del_response = requests.delete("http://localhost:8000/image/blue.jpg")
    del_response_body = del_response.content.decode('ascii')
    get_response = requests.get('http://localhost:8000/images/blue.jpg')
    assert del_response.status_code == 200
    assert get_response.status_code == 404
    assert del_response_body == '{"success":"image deleted"}\n'


def test_create_from_base64_code_200(generate_image):

    # get an image and compare it to the start image
    get_response = requests.get('http://localhost:8000/images/blue.jpg')
    check_base64 = base64.b64encode(get_response.content)

    # delete created image
    del_response = requests.delete('http://localhost:8000/image/blue.jpg')

    add_response = generate_image[0]
    add_response_body = generate_image[1]
    img_str = generate_image[2]

    assert add_response.status_code == 200
    assert get_response.status_code == 200
    assert check_base64 == img_str
    assert add_response_body == '{"success":"image created"}\n'
