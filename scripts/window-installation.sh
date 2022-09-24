#!/usr/bin/env

if ! [[ "$(python -V)" =~ "Python 3.10" ]]; then
    echo "tasks-tracker required Python version >= 3.10 to run. Please download Python version >= 3.10. For more information here https://www.python.org/downloads/macos/"
    exit 0 
fi 

if ! [[ -x "$(command -v pip3.10)" ]]; then
    echo "tasks-tracker required pip version >= 3.10 to run. Please download pip version >= 3.10"
    exit 0 
fi

# Install tasks-tracker package
python -m pip install -e . -r ./requirements.txt