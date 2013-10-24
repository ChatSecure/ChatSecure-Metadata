import localizable
import os
import yaml

LOCALIZATIONS_DIR = 'localizations'
LPROJ_EXTENSION = '.lproj'
STRINGS_FILENAME = 'AppStore.strings'
METADATA_TEMPLATE = 'metadata.yaml'
OUTPUT_FILE = 'output.yaml'
OUTPUT_DIR = 'build'

contents = os.listdir(LOCALIZATIONS_DIR)
localizations = []
stringsets = {}

for directory_name in contents:
    if LPROJ_EXTENSION in directory_name:
        language_name = directory_name.split('.')[0]
        localizations.append(language_name)

for localization in localizations:
    directory_name = localization + LPROJ_EXTENSION
    path = os.path.join(LOCALIZATIONS_DIR, directory_name, STRINGS_FILENAME)
    strings = localizable.parse_strings(filename=path)
    stringsets[localization] = strings

f = open(METADATA_TEMPLATE, 'r')
contents = f.read()
f.close()
template = yaml.load(contents)
locales = template['versions'][0]['locales']
english_locale = locales[0]

new_locales = []

for localization in localizations:
    new_locale = english_locale.copy()
    new_locale['name'] = localization
    new_locale['title'] = new_locale['title']
    new_locale['description'] = 'Test'
    new_locales.append(new_locale)
    break

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

#output_file_path = os.path.join()
#template['versions'][0]['locales'] = new_locales

output_file = file(OUTPUT_FILE, 'w')
yaml.dump(template, output_file, default_flow_style=False, allow_unicode=True, indent=True)