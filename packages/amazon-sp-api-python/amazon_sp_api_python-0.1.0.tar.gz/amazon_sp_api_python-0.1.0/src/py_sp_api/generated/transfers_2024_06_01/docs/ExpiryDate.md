# ExpiryDate

The expiration date of the card used for payment. If the payment method is not `card`, the expiration date is `null`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**month** | **str** | The month the card expires expressed as a number from &#x60;1&#x60; to &#x60;12&#x60;. | [optional] 
**year** | **str** | Year | [optional] 

## Example

```python
from py_sp_api.generated.transfers_2024_06_01.models.expiry_date import ExpiryDate

# TODO update the JSON string below
json = "{}"
# create an instance of ExpiryDate from a JSON string
expiry_date_instance = ExpiryDate.from_json(json)
# print the JSON string representation of the object
print(ExpiryDate.to_json())

# convert the object into a dict
expiry_date_dict = expiry_date_instance.to_dict()
# create an instance of ExpiryDate from a dict
expiry_date_from_dict = ExpiryDate.from_dict(expiry_date_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


