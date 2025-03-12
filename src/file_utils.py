import os, shutil

def copy_files(src, dst):
    delete_folder_contents(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst)
        elif os.path.isdir(src_path):
            dst_path = f"{dst}/{item}"
            os.mkdir(dst_path)
            copy_files(src_path, dst_path)


def delete_folder_contents(folder_path):
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        print(f"Folder {folder_path} does not exist.")