import logging
import os
import shutil
import time
import requests
import csv
from PIL import Image
from enums.platform import Platform

logger = logging.getLogger(__name__)


def move_file_and_add_time_stamp(
    target_folder_path: str, target_file_name: str, destination_folder_path: str
) -> str:
    """
    Moves the file to the destination folder and adds a timestamp to the filename
    """
    unique_filename = ""
    try:
        for root, dirs, files in os.walk(target_folder_path):
            if target_file_name in files:
                print(f"Found {target_file_name} in {root}")
                source_file_path = os.path.join(root, target_file_name)
                destination_folder_path = os.path.join(
                    os.getcwd(), destination_folder_path
                )
                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)
                timestamp = str(int(time.time()))
                file_name_without_extension = os.path.splitext(target_file_name)[0]
                file_extension = os.path.splitext(target_file_name)[1]
                destination_file_path = os.path.join(
                    destination_folder_path,
                    f"{file_name_without_extension}_{timestamp}{file_extension}",
                )
                shutil.move(source_file_path, destination_file_path)
                unique_filename = (
                    f"{file_name_without_extension}_{timestamp}{file_extension}"
                )
                print(f"Moved {target_file_name} to {destination_file_path}")
                break
        else:
            logger.error(f"Could not find {target_file_name} in {target_folder_path}")
            print(f"Could not find {target_file_name} in {target_folder_path}")
    except:
        logger.error("Error: Could not find the specified image")
        print("Error: Could not find the specified image")

    return unique_filename


def save_to_csv(file_name: str, headers: list, data: list, platform: Platform):
    """
    Save data to a csv file
    """
    try:
        write_headers = True
        # check if target folder exist, otherwise create it
        if not os.path.exists(os.path.join(os.getcwd(), "analytics_data")):
            os.makedirs(os.path.join(os.getcwd(), "analytics_data"))
        # check if files exists, if not we need to append headers to the file that will be created
        write_headers = not os.path.exists(
            os.path.join(os.getcwd(), "analytics_data", file_name)
        )
        # create the proper file path
        file_name_with_path = os.path.join(os.getcwd(), "analytics_data", file_name)

        with open(file_name_with_path, "a", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter="|")
            if write_headers:
                csv_writer.writerow(headers)

            if platform == Platform.TWITTER:
                csv_writer.writerow(data)

            if platform == Platform.INSTAGRAM:
                for entry in data:
                    try:
                        row = []
                        row.append(entry["id"])
                        row.append(entry["caption"] if "caption" in entry else "-")
                        row.append(entry["comments_count"])
                        row.append(entry["like_count"])
                        row.append(entry["media_product_type"])
                        row.append(entry["media_type"])
                        row.append(entry["timestamp"])
                        csv_writer.writerow(row)
                    except KeyError as e:
                        logger.error(f"Error: Could not save to csv file. {e}")
                        continue

        logger.info(f"Saved to csv file: {file_name_with_path}")
    except (FileNotFoundError, IOError, KeyError) as e:
        logger.error(f"Error: Could not save to csv file. {e}")


def save_to_text_file(file_path: str, text: str, overwrite_if_exist: bool = False):
    """
    Save data to a text file
    """
    with open(file_path, "w" if overwrite_if_exist else "a", encoding="utf-8") as file:
        file.write(text)


def convert_file_type(original_file_path: str, target_type: str) -> str:
    """
    Tries to convert input file to target type.
    """
    try:
        original_file = Image.open(original_file_path, mode="r", formats=None)
        # save to new format by replacing the extension
        new_file_path = original_file.filname.replace(
            original_file.format.lower(), target_type
        )
        original_file.save(new_file_path, target_type)

        return new_file_path

    except (FileNotFoundError, IOError, SyntaxError, ValueError) as e:
        logger.error(f"Error: Could not convert file: {e}")


def read_file_content(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readline()
            return content
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error: Could not read file: {e}")


def read_first_line(file_path: str) -> str:
    """
    Reads the first line of a text file and returns it as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline()
            return first_line.strip()
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error: Could not read file: {e}")

def download_file(url, target_path):
    """
    Downloads a file from the given url and saves it to the target path
    """
    try:
        response = requests.get(url, stream=True)
        with open(target_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        logger.info(f"Downloaded file from {url} to {target_path}")
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error: Could not download file: {e}")
