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

# Generating the .itmsp file

Install `pip`, `virutalenv`, and `virtualenvwrapper`. Make a new virtual environment and install the dependencies.

    $ mkvirtualenv metadata
    (metadata)$ pip install -r requirements.txt
    $ python generate_itmsp.py
    
# Uploading metadata to iTunes Connect

To verify if your file passes Apple's validation checks:

    $ iTMSTransporter -m verify -u <username> -f build/<file>.itmsp 

To upload the metadata:
	
	$ iTMSTransporter -m upload -u <username> -f build/<file>.itmsp
	

# Transifex

To synchronize translations use Transifex's `tx` tool. 

    $ pip install transifex-client
    
This command will download all existing translations:

    $ tx pull -a -r chatsecure.appstorestrings
    
    
