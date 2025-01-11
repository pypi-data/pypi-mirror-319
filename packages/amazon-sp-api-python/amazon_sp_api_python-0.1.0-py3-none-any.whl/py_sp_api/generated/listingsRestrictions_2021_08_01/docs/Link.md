# Link

A link to resources related to a listing restriction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource** | **str** | The URI of the related resource. | 
**verb** | **str** | The HTTP verb used to interact with the related resource. | 
**title** | **str** | The title of the related resource. | [optional] 
**type** | **str** | The media type of the related resource. | [optional] 

## Example

```python
from py_sp_api.generated.listingsRestrictions_2021_08_01.models.link import Link

# TODO update the JSON string below
json = "{}"
# create an instance of Link from a JSON string
link_instance = Link.from_json(json)
# print the JSON string representation of the object
print(Link.to_json())

# convert the object into a dict
link_dict = link_instance.to_dict()
# create an instance of Link from a dict
link_from_dict = Link.from_dict(link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


