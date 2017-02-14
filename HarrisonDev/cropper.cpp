#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "FlyCapture2.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define IMG_CAPTURE_RATE 2.0;

using namespace cv;
using namespace std;
using namespace FlyCapture2;

struct stat st = {0};
struct imageSaveThreadData {
  Mat img;
  string imageSavePath;
};

int cropCount = 0;
stringstream ss;
RNG rng(12345);
string cropsDirectoryPath = "/media/SSD/crops/";
string fullImagesDirectoryPath = "/media/SSD/full_images/";

void identifyTargets(Mat img, int thresh, int minSize, int maxSize);
void *saveFullImage(void *threadData);

int main(int argc, char** argv){
  Error error;
  Camera camera;
  CameraInfo camInfo;

  // Connect the camera
  error = camera.Connect( 0 );
  if ( error != PGRERROR_OK )
  {
      std::cout << "Failed to connect to camera" << std::endl;
      return false;
  }

  // Get the camera info and print it out
  error = camera.GetCameraInfo( &camInfo );
  if ( error != PGRERROR_OK )
  {
      std::cout << "Failed to get camera info from camera" << std::endl;
      return false;
  }
  std::cout << camInfo.vendorName << " "
        << camInfo.modelName << " "
        << camInfo.serialNumber << std::endl;

  error = camera.StartCapture();
  if ( error == PGRERROR_ISOCH_BANDWIDTH_EXCEEDED )
  {
      std::cout << "Bandwidth exceeded" << std::endl;
      return false;
  }
  else if ( error != PGRERROR_OK )
  {
      std::cout << "Failed to start image capture" << std::endl;
      return false;
  }

  //pixels per inch
  int ppi = atoi( argv[1] );

  // Make the crops directory if it does not exist
  if (stat(cropsDirectoryPath.c_str(), &st) == -1) {
    mkdir(cropsDirectoryPath.c_str(), 0777);
  }

  // Make the full images directory if it does not exist
  if (stat(fullImagesDirectoryPath.c_str(), &st) == -1) {
    mkdir(fullImagesDirectoryPath.c_str(), 0777);
  }

  int index = 0;
  while (1) {
    sleep(1.0 / IMG_CAPTURE_RATE);

    // Get the image
    Image rawImage;
    Error error = camera.RetrieveBuffer( &rawImage );
    if ( error != PGRERROR_OK )
    {
      std::cout << "capture error" << std::endl;
      continue;
    }

    // convert to rgb
    Image rgbImage;
    rawImage.Convert( FlyCapture2::PIXEL_FORMAT_RGB16, &rgbImage );

    // convert to OpenCV Mat
    unsigned int rowBytes = (double)rgbImage.GetReceivedDataSize()/(double)rgbImage.GetRows();
    cv::Mat image = cv::Mat(rgbImage.GetRows(), rgbImage.GetCols(), CV_8UC3, rgbImage.GetData(),rowBytes);

    identifyTargets(image, 85, (12 * ppi), (72 * ppi));

    index++;
    string frameNumber = static_cast<ostringstream*>( &(ostringstream() << index) )->str();
    string imgName = fullImagesDirectoryPath + frameNumber + ".jpg";
    struct imageSaveThreadData imageSaveData;
    imageSaveData.img = image.clone();
    imageSaveData.imageSavePath = imgName;

    pthread_t imageSaveThreadID;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
    pthread_create(&imageSaveThreadID, &attr, saveFullImage, (void *)&imageSaveData);
  }

  return(0);
}

void identifyTargets(Mat img, int thresh, int minSize, int maxSize){

  Mat img_gray; Mat img_canny; Mat img_drawn; Mat img_cropped;
  vector<vector<Point> >contours;
  vector<Vec4i>hierarchy;

  printf("variables setup properly\n");

  cvtColor(img, img_gray, CV_BGR2GRAY);
  blur(img_gray, img_gray, Size(3,3));
  Canny(img_gray, img_canny, thresh, thresh*2, 3);

  printf("canny completed\n");

  findContours(img_canny, contours, hierarchy, CV_RETR_TREE,
      CV_CHAIN_APPROX_SIMPLE, Point(0,0));

  printf("contours found\n");

  vector<vector<Point> >contours_poly(contours.size());
  vector<Rect> boundRect(contours.size());
  vector<RotatedRect> minRect(contours.size());

  for(int i = 0; i < contours.size(); i++){
    approxPolyDP( Mat(contours[i]), contours_poly[i], 3, true);
    boundRect[i] = boundingRect( Mat(contours_poly[i]) );
    minRect[i] = minAreaRect( Mat(contours_poly[i]) );
  }

  printf("bounding Rects found\n");

  Mat drawing = Mat::zeros(img_canny.size(), CV_8UC3);

  for(int i = 0; i < contours.size(); i++){
    if(hierarchy[i][2] > 0){
      int tiltH = static_cast<int>(minRect[i].size.width);
      int tiltW = static_cast<int>(minRect[i].size.height);

      if ((tiltW >= minSize && tiltW <= maxSize) && (tiltH >= minSize && tiltH <= maxSize)){
        img_cropped = Mat(img, boundRect[i]);
        ss << cropCount;
        string cropNumber = ss.str();
        string name = cropsDirectoryPath + cropNumber + ".jpg";
        ss.str("");

        imwrite(name, img_cropped);
        cropCount++;
      }
    }
  }
  printf("image completed. Crops so far is %i\n\n", cropCount);
}

void *saveFullImage(void *threadData) {
  struct imageSaveThreadData *imgData;
  //imgData = (imageSaveThreadData *) threadData;

  //imwrite(imgData->imageSavePath, imgData->img);

  pthread_exit(NULL);
}
