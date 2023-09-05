#!/bin/bash -i
# Sets up dev-vm for APIM development
# Runs in interactive mode to enable environment activation testing

echo "Setting up environment for APIM development ..."


#Installing pyenv from pyenv-installer
echo "Installing pyenv from pyenv-installer ..."
if [[ ! -d $PYENV_ROOT ]] ; then
    if curl https://pyenv.run | bash 2> /dev/null ; then
        echo "Pyenv was installed correctly ..."
    else
        echo "Pyenv was NOT installed correctly ..."
        exit 1
    fi
else
    echo "Pyenv already installed ..."
fi


BASHSTAMP="# APIM_DEV-VM"

#Adding pyenv configuration to .bash_profile
echo "Adding pyenv configuration to .bash_profile ..."
if ! grep -Fxq "$BASHSTAMP" $HOME/.bash_profile ; then
cat <<EOF >> $HOME/.bash_profile

$BASHSTAMP
if ! grep -Fxq "$BASHSTAMP" $HOME/.bashrc ; then
    export PYENV_ROOT="\$HOME/.pyenv"
    export PATH="\$PYENV_ROOT/bin:\$PATH"
    eval "\$(pyenv init --path)"
    eval "\$(pyenv virtualenv-init -)"
    eval "\$(pyenv init -)"
fi

EOF
fi

#Adding pyenv configuration to .bashrc
#Prevents having users to logout/login during setup session
#Safe to be removed afterwards as bash_profile will take its place
echo "Adding pyenv configuration to .bashrc ..."
if ! grep -Fxq "$BASHSTAMP" $HOME/.bashrc ; then
cat <<EOF >> $HOME/.bashrc

$BASHSTAMP
export PYENV_ROOT="\$HOME/.pyenv"
export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init --path)"
eval "\$(pyenv virtualenv-init -)"
eval "\$(pyenv init -)"

EOF
fi


source ~/.bash_profile

#Checking if pyenv is installed
echo "Checking if pyenv is installed ..."
if pyenv -v > /dev/null ; then
    echo "Pyenv is installed."
else
    echo "Pyenv is NOT installed."
    exit 1
fi


#Installing python dependencies
echo "Installing python dependencies ..."
if sudo yum -y install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel ; then
    echo "Python dependencies were installed successfully."
else
    echo "Python dependencies were NOT installed successfully."
    exit 1
fi


#Installing python 3.8.12 with pyenv
echo "Installing python 3.8.12 with pyenv ..."
if pyenv versions | grep -Fq "3.8.12" ; then
    echo "Pyenv has already got Python 3.8.12 installed."
else
    if pyenv install 3.8.12 ; then
        echo "Pyenv installed Python 3.8.12 successfully."
    else
        echo "Pyenv did NOT install Python 3.8.12 successfully."
        exit 1
    fi
fi


#Creating Apigee environment with Python 3.8.12
echo "Creating Apigee environment with Python 3.8.12 ..."
if pyenv versions | grep -q ".*apigee" ; then
    echo "A Python virtualenv named 'apigee' already exists."
else
    if pyenv virtualenv 3.8.12 apigee ; then
        echo "A Python 3.8.12 virtualenv named 'apigee' was created."
    else
        echo "A Python 3.8.12 virtualenv named 'apigee' was NOT created."
        exit 1
    fi
fi


#Activating apigee environment
echo "Activating apigee environment ..."
if pyenv local apigee ; then
    echo "Apigee enviroment activated."
else
    echo "Apigee enviroment NOT activated."
    exit 1
fi


#Checking python version
echo "Checking python version ..."
version=$(python -V 2>&1)
if [[ $version = 'Python 3.8.12' ]] ; then
    echo "Python version is correct."
else
    echo "Python version is NOT correct."
    exit 1
fi


#Updating pip
if pip install --upgrade pip ; then
    echo "Pip was updated."
else
    echo "Pip was NOT updated."
    exit 1
fi


#Installing poetry
echo "Installing poetry ..."
if poetry -V 2> /dev/null ; then
    echo "Poetry is already installed on apigee environment."
else
    if pip install poetry==1.5.1 ; then
        echo "Poetry was installed on apigee environment."
    else
        echo "Poetry was NOT installed on apigee environment."
        exit 1
    fi
fi


printf "\n\nSetup successfull!\n\
The apigee environment is now set with the .python-version file,\n\
\033[1mso there's no need to run $ pyenv activate apigee\033[0m,\n\
cd'ing to the repo should suffice.\n\
Please \033[1mopen another terminal\033[0m to update your \$PATH and run:\n\
\033[1m$ pyenv version\033[0m, which should output 'apigee'\n\
\033[1m$ make install\033[0m to finish environment setup.\n\
If something went wrong during the setup scripts, you can execute\n\
\033[1m$ make clean-environment\033[0m (N.B. This will remove the ~/.pyenv directory)\n\n"
