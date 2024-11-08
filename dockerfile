FROM continuumio/miniconda3
LABEL maintainer="ryanfrancis"

ENV PYTHONBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=geodjango_tutorial.settings



# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Copy the environment YAML file and create the conda environment
COPY ENV.yml .

# Add the conda-forge channel -> fix for whitenoise missing
RUN conda config --add channels conda-forge
RUN conda env create -f ENV.yml

# RUN command should use the new environment
SHELL ["conda", "run", "-n", "awm_env", "/bin/bash", "-c"]

RUN echo "conda activate awm_env" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Copy everything in your Django project to the image
COPY . /app
ENV PYTHONPATH="/app"


# The code to run when the container is started
COPY manage.py .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "awm_env"]

# EXPOSE the port that the container will operate on
EXPOSE 8001

# Finally, start the server and run migrations
CMD [ "python", "manage.py", "runserver","0.0.0.0:8001"]