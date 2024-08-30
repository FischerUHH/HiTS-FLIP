# Automated High-Throughput Selection of DNA Aptamers Using a Common Optical Next-Generation Sequencer

Alissa Drees, Christian Ahlers, Timothy Kehrer, Natascha Ehmke, Alice Frederike Rosa Grün, Charlotte Uetrecht, Zoya Ignatova, Udo Schumacher, Markus Fischer

Pre-print: https://www.biorxiv.org/content/10.1101/2024.06.24.600375v1

# 1 HiTS-FLIP

'High-throughput sequencing–fluorescent ligand interaction profiling' (HiTS-FLIP) is an experiment that enables the study of target molecules with millions of varying DNA sequences in parallel on a flow cell of next-generation sequencers - in this case, Illumina's MiSeq.

In the corresponding publication, we present two different approaches of examining the interactions between target molecules and DNA:

## 1.1 Additional External Valve

The experiment can be carried out by connecting an external valve to port 23 of the internal valve and controlling it via USB. By adding specific wait-times to the recipe `HiTS_FLIP_RECIPE`, in which the execution of the sequencer's main program pauses, the switching of the valve can be triggered as a custom Python script reads out the `log` files which are generated as the routine proceeds. This approach is recommended for setups which require larger reagent volumes than 3 mL and enables the user to execute the sequencing and interaction profiling in one step with minimal hands-on time.

## 1.2 Without Modification of the Hardware

This approach starts with a "regular" proprietary sequencing of the library. The FLIP is performed in a second experiment solely using the internal valve of the MiSeq. A used cartridge of the previous sequencing run has to be customized by removing the RFID and the clear top cover. After cleaning the contained tubes carefully, they can be filled with custom solutions of the desired target molecule in the corresponding buffer. The FLIP can be started by removing the used RFIDs from the other used consumables and holding the RFIDs of a new kit against the RFID sensors during setup. The "new" RFIDs are not corrupted by this process and can be used regularly later on. Despite the requirement for an additional working step, this setup comes with integrated cooling and a lower consumption of target solution, therefore enabling the measurement of triplicates.

# 2. Installation Guide

## 2.1 Hardware Requirements

For the experiments, a MiSeq sequencer (Illumina) was modified according to the corresponding manuscript.

> [!CAUTION] 
> The University of Hamburg assumes no responsibility or liability for any errors or omissions in the content of this document and repository. The information contained in this documentation is provided on an "as is" basis with no guarantees of completeness, accuracy, usefulness, or timeliness and without any warranties of any kind whatsoever, express or implied. 
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
> 6. By accessing or using this document and its associated repository, you explicitly acknowledge that you have read, understood, and agree to be bound by the terms and conditions outlined in this disclaimer. If you do not agree to these terms, you must refrain from making any modifications to the MiSeq Sequencer and discontinue any related activities.
>
> If you are uncertain about any aspect of modifying the MiSeq Sequencer, it is advised that you consult with a qualified professional or directly contact the manufacturer before proceeding.

## 2.2 Software Requirements

2.2.1 MiSeq Control Software

We used MiSeq Control Software V2.6.2.1 but the experiment can also be implemented on newer versions.

2.2.2 External Valve

For the use of an external valve, Python 3.8 was installed on the MiSeq along with the following packages:
- `VICI`
- `ftdi_serial`
- `pandas`

# 3. Installation Guide

## 3.1 HiTS-FLIP Using an Additional External Valve

If using an external valve, install Python and copy the folder [MiSeq_Hits_Flip](MiSeq_Hits_Flip) to `C:\` on your MiSeq. Also, install the drivers for the valve. Afterward, make the alias `sv [pos]` accessible by typing

```bash
reg add "HKCU\Software\Microsoft\Command Processor" /v Autorun /d "doskey /macrofile=\"C:\MiSeq_Hits_Flip\BatchFiles\Makros.doskey\"" /f
```


into the terminal on the sequencer. Afterward, you can use [getSerialAdress.py](MiSeq_Hits_Flip/PythonCode/getSerialAdress.py) to get the serial address and add it to line 27 in [setValve.py](MiSeq_Hits_Flip/PythonCode/setValve.py). From now on the valve can be switched using the command `sv [position]`. Every command send to and recieved from the valve will be logged to [ViciVavleLogs](MiSeq_Hits_Flip/ViciVavleLogs/)

As the recipe for the first approach using the external valve contains Illumina's sequencing routine, we refrain from publishing the complete recipe to preserve Illumina's copyright. Therefore, you need to assemble it yourself: Make a copy of your `Amplicon` recipe from `D:\Illumina\MiSeq Control Software\CustomRecipe\`, rename it to `HiTS_FLIP_RECIPE`, and add the lines/modifications supplied in [HiTS_FLIP_RECIPE_ADDITION](HiTS_FLIP_RECIPE_ADDITION).

While executing the custom `HiTS_FLIP_RECIPE` by specifying the recipe in the sample sheet prior to sequencing, [HiTS_FLIP_main.py](MiSeq_Hits_Flip/PythonCode/HiTS_FLIP_main.py) has to be run to monitor the progress of sequencing and FLIP by reading out the log-files.

## 3.2 HiTS-FLIP from Custom Filled Cartridge

Copy [FLIP_RECIPE](FLIP_RECIPE) to `D:\Illumina\MiSeq Control Software\CustomRecipe\`. Specify the custom recipe in the samplesheet.

## 3.3 Changes in the Configs

3.3.1 C:\MiSeqOverride.xml

These are settings we found to be helpful. Channel Focus C corresponds with the PhiX-FM using IRDye700. The other settings might help you if no focus can be found at the beginning of read two.

```cfg
[Focus Params]
ChannelToUse = Focus C
LowSNRContrastThreshold = 2
DarkSampleContrastThreshold = 1
```



3.3.2 C:\Illumina\RTA\Configs\MiSeq.Configuration.xml

To keep the raw images and re-run the RTA after sequencing the following lines should be adapted. But be warned: this produces a lot of data and you'll have to free up drive space after every run by moving the images to an external hard-drive or server.   

```xml
<CopyIntensities>true</CopyIntensities>
<DeleteImagesFilesAfterProcessing>false</DeleteImagesFilesAfterProcessing>
```


3.3.3 D:\Illumina\MiSeq Control Software\MiSeqSoftware.Options.cfg

```xml
<SaveImagesToOutputForRta>true</SaveImagesToOutputForRta>
<SaveFocusImages>true</SaveFocusImages>
<SaveScanImages>true</SaveScanImages>
```

