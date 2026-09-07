import struct


def int_to_base(n: int, base: int) -> str:
    if not (2 <= base <= 16):
        raise ValueError("Основа має бути в діапазоні 2..16")
    if n == 0:
        return "0"

    digits = "0123456789ABCDEF"
    sign = "-" if n < 0 else ""
    n = abs(n)
    result = ""
    while n > 0:
        result = digits[n % base] + result
        n //= base
    return sign + result


def frac_to_base(f: float, base: int, digits_count: int = 6) -> str:
    if not (0 <= f < 1):
        raise ValueError("f має бути в межах [0, 1)")

    digits = "0123456789ABCDEF"
    result = ""
    for _ in range(digits_count):
        f *= base
        d = int(f)
        result += digits[d]
        f -= d
    return result


def to_twos_complement(n: int, bits: int = 8) -> str:
    if n < 0:
        n = (1 << bits) + n
    return format(n, f"0{bits}b")


def from_twos_complement(bits_str: str) -> int:
    value = int(bits_str, 2)
    if bits_str[0] == "1":
        value -= (1 << len(bits_str))
    return value


def add_twos_complement(a: int, b: int, bits: int = 8):
    mask = (1 << bits) - 1
    ia = int(to_twos_complement(a, bits), 2)
    ib = int(to_twos_complement(b, bits), 2)

    carry = 0
    result = 0
    carry_into_sign = 0
    for i in range(bits):
        abit = (ia >> i) & 1
        bbit = (ib >> i) & 1
        s = abit + bbit + carry
        result |= (s & 1) << i
        carry = s >> 1
        if i == bits - 2:
            carry_into_sign = carry

    carry_out_of_sign = carry
    overflow = carry_into_sign != carry_out_of_sign
    result &= mask
    return format(result, f"0{bits}b"), overflow


def ieee754_single_bits(value: float) -> str:
    packed = struct.pack(">f", value)
    return "".join(f"{byte:08b}" for byte in packed)


def ieee754_single_decode(bits32: str):
    sign = bits32[0]
    exponent = bits32[1:9]
    mantissa = bits32[9:]

    packed = int(bits32, 2).to_bytes(4, "big")
    value = struct.unpack(">f", packed)[0]

    return {
        "sign": sign,
        "exponent": exponent,
        "exponent_dec": int(exponent, 2),
        "exponent_unbiased": int(exponent, 2) - 127,
        "mantissa": mantissa,
        "value": value,
    }


def main():
    N = 105
    F = 0.35
    A, B = -50, -60
    C = -64.25

    print("=== Завдання 1-2: Переведення N у 2, 8, 16 системи; F у двійкову ===")
    print(f"N = {N}")
    print(f"  двійкова:      {int_to_base(N, 2)}")
    print(f"  вісімкова:     {int_to_base(N, 8)}")
    print(f"  шістнадцяткова:{int_to_base(N, 16)}")
    print(f"F = {F}")
    print(f"  двійкова (6 розрядів): 0.{frac_to_base(F, 2, 6)}")

    print()
    print("=== Завдання 3: Додатковий код, додавання A і B, переповнення ===")
    code_a = to_twos_complement(A, 8)
    code_b = to_twos_complement(B, 8)
    print(f"A = {A} -> {code_a}")
    print(f"B = {B} -> {code_b}")
    sum_bits, overflow = add_twos_complement(A, B, 8)
    print(f"Сума (8 біт):     {sum_bits}")
    print(f"Сума в десятковій: {from_twos_complement(sum_bits)}")
    print(f"Переповнення:      {overflow}")

    print()
    print("=== Завдання 4: IEEE 754 single для C ===")
    bits32 = ieee754_single_bits(C)
    decoded = ieee754_single_decode(bits32)
    print(f"C = {C}")
    print(f"32 біти:   {bits32}")
    print(f"Знак:      {decoded['sign']}")
    print(f"Порядок:   {decoded['exponent']} = {decoded['exponent_dec']} "
          f"(зі зміщенням), незміщений = {decoded['exponent_unbiased']}")
    print(f"Мантиса:   {decoded['mantissa']}")
    print(f"Відновлене значення: {decoded['value']}")

    print()
    print("=== Завдання 5: Похибка представлення дробів (0.1 + 0.2) ===")
    a1, b1 = 0.1, 0.2
    s = a1 + b1
    print(f"0.1 + 0.2 = {s!r}")
    print(f"0.1 + 0.2 == 0.3: {s == 0.3}")
    print("Причина: 0.1, 0.2 і 0.3 не мають точного скінченного двійкового "
          "представлення, тому зберігаються з округленням, і сума накопичує похибку.")


if __name__ == "__main__":
    main()
