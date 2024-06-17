import os
import pandas as pd
import utils
import subprocess


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

    def kb_ref(
        self,
        verbose = False,
        d: str = None,
        workflow: str = 'standard',
        overwrite = False,
    ) -> list[str]:
        '''
        Runs the kallisto bustools indexing command kb ref

        d: 
            Download a pre-built kallisto index (along with all necessary files) instead of building it locally
        workflow: Type of workflow to prepare files for. Use `lamanno` for RNA velocity based on La Manno et al. 2018 logic.
            Use `nucleus` for RNA velocity on single-nucleus RNA-seq reads. Use `kite` for feature barcoding. (default:standard)
        '''
        if isinstance(self.gtf, list):
            input_gtf = []
            for gtf in self.gtf:
                url = gtf[-2]
                input_gtf_element = os.path.join(self.index_input, gtf[-1])
                input_gtf.append(input_gtf_element)
                if not os.path.isfile(input_gtf_element):
                    utils.download_from_ftp(url, input_gtf_element)
        elif isinstance(self.gtf, pd.core.series.Series):
            url = self.gtf[-2]
            input_gtf = os.path.join(self.index_input, self.gtf[-1])
            if not os.path.isfile(input_gtf):
                utils.download_from_ftp(url, input_gtf)


        if d:
            if not isinstance(d, str):
                raise TypeError(f"d must be a string, but got {type(d).__name__}")
            if not d in ['human', 'mouse', 'linnarson']:
                raise Exception('d must be either "human", "mouse" or "linnarson"')
        if workflow not in ['standard', 'lamanno', 'nucleus', 'kite']:
            raise Exception('workflow must be one of standard, lamanno, nucleus, kite')

        kb_ref =[
            'kb',
            'ref',
            '-i', f'{self.index_output}/transcriptome.idx',
            '-g', f'{self.index_output}/transcripts_to_genes.txt',
            '-f1', f'{self.index_output}/cdna.fa',
        ] 
        if workflow in ['lamanno', 'nucleus']:
            kb_ref = kb_ref + [
                '-f2', f'{self.index_output}/intron.fa',
                '-c1', f'{self.index_output}/cdna_transcripts_to_capture.txt',
                '-c2', f'{self.index_output}/intron_transcripts_to_capture.txt',
            ]
        if verbose:
            kb_ref.append('--verbose')
        if d:
            kb_ref = kb_ref + ['--d', d]
        if workflow != 'standard':
            kb_ref = kb_ref + ['--workflow', workflow]
        if overwrite:
            kb_ref.append('--overwrite')
        #if type(input_fasta) is str:
        #    kb_ref.append(f'{self.index_input}/{input_fasta}')
        if type(input_gtf) is str:
            kb_ref.append(f'{self.index_input}/{input_gtf}')
        elif type(input_gtf) is list:
            for gtf in input_gtf:
                kb_ref.append(f'{self.index_input}/{gtf}')
        return kb_ref





class Chromium_10X(Single_Cell_Experiment):

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

    def kb_ref(self, verbose=False, d: str = None, workflow: str = 'standard', overwrite=False) -> list[str]:
        return super().kb_ref(verbose, d, workflow, overwrite)

    def initialize_from_dataframe(self):
        pass
