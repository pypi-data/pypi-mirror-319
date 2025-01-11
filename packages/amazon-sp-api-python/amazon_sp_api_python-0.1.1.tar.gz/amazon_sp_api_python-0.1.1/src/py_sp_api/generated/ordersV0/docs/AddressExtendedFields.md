# AddressExtendedFields

The container for address extended fields (such as `street name` and `street number`). Currently only available with Brazil shipping addresses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**street_name** | **str** | The street name. | [optional] 
**street_number** | **str** | The house, building, or property number associated with the location&#39;s street address. | [optional] 
**complement** | **str** | The floor number/unit number in the building/private house number. | [optional] 
**neighborhood** | **str** | The neighborhood. This value is only used in some countries (such as Brazil). | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.address_extended_fields import AddressExtendedFields

# TODO update the JSON string below
json = "{}"
# create an instance of AddressExtendedFields from a JSON string
address_extended_fields_instance = AddressExtendedFields.from_json(json)
# print the JSON string representation of the object
print(AddressExtendedFields.to_json())

# convert the object into a dict
address_extended_fields_dict = address_extended_fields_instance.to_dict()
# create an instance of AddressExtendedFields from a dict
address_extended_fields_from_dict = AddressExtendedFields.from_dict(address_extended_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


