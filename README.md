# H.E.L.E.N.
H.E.L.E.N. (Haplotype Embedded Long-read Error-corrector for Nanopore)


[![Build Status](https://travis-ci.com/kishwarshafin/helen.svg?branch=master)](https://travis-ci.com/kishwarshafin/helen)

`HELEN` is a polisher intended to use for polishing human-genome assemblies generated by the [Shasta](https://github.com/chanzuckerberg/shasta) assembler. `HELEN` operates on the pileup summary generated by [MarginPolish](https://github.com/UCSC-nanopore-cgl/marginPolish). `MarginPolish` uses a probabilistic graphical-model to encode read alignments through a draft assembly to find the maximum-likelihood consensus sequence. The graphical-model operates in run-length space, which helps to reduce errors in homopolymeric regions. `MarginPolish` can produce tensor-like summaries encapsulating the internal likelihood weights. The weights are assigned to each genomic position over multiple likely outcomes that is suitable for inference by a Deep Neural Network model.

`HELEN` uses a Recurrent-Neural-Network (RNN) based Multi-Task Learning (MTL) model that can predict a base and a run-length for each genomic position using the weights generated by `MarginPolish`. The combination of `Shasta-MarginPolish-HELEN` produces state-of-the-art Oxford Nanopore based human genome assemblies.

© 2019 Kishwar Shafin, Trevor Pesout, Benedict Paten. <br/>
Computational Genomics Lab (CGL), University of California, Santa Cruz.

## Why MarginPolish-HELEN ?
* `MarginPolish-HELEN` outperforms other graph-based and Neural-Network based polishing pipelines.
* Highly optimized pipeline that is faster than any other available polishing tool (~5 hours for `HELEN`).
* We have <b>sequenced-assembled-polished 12 samples</b> to ensure robustness, runtime-consistency and cost-efficiency.
* We tested GPU usage on `Amazon Web Services (AWS)` and `Google Cloud Platform (GCP)` to ensure scalability.
* Open source [(MIT License)](LICENSE).

## Table of contents
* [Workflow](#workflow)
* [Results](#Results)
* [Twelve high-quality assemblies](#Twelve-high-quality-assemblies)
* [Installation](#Installation)
* [Usage](#Usage)
* [Models](#Models)
   * [Released Models](#Released-Models)
* [Runtime and Cost](#Runtime-and-Cost)
* [Help](#Help)
* [Acknowledgement](#Acknowledgement)

## Workflow

The workflow is as follows:
* Generate an assembly with [Shasta](https://github.com/chanzuckerberg/shasta).
* Create a mapping between reads and the assembly using [Minimap2](https://github.com/lh3/minimap2).
* Use [MarginPolish](https://github.com/UCSC-nanopore-cgl/marginPolish) to generate the images.
* Use HELEN to generate a polished consensus sequence.
<p align="center">
<img src="img/pipeline.svg" alt="pipeline.svg" height="640p">
</p>


## Results
We compared `Medaka` and `HELEN` as polishing pipelines on Shasta assembly with `assess_assembly` module available from `Pomoxis`. The summary of the quality we produce is here:

<p align="center">
<img src="img/accuracy_plot.png" alt="accuracy_plot" height=420p>
</p>

<b> NOTE: A full set of results can be found [here](docs/results.md) </b>

## Twelve high-quality assemblies
We have sequenced-assembled-polished 12 human genome assemblies at University of California, Santa Cruz with our pipeline. They can be downloaded from our [google bucket](https://console.cloud.google.com/storage/browser/kishwar-helen/polished_genomes/london_calling_2019/).

For quick links, please copy a link from this table and you can run `wget` to download the files:
```bash
wget <link>
```
The twelve assemblies with their download links:

<table>
  <tr>
    <th>Sample name</th>
    <th>Download link</th>
  </tr>
  <tr>
    <td>CHM13</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/CHM13_shasta_marginpolish_helen_consensus.fa">CHM13_download_link</a></td>
  </tr>
  <tr>
    <td>HG00733</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG00733_shasta_marginpolish_helen_consensus.fa">HG00733_download_link</a></td>
  </tr>

  <tr>
    <td>HG01109</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG01109_shasta_marginpolish_helen_consensus.fa">HG01109_download_link</a></td>
  </tr>
  <tr>
    <td>HG01243</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG01243_shasta_marginpolish_helen_consensus.fa">HG01243_download_link</a></td>
  </tr>
  <tr>
    <td>HG02055</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG02055_shasta_marginpolish_helen_consensus.fa">HG02055_download_link</a></td>
  </tr>
  <tr>
    <td>HG02080</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG02080_shasta_marginpolish_helen_consensus.fa">HG02080_download_link</a></td>
  </tr>
  <tr>
    <td>HG02723</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG02723_shasta_marginpolish_helen_consensus.fa">HG02723_download_link</a></td>
  </tr>
  <tr>
    <td>HG03098</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG03098_shasta_marginpolish_helen_consensus.fa">HG03098_download_link</a></td>
  </tr>
  <tr>
    <td>HG03492</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/HG03492_shasta_marginpolish_helen_consensus.fa">HG03492_download_link</a></td>
  </tr>
  <tr>
    <td>GM24143</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/GM24143_shasta_marginpolish_helen_consensus.fa">GM24143_download_link</a></td>
  </tr>
  <tr>
    <td>GM24149</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/GM24149_shasta_marginpolish_helen_consensus.fa">GM24149_download_link</a></td>
  </tr>
  <tr>
    <td>GM24385/HG002</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/polished_genomes/london_calling_2019/GM24385_shasta_marginpolish_helen_consensus.fa">GM24385_download_link</a></td>
  </tr>
</table>

## Installation
`MarginPolish` and `HELEN` can be used in Linux-based system. Users can install `MarginPolish` and `HELEN` on <b>`Ubuntu 18.04`</b> by following this document.

### Step 1: Install MarginPolish

To install MarginPolish in a Ubuntu/Linux bases system, follow these instructions:

##### Install Dependencies
```bash
sudo apt-get -y install cmake make gcc g++ autoconf bzip2 lzma-dev zlib1g-dev
sudo apt-get -y install libcurl4-openssl-dev libpthread-stubs0-dev libbz2-dev
sudo apt-get -y install liblzma-dev libhdf5-dev
```

##### Install marginPolish
```bash
git clone https://github.com/UCSC-nanopore-cgl/marginPolish.git
cd marginPolish
git submodule update --init
```
Make a build directory:
```bash
mkdir build
cd build
```

Generate makefile:
```bash
cmake ..
make
./marginPolish
# to create a symlink
ln -s marginPolish /usr/local/bin
```

### Step 2: Install HELEN with GPU

Although `HELEN` can be used in a `CPU` only machine, we highly recommend using a machine with `GPU`.

This requires installing `CUDA` and the right `PyTorch` version compiled against the installed version of `CUDA`.

##### Install CUDA
To download `CUDA` for `Ubuntu 18.04` follow these insructions:
```bash
# download CUDA for ubuntu 18.04 x86_64 by running:
wget https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_410.48_linux
# if you are using other systems please download the correct version from here:
# https://developer.nvidia.com/cuda-10.0-download-archive

# install CUDA by running:
sudo sh cuda_10.0.130_410.48_linux.run
# 1) Read or scroll through the EULA (you can press 'z' to scroll down).
# 2) Accept the EULA, put yes for OpenGL library, CUDA toolkit.
#    Installing CUDA-samples is optional

# once installed, verify the right version by running:
cat /usr/local/cuda/version.txt
# Expected output: CUDA Version 10.0.130

# Verify that you can see your GPU status by running:
nvidia-smi
```

##### Install PyTorch
Please follow the instructions from this [pytorch-installation-guide](https://pytorch.org/get-started/locally/) to install the right `PyTorch` version.

```bash
# if you are using Ubuntu 18.04, python3 version 3.6.7 and CUDA 10.0 then follow these commands:
python3 -m pip install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp36-cp36m-linux_x86_64.whl
python3 -m pip install torchvision

# otherwise install the right version by following the instructions from:
# https://pytorch.org/get-started/locally/
```

We have tested these PyTorch versions against `HELEN` to ensure GPU accelerated inference:
* PyTorch 1.0 with CUDA 10.0
* PyTorch 1.1 with CUDA 10.0

To ensure `PyTorch` is using `CUDA`, you can follow these instructions:
```bash
$ python3
>>> import torch
>>> torch.cuda.is_available()
TRUE
# the expected output is TRUE
```

#### Install HELEN
`HELEN` requires `cmake` and `python3` to be installed in the system.
```bash
sudo apt-get -y install cmake
sudo apt-get -y install python3
sudo apt-get -y install python3-dev
```
To install `HELEN`:

```bash
git clone https://github.com/kishwarshafin/helen.git
cd helen
./build.sh
```

These steps will install `HELEN` in your local system. `HELEN` also requires installing some python3 packages.
```bash
python3 -m pip install h5py tqdm numpy torchnet
```

We also maintain an [Installation Guide](docs/installation.md) on how to install `MarginPolish` and `HELEN` for reference.

## Usage
`MarginPolish` requires a draft assembly and a mapping of reads to the draft assembly. We commend using `Shasta` as the initial assembler and `MiniMap2` for the mapping.

#### Step 1: Generate an initial assembly
Although any assembler can be used to generate the initial assembly, we highly recommend using [Shasta](https://github.com/chanzuckerberg/shasta).

Please see the [quick start documentation](https://chanzuckerberg.github.io/shasta/QuickStart.html) to see how to use Shasta. Shasta requires memory intensive computing.
> For a human size assembly, AWS instance type x1.32xlarge is recommended. It is usually available at a cost around $4/hour on the AWS spot market and should complete the human size assembly in a few hours, at coverage around 60x.

An assembly can be generated by running:
```bash
# you may need to convert the fastq to a fasta file
shasta/shasta-Linux-0.1.0 --input <reads.fa> --output <path_to_shasta_output>
```

#### Step 2: Create an alignment between reads and shasta assembly
We recommend using `MiniMap2` to generate the mapping between the reads and the assembly.
```bash
# we recommend using FASTQ as marginPolish uses quality values
# This command can run MiniMap2 with 32 threads, you can change the number as you like.
minimap2 -ax map-ont -t 32 shasta_assembly.fa reads.fq | samtools sort -@ 32 | samtools view -hb -F 0x104 > reads_2_assembly.bam
samtools index -@32 reads_2_assembly.bam

#  the -F 0x104 flag removes unaligned and secondary sequences
```
#### Step 3: Generate images using MarginPolish
To generate images with MarginPolish run:
```bash
marginPolish \
</path/to/reads_2_assembly.bam> \
<path/to/shasta_assembly.fa> \
<path/to/marginpolish/params/allParams.np.human.guppy-ff-235.json> \
-t <number_of_threads> \
-o </path/to/marginpolish_output/marginpolish_images> \
-f 2>&1 | tee </path/to/marginpolish.log>
```

#### Step 4: Run HELEN

##### Download Model
Before running `call_consensus.py` please download the appropriate model suitable for your data. Please read our [model guideline](#Model) to understand which model to pick.

##### Run call_consensus.py
First we have to run `call_consensus.py` to generate all the predictions:
```bash
python3 call_consensus.py \
--image_file </path/to/marginpolish_output/marginpolish_images> \
--batch_size 512 \
--model_path <path/to/helen_models/HELEN_v0_lc_r941_flip233_hap.pkl> \
--output_dir <path/to/helen_out/consensus_sequence/> \
--num_workers 32 \
--gpu_mode 1

# you can run CPU inference by removing --gpu_mode parameter
```

##### Run stitch.py
Finally you can run `stitch.py` to get a consensus sequence:
```bash
python3 stitch.py \
--sequence_hdf <path/to/helen_out/consensus_sequence/helen_predictions.hdf> \
--output_dir <path/to/helen_out/consensus_sequence/> \
--threads 32
```

<b>NOTE: We are working on a documentation with instructions for running this pipeline end-to-end.  </b>

## Models
#### Released models
Change in the basecaller algorithm can directly affect the outcome of HELEN. We will release trained models with new basecallers as they come out.
<center>

<table>
  <tr>
    <th>Model Name</th>
    <th>Release Date</th>
    <th>Intended base-caller</th>
    <th>Link</th>
    <th>Comment</th>
  </tr>
  <tr>
    <td>HELEN_v0_lc_r941_flip235.pkl</td>
    <td>21/05/2019</td>
    <td>Guppy 2.3.5</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/helen_trained_models/v0_london_calling_2019/HELEN_v0_lc_r941_flip235.pkl">Model_link</a></td>
    <td>The model trained on autosomes of HG002 except chr 20 <br>with Guppy 2.3.5 base called data.</td>
  </tr>
  <tr>
    <td>HELEN_v0_lc_r941_flip233.pkl</td>
    <td>21/05/2019</td>
    <td>Guppy 2.3.3</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/helen_trained_models/v0_london_calling_2019/HELEN_v0_lc_r941_flip233.pkl">Model_link</a></td>
    <td>The model trained on autosomes of HG002 except <br>chr 20 with Guppy 2.3.3 base called data.</td>
  </tr>
  <tr>
    <td>HELEN_v0_lc_r941_flip233_hap.pkl</td>
    <td>21/05/2019</td>
    <td>Guppy 2.3.3</td>
    <td><a href="https://storage.googleapis.com/kishwar-helen/helen_trained_models/v0_london_calling_2019/HELEN_v0_lc_r941_flip233_hap.pkl">Model_link</a></td>
    <td>The model trained on haploid regions of HG002.</td>
  </tr>
</table>
</center>

We have seen significant difference in the homopolymer base-calls between different basecallers. It is important to pick the right version for the best polishing results.

[Ryan Lorig-Roach](https://github.com/rlorigro) generated confusion matrix for each step of the assembly.
We can see the difference in base caller versions to understand the imporantance of picking the right model.

Confusion matrix of Guppy 2.3.1 on CHM13 chromosome X:
<img src="img/RL_confusion_guppy231.png" alt="guppy235" width="1080p"> <br/>

Confusion matrix of Guppy 2.3.5 on HG002 chromosome 1-10:
<img src="img/RL_confusion_guppy235.png" alt="guppy235" width="1080p"> <br/>

#### Model Schema

HELEN implements a Recurrent-Neural-Network (RNN) based Multi-task learning model with hard parameter sharing. It implements a sliding window method where it slides through the input sequence in chunks. As each input sequence is evaluated independently, it allows HELEN to use mini-batch during training and testing.

<p align="center">
<img src="img/model_schema.svg" alt="pipeline.svg" height="640p">
</p>

## Runtime and Cost
`MarginPolish-HELEN` ensures runtime consistency and cost efficiency. We have tested our pipeline on `Amazon Web Services (AWS)` and `Google Cloud Platform (GCP)` to ensure scalability.

We studied several samples of 50-60x coverage and created a suggestion framework for running the polishing pipeline. Please be advised that these are cost-optimized suggestions. For better run-time performance you can use more resources.
#### Google Cloud Platform (GCP)
For `MarginPolish` please use n1-standard-64 (64 vCPUs, 240GB RAM) instance. <br/>
Our estimated run-time is: 12 hours
Estimated cost for `MarginPolish`: <b>33$</b>

For `HELEN`, our suggested instance type is:
* Instance type: n1-standard-32 (32 vCPUs, 120GB RAM)
* GPUs: 2 x NVIDIA Tesla P100
* Disk: 2TB SSD
* Cost: 4.65$/hour

The estimated runtime with this instance type is 6 hours. <br>
The estimated cost for `HELEN` is <b>28$</b>.

Total estimated run-time for polishing: 18 hours. <br/>
Total estimated cost for polishing: 61$

#### Amazon Web Services (AWS)
For `MarginPolish` we recommend c5.18xlarge (72 CPU, 144GiB RAM) instance. <br/>
Our estimated run-time is: 10 hours
Estimated cost for `MarginPolish`: <b>39$</b>

We recommend using `p2.8xlarge` instance type for `HELEN`. The configuration is as follows:
* Instance type: p2.8xlarge (32 vCPUs, 488GB RAM)
* GPUs: 8 x NVIDIA Tesla K80
* Disk: 2TB SSD
* Cost: 7.20$/hour

The estimated runtime with this instance type: 5 hours <br>
The estimated cost for `HELEN` is: <b>36$</b>

Total estimated run-time for polishing: 18 hours. <br/>
Total estimated cost for polishing: 75$

Please see our detailed [run-time case study](docs/runtime_cost.md) documentation for better insight.

## Help
Please open a github issue if you face any difficulties.

## Acknowledgement
We are thankful to [Segey Koren](https://github.com/skoren) and [Karen Miga](https://github.com/khmiga) for their help with `CHM13` data and evaluation.

We downloaded our data from [Telomere-to-telomere consortium](https://github.com/nanopore-wgs-consortium/CHM13) to evaluate our pipeline against `CHM13`.

We acknowledge the work of the developers of these packages: </br>
* [Shasta](https://github.com/chanzuckerberg/shasta/commits?author=paoloczi)
* [pytorch](https://pytorch.org/)
* [ssw library](https://github.com/mengyao/Complete-Striped-Smith-Waterman-Library)
* [hdf5 python (h5py)](https://www.h5py.org/)
* [pybind](https://github.com/pybind/pybind11)
* [hyperband](https://github.com/zygmuntz/hyperband)

© 2019 Kishwar Shafin, Trevor Pesout, Benedict Paten.
