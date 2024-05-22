import os


def get_file_path(relative_path, base_file):
    # Получение абсолютного пути к базовому файлу
    base_dir = os.path.dirname(os.path.abspath(base_file))

    # Формирование полного пути к целевому файлу
    file_path = os.path.join(base_dir, relative_path)
    return file_path
