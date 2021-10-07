FROM public.ecr.aws/lambda/python:3.8
COPY get_category_totals.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt  .
COPY templates/index.html ${LAMBDA_TASK_ROOT}/templates/index.html
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
CMD [ "get_category_totals.hello_world" ]