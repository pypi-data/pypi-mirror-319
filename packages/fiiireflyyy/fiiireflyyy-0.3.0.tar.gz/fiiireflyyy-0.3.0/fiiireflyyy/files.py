import os
import shutil


def get_all_parent_by_degree(directory, degree):
    """
    Return all the possible parents from a directory at a specific degree.

        Parameters
        ----------
        directory : str.
            the directory to find the specific parents from.
        degree: int
            The nth parents to look for.

        Returns
        -------
        out: list of str
            list of possible parents at degree n.
    """
    files = get_all_files(directory)

    all_parents = []
    for f in files:
        all_parents.append(os.path.basename(nth_parent(f, degree)))

    return all_parents


def nth_parent(path, n):
    return path if n <= 0 else os.path.dirname(nth_parent(path, n - 1))


def get_all_files(directory: str, to_include=None, to_exclude=None):
    """
    Get all the files and subdirectories within a directory recursively, with optional file selection.

        Parameters
        ----------
            directory: str.
                the path of the directory to sparse
            to_include: list
                str chains that all must be present in the path for it to be returned
            to_exclude: list
                str chains that none must be present in the path for it to be returned

        Returns
        -------
        out: list of str
            list of all files under the directory.
    """
    if to_include is None:
        to_include = []
    if to_exclude is None:
        to_exclude = []
    all_files = get_all_files_recursive(directory)
    selected_files = []
    for file in all_files:
        if all(i in file for i in to_include) and (
                not any(e in file for e in to_exclude)):
            selected_files.append(file)
    
    return selected_files

def get_all_files_recursive(directory):
    """
    Get all the files and subdirectories within a directory recursively

        Parameters
        ----------
            directory: str.
                the path of the directory to sparse

        Returns
        -------
        out: list of str
            list of all files under the directory.
    """
    all_paths = []
    paths = []
    subfolders = os.listdir(directory)
    if len(subfolders) >= 1:
        for subfolder in subfolders:
            if os.path.isdir(os.path.join(directory, subfolder)):
                paths = get_all_files(os.path.join(directory, subfolder))
                for p in paths:
                    all_paths.append(p)
            else:
                all_paths.append(os.path.join(directory, subfolder))

    return all_paths


def verify_dir(directory):
    """
    verify if the directory exists. If not, then create it.

        Parameters
        ----------
        directory: str
            the path of the directory to verify
    """
    isExist = os.path.exists(directory)
    if not isExist:
        os.makedirs(directory)


def split_train_test():
    base_path = "E:/HIV-AI Project/20220330 Trial Images/"
    technique = base_path + "CNN"
    train_ni_path = technique + "/Train/NI"
    train_inf_path = technique + "/Train/INF"
    test_ni_path = technique + "/Test/NI"
    test_inf_path = technique + "/Test/INF"

    basic_directories = (train_inf_path, train_ni_path, test_inf_path, test_ni_path)
    for bd in basic_directories:
        isExist = os.path.exists(bd)
        if not isExist:
            os.makedirs(bd)

    all_images = get_all_files("E:/HIV-AI Project/20220330 Trial Images/PNG")
    count_class_one = 0
    count_class_two = 0
    for image in all_images:
        head, tail = os.path.split(image)
        if "INF10^6" in image:
            count_class_two += 1
        elif "NI" in image:
            count_class_one += 1

    if count_class_two > count_class_one:  # getting the same number of entries for each class
        count_class_two = count_class_one
    else:
        count_class_one = count_class_two

    total_images = count_class_two + count_class_one
    train_proportion = int(0.7 * total_images)
    test_proportion = total_images - train_proportion

    inf_train_index = 0
    ni_train_index = 0
    print(train_proportion)
    for image in all_images:
        head, tail = os.path.split(image)
        if "INF10^6" in image and inf_train_index < train_proportion / 2:
            print("train inf ", inf_train_index)
            destination = train_inf_path + "/" + tail
            shutil.copyfile(image, destination)
            inf_train_index += 1
        elif "NI" in image and ni_train_index < train_proportion / 2:
            print("train ni ", ni_train_index)
            destination = train_ni_path + "/" + tail
            shutil.copyfile(image, destination)
            ni_train_index += 1
        elif "INF10^6" in image and inf_train_index >= train_proportion / 2:
            print("test inf ", inf_train_index)
            destination = test_inf_path + "/" + tail
            shutil.copyfile(image, destination)
            inf_train_index += 1
        elif "NI" in image and ni_train_index >= train_proportion / 2:
            print("test ni ", ni_train_index)
            destination = test_ni_path + "/" + tail
            shutil.copyfile(image, destination)
            ni_train_index += 1
