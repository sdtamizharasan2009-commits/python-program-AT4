def read_attendance(filename):
    records = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")

            if len(parts) == 3:
                records.append(parts)

    return records


def calculate_percentage(records):
    stats = {}

    for reg_no, date, status in records:
        if reg_no not in stats:
            stats[reg_no] = [0, 0]

        if status == "P":
            stats[reg_no][0] += 1
        elif status == "A":
            stats[reg_no][1] += 1

    return stats


def write_report(stats):
    with open("attendance_report.txt", "w", encoding="utf-8") as file:
        for reg_no, values in stats.items():
            total = values[0] + values[1]

            if total > 0:
                percentage = values[0] / total * 100
                file.write(f"{reg_no},{percentage:.2f}%\n")


def absent_three_days(records):
    absent_dates = {}

    for reg_no, date, status in records:
        if status == "A":
            if reg_no not in absent_dates:
                absent_dates[reg_no] = []

            absent_dates[reg_no].append(date)

    result = []

    for reg_no, dates in absent_dates.items():
        dates.sort()

        for index in range(len(dates) - 2):
            if (
                (dates[index + 1] > dates[index])
                and (dates[index + 2] > dates[index + 1])
            ):
                result.append(reg_no)
                break

    return result


if __name__ == "__main__":
    with open("attendance.txt", "w", encoding="utf-8") as file:
        file.write("192311001,2026-10-01,P\n")
        file.write("192311001,2026-10-02,A\n")
        file.write("192311001,2026-10-03,A\n")
        file.write("192311001,2026-10-04,A\n")
        file.write("192311002,2026-10-01,P\n")
        file.write("192311002,2026-10-02,P\n")

    records = read_attendance("attendance.txt")
    stats = calculate_percentage(records)

    write_report(stats)

    print("Attendance:", stats)
    print("Absent for three consecutive days:", absent_three_days(records))