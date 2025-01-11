# Graph visualization of InfoNodes
This module contains scripts for visualizing the `info_nodes` in cytoscape.

## Create updated graph files via

```
(pkdb_data) create_nodes
(pkdb_data) python src/pkdb_data/info_nodes/network/pkdb_network.py
```

## Cytoscape visualization
* Start cytoscape
* Load SIF file via `File -> Import Network from file -> ./results/pkdb_network.sif`
* Load node data via `File -> Import Table from file -> ./results/pkdb_nodes.tsv`
* Load styles va `File -> Import Stylse from file -> ./results/pkdb_styles.xml`
* Select network and apply style
