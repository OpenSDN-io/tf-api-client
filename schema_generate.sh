#!/bin/bash
set -e; set -o pipefail; set -m

my_dir=$(realpath $(dirname "$0"))
cd $my_dir

gen_dir=$my_dir/schema/yaml
mkdir -p $gen_dir

export PYTHONPATH=$my_dir/api-lib
generateds/generateDS.py -f -o "$gen_dir" -g contrail-json-schema "$my_dir/schema/all_cfg.xsd"

# check generated schemas for differencies in git to fail build and push user to update yaml files
if [[ "$1" != "check_fail" ]]; then
  exit
fi

output="$(git status --porcelain -- $gen_dir)"
if [[ -z "$output" ]]; then
  exit
fi

echo "ERROR: Schema modified! XML and YAML schema's are out of sync!"
echo ""
echo "$output"
echo ""
echo "Please add yaml schema changes to your commit"
exit 1
