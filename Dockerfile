FROM quay.io/astronomer/astro-runtime:12.7.1

RUN airflow db init 