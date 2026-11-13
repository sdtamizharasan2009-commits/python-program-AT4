import os
import re

def valid_email(email):
    return (
        "@" in email
        and "." in email.split("@")[-1]
        and email.count("@") == 1
        and not email.startswith("@")
        and not email.endswith("@")
        and " " not in email
    )


def process_registrations(folder):
    students = {}
    seen = set()
    events = {}
    errors = []

    for department in range(1, 6):
        filename = f"department{department}.txt"
        path = os.path.join(folder, filename)

        try:
            with open(path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, 1):

                    try:
                        parts = line.strip().split(",")

                        if len(parts) != 5:
                            raise ValueError("Invalid number of fields")

                        reg_no, name, dept, email, event_text = parts

                        if not reg_no or not name or not dept:
                            raise ValueError("Missing student details")

                        if not valid_email(email):
                            raise ValueError("Invalid email")

                        if reg_no in seen:
                            raise ValueError("Duplicate registration")

                        chosen_events = event_text.split(";")

                        if not all(event.strip() for event in chosen_events):
                            raise ValueError("Invalid event list")

                        seen.add(reg_no)

                        students[reg_no] = (
                            name, dept, email, chosen_events
                        )

                        for event in chosen_events:
                            event = event.strip()

                            if event not in events:
                                events[event] = []

                            events[event].append(
                                (reg_no, name, dept, email)
                            )

                    except ValueError as error:
                        errors.append(
                            (filename, line_number, str(error))
                        )

        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
            errors.append((filename, 0, str(error)))

    with open("master_list.txt", "w", encoding="utf-8") as file:
        for reg_no, details in students.items():
            name, dept, email, chosen_events = details

            file.write(
                f"{reg_no},{name},{dept},{email},{';'.join(chosen_events)}\n"
            )

    for event, participants in events.items():
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", event)

        with open(f"{safe_name}.txt", "w", encoding="utf-8") as file:
            for participant in participants:
                file.write(",".join(participant) + "\n")

    with open("summary.txt", "w", encoding="utf-8") as file:
        file.write(f"Total registrations: {len(students)}\n")
        file.write(f"Total events: {len(events)}\n")

        for event, participants in events.items():
            file.write(
                f"{event}: {len(participants)} participants\n"
            )

    with open("error_log.txt", "w", encoding="utf-8") as file:
        for error in errors:
            file.write(f"{error}\n")

    print("Master List:", students)
    print("Events:", events)
    print("Errors:", errors)


os.makedirs("fest_files", exist_ok=True)

with open("fest_files/department1.txt", "w", encoding="utf-8") as file:
    file.write("192311001,Arun,CSE,arun@gmail.com,Singing;Dance\n")
    file.write("192311002,Ravi,IT,ravi@gmail.com,Drama\n")

with open("fest_files/department2.txt", "w", encoding="utf-8") as file:
    file.write("192311001,Arun,CSE,arun@gmail.com,Singing\n")
    file.write("192311003,Kumar,EEE,invalidemail,Dance\n")

with open("fest_files/department3.txt", "w", encoding="utf-8") as file:
    file.write("192311004,Mani,MECH,mani@gmail.com,Music\n")
    file.write("192311005,John,IT,john@gmail.com\n")

with open("fest_files/department4.txt", "w", encoding="utf-8") as file:
    file.write("192311006,Sam,ECE,sam@gmail.com,Dance;Drama\n")

process_registrations("fest_files")