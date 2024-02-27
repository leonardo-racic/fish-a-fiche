#!/bin/bash

run-venv () {
    echo Activating the virtual environment...
    source .venv/bin/activate && echo .venv has been successfully activated.    
}

start () {
    echo launch_venv.sh has been executed.
    run-venv
}

start