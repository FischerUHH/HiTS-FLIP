# Publication 

# HiTS-FLIP
'high-throughput sequencing–fluorescent ligand interaction profiling' (HiTS-FLIP) is an experiment which enables the study of target-molecules with millions of varying DNA-Sequences in parallel on a fow cell of next generation sequencers - in this case Illuminas MiSeq.

In the corresponding publication we present two different ways of examining the interactions between target-molecule and DNA:
1. The experiment can be carried out by connecting an external valve to the tubing and controlling it via USB. By addition of specific wait-times to the `recipe`, in which the execution of the sequencers main program pauses, the switching of the valve can be triggered as a custom python script reads out the `log`-files which are generated as the routine proceeds. This approach is recommended for setups which require larger amounts of reagents than 3 mL.
2. The second approach uses soley the internal valve of the MiSeq subsequent to a "regular" sequencing. Therefore a used cartridge of the previous sequencing run has to be customized by removing the RFID and the clear top cover. After cleaning the contained tubes carefully they can be filled with a solution of the desired target molecule.

# Installation Guide
## Hardware Requirements
For the experiments a MiSeq Sequencer (Illumina) was modified according to the corresponding manuscript. 

> [!CAUTION] 
> The University of Hamburg assumes no responsibility or liability for any errors or omissions in the content of this document and repository. The information contained in this document is provided on an "as is" basis with no guarantees of completeness, accuracy,  usefulness or timeliness and without any warranties of any kind whatsoever, express or implied. 
> 
> Any modifications made to the MiSeq Sequencer are done at your own risk. The University of Hamburg will not be liable for any damages arising from the modification, use, or reliance on the modified MiSeq Sequencer, including but not limited to, direct, indirect, incidental, punitive, and consequential damages.
>
> By proceeding with any technical modifications to the MiSeq Sequencer, you acknowledge and agree that:
>
> 1. You are solely responsible for any and all outcomes resulting from such modifications.
> 2. You fully understand that modifying the MiSeq Sequencer may void any existing warranties.
> 3. The University of Hamburg, including its employees, faculty, and staff, shall not be held accountable for any damage to property or persons, malfunctions, or loss of data resulting from the modification of the MiSeq Sequencer.
> 4. You undertake all necessary precautions to ensure that the modification complies with all applicable laws, regulations, and guidelines.
> 5. You release the University of Hamburg from any and all claims, actions, damages, liabilities, costs, and expenses (including attorney's fees) arising out of or connected with the modification of the MiSeq Sequencer.
>
> If you are uncertain about any aspect of modifying the MiSeq Sequencer, it is advised that you consult with a qualified professional or directly contact the manufacturer before proceeding.

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

