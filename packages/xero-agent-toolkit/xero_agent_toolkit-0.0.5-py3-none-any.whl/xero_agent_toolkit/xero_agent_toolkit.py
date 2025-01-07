from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from .xero_api_calls import XeroApiCalls

xero_api = XeroApiCalls()
# tool
@tool
def xero_get_contact_fullname(contact_nickname: str) -> str:
    """Given a contact nickname, return the contacts full name in Xero"""
    return xero_api.get_contact_name(contact_nickname)

@tool
def xero_create_payment(account_code: str, invoice_number: str, amount: int) -> str:
    """Creates a payment which is linked to an invoice and an account"""
    return xero_api.create_payment(account_code, invoice_number, amount)

@tool
def xero_get_invoices(contact_name_filter: str) -> str:
    """Gets all invoices associated with the given contact name, or all invoices if empty string is provided"""
    return xero_api.get_invoices(contact_name_filter)

class XeroAgentToolkit:

    def __init__(self, client_id, client_secret):
        xero_api.get_token(client_id, client_secret)

    def get_tools(self, ):
        return [xero_get_contact_fullname, xero_create_payment, xero_get_invoices]

    def system_init(self, agent_executor, config):
        prompt = ("[Scenario: When the user tells you they received a payment from a customer, they want you to create a payment for that "
                  "customer. Do the following steps: "
                  "1. The user probably provided the customer nickname. Show the full name to the user for confirmation. If the contact does not exist, tell that to the user, and stop "
                  "2. Once confirmed, Get the invoices using the get_invoices function and ask which invoice to link the payment to "
                  "3. Create a payment linked to that invoice_id. Make sure you have a numeric account code, and amount. If not, ask for it "
                  "-End of Scenario]"
                  "When asked about item information, use the 'xero_get_items' function; "
                  "When asked to create an item, use the 'xero_create_item'; "
                  "When a tool/function returns a string that starts with 'Error:' just state that error to the user;")
        agent_executor.invoke({"messages": [SystemMessage(content=prompt)]}, config)

