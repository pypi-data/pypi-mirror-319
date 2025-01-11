# Buyer

Information about the buyer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buyer_id** | **str** | The identifier of the buyer. | [optional] 
**name** | **str** | The name of the buyer. | [optional] 
**phone** | **str** | The phone number of the buyer. | [optional] 
**is_prime_member** | **bool** | When true, the service is for an Amazon Prime buyer. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.buyer import Buyer

# TODO update the JSON string below
json = "{}"
# create an instance of Buyer from a JSON string
buyer_instance = Buyer.from_json(json)
# print the JSON string representation of the object
print(Buyer.to_json())

# convert the object into a dict
buyer_dict = buyer_instance.to_dict()
# create an instance of Buyer from a dict
buyer_from_dict = Buyer.from_dict(buyer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


