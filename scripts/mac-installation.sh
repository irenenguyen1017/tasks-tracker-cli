#!/bin/bash

if ! [[ -x "$(command -v python3.10)" ]]; then
    echo "tasks-tracker required Python version >= 3.10 to run. Please download Python version >= 3.10. For more information here https://www.python.org/downloads/macos/"
    exit 0 
fi

if ! [[ -x "$(command -v pip3.10)" ]]; then
    echo "tasks-tracker required pip version >= 3.10 to run. Please download pip version >= 3.10"
    exit 0 
fi

# Install tasks-tracker locally
python3.10 -m pip install -e . -r ./requirements.txt