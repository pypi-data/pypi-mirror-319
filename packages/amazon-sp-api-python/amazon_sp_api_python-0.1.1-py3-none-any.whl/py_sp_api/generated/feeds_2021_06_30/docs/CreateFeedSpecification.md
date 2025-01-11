# CreateFeedSpecification

Information required to create the feed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feed_type** | **str** | The feed type. | 
**marketplace_ids** | **List[str]** | A list of identifiers for marketplaces that you want the feed to be applied to. | 
**input_feed_document_id** | **str** | The document identifier returned by the createFeedDocument operation. Upload the feed document contents before calling the createFeed operation. | 
**feed_options** | **Dict[str, str]** | Additional options to control the feed. These vary by feed type. | [optional] 

## Example

```python
from py_sp_api.generated.feeds_2021_06_30.models.create_feed_specification import CreateFeedSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFeedSpecification from a JSON string
create_feed_specification_instance = CreateFeedSpecification.from_json(json)
# print the JSON string representation of the object
print(CreateFeedSpecification.to_json())

# convert the object into a dict
create_feed_specification_dict = create_feed_specification_instance.to_dict()
# create an instance of CreateFeedSpecification from a dict
create_feed_specification_from_dict = CreateFeedSpecification.from_dict(create_feed_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


