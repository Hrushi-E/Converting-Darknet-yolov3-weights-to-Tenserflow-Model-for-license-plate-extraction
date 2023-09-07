Converting-Darknet-yolov3-weights-to-Tenserflow-Model-for-license-plate-extraction

We converted Darknet yolov3 weights to the TensorFlow Model for license-plate-extraction of nonhelmet users. Based on the coordinates of the Human head, helmet, license plate, motorcycle, and person objects in an image, we extract the images of the license plate.

Once my custom training is over. I saved the custom model weights. Saved the custom weights as custom.weights into the data folder of this repo and custom. names to the classes folder. This will help in the conversion of darknet yolov3 weights (custom. weights) to tensorflow model.

For saving model and running the model, I used:

```bash
# Convert darknet weights to TensorFlow
## yolov3
python save_model.py --weights ./data/yolov4.weights --output ./checkpoints/yolov4-416 --input_size 416 --model yolov3

# Run yolov3 tensorflow model
!python detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov3 --images /mydrive/TEST/test0.jpg

# Run yolov3 on video
python detect_video.py --weights ./checkpoints/yolov4-416 --size 416 --model yolov4 --video ./data/video/video.mp4 --output ./detections/results.avi

# Run yolov3 on webcam
python detect_video.py --weights ./checkpoints/yolov4-416 --size 416 --model yolov4 --video 0 --output ./detections/results.avi
```


Once detection are fine, we can pass that detection information to the crop_objets function in core/functions.py to crop the license plate of non helment users.
Extra: If you run ocr function on the cropped image of linense plate, then we can get the text out of it.

References:
*[theAIGuysCode](https://github.com/theAIGuysCode/tensorflow-yolov4-tflite) 
*[tensorflow-yolov4-tflite](https://github.com/hunglc007/tensorflow-yolov4-tflite)


