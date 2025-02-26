# BN-research-project
### This Read me is for the purpose of introduction.
![Work done in colaboration with our Research Project supervisors](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.econometrie.nl%2Fnl%2Funiversiteiten%2Frug%2F&psig=AOvVaw0q724EmOwTGkZixX3WHhp1&ust=1740490419896000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCIDLtpu23IsDFQAAAAAdAAAAABAE)

> [!IMPORTANT]
> The files and scripts in this repository are purely for analysis of time spent in a specific **circular** region of interest. 

How to, for the the use of Deeplabcut on Colab can be found [here](#deeplabcut-through-colab), the local use of the software ***(Recommended; if possible through school or company GPU clusters, personal machines are also fine)***.
Can be guided using the DLC github page (Mathis labs) [here](https://github.com/DeepLabCut/DeepLabCut).

> [!NOTE]
> This repository has been created for the analysis of our own results, but has been made **accessible** for others. Thus integration might be flawed upon raw download. 

## How to use 
This is repository is for analysis of DeepLabCut output files. Specifically fitted to .h5 file.

You can **__clone__** this repository for its files through your compiler. 
> [!IMPORTANT]
> ***You will need to change the paths to certain folderlocations yourself, dont forget to do so.*** 

After cloning it is really up to following the instructions in the Jupyter Notebooks and or ###[enter the website thingy here] provided. You can do the [set_ratios.ipynb](https://github.com/nikulkaaa/BN-research-project/blob/main/set_ratios.ipynb) Notebook prior to actual analysis. This is important since the calculations require some sort of pixel to cm ratio.

Analysis depends on the accuracy of both the model and the labelling, keep in mind that one should always check the videos after application of the model for visual disturbances or problems. 
You can increase these plausibly through:
>* Retraining
>* Adding more labelling
>* Add more variance within labelling
>* Increasing amount of Epochs or Iterrations, till the lr hits 0,05 and plateaus.

## DeepLabCut through Colab

When you are not able to run DeepLabcut locally, due to either hardware specific issues or driver issues. 
You can use an online Colab workspace with proper instructions provided by "Thsi persons" [here](Link to colab).

You need to upload your files to an available Google Drive. Afterward you need to make sure you get your user data (in your config.yaml datafile)
and your paths to your videos. Just like in this analysis but then through Drive rather than locally.

The Notebook does a great job at guiding you through the process.
>[!NOTE]
>You will need to have already labelled your frames prior to running the notebook. But full information can be found in the Colab[here]()

>[!DISCLAIMER]
>We do not own any of the rights to the software produced by Mathis et al. We just solely wanted to provide a hub with some of the necessary information for other students. With regard to using the software.
>Specifically on the points or issues we ran into. 

Colab as a cloud system allows for outsourcing your AI ventures, free of charge if so chosen.
But this does mean you get a daily restricted amount of computing, this timer and free hours aren't always the same.
It is based on online traffic, current usage and GPU intensity required for your specific model *(More complicated = More power needed = Less free time)*.

Additional computation hours can be purchased or one can sign up for a subscription. On average each token grants you **25 +- 4 minutes of computation** (Numbers gathered from own experience and not taking intensity of network into a count). 

## Some things that worked for usage

DeepLabCut needs to be ran locally first for the labelling of the frames and the production of a config file. 
The Github page and provisions from Mathis advice for a conda environment. We personally used a Virtual Environment (venv) and it worked fine.

Fiddling with some of the files from the original repository might be needed. We ran into an error regarding older pyside6 version. 
We advice to ask Google or an LLM for help. It is just important you get the environment set up for the labelling, worst case you'd have to run it on Colab.

Getting the drivers and GPU to work can be hard, we used a Linux machine with just the software to avoid clashes. 
Some discussions online go into some nitty gritty detail we advice to also a look at these solutions, in case they might solve your respective issues. 




