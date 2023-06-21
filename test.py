def add_usage_charge(charge_id, charged_feature_data): 
    initialize_shopify_wrapper(userId)
    usage_charge_data = {
        'usage_charge': {
            'description': charged_feature_data.title,
            'price': charged_feature_data.price,
            'quantity': 1
        }
    }

    url = f'https://adgnosis-test.myshopify.com/admin/api/2023-10/recurring_application_charges/{recurring_charge_id}/usage_charges.json'

    response = requests.post(url, headers=headers, data=json.dumps(usage_charge_data))

    # Check the response
    if response.status_code == 201:
        return response
    else:
        print_object('Failed to add usage charge. Response:', user_id)
