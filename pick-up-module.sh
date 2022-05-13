OC_MODULES_PATH=$(oc config md)
rsync -av --exclude=data --exclude="__pycache__" $OC_MODULES_PATH/annotators/adastra ./
rsync -av --exclude=data --exclude="__pycache__" $OC_MODULES_PATH/webviewerwidgets/wgadastra ./
