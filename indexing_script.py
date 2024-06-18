import experiments

experiment = experiments.Chromium_10X(
    accession='123abc'
)

gtfs = experiment.available_gtf_files
gtfs

experiment.gtf = [gtfs.iloc[1], gtfs.iloc[6], 
                  #gtfs.iloc[9]
                  ]
#experiment.gtf = gtfs.iloc[1]
experiment.gtf

fastas = experiment.available_fasta_files
fastas

experiment.fasta = fastas.iloc[5]
experiment.fasta

experiment.kb_ref(workflow='standard')

