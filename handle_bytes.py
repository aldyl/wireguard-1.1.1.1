
def pretty_bytes(bytes):
    if bytes == 0:
        return '0 B'
    
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0

    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024
        i += 1

    return f'{round(bytes,2)} {sizes[i]}'

def test_pretty_bytes():
    # Test lower bound (zero bytes)
    assert pretty_bytes(0) == '0 B'
    
    # Test within first size unit (bytes)
    assert pretty_bytes(42) == '42 B'
    
    # Test rounding down
    assert pretty_bytes(1023) == '1023 B'
    
    # Test rounding to two decimal places
    assert pretty_bytes(1234567) == '1.18 MB'
    
    # Test exact representable value in binary (binary-based systems)
    assert pretty_bytes(536870912) == '512.0 MB'
    
    # Test upper bound (terabytes)
    assert pretty_bytes(1099511627776) == '1.0 TB'
