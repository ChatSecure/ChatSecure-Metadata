ChatSecure-Metadata
===================

Various metadata for ChatSecure


# Requirements
You will need a recent version of Ruby. We now use [deliver](https://github.com/KrauseFx/deliver) and [snapshot](https://github.com/KrauseFx/snapshot).

    $ gem install deliver
    $ gem install snapshot

# Generating Screenshots

Edit the `Snapfile` and run `snapshot`.

    $ snapshot

# Uploading Metadata

Edit the metadata and pull in new translations with Transifex, then run:

    $ deliver --skip-deploy
    
This will upload new metadata and screenshots to iTC. Make sure to use the `--skip-deploy` option to prevent automatic submission to Apple.

# Transifex

To synchronize translations use Transifex's `tx` tool.

    $ pip install transifex-client
    
This command will download all existing translations:

    $ tx pull
    
New languages on Transifex will need to be [manually mapped](http://docs.transifex.com/developer/client/config) to the correct language code folder in `./metadata`. This is because the language codes in Transifex don't match up with the ones that Apple uses.

    $ nano .tx/config
    
    
# License

GPLv3