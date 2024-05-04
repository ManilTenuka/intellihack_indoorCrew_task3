import tensorflow as tf
from utils.data_utils import load_loan_products, load_faq, load_application_process
from utils.model_utils import load_model

# Load data
loan_products = load_loan_products('data/loan_products.json')
faq = load_faq('data/faq.json')
application_process = load_application_process('data/application_process.json')

# Load the trained model
model = load_model('models/loan_support_model.h5')


def check_loan_eligibility(credit_score, income, employment_status, existing_debts):
    eligible_products = []
    for product in loan_products:
        eligibility = product['eligibility']
        if (
                credit_score >= int(eligibility['credit_score'].split('+')[0])
                and income >= int(eligibility['income_range'].split('-')[0].replace('$', ''))
                and employment_status == eligibility['employment_status']
                and existing_debts == eligibility['existing_debts']
        ):
            eligible_products.append(product)
    return eligible_products


def get_loan_product_info(product_name):
    for product in loan_products:
        if product['name'] == product_name:
            return product
    return None


def get_application_process_info():
    return application_process


def get_faq_answer(question):
    for faq_item in faq:
        if faq_item['question'].lower() == question.lower():
            return faq_item['answer']
    return "I'm sorry, I don't have an answer for that question."


def get_personalized_recommendation(user_data):
    # Implement logic to provide personalized recommendations based on the user's financial situation
    # For example, based on credit score, income, employment status, and existing debts
    recommended_products = check_loan_eligibility(
        user_data['credit_score'],
        user_data['income'],
        user_data['employment_status'],
        user_data['existing_debts']
    )

    tips = []
    if user_data['credit_score'] < 650:
        tips.append("Consider improving your credit score to increase your loan eligibility.")
    if user_data['existing_debts'] != "Manageable debt-to-income ratio":
        tips.append("Try to reduce your existing debt to improve your loan eligibility.")

    return recommended_products, tips


# Example usage
print("Welcome to the Smart Bank Loan Support Chatbot!")

while True:
    user_input = input("How can I assist you today? ")

    # Implement logic to handle different types of user inputs
    # and call the respective functions
    if user_input.lower() == "check loan eligibility":
        credit_score = int(input("Please enter your credit score: "))
        income = int(input("Please enter your annual income: ").replace('$', ''))
        employment_status = input("Please enter your employment status: ")
        existing_debts = input("Please describe your existing debt situation: ")

        eligible_products = check_loan_eligibility(credit_score, income, employment_status, existing_debts)
        if eligible_products:
            print("Based on your information, you are eligible for the following loan products:")
            for product in eligible_products:
                print(f"- {product['name']}")
        else:
            print("Unfortunately, you are not eligible for any loan products at this time.")

    elif user_input.lower().startswith("get info for"):
        product_name = user_input.split("for ")[1]
        product_info = get_loan_product_info(product_name)
        if product_info:
            print(f"Information for {product_name}:")
            print(f"Features: {', '.join(product_info['features'])}")
            print(f"Interest Rate: {product_info['interest_rate']}")
            print(f"Repayment Term: {product_info['repayment_term']}")
            print("Eligibility:")
            for criteria, value in product_info['eligibility'].items():
                print(f"- {criteria.replace('_', ' ').title()}: {value}")
        else:
            print(f"Sorry, I couldn't find information for {product_name}.")

    elif user_input.lower() == "application process":
        process_info = get_application_process_info()
        print("Loan Application Process:")
        print("Required Documents:")
        for document in process_info['required_documents']:
            print(f"- {document}")
        print("\nSteps:")
        for step in process_info['steps']:
            print(f"- {step}")
        print(f"\nTimeline: {process_info['timeline']}")

    elif user_input.lower().startswith("faq"):
        question = user_input.split("faq ")[1]
        answer = get_faq_answer(question)
        print(f"Answer: {answer}")

    elif user_input.lower() == "personalized recommendation":
        credit_score = int(input("Please enter your credit score: "))
        income = int(input("Please enter your annual income: ").replace('$', ''))
        employment_status = input("Please enter your employment status: ")
        existing_debts = input("Please describe your existing debt situation: ")

        user_data = {
            'credit_score': credit_score,
            'income': income,
            'employment_status': employment_status,
            'existing_debts': existing_debts
        }

        recommended_products, tips = get_personalized_recommendation(user_data)
        print("Personalized Recommendation:")
        if recommended_products:
            print("Recommended Loan Products:")
            for product in recommended_products:
                print(f"- {product['name']}")
        else:
            print("Unfortunately, you are not eligible for any loan products at this time.")

        if tips:
            print("\nTips to Improve Eligibility:")
            for tip in tips:
                print(f"- {tip}")

    elif user_input.lower() == "exit":
        break

    else:
        print("I'm sorry, I didn't understand your request. Please try again or type 'exit' to quit.")

print("Thank you for using the Smart Bank Loan Support Chatbot.")
