ChatSecure-Metadata
===================

Various metadata for ChatSecure


# Requirements
You will need a recent version of Python and Ruby.

[itmsp](https://github.com/colinhumber/itunes_transporter_generator) to generate the metadata.xml.

    $ gem install itunes_transporter_generator
    
`iTMSTransporter` aka Transporter, the (extremely bad) CLI utility from Apple to upload metadata to iTunes Connect. Add it to your path by editing `~/.profile`.

    export TRANSPORTER_HOME=`xcode-select --print-path`/../Applications/Application\ Loader.app/Contents/MacOS/itms/bin
    export PATH="$TRANSPORTER_HOME":$PATH

Install `pip`, `virutalenv`, and `virtualenvwrapper`. Make a new virtual environment and install the dependencies.

    $ mkvirtualenv metadata
    (metadata)$ pip install -r requirements.txt

# Generating the .itmsp file

Activate your virtual environment if it isn't already and run `generate_itmsp.py`. This will copy all screenshots, generate your app store descriptions based on your transifex localizations, generate a `metadata.yaml` file for `itmsp`. It will also run `itmsp` with the metadata.yaml file and screenshots to generate the `.itmsp` file.

	$ workon metadata
    (metadata)$ python generate_itmsp.py
    
Sometimes the `metadata.xml` file inside your itmsp file will be empty and require you to copy over the proper one manually.
    
# Uploading metadata to iTunes Connect

iTMSTransporter is probably the worst piece of software Apple has ever written. If it hangs "updating" itself forever, just give up and try again later.

To check out your existing metadata for an app:

    $ iTMSTransporter -u <username> -m lookupMetadata -destination <destination folder> -apple_id <app store id>

To verify if your file passes Apple's validation checks:

    $ iTMSTransporter -m verify -u <username> -f build/<file>.itmsp 

To upload the metadata:
	
	$ iTMSTransporter -m upload -u <username> -f build/<file>.itmsp
	

# Transifex

To synchronize translations use Transifex's `tx` tool. 

    $ pip install transifex-client
    
This command will download all existing translations:

    $ tx pull -a -r chatsecure.appstorestrings
    
    
# License

GPLv3