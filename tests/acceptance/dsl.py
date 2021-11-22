class Dsl:
    def get_home_page_text(self):
        qa_endpoint = os.environ["qa_endpoint"].strip('"')
        print(f'qa_endpoint: {qa_endpoint}')
        qa_endpoint_content = requests.get(qa_endpoint)
        print(f'qa_endpoint_content.text: {qa_endpoint_content.text}')
        print(f'qa_endpoint_content.status_code: {qa_endpoint_content.status_code}')
        return qa_endpoint_content.text