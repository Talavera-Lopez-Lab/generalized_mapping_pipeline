import utils
import os
import pandas as pd
import subprocess

class kallisto_bustools():
    '''Parent Class containing index creation and mapping algorithms from kallisto bustools'''
    def __init__(self) -> None:
        pass

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

        fasta_url = self.fasta[-2]
        input_fasta = os.path.join(self.index_input, self.fasta[-1])
        if not os.path.isfile(input_fasta):
            utils.download_from_ftp(fasta_url, input_fasta)
        if isinstance(self.gtf, list):
            input_gtf = []
            for gtf in self.gtf:
                gtf_url = gtf[-2]
                input_gtf_element = os.path.join(self.index_input, gtf[-1])
                input_gtf.append(input_gtf_element)
                if not os.path.isfile(input_gtf_element):
                    utils.download_from_ftp(gtf_url, input_gtf_element)
        elif isinstance(self.gtf, pd.core.series.Series):
            gtf_url = self.gtf[-2]
            input_gtf = os.path.join(self.index_input, self.gtf[-1])
            if not os.path.isfile(input_gtf):
                utils.download_from_ftp(gtf_url, input_gtf)



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
            '--tmp', os.path.join(self.index_output, 'tmp'),
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
        if type(input_fasta) is str:
            kb_ref.append(input_fasta)
        if type(input_gtf) is str:
            kb_ref.append(input_gtf)
        elif type(input_gtf) is list:
            for gtf in input_gtf:
                kb_ref.append(gtf)
        #return kb_ref
        subprocess.run(kb_ref, check=True)