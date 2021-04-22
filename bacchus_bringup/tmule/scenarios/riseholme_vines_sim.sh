export FARM_NAME="riseholme"
export FIELD_NAME="vines"


export SITE_PATH="`readlink -f ../config/site_files/${FARM_NAME}/${FIELD_NAME}`"

export TMAP_FILE="${SITE_PATH}/tmap.tmap"
export DATUM_FILE="${SITE_PATH}/datum.yaml"

export WAYPOINTS_FILE_PATH="${SITE_PATH}"

export STARTUP_SENTOR=false

export USE_GPS_ONLY=true

export USE_SIM=true
export ROBOT_POS_X_1=40
export ROBOT_POS_Y_1=-40
export ROBOT_POS_Z_1=0.8
export ROBOT_POS_A_1=0.0

