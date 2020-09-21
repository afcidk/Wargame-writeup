# The Floating Aquamarine

Floating point precision error.

The idea is to first buy a large amount of stones, then sell a portion. Floating point number cannot handle the lower digits if the number is too big. If we buy a large amount of stones, our balance would be (-price + ignored_lower_digits). When we sell a portion that still keeps the precision, we could make our balance positive after selling all stones.

`FLAG{floating_point_error_https://0.30000000000000004.com/}`
