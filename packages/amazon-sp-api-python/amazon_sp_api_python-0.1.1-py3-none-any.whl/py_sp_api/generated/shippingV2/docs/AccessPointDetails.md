# AccessPointDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_point_id** | **str** | Unique identifier for the access point | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.access_point_details import AccessPointDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AccessPointDetails from a JSON string
access_point_details_instance = AccessPointDetails.from_json(json)
# print the JSON string representation of the object
print(AccessPointDetails.to_json())

# convert the object into a dict
access_point_details_dict = access_point_details_instance.to_dict()
# create an instance of AccessPointDetails from a dict
access_point_details_from_dict = AccessPointDetails.from_dict(access_point_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


