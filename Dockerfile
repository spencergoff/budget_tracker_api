FROM public.ecr.aws/lambda/python:3.9
COPY app.py requirements.txt ./
RUN python3.9 -m pip install -r requirements.txt -t .
CMD ["get_category_totals.hello_world"]
