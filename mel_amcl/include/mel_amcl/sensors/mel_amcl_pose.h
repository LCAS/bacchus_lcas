///////////////////////////////////////////////////////////////////////////
//
// Desc: Position sensor model for AMCL
// Author: Michael Hutchinson
// Date: 19 Aug 2019
//
///////////////////////////////////////////////////////////////////////////

#ifndef AMCL_POSE_H
#define AMCL_POSE_H

#include "mel_amcl_sensor.h"
#include "../pf/pf_pdf.h"

namespace mel_amcl
{


// Map position sensor data
class AMCLPoseData : public AMCLSensorData
{
  // Map frame pose
  public: 
    AMCLPoseData () {};
    pf_vector_t pose;
    pf_vector_t pose_std;
    double additional_pose_std;
    double additional_yaw_std;
    bool use_ekf_yaw;
};


// Pose sensor model
class AMCLPose : public AMCLSensor
{
  // Default constructor
  public: AMCLPose();
    

  // add some particles at gps position
  // public: virtual bool Resample(pf_t *pf, AMCLSensorData *data);


  // Update the filter based on the sensor model.  Returns true if the filter
  // has been updated.
  public: virtual bool UpdateSensor(pf_t *pf, AMCLSensorData *data);

  // Determine the probability for the given pose
  private: static double GaussianModel(AMCLPoseData *data, 
                                   pf_sample_set_t* set);


  // Current data timestamp
  private: double time;

  private: double additional_pose_std;
  private: double additional_yaw_std;
  
};


}

#endif
