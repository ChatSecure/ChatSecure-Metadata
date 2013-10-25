import localizable
import os
import yaml
import copy
import shutil
import subprocess


SUPPORTED_LANGUAGES =  {'en-US': 'English (Default)',
                        'en-AU': 'English (Australia)',
                        'en-CA': 'English (Canada)',
                        'en-GB': 'English (UK)',
                        'pt-BR': 'Portugese (Brazil)',
                        'de-DE': 'German',
                        'no': 'Norwegian',
                        'ru': 'Russian',
                        'zh-CN': 'Chinese',
                        'zh-TW': 'Chinese (Traditional)',
                        'sv': 'Swedish',
                        'tr': 'Turkish',
                        'fr': 'French',
                        'fr-CA': 'French (Canada)',
                        'da': 'Danish',
                        'nl': 'Dutch',
                        'fi': 'Finnish',
                        'el': 'Greek',
                        'id': 'Indonesian',
                        'it': 'Italian',
                        'ja': 'Japanese',
                        'ko': 'Korean',
                        'ms': 'Malay',
                        'es': 'Spanish',
                        'es-MX': 'Spanish (Mexico)',
                        'pt': 'Portugese',
                        'th': 'Thai',
                        'vi': 'Vietnamese',
                       }
LOCALIZATIONS_DIR = 'localizations'
LPROJ_EXTENSION = '.lproj'
STRINGS_FILENAME = 'AppStore.strings'
METADATA_TEMPLATE = 'metadata.yaml'
OUTPUT_DIR = 'build'
SCREENSHOTS_DIR = 'screenshots'
DEVICE_IPAD = 'ipad'
DEVICE_IPHONE_35 = 'iphone-3.5'
DEVICE_IPHONE_4 = 'iphone-4'
DEVICE_TYPES = [DEVICE_IPAD, DEVICE_IPHONE_4, DEVICE_IPHONE_35]
CURRENT_DIR = os.getcwd()
GITHUB_PROJECT_URL = u'https://github.com/chrisballinger/Off-the-Record-iOS'

localizations = []
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
        if os.path.isdir(path):
            languages.append(filename)

    return languages

def load_all_screenshots():
    device_types = {}
    for DEVICE_TYPE in DEVICE_TYPES:
        device_types[DEVICE_TYPE] = load_device_screenshot_languages(DEVICE_TYPE)

    for device_type in device_types.keys():
        languages = device_types[device_type]
        for language in languages:
            load_screenshots(language, device_type)

def parse_localizations():
    stringsets = {}
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
            value = unicode(string['value'])
            if i == 0:
                appstore_titles[localization] = value
            else:
                if u'github' in value.lower():
                    value = value + u' ' + GITHUB_PROJECT_URL
                if i == 1:
                    description = value
                else:
                    description = description + u'\n' + value
        appstore_descriptions[localization] = description

def key_for_device_type(device_type):
    if device_type is DEVICE_IPAD:
        return 'ipad'
    elif device_type is DEVICE_IPHONE_4:
        return 'iphone_4in'
    elif device_type is DEVICE_IPHONE_35:
        return 'iphone_3.5in'
    return None

def screenshots_for_language(language_code=None):
    language_screens = {}
    for DEVICE_TYPE in DEVICE_TYPES:
        screens_for_type = screenshots[DEVICE_TYPE]
        key_for_type = key_for_device_type(DEVICE_TYPE)
        screens_for_language = screens_for_type.get(language_code, None)
        if screens_for_language is None and '_' in language_code:
            print DEVICE_TYPE + ': No screens found for full language code ' + language_code
            language_code = language_code.split('_')[0]
            screens_for_language = screens_for_type.get(language_code, None)
        if screens_for_language is None:
            print DEVICE_TYPE + ': No screens found for ' + language_code
            screens_for_language = screens_for_type.get('en')
        file_names = []
        for screen_path in screens_for_language:
            file_name = os.path.basename(screen_path)
            file_names.append(file_name)
            input_path = os.path.join(CURRENT_DIR, screen_path)
            output_path = os.path.join(CURRENT_DIR, OUTPUT_DIR, file_name)
            if not os.path.exists(output_path):
                print 'Copying ' + file_name + ' to ' + OUTPUT_DIR
                shutil.copy(input_path, output_path)
        language_screens[key_for_type] = file_names
    return language_screens

def find_language(localization):
    name = localization

    if localization == 'de':
        return 'de-DE'
    if localization == 'en':
        return 'en-US'

    if '_' in localization:
        name = localization.replace('_', '-') 
    language = SUPPORTED_LANGUAGES.get(name, None)

    if language is None and '-' in name:
        name = name.split('-')[0]
        language = SUPPORTED_LANGUAGES.get(name, None)
    if language is not None:
        return name
    return None

def generate_yaml():
    f = open(METADATA_TEMPLATE, 'r')
    contents = f.read()
    f.close()
    template = yaml.load(contents)
    locales = template['versions'][0]['locales']
    english_locale = locales[0]

    new_locales = []
    completed_languages = {}

    for localization in localizations:
        new_locale = copy.deepcopy(english_locale)
        name = find_language(localization)
        if name is None:
            print 'Found localization for ' + localization + ' but not in supported iTunes Connect languages, skipping...'
            continue
        new_locale['name'] = name
        new_locale['title'] = appstore_titles[localization]
        new_locale['description'] = appstore_descriptions[localization]
        new_locale['screenshots'] = screenshots_for_language(localization)
        #new_locale['version_whats_new'] = new_locale['version_whats_new'] # how do we fix the broken linebreaks?
        if completed_languages.get(name, None) is None:
            print 'Adding metadata for ' + name + ' / ' + localization
            completed_languages[name] = name
            new_locales.append(new_locale)
        else:
            print 'Already completed language ' + name + ' for ' + localization

    template['versions'][0]['locales'] = new_locales

    output_file_path = os.path.join(OUTPUT_DIR, METADATA_TEMPLATE)

    output_file = file(output_file_path, 'w')
    yaml.safe_dump(template, output_file, default_flow_style=False, allow_unicode=True, indent=True)

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        print 'Creating build directory'
        os.mkdir(OUTPUT_DIR)
    print 'Copying screenshots to build dir'
    load_all_screenshots()
    print 'Parsing .strings files'
    parse_localizations()
    print 'Generating metadata.yaml'
    generate_yaml()
    print 'Creating .itmsp file'
    os.chdir(OUTPUT_DIR)
    subprocess.call(['itmsp', 'package', '-i', METADATA_TEMPLATE])
    print 'All done!'
