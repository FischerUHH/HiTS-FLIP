# HiTS-FLIP
'high-throughput sequencing–fluorescent ligand interaction profiling' (HiTS-FLIP) is an experiment which enables the study of target-molecules with millions of different DNA-Sequences in parallel on a fow cell of next generation sequencers.

There are two possible ways of examining the interactions between 

# Installation Guide
## Hardware Requirements
For the experiments a MiSeq Sequencer (Illumina) was modified according to the corresponding manuscript. 

> [!CAUTION] 
> Modifing the MiSeq will result in loss of warranty and may lead to irreversible damage to the device, esp. when fiddling with the focus settings.

## Software Requirements
### MiSeq Control Software 
### External Valve
For the use of an external valve python 3.8 was installed on the MiSeq along with the folling packages:
- `VICI`
- `ftdi_serial`
- `pandas`

### Data Extractrion
Data extraction from `cif`,`loc` and`fastq`-files was performed using python 3.11 utilizing the following packages:
- `numpy`
- `matplotlib`


# Installation Guide
## HiTS-FLIP with external valve
If using an external valve, install python and copy the folder `MiSeq_Hits_Flip` to `C:\` of your MiSeq. Also install the drivers for the valve. Afterwards make the alias `sv [pos]`accessible by typing 
`reg add "HKCU\Software\Microsoft\Command Processor" /v Autorun /d "doskey /macrofile=\"C:\MiSeq_Hits_Flip\BatchFiles\Makros.doskey\"" /f`
into the terminal on the sequencer. 
Make a copy your `Amplicon` recipe from `CustomRecipe` on `D:\` and add the lines supplied in XXXXX.

## HiTS-FLIP from custom filled cartride

## Changes in the configs

### MiSeqOverrride

