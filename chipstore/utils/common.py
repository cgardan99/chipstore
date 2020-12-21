from time import strftime


def get_image_directory_path(instance, filename):
    date_str = strftime('%Y-%m-%d-%H-%M-%S')
    return f'{date_str}-{filename}'
