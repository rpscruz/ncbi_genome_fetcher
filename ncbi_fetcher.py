import xml.etree.ElementTree as ET
import subprocess
import logging
import csv
import re

def query_and_get_result_count(query):
    esearch_cmd = 'esearch -db nucleotide -query'.split()
    esearch_cmd.append(query)

    out = subprocess.Popen(esearch_cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()

    if stderr == None:
        try:
            search_tree = ET.fromstring(stdout)

            search_result_count = int(search_tree.find('Count').text)
            logging.info('Successfully searched for {}. Yielded {} results.'.format(query, search_result_count))
            return search_result_count
        except:
            logging.debug("Unsuccessful search. stderr = None; stdout = {}".format(stdout)
                )
            return
    else:
        logging.debug("Unsuccessful search. stderr = {}".format(stderr))
        return

def new_results_available(search_result_count, log_filename):
    search_result_count_regex = r'Fetched ([0-9]+) files.'

    try:
        log_last_line = subprocess.check_output(['tail', '-2', log_filename]).decode('utf-8')
        prev_search_result_count = int(re.search(search_result_count_regex, log_last_line, re.IGNORECASE)[1])
        return search_result_count > prev_search_result_count
    except:
        logging.info("No previous search results to check. ")
        return True

def query_and_get_results(query, result_count, fetched_filename, id_filename):
    esearch_cmd = 'esearch -db nucleotide -query'.split()
    esearch_cmd.append(query)

    esummary_cmd = 'esearch_cmd'

    efetch_cmd = 'efetch -format fasta'.split()

    esearch_process = subprocess.Popen(esearch_cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    efetch_fasta_process = subprocess.Popen(efetch_cmd, 
            stdin=esearch_process.stdout,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

    efetch_fasta_stdout, efetch_fasta_stderr = efetch_fasta_process.communicate()

    if efetch_fasta_stderr == None:
        open(fetched_filename, 'wb').write(efetch_fasta_stdout)
        logging.info('Successfull fetched fasta files for query {}. Fetched {} files.'.format(query, result_count))
    else:
        logging.debug("Unsuccessful fetch. stderr = {}".format(stderr))

    return

def main():
    query = '"betacoronavirus" AND "complete genome"'
    log_filename = 'NCBI_efetcher.log'
    fasta_filename = 'all_genoomes.fasta'
    summary_filename = 'all_genoomes_ids.txt'

    log_format = FORMAT = '%(asctime)s : %(levelname)s : %(message)s'
    logging.basicConfig(filename=log_filename, level=logging.INFO,
        format=log_format)
    
    search_result_count = query_and_get_result_count(query)
    new_results_are_available = new_results_available(search_result_count, log_filename)

    if new_results_are_available:
        logging.info("Additional genomes available. Fetching additional genomes.")
        query_and_get_results(query, search_result_count, fasta_filename, summary_filename)
    else:
        logging.info('No new results to fetch. Perviously fetched {} files.'.format(search_result_count))


if __name__ == '__main__': 
    main()
