# #!/bin/bash

# Setup test environment

python3.8 -m venv venv
source ./venv/bin/activate
cd server
pip install -I -r ./requirements-dev.txt
echo "source ./venv/bin/activate"
