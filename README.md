ChatSecure-Metadata
===================

Various metadata for ChatSecure

Use [itmsp](https://github.com/colinhumber/itunes_transporter_generator) to generate the metadata.xml.


# Generating the YAML file

Install `pip`, `virutalenv`, and `virtualenvwrapper`. Make a new virtual environment and install the dependencies.

    $ mkvirtualenv metadata
    (metadata)$ pip install -r requirements.txt
    



# Transifex

To synchronize translations use Transifex's `tx` tool. 

    $ pip install transifex-client
    
This command will download all existing translations:

    $ tx pull -a -r chatsecure.appstorestrings