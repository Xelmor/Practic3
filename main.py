import json
import argparse

CMD_SPECS = {
    "load_const":  {"size": 4, "A_bits": (0, 8), "B_bits": (8, 21), "C_bits": (21, 28)},
    "load_mem":    {"size": 6, "A_bits": (0, 8), "B_bits": (8, 15), "C_bits": (15, 47)},
    "store_mem":   {"size": 3, "A_bits": (0, 8), "B_bits": (8, 15), "C_bits": (15, 22)},
    "less":        {"size": 6, "A_bits": (0, 8), "B_bits": (8, 15), "C_bits": (15, 47)},
}

def pack_command(cmd, A, B, C):
    spec = CMD_SPECS[cmd]

    A_from, A_to = spec["A_bits"]
    B_from, B_to = spec["B_bits"]
    C_from, C_to = spec["C_bits"]

    value = 0
    value |= A << A_from
    value |= B << B_from
    value |= C << C_from

    size = spec["size"]
    return value.to_bytes(size, byteorder="little")


def translate_to_ir(program):
    return [
        {"cmd": instr["cmd"], "A": instr["A"], "B": instr["B"], "C": instr["C"]}
        for instr in program
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to JSON program")
    parser.add_argument("output", help="Path to binary output")
    parser.add_argument("--test", action="store_true", help="Print IR and machine code")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        program = json.load(f)

    ir = translate_to_ir(program)

    # Этап 2 — формирование машинного кода
    machine_code = b""
    for instr in ir:
        cmd, A, B, C = instr["cmd"], instr["A"], instr["B"], instr["C"]
        machine_code += pack_command(cmd, A, B, C)

    with open(args.output, "wb") as f:
        f.write(machine_code)

    print(f"Количество ассемблированных команд: {len(ir)}")

    if args.test:
        print("\n=== MACHINE CODE (hex) ===")
        print(" ".join(f"{b:02X}" for b in machine_code))


if __name__ == "__main__":
    main()