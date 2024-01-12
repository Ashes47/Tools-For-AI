import os
import uuid


def storeCodeAsFile(code, file_type):
    """
    Stores a code in a text file within a specified directory.

    :param code: The code to be stored.
    :param file_type: The type of the file which will also be used as the directory name.
    """
    # Construct the directory path
    dir_path = os.path.join(os.getcwd(), f"code/{file_type}")

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Define the file path
    file_path = os.path.join(dir_path, str(uuid.uuid4()) + ".txt")

    # Write the message to the file
    with open(file_path, "w") as file:
        file.write(code)
