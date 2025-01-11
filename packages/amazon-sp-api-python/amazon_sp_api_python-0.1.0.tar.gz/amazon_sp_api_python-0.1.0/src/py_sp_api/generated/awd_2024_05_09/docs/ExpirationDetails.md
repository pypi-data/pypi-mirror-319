# ExpirationDetails

The expiration details of the inventory. This object will only appear if the details parameter in the request is set to `SHOW`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expiration** | **datetime** | The expiration date of the SKU. | [optional] 
**onhand_quantity** | **int** | The quantity that is present in AWD. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.expiration_details import ExpirationDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ExpirationDetails from a JSON string
expiration_details_instance = ExpirationDetails.from_json(json)
# print the JSON string representation of the object
print(ExpirationDetails.to_json())

# convert the object into a dict
expiration_details_dict = expiration_details_instance.to_dict()
# create an instance of ExpirationDetails from a dict
expiration_details_from_dict = ExpirationDetails.from_dict(expiration_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


