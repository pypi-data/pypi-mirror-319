# LockerDetails

The locker details, which you can use to access the locker delivery box.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locker_number** | **str** | Indicates the locker number | [optional] 
**locker_access_code** | **str** | Indicates the locker access code | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.locker_details import LockerDetails

# TODO update the JSON string below
json = "{}"
# create an instance of LockerDetails from a JSON string
locker_details_instance = LockerDetails.from_json(json)
# print the JSON string representation of the object
print(LockerDetails.to_json())

# convert the object into a dict
locker_details_dict = locker_details_instance.to_dict()
# create an instance of LockerDetails from a dict
locker_details_from_dict = LockerDetails.from_dict(locker_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


