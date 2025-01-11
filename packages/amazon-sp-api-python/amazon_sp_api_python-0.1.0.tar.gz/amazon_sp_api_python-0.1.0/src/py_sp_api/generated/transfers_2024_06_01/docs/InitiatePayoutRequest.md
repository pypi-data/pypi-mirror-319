# InitiatePayoutRequest

The request schema for the `initiatePayout` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The identifier of the Amazon marketplace. For the list of all marketplace IDs, refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids). | 
**account_type** | **str** | The account type in the selected marketplace for which a payout must be initiated. For supported EU marketplaces, the only account type is &#x60;Standard Orders&#x60;. | 

## Example

```python
from py_sp_api.generated.transfers_2024_06_01.models.initiate_payout_request import InitiatePayoutRequest

# TODO update the JSON string below
json = "{}"
# create an instance of InitiatePayoutRequest from a JSON string
initiate_payout_request_instance = InitiatePayoutRequest.from_json(json)
# print the JSON string representation of the object
print(InitiatePayoutRequest.to_json())

# convert the object into a dict
initiate_payout_request_dict = initiate_payout_request_instance.to_dict()
# create an instance of InitiatePayoutRequest from a dict
initiate_payout_request_from_dict = InitiatePayoutRequest.from_dict(initiate_payout_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


