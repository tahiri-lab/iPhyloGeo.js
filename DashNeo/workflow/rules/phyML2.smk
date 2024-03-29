rule rf_distance:
    input: 
        seq_tree = "results/bootstrap_consensus/window_position_{position}",
        ref_tree = "results/reference_tree/{feature}_newick"
    output:
        ete3_output = "results/rf/{position}.{feature}.rf_ete"
    priority:
        50
    script:
        "../scripts/rfCalculate.py"

rule bootstrap_consensus:
    input:
        "results/windows/window_position_{position}.fa",
    output:
        "results/bootstrap_consensus/window_position_{position}",
    params:
        data_type = config['params']['data_type']
    priority:
        50
    script:
        "../scripts/bootstrapFilter.py"
