def process_file(filename):
    total = 0
    report = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, 1):
                if not line.strip():
                    continue

                try:
                    parts = line.strip().split(",")

                    if len(parts) != 3:
                        raise ValueError("Invalid number of fields")

                    amount = float(parts[2])
                    total += amount
                    report.append(f"{parts[1]} {amount:.2f}")

                except (ValueError, IndexError) as error:
                    rejected.append((line_number, line.strip(), str(error)))

        print("\n".join(report))
        print("Total:", total)
        print("Rejected:", rejected)

    except FileNotFoundError:
        print("File not found")

filename = "mess_oct.txt"

with open(filename, "w", encoding="utf-8") as file:
    file.write("192311001,Arun,1250.50\n")
    file.write("192311002,Ravi,1500.00\n")
    file.write("192311003,Kumar,invalid\n")

process_file(filename)