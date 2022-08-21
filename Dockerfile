# syntax=docker/dockerfile:1

FROM fnndsc/conda

RUN conda install -c conda-forge cmake wheel;pip install rhino3dm
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "app.py"]