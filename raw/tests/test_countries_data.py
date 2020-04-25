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
    result = parse_country_info('Afganistán', data)
    should = {
        'name_translated': 'República Islámica de Afganistán',
        'name_original': 'د افغانستان اسلامي جمهوریت',
        'capital_name': 'Kabul',
        'languages': 'Pastún, Darí (persa)',
        'demonyms': 'Afgano/a',
        'iso_code': 'AFG',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Afghanistan.svg',
        'world_location_url': 'Afghanistan (orthographic projection).svg',
    }
    assert result == should


def test_country_info_alemania():
    data = _get_fixture('country_info_alemania.json')
    result = parse_country_info('Alemania', data)
    should = {
        'name_translated': 'República Federal de Alemania',
        'name_original': 'Bundesrepublik Deutschland',
        'capital_name': 'Berlín',
        'languages': 'Alemán',
        'demonyms': 'Alemán/na, Germano/na, Tudesco/ca',
        'iso_code': 'DEU',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Germany.svg',
        'world_location_url': 'EU-Germany.svg',
    }
    assert result == should


def test_country_info_andorra():
    data = _get_fixture('country_info_andorra.json')
    result = parse_country_info('Andorra', data)
    should = {
        'name_translated': 'Principado de Andorra',
        'name_original': "Principat d'Andorra",
        'capital_name': 'Andorra la Vieja',
        'languages': 'Catalán',
        'demonyms': 'Andorrano/na',
        'iso_code': 'AND',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Andorra.svg',
        'world_location_url': 'Location Andorra Europe.png',
    }
    assert result == should


def test_country_info_barbados():
    data = _get_fixture('country_info_barbados.json')
    result = parse_country_info('Barbados', data)
    should = {
        'name_translated': 'Barbados',
        'name_original': "Barbados",
        'capital_name': 'Bridgetown',
        'languages': 'Inglés',
        'demonyms': 'Barbadense',
        'iso_code': 'BRB',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Barbados.svg',
        'world_location_url': 'BRB orthographic.svg',
    }
    assert result == should


def test_country_info_banglades():
    data = _get_fixture('country_info_bangladés.json')
    result = parse_country_info('Bangladés', data)
    should = {
        'name_translated': 'República Popular de Bangladés',
        'name_original': "গণপ্রজাতন্ত্রী বাংলাদেশ",
        'capital_name': 'Daca',
        'languages': 'Bengalí',
        'demonyms': 'Bangladesí',
        'iso_code': 'BGD',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Bangladesh.svg',
        'world_location_url': 'Bangladesh (orthographic projection).svg',
    }
    assert result == should


def test_country_info_comoras():
    data = _get_fixture('country_info_comoras.json')
    result = parse_country_info('Comoras', data)
    should = {
        'name_translated': 'Unión de las Comoras',
        'name_original': 'الاتحاد القمري',
        'capital_name': 'Moroni',
        'languages': 'Árabe, Suajili (Comorense), Francés',
        'demonyms': 'Comorense',
        'iso_code': 'COM',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of the Comoros.svg',
        'world_location_url': 'Comoros (orthographic projection).svg',
    }
    assert result == should


def test_country_info_dominica():
    data = _get_fixture('country_info_dominica.json')
    result = parse_country_info('Dominica', data)
    should = {
        'name_translated': 'Mancomunidad de Dominica',
        'name_original': 'Commonwealth of Dominica',
        'capital_name': 'Roseau',
        'languages': 'Inglés',
        'demonyms': 'Dominiqués/esa',
        'iso_code': 'DMA',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Dominica.svg',
        'world_location_url': 'Dominica on the globe (Americas centered).svg',
    }
    assert result == should


def test_country_info_irak():
    data = _get_fixture('country_info_irak.json')
    result = parse_country_info('Irak', data)
    should = {
        'name_translated': 'República de Irak',
        'name_original': 'جمهورية ألعراق',
        'capital_name': 'Bagdad',
        'languages': 'Árabe y kurdo',
        'demonyms': 'Iraquí',
        'iso_code': 'IRQ',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Iraq.svg',
        'world_location_url': 'Iraq (orthographic projection).svg',
    }
    assert result == should


def test_country_info_nigeria():
    data = _get_fixture('country_info_nigeria.json')
    result = parse_country_info('Nigeria', data)
    should = {
        'name_translated': 'República Federal de Nigeria',
        'name_original': 'Federal Republic of Nigeria',
        'capital_name': 'Abuya',
        'languages': 'Inglés',
        'demonyms': 'Nigeriano/a',
        'iso_code': 'NGA',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Nigeria.svg',
        'world_location_url': 'Nigeria (orthographic projection).svg',
    }
    assert result == should


def test_country_info_españa():
    data = _get_fixture('country_info_españa.json')
    result = parse_country_info('España', data)
    should = {
        'name_translated': 'Reino de España',
        'name_original': None,
        'capital_name': 'Madrid',
        'languages': 'Castellano',
        'demonyms': 'Español/la',
        'iso_code': 'ESP',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Spain.svg',
        'world_location_url': 'EU-Spain.svg',
    }
    assert result == should


def test_country_info_macedonia():
    data = _get_fixture('country_info_macedonia.json')
    result = parse_country_info('Macedonia', data)
    should = {
        'name_translated': 'República de Macedonia del Norte',
        'name_original': 'Република Северна Македонија',
        'capital_name': 'Skopie',
        'languages': 'Macedonio',
        'demonyms': 'Macedonio/a, Normacedonio/a',
        'iso_code': 'MKD',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of North Macedonia.svg',
        'world_location_url': 'Europe-Macedonia.svg',
    }
    assert result == should


def test_country_info_sudandelsur():
    data = _get_fixture('country_info_sudandelsur.json')
    result = parse_country_info('Sudán del Sur', data)
    should = {
        'name_translated': 'República de Sudán del Sur',
        'name_original': 'Republic of South Sudan',
        'capital_name': 'Yuba',
        'languages': 'Inglés',
        'demonyms': 'Sursudanés/esa',
        'iso_code': 'SSD',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of South Sudan.svg',
        'world_location_url': 'South Sudan hd (orthographic projection).svg',
    }
    assert result == should
