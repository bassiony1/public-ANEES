FROM python:3.10.12-alpine3.18


RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev



RUN addgroup -S app && adduser -S app -G app
USER app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY --chown=app:app requirements.txt .
USER root
RUN pip install -r requirements.txt
USER app
COPY --chown=app:app entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

COPY --chown=app:app . .
RUN mkdir staticfiles
RUN mkdir staticfiles/build
RUN mkdir staticfiles/build/static
RUN mkdir media

ENTRYPOINT [ "./entrypoint.sh" ]