# Integration of the ADASTRA database as a novel annotator module in the OpenCRAVAT pipeline

Students:

* Kuznetsov Stepan
* Fofanov Mikhail
* Suponin Andrey

Supervisor:
* Kasyanov Artem, IITP RAS

## Motivation

Currently, there are a large number of ways to annotate genetic variants and various databases containing results of variant calling from different experiments. Here, we used the OpenCRAVAT pipeline able to annotate SNPs and other genetic variants using more than 150 databases and added a novel module to it that contains ADASTRA database. The ADASTRA database contains information about allele-specific transcription factor binding events. A Transcription Factor (TF) might prefer to bind one of two alternative alleles of homologous chromosomes and thus exhibit allele-specific binding (ASB). ASB highlights regulatory SNPs with high potential to affect gene expression.

## Integration of a novel ADASTRA annotator module in the OpenCRAVAT pipeline

![image](https://user-images.githubusercontent.com/70381751/169640530-d6e9a033-d517-4a49-bddf-1f6b4cbbefb5.png)

## Requirements

This project has been tested using the following software:

Feature | Version
------------ | -------------
Operating system | Ubuntu 20.04
Python | Python 3.9
OpenCRAVAT | open-cravat 2.2.7
ADASTRA database | ADASTRA v4.0

You can install the versions of the python libraries that were used during the testing of the pipeline using the requirements.txt:

```
pip install -r requirements.txt
```

## Installation

Cloning the OpenCravat-Adastra github repository and install requirements.

```
git clone https://github.com/gottalottarock/OpenCravat-Adastra.git
cd OpenCravat-Adastra
pip install -r requirements.txt
```

To download the Adastra database, you need to contact one of the developers of this repository.  
Move adastra.sqlite to `adastra/data`  
   
Next, you need to transfer the module and widget to the open-cravat repo.   

```
OC_MODULES_PATH=$(oc config md)  
cp -r ./OpenCravat-Adastra/adastra/ $OC_MODULES_PATH/annotators/  
cp -r ./OpenCravat-Adastra/wgadastra/ $OC_MODULES_PATH/webviewerwidgets/  
```

NOTE: 
Make sure you can open adastra.slick and select the contents of the tables,  
 otherwise you need to fix permissions.


## Usage

Run OpenCRAVAT pipeline with a novel ADASTRA annotator module

```
oc run example_input_new.vcf -a adastra -l hg38
```

Open the results from OpenCRAVAT pipeline with a novel ADASTRA annotator module in browser

```
oc gui example_input_new.vcf.sqlite
```

## Results

### Results of an annotation via a novel ADASTRA annotator module

![table_1](https://user-images.githubusercontent.com/70381751/169640611-248f4004-fa2b-4c57-b4e0-1ae3900717e5.png)

![table_2](https://user-images.githubusercontent.com/70381751/169640638-090e8738-8282-41ac-a330-7e4ce825db38.png)

### Background Allelic Dosage

Background Allelic Dosage (BAD) is the expected ratio of major to minor allelic frequencies in a particular genomic region. For example, if a copy number of two alternating alleles is the same (e.g. 1:1 (diploid), 2:2, or 3:3), then the respective region has BAD=1, i.e. the expected ratio of reads mapped to alternative alleles on heterozygous SNVs is 1. All triploid regions have BAD=2 and the expected allelic read ratio is either 2 or ½. In general, if BAD of a particular region is known, then the expected frequencies of allelic reads are 1/(BAD +1) and BAD/(BAD + 1).
ASB significance (FDR)

### Allele-Specific Binding

ASB stands for Allele-Specific Binding. A Transcription Factor (TF) might prefer to bind one of two alternative alleles of homologous chromosomes and thus exhibit allele-specific binding. ASB highlights regulatory SNPs with high potential to affect gene expression.

Allele-Specific Binding

![image](https://user-images.githubusercontent.com/70381751/169641314-4d2494fb-8ebb-4733-8afe-ba0fcdedee13.png)

The alignment of the motif relative to the SNP is shown at the top. Motif P-values indicate the predicted binding specificities for the alternative alleles. The preferred allele according to ADASTRA data along with the ASB FDR and Effect Size is shown at the bottom. The higher bell corresponds to the allele preferentially bound by the TF in vivo according to the underlying ChIP-Seq data. The DNA strand/orientation is marked in the bottom left corner.

### ASB effect size

The Effect Size of an ASB event is calculated separately for Reference and Alternative alleles and is defined as the weighted mean of log-ratios of observed and expected allelic read counts, with weights being -log10 of the respective P-values.

### Motif Concordance

Motif Concordance indicates whether the allelic read imbalance is consistent with the transcription factor motif Fold Change (FC, predicted from sequence analysis). The following notation is used:

*  n/a: Motif is not available;
*  No hit: The best hit P-value is higher than 0.0005 threshold;
*  Weak concordant: The absolute value of FC is less than 2 but consistent with the allelic read imbalance;
*  Weak discordant: The absolute value of FC is less than 2 and not consistent with the allelic read imbalance;
*  Concordant: The absolute value of FC is greater or equal to 2 and consistent with allelic read imbalance;
*  Discordant: The absolute value of FC is greater or equal to 2 but not consistent with allelic read imbalance.

![image](https://user-images.githubusercontent.com/70381751/169641105-abaa7bc4-9841-4179-a2a2-ceaf34c98ae1.png)


For more information please visit: [Link](https://adastra.autosome.org/zanthar/help) and  [Link](https://ananastra.autosome.org/help)

## References

### Landscape of allele-specific transcription factor binding in the human genome.

Sergey Abramov, Alexandr Boytsov, Dariia Bykova, Dmitry D. Penzar, Ivan Yevshin, Semyon K. Kolmykov, Marina V. Fridman, Alexander V. Favorov, Ilya E. Vorontsov, Eugene Baulin, Fedor Kolpakov, Vsevolod J. Makeev, Ivan V. Kulakovskiy. Nature communications, 2021. doi: 10.1038/s41467-021-23007-0

### ANANASTRA: annotation and enrichment analysis of allele-specific transcription factor binding at SNPs.

Alexandr Boytsov, Sergey Abramov, Ariuna Z Aiusheeva, Alexandra M Kasianova, Eugene Baulin, Ivan A Kuznetsov, Yurii S Aulchenko, Semyon Kolmykov, Ivan Yevshin, Fedor Kolpakov, Ilya E Vorontsov, Vsevolod J Makeev, Ivan V Kulakovskiy. Nucleic Acids Research, 2022 doi: 10.1093/nar/gkac262

### Integrated Informatics Analysis of Cancer-Related Variants.

Pagel KA, Kim R, Moad K, Busby B, Zheng L, Tokheim C, Ryan M, Karchin R. JCO Clin Cancer Inform, 2020. doi: 10.1200/CCI.19.00132.
