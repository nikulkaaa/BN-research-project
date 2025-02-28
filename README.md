# BN-research-project
### This Read Me is for the purpose of introduction.
Work done in colaboration with our Research Project supervisors
![Work done in colaboration with our Research Project supervisors](image.png)

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

After cloning it is really up to following the instructions in the Jupyter Notebooks and or [The streamlit application](streamlit_application.py) provided. You can do the [set_ratios.ipynb](https://github.com/nikulkaaa/BN-research-project/blob/main/set_ratios.ipynb) Notebook prior to actual analysis. This is important since the calculations require some sort of pixel to cm ratio.

You can run the streamlit application by running the below mentioned code in your Virtual Environment terminal (conda, venv etc.)

```
python -m streamlit run streamlit_application.py
```

Both the streamlit application and the Notebook [analyze_multiple_videos.ipynb](analyze_multiple_videos.ipynb) serve the same function. The Notebook serves as an easy access way of changing the code, whereas the streamlit application is more userfriendly, better GUI, but harder to change code. 

Analysis depends on the accuracy of both the model and the labelling, keep in mind that one should always check the videos after application of the model for visual disturbances or problems. If there is clear overfitting or weird labels in the product videos; 
you can increase the accuracy through:
>* Retraining with more- , adjusted- and or fixed problematic frames
>* Adding more labelling
>* Add more variance within labelled data - different behaviours for example. 
>* Increasing amount of Epochs or Iterrations, till the loss plateaus


## What does what file do?

This part is a sum-up of all the functions and what you can find where. Can be used as a guide to finding certain code or functions. 

[analyze_multiple_videos.ipynb](analyze_multiple_videos.ipynb) = A Jupyter Notebook for the analysis of a folder of videos and their comparison. Does not provide graphs.  

[functions_for_DLC_analysis.py](functions_for_DLC_analysis.py) = A Python script containing most functions that will be used for analysis and plottin of data in the [analyze_multiple_videos](analyze_multiple_videos.ipynb) and [loadandanalyzeDLCdata](loadandanalyzeDLCdata.ipynb) Notebooks.  

[image_draw.py](image_draw.py) = this file contains the functions needed for the [set_ratios](set_ratios.ipynb) Notebook. Regarding the pixel-cm ratio calculations. 

[loadandanalyzeDLCdata.ipynb](loadandanalyzeDLCdata.ipynb) = A Jupyter Notebook for the analysis of **one** video, providing graphs and other means for that specific data as well. Not updated to the new function names yet within [functions_for_DLC_analysis](functions_for_DLC_analysis.py).

[README.md](README.md) = This README containing important and supplementary information on the use and goals of the project. 

[requirements.txt](requirements.txt)  =  A txt file that can be selected to automatically download the necessary dependencies in your virtual environment.

[set_ratios.ipynb](set_ratios.ipynb) = A Jupyter Notebook that is necessary for setting the pixel to cm ratios. In this file functions will create a .png file on which the user can draw two dots by ***double left clicking***, it will keep showing you the first frame of every video till all have been done. The calculated data is stored in [video_data.csv](video_data.csv) and used in the analysis Notebooks.

[streamlit_application.py](streamlit_application.py)  =  A userfriendly GUI as a front for the [analyze_multiple_videos](analyze_multiple_videos.ipynb), output will be the same just a lot easier to use. 





## DeepLabCut through Colab

When you are not able to run DeepLabcut locally, due to either hardware specific issues or driver issues. 
You can use an online Colab workspace with proper instructions provided by the DeepLabCut repository [here](https://github.com/DeepLabCut/DeepLabCut/blob/main/examples/COLAB/COLAB_YOURDATA_TrainNetwork_VideoAnalysis.ipynb).

Upon opening the link, you can find a small button up top: ![alt text](image-1.png)

By clicking on this you will create a copy of the Jupyter notebook, make sure you save this to your drive so you dont have to edit the file paths everytime you open the notebook, nor have to go throught their repository for access. 

You need to upload your files to an available Google Drive. Afterward you need to make sure you get your user data (in your config.yaml datafile)
and your paths to your videos. Just like in this analysis but then through Drive rather than locally.

The Notebook does a great job at guiding you through the process.
>[!NOTE]
>You will need to have already labelled your frames prior to running the notebook. But full information can be found in the Colab[here](https://colab.research.google.com/github/DeepLabCut/DeepLabCut/blob/master/examples/COLAB/COLAB_YOURDATA_TrainNetwork_VideoAnalysis.ipynb#scrollTo=Z7ZlDr3wV4D1)

>[!WARNING]
>We do not own any of the rights to the software produced by [Mathis et al.](https://github.com/DeepLabCut).  We just solely wanted to provide a hub with some of the necessary information for other students. With regard to using the software.
>Specifically on the points or issues we ran into. 

Colab as a cloud system allows for outsourcing your AI ventures, free of charge if so chosen.
But this does mean you get a daily restricted amount of computing, this timer and free hours aren't always the same.
It is based on online traffic, current usage and GPU intensity required for your specific model *(More complicated = More power needed = Less free computation at a time)*.

Additional computation hours can be purchased or one can sign up for a subscription. On average each token grants you **25 +- 4 minutes of computation** (Numbers gathered from own experience and not taking intensity of network into a count). 

## Some things that worked for usage

DeepLabCut needs to be ran locally first for the labelling of the frames and the production of a config file. Generally; following the how to page on deeplabcut suffices. If there is more trouble, setting up a clean Linux machine can work, this way there will be very limited driver clashes and or program issues. For this there are tutorials on how to set up these machines, and their GUI's. From there follow the install guide on the deeplabcut repository.


>The Github page and provisions from Mathis advice for a conda environment. We personally used a Virtual Environment (venv) and it worked fine.

Fiddling with some of the files from the original DeepLabCut repository might be needed. We ran into an error regarding for example; an older pyside6 version. 
We advice to ask Google or an LLM for help. It is just important you get the environment set up for the labelling, worst case you can run it on Colab if you cannot do so locally.

Getting the drivers and GPU to work can be hard, if you want to run it locally. Make sure your drivers and library version match, for example CUDA 11 with the newest pytorch etc. or if you use a tensorflow version double check the cuDNN driver compatibility as well. 

Some discussions online go into some nitty gritty detail we advice to also a look at these solutions, in case they might solve your respective issues.  




