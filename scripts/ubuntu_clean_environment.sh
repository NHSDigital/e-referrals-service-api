#!/bin/bash

BASHSTAMP="# APIM_DEV-VM"

rm -rf $HOME/.pyenv
rm -f .python-version
sed -i "/$BASHSTAMP/Q" $HOME/.bashrc
printf "\nDone. Logout and login to restore your PATH.\n\n"
