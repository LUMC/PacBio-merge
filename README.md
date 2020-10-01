# PacBio-merge
Merge report files from PacBio tools

PacBio tools report summary statistics of the following format:
```
ZMWs input          (A)  : 47
ZMWs generating CCS (B)  : 22 (46.81%)
ZMWs filtered       (C)  : 25 (53.19%)

Exclusive ZMW counts for (C):
Median length filter     : 0 (0.00%)
Below SNR threshold      : 0 (0.00%)
Lacking full passes      : 20 (80.00%)
Heteroduplex insertions  : 0 (0.00%)
Coverage drops           : 0 (0.00%)
Insufficient draft cov   : 0 (0.00%)
Draft too different      : 0 (0.00%)
Draft generation error   : 0 (0.00%)
Draft above --max-length : 0 (0.00%)
Draft below --min-length : 0 (0.00%)
Reads failed polishing   : 0 (0.00%)
Empty coverage windows   : 0 (0.00%)
CCS did not converge     : 0 (0.00%)
CCS below minimum RQ     : 5 (20.00%)
Unknown error            : 0 (0.00%)
```

In cases where PacBio tools such as `CCS` are run in scatter mode, a report is produced for every individual scatter.
To get a full picture of the statistics that have been produced by `CCS`, these report files have to be merged back together.
This tool parses the content of the PacBio report files into json, and can output the merged and original files in both json and PacBio format.
Currently, only the counts are supported, while the percentages are left out.
