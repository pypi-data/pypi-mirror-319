[![Tests](https://github.com/DataShades/ckanext-iso19115/workflows/Tests/badge.svg?branch=main)](https://github.com/DataShades/ckanext-iso19115/actions)

# ckanext-iso19115

Export dataset into ISO 19115 XML.


## Requirements

Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.9          | yes         |
| 2.10         | yes         |


## Installation

To install ckanext-iso19115:

1. Install it into virtualenv:
   ```sh
   pip install ckanext-iso19115
   ```

1. Add `iso19115` to the `ckan.plugins`.

## Config settings

None at present

```ini
# Storage path for pre-compiled schema definition
# (optional, default: somewhere inside system's tempdir).
ckanext.iso19115.misc.cache_dir = /var/data/iso19115_cache
```

## Usage

Customize the way of mapping dataset into ISO 19115 by implementing `IIso18115` interface.

```python
from ckanext.iso19115.interfaces import IIso19115

class Iso19115(p.SingletonPlugin):
    p.implements(IIso19115, inherit=True)

    def iso19115_metadata_converter(self, data_dict: dict[str, Any]):
        return Converter(data_dict)
```

`Converter` must be defined as a sub-class of
`ckanext.iso19115.converter.Converter`. It already contains some basic logic
that can be used as a starting point for extension.

## API

### `iso19115_package_show`

Export dataset into ISO 19115 JsonML.

Format can be changed using `format` parameter of the action. Possible alternatives:

* xml

### `iso19115_package_check`

Check if the dataset can be rendered as a valid ISO 19115 document

## Tests

To run the tests, do:

    pytest



## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
