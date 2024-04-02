import argparse , requests , io , os
import pandas as pd

def get_args():
    parser = argparse.ArgumentParser(description='\033[93mThis script is used to download new ONT and Illumina submissions (runs) of COVID-19. \033[0m')
    parser.add_argument('-d', '--date', type=str, help='date - YYYY-MM-DD', required=True)
    args = parser.parse_args()
    return args

args = get_args()

BASE_PORTAL_API_SEARCH_URL = 'https://www.ebi.ac.uk/ena/portal/api/search'
instrument_platform = ['illumina','oxford_nanopore']
fields =['run_accession','sample_accession','instrument_platform','instrument_model','fastq_aspera','fastq_bytes','fastq_ftp','fastq_galaxy','fastq_md5','first_created','first_public','country','collection_date','isolate','strain']

def get_url(instrument_platform):
        url = ''.join([
            BASE_PORTAL_API_SEARCH_URL,
            '?result=read_run&query=tax_tree(2697049)',
            f'%20AND%20instrument_platform%3D%22{instrument_platform}%22'
            '&',
            'fields=' + '%2C'.join(fields),
            '&format=tsv&limit=0' 
        ])
        return url

def main():
    for i in instrument_platform : 
        url = get_url (i)
        response = requests.get(url)
        data = pd.read_csv(io.StringIO(response.content.decode('UTF-8')), sep="\t", low_memory=False)

        # Convert 'first_created' column to datetime objects
        first_created= [pd.to_datetime(date_str) for date_str in data['first_created']]
        data['first_created'] = first_created

        # Filter the data based on user-provided date
        filtered_data = data[data["first_created"] >= args.date]

        # Save the filtered data to a TSV file and liked 
        if i == 'illumina':
            output_file = f"illumina.index.{str(args.date)}.tsv"
            filtered_data.to_csv(output_file, sep="\t", index=False)
            #os.system(" ln -sf  "+output_file+"  illumina.index.tsv")
        else:
            output_file = f"nanopore.index.{str(args.date)}.tsv"
            filtered_data.to_csv(output_file, sep="\t", index=False)
            #os.system(" ln -sf  "+output_file+"  nanopore.index.tsv")
        
        

if __name__ == '__main__':
    main()