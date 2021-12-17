FROM public.ecr.aws/lambda/python:3.9
COPY src/get_category_totals.py src/category_mappings.json requirements.txt ./
RUN python3.9 -m pip install -r requirements.txt -t .
CMD ["get_category_totals.main"]
