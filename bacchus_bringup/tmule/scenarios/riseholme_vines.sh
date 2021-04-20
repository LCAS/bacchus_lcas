export FARM_NAME="riseholme"
export FIELD_NAME="vines"


export SITE_PATH="`readlink -f ../config/site_files/${FARM_NAME}/${FIELD_NAME}`"

export TMAP_FILE="${SITE_PATH}/tmap.tmap"
export DATUM_FILE="${SITE_PATH}/datum.yaml"
