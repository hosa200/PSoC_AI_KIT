# Motor condition detection based on motor sound

**NOTE:** This project is based on deepcraft/Imagimob starter models.

## Overview

This model uses sounds recorded by [Kaggle.com](https://www.kaggle.com/datasets/pythonafroz/electrical-motor-operational-state-sound-data/code)
to determine the motor status (normal, heavyload or broken)


## Data and Classes

The provided data consists of 3 recordings from motors in the mentioned states and other sounds/background noise. 
Each recording contains:
- Audio (16 kHz mono, used as input to the AI model)


*Note:* If you are using your own data, record it as 16 kHz mono, or edit the project preprocessor to fit your data format.


## Contents

`Data` - Folder where data is located
Contain:
- engine1_good	- engine2_broken - engine3_heavyload folders with data for motor audio
- other	- folder that contain all data that's unlabelled. It's intended make the model more robust against random noises and thus lowering false positives

`Models` - Folder where trained models, their predictions and generated Edge code are saved. The folder includes also GradCam results for each session, which provide visual explanations of the model's predictions. For more information about GradCam, you can refer to the following [link](https://keras.io/examples/vision/grad_cam/).

`PreprocessorTrack` - Folder where preprocessed data is located

## More info about deepcraft

Please visit [developer.imagimob.com](https://developer.imagimob.com), where you can read about Imagimob Studio and go through step-by-step tutorials to get you quickly started.
