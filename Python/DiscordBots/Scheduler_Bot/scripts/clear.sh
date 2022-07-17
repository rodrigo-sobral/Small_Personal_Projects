#   Clear Log Files Contents
if [ "$1" = "logs" ]; then
	if [ "$2" = "errors" ]; then
    	echo "" > ../logs/errors.log
	fi
	if [ "$2" = "debugs" ]; then
    	echo "" > ../logs/debugs.log
	fi
	if [ "$2" = "infos" ]; then
    	echo "" > ../logs/infos.log
	fi
fi
