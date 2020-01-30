# Abstractor

Abstraction generator: Generate AskOmics abstraction from a distant SPARQL endpoint or a RDF file

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

Use `abstractor --help` to get all available options.

#### With a SPARQL endpoint

```bash
abstractor -s <endpoint_url> -o <output_file>
```

Example with [NeXtProt](https://sparql.nextprot.org):

```bash
abstractor -s https://sparql.nextprot.org -o nextprot_abstraction.ttl
```

#### With a RDF file

```bash
abstractor -s <path> -t <type> -o <output_file>
```

Example with a file `data.rdf`. Input and output file in xml format.

```bash
abstractor -s ~/me/data.xml -t xml -o data_abstraction.xml -f xml
```

Obtained TTL file can be used with [AskOmics](https://github.com/askomics/flaskomics)
