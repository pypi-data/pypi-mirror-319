import json
from pathlib import Path

import pytest
import requests

from ocdsextensionregistry import Extension, ExtensionVersion
from ocdsextensionregistry.exceptions import DoesNotExist, NotAvailableInBulk


def arguments(**kwargs):
    data = {
        'Id': 'location',
        'Date': '2018-02-01',
        'Version': 'v1.1.3',
        'Base URL': 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.3/',
        'Download URL': 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1.3',
    }

    data.update(kwargs)
    return data


def test_init():
    args = arguments()
    obj = ExtensionVersion(args)

    assert obj.id == args['Id']
    assert obj.date == args['Date']
    assert obj.version == args['Version']
    assert obj.base_url == args['Base URL']
    assert obj.download_url == args['Download URL']


@pytest.mark.parametrize(('args', 'expected'), [
    (arguments(),
     'location==v1.1.3'),
    (arguments(**{
        'Id': None,
        'Base URL': 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.3/',
    }), 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.3/'),
    (arguments(**{
        'Id': None,
        'Base URL': None,
        'Download URL': 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1.3',
    }), 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1.3'),
])
def test_repr(args, expected):
    obj = ExtensionVersion(args)

    assert repr(obj) == expected


def test_repr_file_urls():
    data = dict.fromkeys(['Id', 'Date', 'Version', 'Base URL', 'Download URL'])
    obj = ExtensionVersion(data, file_urls={'release-schema.json': 'https://example.com/release-schema.json'})

    assert repr(obj) == 'https://example.com/release-schema.json'


def test_repr_url_pattern():
    data = dict.fromkeys(['Id', 'Date', 'Version', 'Base URL', 'Download URL'])
    obj = ExtensionVersion(data, url_pattern='https://example.com/?file={4F434453}&key=value')

    assert repr(obj) == 'https://example.com/?file={4F434453}&key=value'


def test_update():
    obj = ExtensionVersion(arguments())
    obj.update(Extension({'Id': 'location', 'Category': 'item', 'Core': 'true'}))

    assert obj.id == 'location'
    assert obj.category == 'item'
    assert obj.core is True


def test_update_ignore_private_properties():
    obj = ExtensionVersion(arguments())
    other = ExtensionVersion(arguments())
    other._files = {'key': 'value'}  # noqa: SLF001
    obj.update(other)

    assert obj._files is None  # noqa: SLF001


def test_as_dict():
    args = arguments()
    obj = ExtensionVersion(args)

    assert obj.as_dict() == {
        'id': args['Id'],
        'date': args['Date'],
        'version': args['Version'],
        'base_url': args['Base URL'],
        'download_url': args['Download URL'],
    }


@pytest.mark.parametrize(('args', 'expected'), [
    (arguments(),
     'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.3/extension.json'),
    (arguments(**{
        'Id': None,
        'Base URL': 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.3/',
    }), 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.3/extension.json'),
])
def test_get_url(args, expected):
    obj = ExtensionVersion(args)

    assert obj.get_url('extension.json') == expected


def test_get_url_file_urls():
    url = 'https://example.com/release-schema.json'

    obj = ExtensionVersion(arguments(), file_urls={'release-schema.json': url})

    assert obj.get_url('release-schema.json') == url


def test_get_url_url_pattern():
    obj = ExtensionVersion(arguments(**{
        'Id': None,
        'Base URL': None,
    }), url_pattern='https://example.com/?file={4F434453}&key=value')

    assert obj.get_url('release-schema.json') == 'https://example.com/?file=release-schema.json&key=value'


def test_get_url_download_url():
    args = arguments(**{
        'Id': None,
        'Base URL': None,
        'Download URL': 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1.3',
    })

    with pytest.raises(NotImplementedError) as excinfo:
        ExtensionVersion(args).get_url('extension.json')

    assert str(excinfo.value) == 'get_url() with no base URL or matching file URL is not implemented'


def test_remote():
    obj = ExtensionVersion(arguments(**{'Download URL': None}))

    data = obj.remote('extension.json')
    # Repeat requests should return the same result.
    data = obj.remote('extension.json')

    assert json.loads(data)


def test_remote_download_url():
    obj = ExtensionVersion(arguments())

    data = obj.remote('extension.json')
    # Repeat requests should return the same result.
    data = obj.remote('extension.json')

    assert json.loads(data)


def test_remote_directory(tmpdir):
    file = tmpdir.join('extension.json')
    file.write('{"key": "value"}')

    obj = ExtensionVersion(arguments(**{'Download URL': None}))
    obj.download_url = Path(tmpdir).as_uri()
    obj.allow_schemes.add('file')

    data = obj.remote('extension.json')
    # Repeat requests should return the same result.
    data = obj.remote('extension.json')

    assert json.loads(data) == {'key': 'value'}


def test_remote_file_urls():
    url = 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_coveredBy_extension/master/release-schema.json'

    obj = ExtensionVersion(arguments(), file_urls={'release-schema.json': url})
    obj.download_url = None

    data = obj.remote('release-schema.json')
    # Repeat requests should return the same result.
    data = obj.remote('release-schema.json')

    assert 'coveredBy' in json.loads(data)['definitions']['Tender']['properties']


def test_remote_nonexistent():
    obj = ExtensionVersion(arguments())
    obj.download_url = None
    with pytest.raises(requests.HTTPError) as excinfo:
        obj.remote('nonexistent')

    assert str(excinfo.value) == "404 Client Error: Not Found for url: https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1.3/nonexistent"


def test_remote_download_url_nonexistent():
    obj = ExtensionVersion(arguments())
    with pytest.raises(DoesNotExist) as excinfo:
        obj.remote('nonexistent')

    assert str(excinfo.value) == "File 'nonexistent' does not exist in location==v1.1.3"


def test_zipfile_not_available_in_bulk():
    obj = ExtensionVersion(arguments())
    obj.download_url = None
    with pytest.raises(NotAvailableInBulk) as excinfo:
        obj.zipfile()

    assert str(excinfo.value) == "ExtensionVersion.zipfile() requires a download_url."


def test_remote_codelists_only_base_url():
    args = dict.fromkeys(['Id', 'Date', 'Version', 'Base URL', 'Download URL'])
    args['Base URL'] = 'https://raw.githubusercontent.com/contratacionesabiertas/ocds_publicNotices_extension/master/'

    obj = ExtensionVersion(args)

    assert obj.remote('release-schema.json', default='{}') == '{}'


def test_remote_codelists_only_download_url():
    args = dict.fromkeys(['Id', 'Date', 'Version', 'Base URL', 'Download URL'])
    args['Download URL'] = 'https://api.github.com/repos/contratacionesabiertas/ocds_publicNotices_extension/zipball/master'

    obj = ExtensionVersion(args)

    assert obj.remote('release-schema.json', default='{}') == '{}'


def test_files():
    obj = ExtensionVersion(arguments())
    result = obj.files

    assert 'LICENSE' in result

    # This method should not parse file contents.
    for value in result.values():
        assert isinstance(value, (bytes, str))


def test_files_without_download_url():
    obj = ExtensionVersion(arguments())
    obj.download_url = None
    result = obj.files

    assert result == {}


def test_metadata():
    obj = ExtensionVersion(arguments())
    result = obj.metadata

    assert result['codelists'] == ['locationGazetteers.csv', 'geometryType.csv']


def test_metadata_old_format():
    # See https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1/extension.json
    download_url = 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1'

    obj = ExtensionVersion(arguments(**{'Download URL': download_url}))
    result = obj.metadata

    assert result['name']['en'] == 'Location'
    assert result['description']['en'] == 'Communicates the location of proposed or executed contract delivery.'
    assert result['documentationUrl'] == {}
    assert result['compatibility'] == ['1.1']


def test_schemas():
    download_url = 'https://github.com/open-contracting-extensions/ocds_location_extension/archive/master.zip'

    obj = ExtensionVersion(arguments(**{'Download URL': download_url}))
    result = obj.schemas

    assert len(result) == 1
    assert 'Location' in result['release-schema.json']['definitions']


def test_schemas_without_metadata():
    download_url = 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1'

    obj = ExtensionVersion(arguments(**{'Download URL': download_url}))
    result = obj.schemas

    assert len(result) == 3
    assert result['record-package-schema.json'] == {}
    assert result['release-package-schema.json'] == {}
    assert 'Location' in result['release-schema.json']['definitions']


def test_schemas_without_metadata_or_download_url():
    base_url = 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1/'
    download_url = None

    obj = ExtensionVersion(arguments(**{'Base URL': base_url, 'Download URL': download_url}))
    result = obj.schemas

    assert len(result) == 3
    assert result['record-package-schema.json'] == {}
    assert result['release-package-schema.json'] == {}
    assert 'Location' in result['release-schema.json']['definitions']


def test_codelists():
    obj = ExtensionVersion(arguments())
    result = obj.codelists

    assert len(result) == 2
    assert result['locationGazetteers.csv'].fieldnames == ['Category', 'Code', 'Title', 'Description', 'Source',
                                                           'URI Pattern']


def test_codelists_without_metadata():
    download_url = 'https://api.github.com/repos/open-contracting-extensions/ocds_location_extension/zipball/v1.1'

    obj = ExtensionVersion(arguments(**{'Download URL': download_url}))
    result = obj.codelists

    assert len(result) == 1
    assert result['locationGazeteers.csv'].fieldnames == ['Category', 'Code', 'Title', 'Description', 'Source',
                                                          'URI_Pattern']


def test_codelists_without_metadata_or_download_url():
    base_url = 'https://raw.githubusercontent.com/open-contracting-extensions/ocds_location_extension/v1.1/'

    obj = ExtensionVersion(arguments(**{'Base URL': base_url}))
    obj.download_url = None
    result = obj.codelists

    assert result == {}


def test_codelists_with_cr_newlines():
    download_url = 'https://api.github.com/repos/open-contracting-extensions/ocds_bid_extension/zipball/v1.1'

    obj = ExtensionVersion(arguments(**{'Download URL': download_url}))
    result = obj.codelists

    assert len(result) == 2
    assert result['bidStatistics.csv'].fieldnames == ['Category', 'Code', 'Title', 'Description', 'Min', 'Max',
                                                      'Required by']


def test_repository_full_name():
    obj = ExtensionVersion(arguments())
    result = obj.repository_full_name

    assert result == 'open-contracting-extensions/ocds_location_extension'


def test_repository_name():
    obj = ExtensionVersion(arguments())
    result = obj.repository_name

    assert result == 'ocds_location_extension'


def test_repository_user():
    obj = ExtensionVersion(arguments())
    result = obj.repository_user

    assert result == 'open-contracting-extensions'


def test_repository_ref():
    obj = ExtensionVersion(arguments())
    result = obj.repository_ref

    assert result == 'v1.1.3'


def test_repository_user_page():
    obj = ExtensionVersion(arguments())
    result = obj.repository_user_page

    assert result == 'https://github.com/open-contracting-extensions'


def test_repository_html_page():
    obj = ExtensionVersion(arguments())
    result = obj.repository_html_page

    assert result == 'https://github.com/open-contracting-extensions/ocds_location_extension'


def test_repository_url():
    obj = ExtensionVersion(arguments())
    result = obj.repository_url

    assert result == 'git@github.com:open-contracting-extensions/ocds_location_extension.git'


def test_repository_ref_download_url():
    obj = ExtensionVersion(arguments())
    result = obj.repository_ref_download_url

    assert result == 'https://github.com/open-contracting-extensions/ocds_location_extension/archive/v1.1.3.zip'
