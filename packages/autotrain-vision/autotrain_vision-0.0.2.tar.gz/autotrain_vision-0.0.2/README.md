# AutoTrain
**Auto training pipeline for object detection models**

This pipeline trains object detection model(YOLOv8) using real time inference data. It is for automating the supervised learning, specifically cutting out the manual labelling task and training the model for it to remember the object as per the label we want.

## Requirements
* Python >= 3.8
* GPU (optional but prefferable)

## Package Installation
```
pip install autotrain-vision
```

### To use auto train:
```
from autotrain_vision import AutoTrain
at = AutoTrain(combined_folder="/path/to/local/folder")
at.run()
```

#### Arguments:
- `combined_folder` (str, required): Path to local folder to store the new data
- `prev_data_folder` (str): Path to local previous folder containing images and labels folder
- `new_weights` (boolean): True if to not use any previous data
- `abs_yaml_file` (str): Absolute path to the YAML file for given prev_data_folder
- `draw_bb` (boolean): True to draw bounding boxes on previous image dataset
- `image_threshold` (int): Number of images to capture for creating new dataset
- `number_aug` (int): Number of times to apply augmentations
- `epochs` (int): Number of epochs for training
- `map_threshold` (float): value<=1 ; Threshold to compare mAP50 score
- `inference` (boolean): True to perform the inference on live feed
- `inference_threshold` (float): value<=1 ; Threshold for inference confidence score
- `camera_range` (int): Range of camera indexes to look for

#### Output:
- `weights.pt` : Weights file for trained model.

### Capabilities
* Creates new annotated data 
* Combines previous annotated data with newly captured
* Annotates the data with visible bounding boxes, given images and corresponding v8 txt label files
* Generates new weights (pt) file for given dataset
* Generates analysis graphs and metrices for validation

### To-dos
* Add multiple objects annotation in single frame
* RnD on Florence capabilities for giving in text prompt to ZSD model
* RnD on discarding faulty annotations from procured dataset