///////////////////////////////////////////////////////////////////////////
//
// Desc: AMCL pose routines
// Author: Michael Hutchinson
// Date: 19 Aug 2019
//
///////////////////////////////////////////////////////////////////////////

#include <algorithm>
#include <assert.h>

#include <sys/types.h> // required by Darwin
#include <math.h>
#include "ros/ros.h"
#include "mel_amcl/sensors/mel_amcl_pose.h"

using namespace mel_amcl;


////////////////////////////////////////////////////////////////////////////////
// Default constructor
AMCLPose::AMCLPose() : AMCLSensor()
{
  this->time = 0.0;
  return;
}



////////////////////////////////////////////////////////////////////////////////
// Apply the position sensor model
bool AMCLPose::UpdateSensor(pf_t *pf, AMCLSensorData *data)
{

  pf_update_sensor(pf, (pf_sensor_model_fn_t) GaussianModel, data);

  return true;
}


double AMCLPose::GaussianModel(AMCLPoseData *data, pf_sample_set_t* set)
{  
  int j;
  double p;
  double total_weight;
  pf_sample_t *sample;
  pf_vector_t pose;
  double angle_error;
  double pose_cov;
  double yaw_cov;
  double euclidean_distance_sqared;
  double euclidean_p;
  double euclidean_denom;
  double yaw_denom;

  total_weight = 0.0;


  double additional_pose_cov = pow(data->additional_pose_std,2);
  double additional_yaw_cov = pow(data->additional_yaw_std,2);

  // To be conservative choose the largest reported error from GNSS receiver
  // To avoid multiple calculations in loop - get total cov now
  if (data->pose_std.v[0] > data->pose_std.v[1])
  {
    pose_cov = pow(data->pose_std.v[0],2) + additional_pose_cov;
  }
  else
  {
    pose_cov = pow(data->pose_std.v[1],2) + additional_pose_cov;
  }
  
  // To avoid multiple calculations in loop - get total cov now
  if (data->use_ekf_yaw)
  {
    yaw_cov = pow(data->pose_std.v[2],2) + additional_yaw_cov;
  }

  //ROS_INFO("Additional pose cov %f, yaw cov %f, input pose cov %f, input yaw cov %f, fuse pose cov %f, yaw cov %f.", data->additional_pose_std,
    //additional_yaw_cov, pow(data->pose_std.v[0],2), pow(data->pose_std.v[2],2), pose_cov, yaw_cov);



  // Precomputing values where possible 
  euclidean_denom = sqrt(2 * M_PI * pose_cov);
  yaw_denom = sqrt(2 * M_PI * yaw_cov);

  

  // Compute the sample weights
  for (j = 0; j < set->sample_count; j++)
  {


    sample = set->samples + j;
    pose = sample->pose;


    euclidean_distance_sqared = pow(pose.v[0] - data->pose.v[0],2) + pow(pose.v[1] - data->pose.v[1],2);

    euclidean_p = exp(-0.5 * (euclidean_distance_sqared / pose_cov) ) / euclidean_denom;
    

    if (data->use_ekf_yaw)
    {
      angle_error = fmod(pose.v[2] - data->pose.v[2] + M_PI, 2*M_PI);

      if (angle_error < 0)
      {
        angle_error += 2*M_PI;
      }

      angle_error -= M_PI;
      
      double yaw_p =  exp(-0.5 * (pow(angle_error, 2) / yaw_cov)) / yaw_denom;
      p = euclidean_p*yaw_p;
    }
    else
    {
      p = euclidean_p;
    }

   
    //assert(p <= 1.0);
    //assert(p >= 0.0);
    

    sample->weight *= p;
    
    total_weight += sample->weight;
  }

  //ROS_INFO("Angle_error %f.", angle_error);

  return(total_weight);

}
