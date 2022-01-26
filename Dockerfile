# first stage
FROM python:3.8-alpine AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt


# second unnamed stage
FROM python:3.8-slim
WORKDIR /code
# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY . .
# update PATH environment variable
ENV PATH=/root/.local:$PATH

CMD [ "python", "./main.py" ]