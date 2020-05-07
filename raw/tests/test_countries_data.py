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
        'languages': 'Macedonio, Albanés',
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
        'demonyms': 'Sursudanés/esa, Sudsudanés/esa',
        'iso_code': 'SSD',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of South Sudan.svg',
        'world_location_url': 'South Sudan hd (orthographic projection).svg',
    }
    assert result == should


def test_country_info_bolivia():
    data = _get_fixture('country_info_bolivia.json')
    result = parse_country_info('Bolivia', data)
    should = {
        'name_translated': 'Estado Plurinacional de Bolivia',
        'name_original': None,
        'capital_name': 'Sucre (constitucional) y La Paz',
        'languages': 'Español, aimara, quechua, guaraní y otras 33 lenguas',
        'demonyms': 'Boliviano/a',
        'iso_code': 'BOL',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Bolivia.svg',
        'world_location_url': 'BOL orthographic.svg',
    }
    assert result == should


def test_country_info_cuba():
    data = _get_fixture('country_info_cuba.json')
    result = parse_country_info('Cuba', data)
    should = {
        'name_translated': 'República de Cuba',
        'name_original': None,
        'capital_name': 'La Habana',
        'languages': 'Español',
        'demonyms': 'Cubano/na',
        'iso_code': 'CUB',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Cuba.svg',
        'world_location_url': 'CUB orthographic.svg',
    }
    assert result == should


def test_country_info_francia():
    data = _get_fixture('country_info_francia.json')
    result = parse_country_info('Francia', data)
    should = {
        'name_translated': 'República Francesa',
        'name_original': 'République française',
        'capital_name': 'París',
        'languages': 'Francés',
        'demonyms': 'Francés/esa, Galo/la',
        'iso_code': 'FRA',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of France.svg',
        'world_location_url': 'EU-France.svg',
    }
    assert result == should


def test_country_info_suazilandia():
    data = _get_fixture('country_info_suazilandia.json')
    result = parse_country_info('Suazilandia', data)
    should = {
        'name_translated': 'Reino de Suazilandia',
        'name_original': 'Umbuso weSwatini',
        'capital_name': 'Mbabane, Lobamba',
        'languages': 'Suazi e inglés',
        'demonyms': 'Suazi',
        'iso_code': 'SWZ',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Eswatini.svg',
        'world_location_url': 'Location Swaziland AU Africa.svg',
    }
    assert result == should


def test_country_info_vaticano():
    data = _get_fixture('country_info_vaticano.json')
    result = parse_country_info('Ciudad del Vaticano', data)
    should = {
        'name_translated': 'Estado de la Ciudad del Vaticano',
        'name_original': 'Status Civitatis Vaticanæ',
        'capital_name': 'Ciudad del Vaticano',
        'languages': 'Ninguno',
        'demonyms': 'Vaticano/a',
        'iso_code': 'VAT',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of the Vatican City.svg',
        'world_location_url': 'Location of the Vatican City in Europe.svg',
    }
    assert result == should


def test_country_info_santalucía():
    data = _get_fixture('country_info_santalucía.json')
    result = parse_country_info('Santa Lucía', data)
    should = {
        'name_translated': 'Santa Lucía',
        'name_original': 'Saint Lucia',
        'capital_name': 'Castries',
        'languages': 'Inglés, Criollo antillano',
        'demonyms': 'Santalucense',
        'iso_code': 'LCA',
    }
    should[IMAGES_CONTAINER] = {
        'flag_url': 'Flag of Saint Lucia.svg',
        'world_location_url': 'Saint Lucia on the globe (Americas centered).svg',
    }
    assert result == should
