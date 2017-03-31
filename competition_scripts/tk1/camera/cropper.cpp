#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "FlyCapture2.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <ctime>

using namespace cv;
using namespace std;
using namespace FlyCapture2;

struct stat st = {0};

int cropCount = 0;
stringstream ss;
RNG rng(12345);
string cropsDirectoryPath = "/media/SSD/crops/";
string fullImagesDirectoryPath = "/media/SSD/full_images/";

void identifyTargets(Mat img, int thresh, int minSize, int maxSize);

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
    string imgName = fullImagesDirectoryPath + frameNumber + ".PNG";

    imwrite(imgName, image);
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
    int currentContour = i;
    if(hierarchy[i][2] > 0){

      Mat bigMask = Mat(img.rows, img.cols, CV_8U);
      drawContours(bigMask, contours_poly, i, 255, CV_FILLED, 8,
          vector<Vec4i>(), 0, Point());

      int maxX = img.cols;
      int maxY = img.rows;

      int xRangeStart = boundRect[i].tl().x - 5;
      int yRangeStart = boundRect[i].tl().y - 5;
      int xRangeEnd = boundRect[i].br().x + 5;
      int yRangeEnd = boundRect[i].br().y + 5;

      int xMidPoint = static_cast<float>(xRangeStart + yRangeStart) / 2;
      int yMidPoint = static_cast<float>(yRangeStart + yRangeEnd) / 2;

      Range yRange = Range(yRangeStart, yRangeEnd);
      Range xRange = Range(xRangeStart, xRangeEnd);

      int tiltH = static_cast<int>(minRect[i].size.width);
      int tiltW = static_cast<int>(minRect[i].size.height);

      if ((tiltW >= minSize && tiltW <= maxSize) &&
        (tiltH >= minSize && tiltH <= maxSize)){
        if ((xRangeStart > 0) && (yRangeStart > 0) &&
          (xRangeEnd < maxX) && (yRangeEnd < maxY)){

          //img_cropped = Mat(img, boundRect[i]);
          //printf("yRange: %i\n", yRange.size());
          //printf("xRange: %i\n", xRange.size());

          img_cropped = Mat(img, yRange, xRange);

          //now that we have img_cropped

          Mat insideMask;
          insideMask = Mat(bigMask, yRange, xRange);

          Mat outsideMask;
          outsideMask = insideMask.clone();
          bitwise_not(insideMask, outsideMask);

          //convert the image to the L*a*b* colorspace
          Mat Lab_img = img_cropped.clone();
          cvtColor(img_cropped, Lab_img, CV_BGR2Lab);

          //Now that the image is in the lab colorspace, we can easily
          //measure the distance between the inside color and the outside

          vector<Mat> channels;
          split(img_cropped,channels);

          Scalar internalAverage = mean(Lab_img, insideMask);
          Scalar externalAverage = mean(Lab_img, outsideMask);

          double iL = internalAverage[0];
          double iA = internalAverage[1];
          double iB = internalAverage[2];

          double eL = externalAverage[0];
          double eA = externalAverage[1];
          double eB = externalAverage[2];

          double Ldiff = iL - eL;
          double Adiff = iA - eA;
          double Bdiff = iB - eB;

          double deltaE = sqrt((Ldiff*Ldiff) + (Adiff*Adiff) + (Bdiff*Bdiff));

          if (deltaE > 55) {
            //time to do analysis between the inside and out of the crop

            Mat contourAnalysisCrop;
            img_cropped.copyTo(contourAnalysisCrop, insideMask);

            Scalar cornerPixel = contourAnalysisCrop.at<uchar>(0,0);

            double L = cornerPixel[0];
            double A = cornerPixel[1];
            double B = cornerPixel[2];

            printf("\nL:%f A:%f B:%f\n", L, A, B);

            ss << cropCount;
            string cropNumber = ss.str();
            string cropName = cropsDirectoryPath + cropNumber + ".PNG";
            string cropDataName = cropsDirectoryPath + cropNumber + ".txt";
            ss.str("");
            printf("saved %s\n", orginal.c_str());
            printf("DeltaE of crop is %f\n\n", deltaE);

            time_t currentTime = time(0);
            struct tm * currentLocalTime = localtime(&currentTime);

            std::ofstream cropDataFile;
            cropDataFile.open(cropDataName);
            cropDataFile << "center_location_x:" + xMidPoint << endl;
            cropDataFile << "center_location_y:" + yMidPoint << endl;
            cropDataFile << "time_hours:" + currentLocalTime->tm_hour << endl;
            cropDataFile << "time_minutes:" + currentLocalTime->tm_min << endl;
            cropDataFile << "time_seconds:" + currentLocalTime->tm_sec << endl;
            cropDataFile.close();

            imwrite(cropName, contourAnalysisCrop);
            cropCount++;
          }
        }
      }
    }
  }
  printf("image completed. Crops so far is %i\n\n\n\n", cropCount);
}
