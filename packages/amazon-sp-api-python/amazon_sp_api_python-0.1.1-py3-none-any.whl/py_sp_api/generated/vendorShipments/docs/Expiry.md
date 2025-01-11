# Expiry

Expiry refers to the collection of dates required  for certain items. These could be either expiryDate or mfgDate and expiryAfterDuration. These are mandatory for perishable items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**manufacturer_date** | **datetime** | Production, packaging or assembly date determined by the manufacturer. Its meaning is determined based on the trade item context. | [optional] 
**expiry_date** | **datetime** | The date that determines the limit of consumption or use of a product. Its meaning is determined based on the trade item context. | [optional] 
**expiry_after_duration** | [**Duration**](Duration.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.expiry import Expiry

# TODO update the JSON string below
json = "{}"
# create an instance of Expiry from a JSON string
expiry_instance = Expiry.from_json(json)
# print the JSON string representation of the object
print(Expiry.to_json())

# convert the object into a dict
expiry_dict = expiry_instance.to_dict()
# create an instance of Expiry from a dict
expiry_from_dict = Expiry.from_dict(expiry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


