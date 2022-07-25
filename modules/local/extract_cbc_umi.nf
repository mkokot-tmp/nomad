
process EXTRACT_CBC_UMI {

    tag "${fastq_id}"
    label 'process_low'
    conda (params.enable_conda ? "conda-forge::python=3.9.5" : null)

    input:
    tuple val(fastq_id), path(fastq), val(group_id)
    val num_reads_first_pass

    output:
    tuple val(fastq_id), path(outfile), val(group_id), emit: seqs

    script:
    outfile         = "extracted_cbc_umi_${fastq_id}.txt.gz"
    """
    extract_cbc_umi.py \\
        --infile ${fastq} \\
        --num_lines ${num_reads_first_pass} \\
        --outfile ${outfile}
    """
}
