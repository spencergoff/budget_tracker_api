FROM public.ecr.aws/lambda/python:3.9
COPY src/get_category_totals.py requirements.txt ./
COPY src/category_mappings.json ./src/category_mappings.json
RUN python3.9 -m pip install -r requirements.txt -t .
CMD ["get_category_totals.main"]
