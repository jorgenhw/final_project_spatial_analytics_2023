# install requirements.txt for project
# Usage: source setup.sh

# create virtual environment
python3 -m venv bar_map_venv

# activate virtual environment
source ./bar_map_venv/bin/activate

# Install requirements
python3 -m pip install --upgrade pip # upgrade pip
pip3 install -r requirements.txt