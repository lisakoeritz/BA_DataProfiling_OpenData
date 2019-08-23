import pytest
import numpy as np
import pandas as pd

import column_profile as cp


@pytest.fixture(scope='module')
def test_col():
    test_col = pd.read_csv("testdata/test_col.csv", index_col=0)
    test_col.index = pd.to_datetime(test_col.index)
    return test_col

@pytest.fixture(scope='module')
def test_null_data():
    return pd.Series(np.nan, index=[0, 1, 2, 3])

def test_column_metadata():
    metadata = {
        'Beschreibung': 'This data represents the best available monthly value\nBrazil; Wholesale; National average.\nChina; wheat (flour); Retail; Average of market prices in 50 large and medium cities.\nEthiopia; Retail; Addis Ababa: Wheat.\nIndia; Retail; Mumbai: Wheat.\nIndonesia; Retail;',
        'Quelle': 'Food and Agriculture Organization (FAO). 2014. Global Information and Early Warning System (GIEWS). Available online at http://www.fao.org/giews/pricetool/',
        'Herausgeber': 'FAO', 'Titel': 'Wheat Prices', 'ID': None, 'Kategorie': None, 'Dateneinheit': 'U.S. Dollars/Kg',
        'zeitlAbdeckung': 'Monthly', 'Erstellungsdatum': 2014}
    assert cp.column_metadata('India', metadata) == 'India; Retail; Mumbai: Wheat.'
    assert cp.column_metadata('India', {'Quelle':'','Beschreibung':''}) == ""


def test_consecutive_dates(test_col, test_null_data):
    assert cp.check_is_consecutive(test_col) == ['2012-09-01 - 2015-03-01', '2015-05-01 - 2019-06-01']
    assert cp.check_is_consecutive(test_null_data) == []

