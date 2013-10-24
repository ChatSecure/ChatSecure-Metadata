import localizable
import os
import yaml
import copy

LOCALIZATIONS_DIR = 'localizations'
LPROJ_EXTENSION = '.lproj'
STRINGS_FILENAME = 'AppStore.strings'
METADATA_TEMPLATE = 'metadata.yaml'
OUTPUT_DIR = 'build'
SCREENSHOTS_DIR = 'screenshots'
DEVICE_IPAD = 'ipad'
DEVICE_IPHONE_35 = 'iphone-3.5'
DEVICE_IPHONE_4 = 'iphone-4'

localizations = []
stringsets = {}
appstore_descriptions = {}
appstore_titles = {}

screenshots = {}

def load_screenshots(language_name=None, device_type=None):
    device_screens = screenshots.get(device_type, {})
    
    screens_path = os.path.join(SCREENSHOTS_DIR, device_type, language_name)
    contents = os.listdir(screens_path)
    screenshot_paths = []

    for filename in contents:
        if '.png' in filename:
            file_path = os.path.join(screens_path, filename)
            screenshot_paths.append(file_path)
    device_screens[language_name] = screenshot_paths

    screenshots[device_type] = device_screens

def load_device_screenshot_languages(device_type=None):
    device_path = os.path.join(SCREENSHOTS_DIR, device_type)

    contents = os.listdir(device_path)
    languages = []

    for filename in contents:
        path = os.path.join(device_path, filename)
        print path
        if os.path.isdir(path):
            languages.append(filename)

    return languages

def load_all_screenshots():
    device_types = {}
    device_types[DEVICE_IPAD] = load_device_screenshot_languages(DEVICE_IPAD)
    device_types[DEVICE_IPHONE_35] = load_device_screenshot_languages(DEVICE_IPHONE_35)
    device_types[DEVICE_IPHONE_4] = load_device_screenshot_languages(DEVICE_IPHONE_4)

    for device_type in device_types.keys():
        languages = device_types[device_type]
        for langauge in languages:
            print langauge + ' ' + device_type
            load_screenshots(langauge, device_type)


def parse_localizations():
    contents = os.listdir(LOCALIZATIONS_DIR)
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

def generate_yaml():
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

if __name__ == '__main__':
    load_all_screenshots()
    print screenshots