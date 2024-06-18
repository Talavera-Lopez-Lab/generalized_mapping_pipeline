import os
import pandas as pd
import algorithms

class Single_Cell_Experiment():

    def __init__(
            self,
            accession,
            download_table=None,
    ):
        super().__init__()
        self.base_dir = os.path.join(os.getcwd(), 'mapping_dir', accession)
        os.makedirs(self.base_dir, exist_ok=True)
        self.meta_data = os.path.join(self.base_dir, 'meta_data')
        os.makedirs(self.meta_data, exist_ok=True)
        self.mapping = os.path.join(self.base_dir, 'mapping')
        os.makedirs(self.mapping, exist_ok=True)
        self.index_input = os.path.join(self.base_dir, 'index_input')
        os.makedirs(self.index_input, exist_ok=True)
        self.index_output = os.path.join(self.base_dir, 'index_output')
        os.makedirs(self.index_output, exist_ok=True)
        self.available_gtf_files = pd.read_csv('gtf_files.csv', index_col=0)
        self.available_fasta_files = pd.read_csv('fasta_files.csv', index_col=0)

class Chromium_10X(
    Single_Cell_Experiment,
    algorithms.kallisto_bustools
):

    def __init__(
            self,
            accession,
            download_table=None
    ):
        super().__init__(
            accession,
            download_table,
        )
        self.available_methods = ['kb_ref']

