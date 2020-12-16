#include <iostream>
#include <random>
#include <math.h>
#include <opencv2/opencv.hpp>

const int N_POINTS = 250;
const int SIZE = 500;
const int CENTER = SIZE / 2;
const float variation = 50.f;
const int radius = 120.0f;

// Gausian function to calculate Z 
float gaussianFunction(float x, float y){
  float dev = (2.f * variation * variation);
  float xx = exp(-(pow(x - CENTER, 2) / dev));
  float yy = exp(-(pow(y - CENTER, 2) / dev));
  return xx * yy * 255; 
}

// Function to generate numbers on 500 x 500
cv::Mat1f generateNumbers(){
  std::random_device rd; 
  std::mt19937 gen(rd()); 
  cv::Mat1f points = cv::Mat1f(N_POINTS, 2);
  
  for(int i = 0; i < N_POINTS; i++)
  {
      std::normal_distribution<float> x_generator(CENTER, variation); 
      std::normal_distribution<float> y_generator(CENTER, variation); 

      float x = x_generator(gen); 
      float y = y_generator(gen);
      float z = gaussianFunction(x, y);

      if(x < 0.f || x > SIZE - 1 || y < 0.f || y > SIZE - 1)
        i--;
      else{

        std::cout << z << std::endl;
        points.at<float>(i, 0) = x;
        points.at<float>(i, 1) = y;
        points.at<float>(i, 2) = z;
      }
  }

  return points;
}

cv::Mat1f getZ(cv::Mat1f points){
  cv::Mat1f pointsVal = cv::Mat1f(N_POINTS, 1);
  for(int i = 0; i < N_POINTS; i++)
  {
      float z = gaussianFunction(points.at<float>(i, 0), points.at<float>(i, 1));
      pointsVal.at<float>(i) = z;
  }
  return pointsVal;
}

int main(int argc, const char **argv) {
  cv::Mat1b matrix = cv::Mat1b::zeros(SIZE, SIZE);
  cv::Mat3b res = cv::Mat3b::zeros(SIZE, SIZE);
  std::vector<cv::Point3i> points;
  
  cv::Mat1f samplePoints = generateNumbers();
  cv::Mat1f samplePointsValues = getZ(samplePoints);
  
  for(int i = 0; i < N_POINTS; i++)
  { 
    cv::circle(matrix, cv::Point(samplePoints.at<float>(i, 0), samplePoints.at<float>(i, 1)), 5, samplePointsValues.at<float>(i), cv::FILLED);
  }
  
  applyColorMap(matrix, res, cv::COLORMAP_MAGMA);
  cv::imshow("Original", res);

  cv::Mat1b reconstructionMat = cv::Mat1b::zeros(SIZE, SIZE);
  cv::Mat3b reconstructionRgbMat = cv::Mat3b::zeros(SIZE, SIZE);
  
  //euclidean distance -> presentation page 5
  cv::flann::Index flannIndex = cv::flann::Index(samplePoints, cv::flann::KDTreeIndexParams(1), cvflann::FLANN_DIST_EUCLIDEAN);

  
  for (int row = 0; row < reconstructionMat.rows; row++) {
    for (int col = 0; col < reconstructionMat.cols; col++) {
      std::vector<int> indices;
      std::vector<float> distances;
      std::vector<float> query = {static_cast<float>(row), static_cast<float>(col)};
      
      
      int n = flannIndex.radiusSearch(query, indices, distances, radius * radius, 20, cv::flann::SearchParams(32));
      int n = 1;
      if (n > 0) {
        const int indicesCount = std::min<int>(indices.size(), n);
        
        float nearestDistance = distances.at(0);
        
        float shepardNumer = 0;
        float shepardDenom = 0;
        for (int i = 0; i < indicesCount; i++) {
          const int indice = indices.at(i);
          const float distance = distances.at(i);
          if (distance > 0) {
            const int z = samplePointsValues.at<float>(indice);
            float lambda = static_cast<float>(z) / (nearestDistance * radius + nearestDistance);
            lambda *= lambda;
            
            shepardNumer += z * exp(-lambda);
            shepardDenom += exp(-lambda);
          }
        }
        reconstructionMat.at<uint8_t>(row, col) = (shepardNumer / shepardDenom);
      }
    }
  }
  
  //cv::imshow("reconstructionMat", reconstructionMat);
  applyColorMap(reconstructionMat, reconstructionRgbMat, cv::COLORMAP_MAGMA);
  cv::imshow("reconstructionRgbMat", reconstructionRgbMat);
  
  cv::waitKey();
  return 0;
}