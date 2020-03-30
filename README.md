# ncbi_genome_efetcher

A script to automatically fetch genome data from the Nucleotide database of the NCBI, by querying by genome.

## Dependencies
This script requires Entrez Direct: E-utilities on the UNIX Command Line, available here https://www.ncbi.nlm.nih.gov/books/NBK179288/.


## How to run?
When this is available, the script can be run via the command line with the following command:

```
python3 ncbi_fetcher.py [-h] [-l L] [-f F] [-q Q]
```

The following are the optional arguments for this script:
```
  -h, --help  show this help message and exit
  -l L        Log filename (default: NCBI_efetcher.log)
  -f F        Fasta filename (default: all_genomes_betacoronavirus.fasta)
  -q Q        Query for Database (default: "betacoronavirus[orgn]")
```

## Output
After each run, a `.fasta` file with the provided filename will be produced or updated with all available genome data based for the given query, from the given database.

After the first run,  `log` file file will be produced with the specified filename. This will be updated with each run.
