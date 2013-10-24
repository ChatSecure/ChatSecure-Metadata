import localizable
import os
import yaml
import copy

LOCALIZATIONS_DIR = 'localizations'
LPROJ_EXTENSION = '.lproj'
STRINGS_FILENAME = 'AppStore.strings'
METADATA_TEMPLATE = 'metadata.yaml'
OUTPUT_DIR = 'build'

contents = os.listdir(LOCALIZATIONS_DIR)
localizations = []
stringsets = {}
appstore_descriptions = {}
appstore_titles = {}


for directory_name in contents:
    if LPROJ_EXTENSION in directory_name:
        language_name = directory_name.split('.')[0]
        localizations.append(language_name)

for localization in localizations:
    directory_name = localization + LPROJ_EXTENSION
    path = os.path.join(LOCALIZATIONS_DIR, directory_name, STRINGS_FILENAME)
    strings = localizable.parse_strings(filename=path)
    stringsets[localization] = strings
    description = u""
    for i, string in enumerate(strings):
        if i == 0:
            appstore_titles[localization] = unicode(string['value'])
        else:
            description = description + u'\n' + unicode(string['value'])
    appstore_descriptions[localization] = description

f = open(METADATA_TEMPLATE, 'r')
contents = f.read()
f.close()
template = yaml.load(contents)
locales = template['versions'][0]['locales']
english_locale = locales[0]

new_locales = []

for localization in localizations:
    new_locale = copy.deepcopy(english_locale)
    new_locale['name'] = localization
    new_locale['title'] = appstore_titles[localization]
    new_locale['description'] = appstore_descriptions[localization]
    new_locales.append(new_locale)

template['versions'][0]['locales'] = new_locales

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

output_file_path = os.path.join(OUTPUT_DIR, METADATA_TEMPLATE)

output_file = file(output_file_path, 'w')
yaml.safe_dump(template, output_file, default_flow_style=False, allow_unicode=True, indent=True)
