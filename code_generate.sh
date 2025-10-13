#!/bin/bash
set -e; set -o pipefail; set -m

my_dir=$(realpath $(dirname "$0"))
cd $my_dir

export HEAT_BUILDTOP="$my_dir"

gen_dir=$my_dir/api-lib/vnc_api/gen
mkdir -p $gen_dir
cp $my_dir/generateds/generatedssuper.py $gen_dir/
cp $my_dir/generateds/cfixture.py $gen_dir/

export PYTHONPATH=$my_dir/api-lib
generateds/generateDS.py -f -o "$gen_dir/resource" -g ifmap-frontend "$my_dir/schema/all_cfg.xsd"
