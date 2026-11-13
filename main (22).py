import os

def process_attendance(folder):
    attendance = {}
    rejected = []

    files = sorted(os.listdir(folder))

    for filename in files:
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)

        try:
            with open(path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, 1):
                    if not line.strip():
                        continue

                    try:
                        parts = line.strip().split(",")

                        if len(parts) != 3:
                            raise ValueError("Invalid fields")

                        reg_no, date, status = parts

                        if status not in ("P", "A"):
                            raise ValueError("Invalid status")

                        if reg_no not in attendance:
                            attendance[reg_no] = [0, 0]

                        if status == "P":
                            attendance[reg_no][0] += 1
                        else:
                            attendance[reg_no][1] += 1

                    except ValueError as error:
                        rejected.append(
                            (filename, line_number, str(error))
                        )

        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
            rejected.append((filename, 0, str(error)))

    with open("attendance_report.txt", "w", encoding="utf-8") as report:
        with open("below_75.txt", "w", encoding="utf-8") as below:
            for reg_no, counts in attendance.items():
                present, absent = counts
                total = present + absent

                percentage = (present / total) * 100

                report.write(
                    f"{reg_no},{present},{absent},{percentage:.2f}%\n"
                )

                if percentage < 75:
                    below.write(f"{reg_no},{percentage:.2f}%\n")

    with open("damaged_lines.txt", "w", encoding="utf-8") as error_file:
        for item in rejected:
            error_file.write(f"{item}\n")

    print(attendance)
    print("Rejected:", rejected)


os.makedirs("attendance_files", exist_ok=True)

with open("attendance_files/day1.txt", "w", encoding="utf-8") as file:
    file.write("192311001,2026-10-01,P\n")
    file.write("192311002,2026-10-01,A\n")
    file.write("192311003,2026-10-01,X\n")

with open("attendance_files/day2.txt", "w", encoding="utf-8") as file:
    file.write("192311001,2026-10-02,P\n")
    file.write("192311002,2026-10-02,P\n")

process_attendance("attendance_files")