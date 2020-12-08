# transformers-for-qde
This repo contains the code used in the thesis  “Transformers for Question Difficulty Estimation from Text”. 

## Dataset
The dataset cointaining the interactins of ASSISTments can be download [here](https://sites.google.com/site/assistmentsdata/home/2012-13-school-data-with-affect).

The dataset cointaining the text of the questions can be requested [here](https://sites.google.com/site/assistmentsdata/home/assistments-problems).

## Usage

The results obtained can be replicated running in the following order:

1. *pre_processing.py*
2. *create_train_ds.py*
3. *transformers_to_qde.ipynb*

Costant parameters can be changed in *utils/constant.py*