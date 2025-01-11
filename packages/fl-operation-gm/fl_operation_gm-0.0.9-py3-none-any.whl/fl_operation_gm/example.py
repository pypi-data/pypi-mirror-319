import argparse
import os
import logging
import sys
import time

logging.basicConfig(filename='../../error.log', level=logging.INFO)


def cli():
    """
    Function to work with the CLI
    :return:    str: source file location
                str: target location where file should be saved
    """
    parser = argparse.ArgumentParser(
        description="Script reads the source file, provides the action and saves result to the new file")

    parser.add_argument('src_loc', help='Location of the source file')
    parser.add_argument('trg_loc', help='Target location, where file should be saved')

    args = parser.parse_args()
    return args.src_loc, args.trg_loc


def read_file(path):
    """
    Function to open a file and take text to the str variable
    :param path: str: location of the file
    :return: str: file content
    """
    file_path = os.path.join(path, 'sample.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logging.info('File was read successfully.')
        return content
    except FileNotFoundError as error:
        logging.error(f"Error occurred: {error}")
        print("File was not found in the provided directory. Please make sure to provide correct path to the file and "
              "restart the program.")
        sys.exit()


def time_tracker(func):
    def track_exec_time(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        finish = time.time()
        exec_time = finish - start
        logging.info(f"Execution time: {exec_time}")
        return res
    return track_exec_time


@time_tracker
def count_word_body(text):
    """
    Function for counting how many times word 'body' appears in the text
    :param text: str: provided text from the file
    :return: int: number of 'body' word in the text
    """
    cnt = text.count('body')
    return cnt


def write_to_file(path, cnt):
    file_path = os.path.join(path, 'output.txt')
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(f"Word 'body' appears for the {cnt} times in the provided text.")
        logging.info('Information was written to the file successfully.')



def main():
    write_to_file(cli()[1], count_word_body(read_file(cli()[0])))


if __name__ == "__main__":
    main()
