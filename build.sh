mkdir -p build
pipenv requirements > ./build/requirements.txt
cp -r *.py acalendar/ build # Need a better way to get all the relevant files
rm build/acalendar/*.pyc # Workaround to remove *.pyc files
docker run --rm -v ${PWD}/build:/var/task \
    -u 0 lambci/lambda\:build-python3.8 \
    python3.8 -m pip install -t /var/task/ -r /var/task/requirements.txt
cd build && zip -r ../lambda.zip *
