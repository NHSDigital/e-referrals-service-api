#!/bin/bash
# this script copies files from mock sandbox to specification. This is done so that we only need to maintain set in one place.
cp -r ./sandbox/src/mocks/. ./specification/components/examples/
