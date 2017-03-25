ChatSecure-Metadata
===================

Various metadata for ChatSecure


# Requirements
You will need a recent version of Ruby. We now use [deliver](https://github.com/KrauseFx/deliver) and [snapshot](https://github.com/KrauseFx/snapshot).

    $ gem install fastlane

# Generating Screenshots

Snapshot stuff has been moved to the main repo for now.

# Uploading Metadata

Edit the metadata and pull in new translations with Transifex, then run:

    $ fastlane deliver --force

# Transifex

To synchronize translations use Transifex's `tx` tool.

    $ pip install transifex-client
    
This command will download all existing translations:

    $ tx pull -f
    
New languages on Transifex will need to be [manually mapped](http://docs.transifex.com/developer/client/config) to the correct language code folder in `./metadata`. This is because the language codes in Transifex don't match up with the ones that Apple uses.

    $ nano .tx/config
    
Available Languages Codes: https://github.com/KrauseFx/deliver#available-language-codes
    
    
# Updating What's New
    
When releasing a new version we need to have a `version_whats_new.txt` for each language. Edit `metadata/en-US/version_whats_new.txt` then run:

    $ python ./scripts/copy_whats_new.py
    
# License

GPLv3