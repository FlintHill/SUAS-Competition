#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace cv;
using namespace std;

int cropCount = 0;
stringstream ss;
RNG rng(12345);

void findInterestingImage(Mat img, int thresh, int minSize, int maxSize);

int main(int argc, char** argv){
  //pixels per inch
  int ppi = atoi( argv[1] ); 
  //number of images
  int noi = atoi( argv[2] );

  for (int i = 1; i < (noi+1); i++){
    ss << i;
    string imgNumb = ss.str();
    string imgName = "./" + imgNumb + ".JPG";
    ss.str("");

    Mat source = imread(imgName, 1);
    printf("loaded image number %i\n",i);
    findInterestingImage(source, 85, (12 * ppi), (72 * ppi));
    ss.str("");
  }

  return(0);
}

void findInterestingImage(Mat img, int thresh, int minSize, int maxSize){

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

      /*
      Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255),
          rng.uniform(0, 255));
      drawContours(drawing, contours_poly, i, color, 1, 8,
          vector<Vec4i>(), 0, Point());
      rectangle(drawing, boundRect[i].tl(), boundRect[i].br(),
          color, 2, 8, 0);

      int h = boundRect[i].br().y - boundRect[i].tl().y;
      int w = boundRect[i].br().x - boundRect[i].tl().x;
      */

      int tiltH = static_cast<int>(minRect[i].size.width);
      int tiltW = static_cast<int>(minRect[i].size.height);

      if ((tiltW >= minSize && tiltW <= maxSize) && (tiltH >= minSize && tiltH <= maxSize)){
        img_cropped = Mat(img, boundRect[i]);
        ss << cropCount;
        string cropNumber = ss.str();
        string name = "./crops/crop" + cropNumber + ".jpg";
        ss.str("");

        imwrite(name, img_cropped);
        cropCount++;
      }
    }
  }
  printf("image completed. Crops so far is %i\n\n", cropCount);
}
