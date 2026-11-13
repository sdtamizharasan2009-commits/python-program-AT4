import os
import tempfile

class InvalidRecord(Exception):
    pass


def parse_line(line):
    parts = line.strip().split(",")

    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )

    if parts[2] not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{parts[2]}'")

    return tuple(parts)


def summarise(path):
    present = 0
    absent = 0
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, 1):
                if not line.strip():
                    continue

                try:
                    reg_no, date, status = parse_line(line)

                    if status == "P":
                        present += 1
                    else:
                        absent += 1

                except InvalidRecord as error:
                    errors.append((line_number, str(error)))

    except FileNotFoundError as error:
        raise FileNotFoundError("Attendance file not found") from error

    except PermissionError as error:
        raise PermissionError("Permission denied") from error

    except UnicodeDecodeError as error:
        raise UnicodeError("Invalid file encoding") from error

    else:
        return present, absent, errors

    finally:
        print("File processing completed")


data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

with tempfile.NamedTemporaryFile(
    "w", suffix=".csv", delete=False, encoding="utf-8"
) as tmp:
    tmp.write(data)
    filename = tmp.name

try:
    print(summarise(filename))

except FileNotFoundError as error:
    print(error)

finally:
    os.remove(filename)


try:
    print(summarise("missing_attendance.csv"))

except FileNotFoundError as error:
    print(error)