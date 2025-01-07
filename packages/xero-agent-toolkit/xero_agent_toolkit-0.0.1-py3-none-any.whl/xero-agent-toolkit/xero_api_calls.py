import base64
import requests
import json

def map_response_to_agent_friendly_error(response_json):
    if response_json['Message'] == 'Account not found for supplied sales account code.':
        return 'Error: account not in the system'
    else:
        return 'Unknown error occurred'

class XeroApiCalls:
    def __init__(self):
        self.access_token = None

    def get_token(self, client_id, client_secret):
        # Encode client_id:client_secret to base64
        credentials = f'{client_id}:{client_secret}'
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        # Define the token URL
        token_url = 'https://identity.xero.com/connect/token'

        # Prepare the headers with the authorization header
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        # Prepare the body with the grant type and scope
        data = {
            'grant_type': 'client_credentials',
            'scope': 'accounting.settings accounting.transactions accounting.contacts'
        }

        # Send the POST request to get the access token
        response = requests.post(token_url, headers=headers, data=data)

        # Check the response and print the access token if successful
        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data.get('access_token')
            self.access_token = access_token
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            # throw exception

    def http_get(self, url):
        print('calling http_get...')
        # Add the Authorization header with the Access Token
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

        # Make the GET request to fetch items
        response = requests.get(url, headers=headers)
        print(response.url)

        # Check for errors
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(response.text)
        else:
            # Parse and print the items
            result = response.json()
            return json.dumps(result)

    def get_items(self):
        # get items
        return self.http_get("https://api.xero.com/api.xro/2.0/Items")

    def get_invoices(self, contact_name_filter = None):
        url = "https://api.xero.com/api.xro/2.0/Invoices"

        if contact_name_filter:
            # Format the contact name to be URL-safe (URL encode the spaces and special characters)
            contact_name_encoded = contact_name_filter.replace(' ', '%20')
            url = url + '?where=contact.name%3D%22' + contact_name_encoded + '%22'

        return self.http_get(url)

    def get_organizations(self):
        return self.http_get("https://api.xero.com/api.xro/2.0/Organisation")

    def get_contacts(self):
        return self.http_get("https://api.xero.com/api.xro/2.0/Contacts")

    def get_contact_name(self, contact_nickname):
        try:
            response_dict = json.loads(self.get_contacts())
            contacts = response_dict['Contacts']
            filtered_contact_names = [contact["Name"] for contact in contacts if contact_nickname in contact["Name"]]
            return json.dumps(filtered_contact_names)
        except Exception as e:
            return "Error: could not find contact"

    def http_put(self, url, data):
        # Add the Authorization header with the Access Token
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

        # Make the PUT request to create the item
        response = requests.put(url, headers=headers, data=json.dumps(data))

        # Check if the item creation was successful
        if response.status_code == 200:
            print("Object created successfully!")
            return json.dumps(response.json(), indent=2)
        else:
            print(f"Failed to create object. Status Code: {response.status_code}")
            response_json = response.json()
            print("Response: ", response_json)
            # return f"got error: {response_json['Message']}"
            return map_response_to_agent_friendly_error(response_json)

    def create_item(self,
                    item_code,
                    item_name,
                    item_description,
                    account_code = None,
                    sale_unit_price = None):

        items_url = "https://api.xero.com/api.xro/2.0/Items"
        sales_details = {}
        if account_code is not None:
            sales_details["AccountCode"] = account_code
        if sale_unit_price is not None:
            sales_details["UnitPrice"] = sale_unit_price
        new_item = {
            "Code": item_code,
            "Name": item_name,
            "Description": item_description,
            "SalesDetails": sales_details
        }
        return self.http_put(items_url, new_item)

    def create_contact(self, name, email_address = None):
        contacts_url = "https://api.xero.com/api.xro/2.0/Contacts"
        new_contact = {
            "Name": name,
        }
        if email_address is not None:
            new_contact['EmailAddress'] = email_address
        return self.http_put(contacts_url, new_contact)

    def create_account(self, account_code, account_name, account_description):
        accounts_url = "https://api.xero.com/api.xro/2.0/Accounts"
        new_account = {
            "Code": account_code,
            "Name": account_name,
            "Description": account_description,
            "Type": "EXPENSE"
        }
        return self.http_put(accounts_url, new_account)

    def create_payment(self, account_code, invoice_number, amount):
        payments_url = "https://api.xero.com/api.xro/2.0/Payments"
        new_payment = {
            "Invoice": {
                "InvoiceNumber": invoice_number
            },
            "Account": {
                "Code": account_code
            },
            "Amount": amount
        }
        return self.http_put(payments_url, new_payment)
