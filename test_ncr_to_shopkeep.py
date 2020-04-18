from ncr_to_shopkeep import fix_barcode

def test_fix_barcode_len0():
    assert fix_barcode('') == ''
    
def test_fix_barcode_len5():
    assert fix_barcode('12345') == '00012345'

def test_fix_barcode_len8():
    assert fix_barcode('12345678') == '12345678'

def test_fix_barcode_len10():
    assert fix_barcode('1234567890') == '001234567890'

def test_fix_barcode_len12():
    assert fix_barcode('123456789999') == '123456789999'

def test_fix_barcode_len13():
    assert fix_barcode('1234567899999') == '1234567899999'