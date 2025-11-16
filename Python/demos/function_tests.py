def unpack_rgb332(packed_color: int) -> tuple[int, int, int]:
    """
    Unpacks a 16-bit RGB565 integer into its 8-bit R, G, and B components.
    
    The R and B 5-bit values and G 6-bit value are expanded to the 0-255 range.
    """
    
    # 1. Extract the R component (5 bits)
    # R is in bits 7-5. Shift right by 5 bits.
    R3 = (packed_color >> 5) & 0b111
    
    # 2. Extract the G component (6 bits)
    # G is in bits 4-2. Shift right by 2 bits.
    G3 = (packed_color >> 2) & 0b111
    
    # 3. Extract the B component (5 bits)
    # B is in bits 1-0.
    B2 = packed_color & 0b11
    
    # --- Convert 3-bit/2-bit to 8-bit (0-255 range) ---
    
    # To scale a 3-bit value (0-7) to 8-bit (0-255), we can multiply by 255/7 (~36.4)
    # A common bit-shifting approximation is to replicate the most significant bits
    # into the least significant bits.
    # For 3 to 8 bits: (val << 5) | (val << 2) | (val >> 1)
    R8 = (R3 << 5) | (R3 << 2) | (R3 >> 1)
    G8 = (G3 << 5) | (G3 << 2) | (G3 >> 1)
    
    # To scale a 2-bit value (0-3) to 8-bit (0-255), we multiply by 255/3 (85)
    # A common bit-shifting approximation is to replicate the 2 bits.
    # For 2 to 8 bits: (val << 6) | (val << 4) | (val << 2) | val
    B8 = (B2 << 6) | (B2 << 4) | (B2 << 2) | B2
    
    return (R8, G8, B8)

# The color orange (255, 128, 0) in RGB332 is R=7, G=4, B=0
# Packed: (7 << 5) | (4 << 2) | 0 = 224 | 16 | 0 = 240
# Expecting unpacked values to be approximations of the original.
(r, g, b) = unpack_rgb332(16744448)
print(f"Unpacked from (RGB332): R={r}, G={g}, B={b}")
