#!/bin/bash

cd /home/admin/iati-datastore
source pyenv/bin/activate
iati crawler download-and-update
