# ProductTypeDefinition

A product type definition represents the attributes and data requirements for a product type in the Amazon catalog. Product type definitions are used interchangeably between the Selling Partner API for Listings Items, Selling Partner API for Catalog Items, and JSON-based listings feeds in the Selling Partner API for Feeds.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**meta_schema** | [**SchemaLink**](SchemaLink.md) |  | [optional] 
**var_schema** | [**SchemaLink**](SchemaLink.md) |  | 
**requirements** | **str** | Name of the requirements set represented in this product type definition. | 
**requirements_enforced** | **str** | Identifies if the required attributes for a requirements set are enforced by the product type definition schema. Non-enforced requirements enable structural validation of individual attributes without all of the required attributes being present (such as for partial updates). | 
**property_groups** | [**Dict[str, PropertyGroup]**](PropertyGroup.md) | Mapping of property group names to property groups. Property groups represent logical groupings of schema properties that can be used for display or informational purposes. | 
**locale** | **str** | Locale of the display elements contained in the product type definition. | 
**marketplace_ids** | **List[str]** | Amazon marketplace identifiers for which the product type definition is applicable. | 
**product_type** | **str** | The name of the Amazon product type that this product type definition applies to. | 
**display_name** | **str** | Human-readable and localized description of the Amazon product type. | 
**product_type_version** | [**ProductTypeVersion**](ProductTypeVersion.md) |  | 

## Example

```python
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.product_type_definition import ProductTypeDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of ProductTypeDefinition from a JSON string
product_type_definition_instance = ProductTypeDefinition.from_json(json)
# print the JSON string representation of the object
print(ProductTypeDefinition.to_json())

# convert the object into a dict
product_type_definition_dict = product_type_definition_instance.to_dict()
# create an instance of ProductTypeDefinition from a dict
product_type_definition_from_dict = ProductTypeDefinition.from_dict(product_type_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


