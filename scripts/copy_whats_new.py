#!/usr/bin/python
from __future__ import print_function
import os
import sys
from distutils.util import strtobool
import shutil

# http://stackoverflow.com/a/22222073/805882
def user_yes_no_query(question):
    print(question + ' [y/n]: ')
    while True:
        try:
            response = raw_input().lower()
            value = strtobool(response)
            return bool(strtobool(response))
        except ValueError:
            print('Please respond with \'y\' or \'n\'.\n')
        except KeyboardInterrupt:
            return False


def main():
    script_dir = os.path.dirname(__file__)
    metadata_dir = os.path.abspath(os.path.join(script_dir, os.pardir, 'metadata'))
    source_lang = 'en-US'
    source_file_name = 'release_notes.txt'

    source_file_path = os.path.abspath(os.path.join(metadata_dir, source_lang, source_file_name))
    if os.path.isfile(source_file_path) is False:
        print('Source file not found at path: ' + source_file_path)
        return

    print('source file: ' + source_file_path)

    files_to_overwrite = []

    for root, subdirs, files in os.walk(metadata_dir):
        # Skip containing directory
        if root is metadata_dir:
            continue
        
        file_name = os.path.abspath(os.path.join(root, source_file_name))

        # Skip source language
        if file_name == source_file_path:
            continue
        else:
            files_to_overwrite.append(file_name)

    print('The following files will be overwritten: ')
    for file_path in files_to_overwrite:
        print(file_path)

    should_continue = user_yes_no_query('Overwrite these files?')
    if should_continue is True:
        print('Overwriting files...')
        for file_path in files_to_overwrite:
            print ('Overwriting ' + file_path)
            shutil.copy(source_file_path, file_path)
        print('Done!')
    else:
        print('Okay, nevermind then!')
        return

if __name__ == "__main__":
    main()