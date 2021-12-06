import os


def travel_python_path_file(file_path: str) -> list:
    file_list = []
    for parent, dir_names, filenames in os.walk(file_path):
        for filename in filenames:
            if filename.endswith(".py") and \
                    "__init__" not in filename and \
                    "test" not in filename and \
                    "config_product" not in filename:
                file_list.append(os.path.join(parent, filename))
    return file_list


def travel_js_path_file(file_path: str) -> list:
    file_list = []
    for parent, dir_names, filenames in os.walk(file_path):
        for filename in filenames:
            if filename.endswith(".js") or filename.endswith(".ts") or filename.endswith(".vue"):
                file_list.append(os.path.join(parent, filename))
    return file_list


def copy_file(file_path, file_list: list):
    with open(file_path, "a") as copy_f:
        for one_file_path in file_list:
            with open(one_file_path, "r") as f:
                data = f.read()
                copy_f.write(one_file_path)
                copy_f.write("\n")
                copy_f.write(data)
                copy_f.write("\n\n\n")
