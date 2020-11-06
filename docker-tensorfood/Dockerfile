FROM python:3

ARG WORK_DIR="/usr/src/app"

WORKDIR $WORK_DIR

COPY requirements.txt .
COPY models models
COPY src src
COPY data/image_wanton_noodle.png data
COPY upload_folder upload_folder

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "-m", "src.app"]