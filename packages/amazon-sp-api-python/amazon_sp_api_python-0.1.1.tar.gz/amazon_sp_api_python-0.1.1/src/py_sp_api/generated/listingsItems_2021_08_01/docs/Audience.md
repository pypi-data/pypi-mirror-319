# Audience

Buyer segment or program this offer is applicable to.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | Name of the audience an offer is applicable to.   Common values:   * &#39;ALL&#39; - Standard offer audience for buyers on Amazon retail websites.   * &#39;B2B&#39; - Offer audience for Amazon Business website buyers. | [optional] 
**display_name** | **str** | Localized display name for the audience. | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.audience import Audience

# TODO update the JSON string below
json = "{}"
# create an instance of Audience from a JSON string
audience_instance = Audience.from_json(json)
# print the JSON string representation of the object
print(Audience.to_json())

# convert the object into a dict
audience_dict = audience_instance.to_dict()
# create an instance of Audience from a dict
audience_from_dict = Audience.from_dict(audience_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


