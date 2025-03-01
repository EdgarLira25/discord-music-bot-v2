FROM python:3.12.9-bookworm

COPY . .

# TODO: Talvez usar uma imagem debian com ffmpeg pré-instalado?
# 5 min para dar build na imagem atualmente, SIZE=1.8GB
RUN apt-get update; apt-get install -y ffmpeg
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
