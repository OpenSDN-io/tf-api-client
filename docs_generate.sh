#!/bin/bash
set -e; set -o pipefail; set -m

target=$1

my_dir=$(realpath $(dirname "$0"))
cd $my_dir

doc_build_dir=$my_dir/docbuild
rm -rf $doc_build_dir
mkdir -p $doc_build_dir
SPHINX_APIDOC_OPTIONS="members,show-inheritance" sphinx-apidoc -f -o $doc_build_dir $my_dir/api-lib/vnc_api/gen $doc_build_dir

cp -r $my_dir/api-lib/doc/source $doc_build_dir/
cp $my_dir/api-lib/vnc_api/gen/contrail_openapi.rst $doc_build_dir/source/
cp $my_dir/api-lib/vnc_api/gen/contrail_openapi.json $doc_build_dir/source/
cp $my_dir/base/version.info $doc_build_dir/

cd $doc_build_dir
export PYTHONPATH=$my_dir/api-lib:$my_dir/api-lib/vnc_api
make -C source html

# copy 
if [[ -n "$target" ]]; then
    echo "INFO: copy built docs to $target"
    mkdir -p $target
    cp -r $doc_build_dir/source $target/
fi
