mkdir -p build
pipenv lock -r > ./build/requirements.txt
cp *.py build
docker run --rm -v ${PWD}/build:/var/task \
    -u 0 lambci/lambda\:build-python3.8 \
    python3.8 -m pip install -t /var/task/ -r /var/task/requirements.txt
cd build && zip -r ../lambda.zip *
