import pytest
import numpy as np
import numpy.testing as npt
import pandas as pd
import datetime

import dataset_profile as dp


@pytest.fixture(scope='module')
def test_data():
    return pd.read_csv("testdata/test_dataset.csv", index_col=0)


@pytest.fixture(scope='module')
def test_null_data():
    return pd.DataFrame(np.nan, index=[0, 1, 2, 3], columns=['A'])

@pytest.fixture(scope='module')
def test_index_data():
    data = pd.read_csv("testdata/test_dataset.csv", index_col=0)
    data.index = pd.to_datetime(data.index)
    return data


@pytest.fixture(scope='module')
def test_metadata():
    return {'Beschreibung': 'This data', 'Herausgeber': 'FAO',
            'Quelle': 'Food and Agriculture Organization (FAO). 2014. Global Information and Early Warning System (GIEWS). Available online at http://www.fao.org/giews/pricetool/',
            'Titel': 'Wheat Prices', 'ID': None, 'Kategorie': None, 'Dateneinheit': 'U.S. Dollars/Kg',
            'zeitlAbdeckung': 'Monthly', 'Erstellungsdatum': 2014}


def test_null_values(test_data, test_null_data):
    npt.assert_almost_equal(dp.get_null_values_pct(test_data), 82.40, decimal=2)
    assert dp.get_null_values_pct(pd.DataFrame()) == None
    npt.assert_almost_equal(dp.get_null_values_pct(test_null_data),100.00, decimal=2) ##


def test_unique_values(test_data, test_null_data):
    npt.assert_almost_equal(dp.get_unique_values_pct(test_data), 14.83, decimal=2)
    assert dp.get_unique_values_pct(test_null_data) == None
    assert dp.get_null_values_pct(pd.DataFrame()) == None


def test_duplicated_columns(test_data, test_null_data):
    assert dp.get_duplicated_columns(test_data) == ['India', 'Kenya']
    assert dp.get_duplicated_columns(pd.DataFrame()) == None


def test_time_range(test_data, test_index_data, test_null_data):
    assert dp.get_time_range_ds(test_data) == []
    assert dp.get_time_range_ds(test_index_data) == [datetime.date(2012, 8, 1), datetime.date(2019, 6, 1)]
    assert dp.get_time_range_ds(test_null_data) == []


def test_data_types(test_data, test_null_data):
    assert dp.get_data_types(test_data) == {'NUM': 23, 'STRING': 1, 'CONST': 19}
    assert dp.get_data_types(test_null_data) == {'NUM': 0, 'STRING': 0, 'CONST': 1}
    assert dp.get_data_types(pd.DataFrame()) == {'NUM': 0, 'STRING': 0, 'CONST': 0}


def test_categorize_source(test_metadata):
    assert dp.categorize_source(test_metadata) == 'Zwischenstaatliche Organisation'


def test_fivestar_opendata(test_metadata):
    assert dp.fivestar_opendata(test_metadata) == 3
    test_metadata['Herausgeber'] = 'World Bank'
    assert dp.fivestar_opendata(test_metadata) == 4


def test_check_domain(test_data):
    with pytest.raises(AttributeError):
        dp.check_domain(test_data)
    test_data = test_data.rename_axis('Country', axis=1)
    not_a_country, iso_list = dp.check_domain(test_data)
    assert not_a_country == ['Not Available']
    assert iso_list == ['ATG', 'BHS', 'BGD', 'BRB', 'BLZ', 'BRA', 'KHM', 'TCD', 'CHN', 'COL', 'CRI', 'CUB',
                        'COD', 'DMA', 'DOM', 'SLV', 'ETH', 'GRD', 'GTM', 'HTI', 'HND', 'IND', 'IDN', 'JAM', 'KEN',
                        'LAO', 'LBR', 'MDG', 'MWI', 'MOZ', 'NIC', 'NER', 'NGA', 'PAK', 'PAN', 'PER', 'LCA', 'VCT',
                        'SLE', 'TTO', 'UGA', 'VNM']


def test_check_regions():
    assert dp.check_regions(['ATG', 'BHS', 'BGD', 'BRB', 'BLZ', 'BRA', 'KHM', 'TCD']) == ['Africa', 'Americas', 'Asia']
    assert dp.check_regions([]) == ['N/A']
    assert dp.check_regions(['ABG', 'BTS']) == ['N/A']


def test_check_interval(test_data, test_index_data):
    assert dp.check_interval(test_data) == 'N/A'
    assert dp.check_interval(test_index_data) == 'Monthly'


def test_aggregation(test_data):
    assert dp.check_aggregation(test_data, ['ABG', 'BTS'] ) == []


def test_check_units(test_data, test_null_data, test_metadata):
    assert dp.check_units(test_data, test_metadata) == ['Sierra Leone']
    assert dp.check_units(test_null_data, test_metadata) == []
    assert dp.check_units(pd.DataFrame(), test_metadata) == []


def test_check_months_since_upload(test_metadata):
    assert dp.check_months_since_upload(test_metadata) == '67'
    assert dp.check_months_since_upload({'Erstellungsdatum': ''}) == 'N/A'


def test_delay_upload(test_index_data, test_metadata):
    assert dp.check_delay_upload(test_index_data, test_metadata) == '+65'
    assert dp.check_delay_upload(test_data, {'Erstellungsdatum': 'N/A'}) == 'N/A'
