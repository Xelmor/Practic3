import json
import argparse

# таблица размеров команд из спецификации УВМ
CMD_SIZES = {
    "load_const": 4,
    "load_mem": 6,
    "store_mem": 3,
    "less": 6
}

def translate_to_ir(program):
    ir = []
    for instr in program:
        cmd = instr["cmd"]

        if cmd not in CMD_SIZES:
            raise ValueError(f"Unknown command: {cmd}")

        # промежуточное представление
        ir_entry = {
            "cmd": cmd,
            "A": instr["A"],
            "B": instr["B"],
            "C": instr["C"],
            "size": CMD_SIZES[cmd]
        }
        ir.append(ir_entry)
    return ir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to JSON program")
    parser.add_argument("output", help="Path to binary output (unused in stage 1)")
    parser.add_argument("--test", action="store_true", help="Print IR")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        program = json.load(f)

    ir = translate_to_ir(program)

    if args.test:
        print("========INTERMEDIATE REPRESENTATION (IR):=========")
        for instr in ir:
            print(instr)

    # этап 1 не требует записи бинарного файла
    # создадим пока пустой файл
    with open(args.output, "wb") as f:
        f.write(b"")


if __name__ == "__main__":
    main()