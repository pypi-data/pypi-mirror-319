# AmazonPrograms

Contains the list of programs that are associated with an item.  Possible programs are:  - **Subscribe and Save**: Offers recurring, scheduled deliveries to Amazon customers and Amazon Business customers for their frequently ordered products.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**programs** | **List[str]** | A list of the programs that are associated with the specified order item.  **Possible values**: &#x60;SUBSCRIBE_AND_SAVE&#x60; | 

## Example

```python
from py_sp_api.generated.ordersV0.models.amazon_programs import AmazonPrograms

# TODO update the JSON string below
json = "{}"
# create an instance of AmazonPrograms from a JSON string
amazon_programs_instance = AmazonPrograms.from_json(json)
# print the JSON string representation of the object
print(AmazonPrograms.to_json())

# convert the object into a dict
amazon_programs_dict = amazon_programs_instance.to_dict()
# create an instance of AmazonPrograms from a dict
amazon_programs_from_dict = AmazonPrograms.from_dict(amazon_programs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


