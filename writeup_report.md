# **Behavioral Cloning** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/center.jpg "Center Image"
[image2]: ./examples/left.jpg "Left Image"
[image3]: ./examples/right.jpg "Right Image"
[image4]: ./examples/center_driving.JPG "Center Driving"
[image5]: ./examples/shadow.PNG "Shadow of Tree"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of a convolution neural network includes 5x5 filters and 3x3 filters with relu as the activation function. (model.py lines 67-71) 

The data is normalized in the model using a Keras lambda layer (code line 65), and cropped by cropping layer to remove the useless part of the image (code line 66).

#### 2. Attempts to reduce overfitting in the model


The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 13). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 78).

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road.

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to let the car driving between those lines.

My first step was to use a convolution neural network model similar to the nvidia net, because I thought this model might be appropriate to a real self-driving car.

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that my first model had a low mean squared error on the training set but a high mean squared error on the validation set. This implied that the model was overfitting. 

Then I add a normalization layer and a cropping layer to boost the performance of the model .

The next step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track or got stocked, to improve the driving behavior in these cases, I recorded more data in different situations.

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture (model.py lines 64-76) consisted of a convolution neural network with the following layers and layer sizes

* Lambda Layer (Regularization)
* Cropper Layyer (Focusing on the center area of input image)
* 5x5 convolution layer
* 5x5 convolution layer
* 5x5 convolution layer
* 3x3 convolution layer
* 3x3 convolution layer
* flatten layer
* fully connected layer(100)
* fully connected layer(50)
* fully connected layer(10)
* fully connected layer(1)

#### 3. Creation of the Training Set & Training Process

In order to get the angle precisely, I used a XBOX controller to drive the car in recording training data.

I used the images of front side camera and both of left and right side camera with slightly steering angle correction.

![Front side][image1]
![Left side][image2]
![Right side][image3]

I first recorded two laps in original direction and two laps in oppisite direction in the center of the lane to balance the data of left turn and right turn.

To augment the data set, I also flipped images and angles of center image thinking that this would more balance.

![Center Driving][image4]

After collectiong data, I randomly shuffled the data set and put 20% of the data into a validation set. And cropping the top and the bottom as useless part of the images. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. I used an adam optimizer so that manually training the learning rate wasn't necessary.

I train the first model in 3 epoch, then I found that the car can barely recovery from the edge of lane. So I record more data about recovery to center.

In the second model trained in 5 epoch , the car could recovery to center but it was like a drunk man that keep driving bias from the left side to the right side. Then I removed the dataset and did it again. 

After few times of tring and tuning, I got a model that drive well in result. I trained it in 10 epoch.


Something is very interesting that I found the car will avoid to "Hit" the shadow of tree, I thought the reason of this is that the color of that part of lane in different from others, so the network might thinks it some unsafe area.

![Shadow of tree][image5]
