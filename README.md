# Extractor

Purpose of the project: take a single scanned image and return the table found in it as a csv.

## How Do I Integrate?

### Prerequisites

- Python3.6
- Python Virtual Environment

### Setup Extractor Virtual Env

Make sure you are in project directory and:

```
mkvirtualenv --python=$(which python3.6) --no-site-packages extractor
mkdir -p ~/workspace
cd ~/workspace
git clone git@github.com:shivanouri/extractor.git
cd extractor
pip install -e .
```

### Start

Activate the project and run it by typing `extractor`.
Then you may select the scanned image and see the out put. (not yet implemented)
