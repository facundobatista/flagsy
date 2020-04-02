import json
import os

from raw.fill_country_info import parse_image_url, parse_country_info, IMAGES_CONTAINER

BASEDIR = os.path.dirname(__file__)


def _get_fixture(filename):
    filepath = os.path.join(BASEDIR, "fixtures", filename)
    with open(filepath, "rt", encoding="utf8") as fh:
        return json.load(fh)


def test_parse_image_simple():
    data = _get_fixture('image_flag_afganistán.json')
    final_url = parse_image_url(data)
    should = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Flag_of_Afghanistan.svg"
    assert final_url == should


def test_country_info_afganistán():
    data = _get_fixture('country_info_afganistán.json')
    result = parse_country_info(data)
    should = {
        'name_translated': 'República Islámica de Afganistán',
        'name_original': 'د افغانستان اسلامي جمهوریت',
        'capital_name': 'Kabul',
        'languages': 'Pastún, Darí (persa)',
        'demonyms': 'Afgano/a',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Afghanistan.svg',
        'world_location_url': 'Afghanistan (orthographic projection).svg',
    }
    assert result == should


def test_country_info_alemania():
    data = _get_fixture('country_info_alemania.json')
    result = parse_country_info(data)
    should = {
        'name_translated': 'República Federal de Alemania',
        'name_original': 'Bundesrepublik Deutschland',
        'capital_name': 'Berlín',
        'languages': 'Alemán',
        'demonyms': 'Alemán/na, Germano/na, Tudesco/ca',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Germany.svg',
        'world_location_url': 'EU-Germany.svg',
    }
    assert result == should


def test_country_info_aland():
    data = _get_fixture('country_info_aland.json')
    result = parse_country_info(data)
    assert result is None


def test_country_info_andorra():
    data = _get_fixture('country_info_andorra.json')
    result = parse_country_info(data)
    should = {
        'name_translated': 'Principado de Andorra',
        'name_original': "Principat d'Andorra",
        'capital_name': 'Andorra la Vieja',
        'languages': 'Catalán',
        'demonyms': 'Andorrano/na',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Andorra.svg',
        'world_location_url': 'Location Andorra Europe.png',
    }
    assert result == should


def test_country_info_anguila():
    data = _get_fixture('country_info_anguila.json')
    result = parse_country_info(data)
    assert result is None
