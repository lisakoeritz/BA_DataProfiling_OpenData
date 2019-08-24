import pytest
import pandas.testing as ppt
import pandas as pd

import import_data as ip

@pytest.fixture(scope='module')
def test_data():
    data = pd.read_csv("testdata/test_import.csv", index_col=0).T
    data.index = pd.to_datetime(data.index)
    data = data.rename_axis('Country', axis=1)
    return data

@pytest.fixture(scope='module')
def test_metadata():
    return {'Beschreibung': 'Receipts of Food Aid is the amount of cereals designated as food aid and transferred to that country from all donors. Cereals include wheat, barley, maize, rye, oats, millet, sorghum, rice, buckwheat, alpiste/canary seed, fonio, quinoa, triticale, wheat flour, and the cereal component of blended foods. The figure represents cereal aid donated on a total-grant basis or on highly concessional terms. Data is compiled from information from donor countries and the World Food Programme (WFP).',
 'Quelle': 'Food and Agriculture Organization of the United Nations (FAO). 2012. FAOSTAT Online Statistical Service. Rome: FAO. Available online at: http://faostat.fao.org/.',
 'Herausgeber': 'FAO',
 'Titel': 'Receipts of Food Aid (cereals)',
 'ID': 'N/A',
 'Kategorie': 'N/A',
 'Dateneinheit': 'Metric Tons',
 'Erstellungsdatum': 2012}

def test_get_metadata_fsp(test_metadata):
    test_meta_att = ip.get_metadata_attributes_fsp('http://www.foodsecurityportal.org/api/receipts-food-aid-cereals')
    assert (test_metadata == test_meta_att) == True
    assert sorted(ip.get_metadata_attributes_fsp('http://www.foodsecurityportal.org/api/receipts')) == ['Beschreibung', 'Dateneinheit', 'Erstellungsdatum', 'Herausgeber', 'ID', 'Kategorie', 'Quelle', 'Titel']
    with pytest.raises(TypeError):
        ip.get_metadata_attributes_fsp()

def test_get_dataset_fsp(test_data):
    output = ip.get_dataset_fsp('http://www.foodsecurityportal.org/api/countries/percent-below-povert.csv')
    ppt.assert_frame_equal(test_data,output)
    with pytest.raises(TypeError):
        ip.get_dataset_fsp()
    with pytest.raises(RuntimeWarning):
        ip.get_dataset_fsp("http://www.foodsecurityportal.org/api/countries/percent-below-.csv")

def test_get_metatdata_wb():
    test_meta_att = ip.get_metadata_attributes_wb('SI.POV.NAH') #non-existent indicator
    empty_metadata = {'Beschreibung':'N/A', 'Dateneinheit':'N/A', 'Erstellungsdatum':'N/A', 'Herausgeber':'N/A', 'ID':'N/A', 'Kategorie':'N/A', 'Quelle':'N/A', 'Titel':'N/A'}
    assert test_meta_att == empty_metadata


