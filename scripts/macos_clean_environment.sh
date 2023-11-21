#!/bin/bash

BASHSTAMP="# APIM_DEV-Mac"

rm -rf $HOME/.pyenv
rm -f .python-version
sed -i "/$BASHSTAMP/Q" $HOME/.zshrc
printf "\nDone. Logout and login to restore your PATH.\n\n"
