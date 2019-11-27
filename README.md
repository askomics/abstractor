# Abstractor

Abstraction generator: Generate AskOmics abstraction from a distant endpoint

## Installation

### With pip

Create and activate a python virtual environment

```bash
# Create a python virtual environment
python3 -m venv venv
# Activate python virtual env
source venv/bin/activate
```

Install

```bash
pip install abstractor
```

### With git

First, clone the git repo

```bash
# clone
git clone https://github.com/askomics/abstractor.git
# cd
cd abstractor
```

Then, create and activate a python virtual environment

```bash
# Create a python virtual environment
python3 -m venv venv
# Activate python virtual env
source venv/bin/activate
```

Install

```bash
python setup.py install
```

Use

```bash
# Get help
abstractor -h
```

## Usage

### General usage

```bash
abstractor -e <endpoint_url> -p <entity_prefix> -o <output_file>
```

### Example with NeXtProt

```bash
# Get help
abstractor -e "https://sparql.nextprot.org" -p "http://nextprot.org/rdf#" -n nextprot -o "abstraction.ttl"
```

Obtained TTL file can be used with [AskOmics](https://github.com/askomics/flaskomics)