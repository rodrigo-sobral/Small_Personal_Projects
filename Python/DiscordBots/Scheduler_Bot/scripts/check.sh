#   Check Flake8 rules
if [ "$1" = "check" ]; then
    flake8 . --max-line-length=100 --ignore=B008,W503,E203,E501,E722 --enable-extensions=W504
fi
