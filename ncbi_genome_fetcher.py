import xml.etree.ElementTree as ET
import subprocess
import logging
import argparse
import mmap
import csv
import re

def query_and_get_result_count(query, database):
    esearch_cmd = 'esearch -db {} -query'.format(database).split()
    esearch_cmd.append(query)
    elink_cmd = 'elink -target nuccore'.split()

    esearch_process = subprocess.Popen(esearch_cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    elink_process = subprocess.Popen(elink_cmd, 
        stdin=esearch_process.stdout,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = elink_process.communicate()

    if stderr == None:
        try:
            search_tree = ET.fromstring(stdout)

            search_result_count = int(search_tree.find('Count').text)
            logging.info('Successfully searched for {} from {} database. Yielded {} results.'.format(query, database, search_result_count))
            return search_result_count
        except:
            logging.debug("Unsuccessful search. stderr = None; stdout = {}".format(stdout)
                )
            return
    else:
        logging.debug("Unsuccessful search. stderr = {}".format(stderr))
        return

def new_results_available(query, database, search_result_count, log_filename):
    search_result_count_regex = 'Successfully fetched fasta files for query {} from {} database. Fetched {} files.'.format(query, database, search_result_count).encode()

    try:
        with open(log_filename) as f:
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return False if s.find(search_result_count_regex) > 0 else True
    except:
        raise
        logging.info("No previous search results to check. ")
        return True

def query_and_get_results(query, database, result_count, fetched_filename):
    esearch_cmd = 'esearch -db {} -query'.format(database).split()
    esearch_cmd.append(query)
    elink_cmd = 'elink -target nuccore'.split()
    efetch_cmd = 'efetch -format fasta'.split()

    esearch_process = subprocess.Popen(esearch_cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    elink_process = subprocess.Popen(elink_cmd, 
        stdin=esearch_process.stdout,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    efetch_fasta_process = subprocess.Popen(efetch_cmd, 
            stdin=elink_process.stdout,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

    efetch_fasta_stdout, efetch_fasta_stderr = efetch_fasta_process.communicate()

    if efetch_fasta_stderr == None:
        open(fetched_filename, 'wb').write(efetch_fasta_stdout)
        logging.info('Successfully fetched fasta files for query {} from {} database. Fetched {} files.'.format(query, database, result_count))
    else:
        logging.debug("Unsuccessful fetch. stderr = {}".format(stderr))

    return

def main(log_filename=None):
    parser = argparse.ArgumentParser(description='Please note the following acceptable command-line options for this script:')
    parser.add_argument("-l", default='NCBI_efetcher.log', help="Log filename (default: NCBI_efetcher.log)")
    parser.add_argument("-f", default='all_genomes_betacoronavirus.fasta', help="Fasta filename (default: all_genomes_betacoronavirus.fasta)")
    parser.add_argument("-q", default='betacoronavirus[orgn]', help='Query for Database (default: betacoronavirus[orgn])')
    
    args = parser.parse_args()
    log_filename = args.l
    fasta_filename = args.f
    query = args.q
    database = 'genome'

    log_format = FORMAT = '%(asctime)s : %(levelname)s : %(message)s'
    logging.basicConfig(filename=log_filename, level=logging.INFO,
        format=log_format)
    
    search_result_count = query_and_get_result_count(query, database)
    
    new_results_are_available = new_results_available(query, database, search_result_count, log_filename)

    if new_results_are_available:
        logging.info("Additional genomes available. Fetching additional genomes.")
        query_and_get_results(query, database, search_result_count, fasta_filename)
    else:
        logging.info('No new results to fetch. Perviously fetched {} files.'.format(search_result_count))
    


if __name__ == '__main__': 
    main()
