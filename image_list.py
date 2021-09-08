import os
import time
import base64

def get_list_of_files(route='/images'):

    '''list all images with name, size in kB and last modification date'''

    image_list = os.listdir(route)
    all_files = []
    info = {}
    for i in image_list:
        full_path = os.path.join(route, i)
        if os.path.isdir(full_path):
            all_files.append(get_list_of_files(full_path))
        else:
            size = round(os.path.getsize(full_path)/1000, 2)
            times = os.path.getmtime(full_path)
            modification_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times))
            info[i] = {'size' : size, 'date' : modification_time}
    return info


def remove(name):

    '''remove image by it's name '''

    path = '/images/' + name
    os.remove(path)
    return {'success' : 'image deleted'}


def make_image_base64(name, str_in_base64):

    ''' create new image by base64 string '''

    with open(f'/images/{name}', 'wb') as decoded:
        decoded.write(base64.b64decode(str_in_base64))
    return {'success' : 'image created'}
