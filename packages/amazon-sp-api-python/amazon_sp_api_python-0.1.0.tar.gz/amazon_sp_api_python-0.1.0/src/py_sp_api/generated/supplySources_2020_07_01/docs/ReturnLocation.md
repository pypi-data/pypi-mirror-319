# ReturnLocation

The address or reference to another `supplySourceId` to act as a return location.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supply_source_id** | **str** | The Amazon provided &#x60;supplySourceId&#x60; where orders can be returned to. | [optional] 
**address_with_contact** | [**AddressWithContact**](AddressWithContact.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.return_location import ReturnLocation

# TODO update the JSON string below
json = "{}"
# create an instance of ReturnLocation from a JSON string
return_location_instance = ReturnLocation.from_json(json)
# print the JSON string representation of the object
print(ReturnLocation.to_json())

# convert the object into a dict
return_location_dict = return_location_instance.to_dict()
# create an instance of ReturnLocation from a dict
return_location_from_dict = ReturnLocation.from_dict(return_location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


