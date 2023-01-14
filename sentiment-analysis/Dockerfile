FROM continuumio/miniconda3

SHELL ["conda", "run", "--no-capture-output", "-n", "base", "/bin/bash", "-c"]
RUN echo $PATH
RUN echo $CONDA_PREFIX
RUN conda --version

RUN conda install -c conda-forge python-avro -y \
    &&  conda install -c conda-forge joblib=1.2.0 -y \
    &&  conda install -c conda-forge python-confluent-kafka -y \
    &&  conda install -c conda-forge requests -y \
    &&  conda install -c conda-forge nltk -y \
    &&  conda install -c zeroae ekphrasis -y \
    &&  conda install -c conda-forge scikit-learn=1.0.2 -y \
    &&  conda install -c conda-forge fastavro -y

RUN pip install ekphrasis -U

WORKDIR /src

COPY model /model
COPY python-cp /src

CMD ["python", "main.py"]