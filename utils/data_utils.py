import json

def load_loan_products(file_path):
    with open(file_path, 'r') as f:
        loan_products = json.load(f)
    return loan_products

def load_faq(file_path):
    with open(file_path, 'r') as f:
        faq = json.load(f)
    return faq

def load_application_process(file_path):
    with open(file_path, 'r') as f:
        application_process = json.load(f)
    return application_process
