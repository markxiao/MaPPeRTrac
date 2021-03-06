#!/usr/bin/env bash
if [ ! -f license.txt ]; then
    echo "Freesurfer license not found! Download at https://surfer.nmr.mgh.harvard.edu/fswiki/License"
    exit 1
fi
sudo rm -rf container/image.simg
sudo singularity build container/image.simg container/Singularity