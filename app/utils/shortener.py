BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]

    chars = []

    while num:
        num, rem = divmod(num, 62)
        chars.append(BASE62[rem])

    return "".join(reversed(chars))


def generate_short_code(id: int, length: int = 7) -> str:
    return encode_base62(id).rjust(length, "0")
