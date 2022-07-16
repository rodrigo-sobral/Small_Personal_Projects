#   Update dependencies
if [ "$1" = "update" ]; then
    pip freeze > ../config/requirements.txt
fi

#   Install depedencies
if [ "$1" = "install" ]; then
    pip install -r ../config/requirements.txt
fi
