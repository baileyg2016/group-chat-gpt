from Contacts import CNContactStore, CNContact, CNPhoneNumber
from Foundation import NSPredicate

def find_contact_name(phone_number):
    # Initialize the contact store
    contact_store = CNContactStore.alloc().init()

    # Define the keys to fetch from the contacts
    keys_to_fetch = [CNContact.givenNameKey(), CNContact.familyNameKey(), CNContact.phoneNumbersKey()]

    # Create a predicate to search for the phone number
    predicate = NSPredicate.predicateWithFormat_("phoneNumbers.value.stringValue CONTAINS %@", phone_number)

    # Fetch the matching contacts
    contacts = contact_store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys_to_fetch, None)

    if contacts:
        # Get the first matching contact
        contact = contacts[0]
        contact_name = f"{contact.givenName()} {contact.familyName()}".strip()
        return contact_name
    else:
        return None

# # Replace with the phone number you want to search for
# phone_number = "123-456-7890"
# contact_name = find_contact_name(phone_number)

# if contact_name:
#     print(f"Name for {phone_number}: {contact_name}")
# else:
#     print(f"No contact found for {phone_number}")
