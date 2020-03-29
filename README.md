# ncbi_efetcher

A script to automatically fetch genome data from the Nucleotide database of the NCBI, by querying by genome.

## Dependencies
This script requires Entrez Direct: E-utilities on the UNIX Command Line, available here https://www.ncbi.nlm.nih.gov/books/NBK179288/.

When this is available, the script can be run via the command line with the following command:

```
python3 ncbi_fetcher.py
```

## Output
After each run, a `.fasta` file (default filename: `all_genoomes.fasta`) with all available genome data based on the query will be produced or updated.

After the first run,  `log` file (default filename: `NCBI_efetcher.log`) file will be produced. This will be updated with each run.