#!/bin/bash

run-flask () {
    echo Activating the virtual environment...
    source .venv/bin/activate && echo .venv has been successfully activated.
    echo Running Flask...

    currentport="${1:-8000}"
    echo Flask is going to run in port: $currentport

    {
        flask run --port $currentport 
    } || {
        echo main.sh has failed.
        while true; do
            read -p "Is it due to the 'OsError 98 : Address port already in use' error? (Y/N) :  " confirmation

            if [[ $confirmation == "Y" ]]; then
                echo Keep in mind that flask should not be running in ports lower than "1600" for safety reasons.            
                read -p "Insert an address port in which flask will be running: " newport
                run-flask $newport
                break
            elif [[ $confirmation == "N" ]]; then
                echo Please inform the developers about the error, as the script has currently no way of resolving it.
                exit 1
            else
                echo Invalid input, it is strictly Y/N.
            fi
        done   
    }
}

start () {
    echo main.sh has been executed.
    run-flask
}

start