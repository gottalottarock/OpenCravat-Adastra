# ADASTRA

The ADASTRA database contains information about allele-specific transcription factor binding events. Allele-specific binding (ASB) highlights regulatory SNPs with high potential to affect gene expression. 

For every SNP in database ADASTRA provides the following information about ASB: names of top 5 TFs, total number of TF, names of top 3 cell types, total number of cell types and motif concordance(1).

Additionally, for each TF and cell type, the tool shows: the effect size of an ASB event for reference and alternative alleles (log2-scale), ASB significance (FDR columns) for reference and alternative alleles, background allelic dosage (BAD)(2). 


1) Motif Concordance indicates whether the allelic read imbalance is consistent with the transcription factor motif Fold Change (FC, predicted from sequence analysis). The following notation is used:\
o  n/a: Motif is not available;\
o  No hit: The best hit P-value is higher than 0.0005 threshold;\
o  Weak concordant: The absolute value of FC is less than 2 but consistent with the allelic read imbalance;\
o  Weak discordant: The absolute value of FC is less than 2 and not consistent with the allelic read imbalance;\
o  Concordant: The absolute value of FC is greater or equal to 2 and consistent with allelic read imbalance;\
o  Discordant: The absolute value of FC is greater or equal to 2 but not consistent with allelic read imbalance.

2) BAD is the expected ratio of major to minor allelic frequencies in a particular genomic region.

For more information please visit: https://adastra.autosome.org/zanthar/help
