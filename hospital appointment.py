import sys
import os
import json

# Dictionary with available doctors
doctors = {
    1: "Dr. Smith - General Physician",
    2: "Dr. Johnson - Cardiologist",
    3: "Dr. Williams - Dentist",
    4: "Dr. Brown - Pediatrician",
    5: "Dr. Davis - Neurologist"
}


def read_appointments(file_path):
    """Load appointments from a CSV-like text file. Each line: Name,Age,Gender,Doctor_ID

    Malformed lines are skipped with a warning rather than aborting the program.
    """
    if not os.path.exists(file_path):
        print(f"[Warning] File '{file_path}' not found. Starting with empty list.")
        return []

    appointments = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for lineno, line in enumerate(file, start=1):
                parts = [p.strip() for p in line.strip().split(',')]
                if len(parts) != 4:
                    if line.strip():
                        print(f"[Warning] Skipping malformed line {lineno}: {line.strip()}")
                    continue

                name, age_s, gender, doctor_id_s = parts
                try:
                    age = int(age_s)
                    doctor_id = int(doctor_id_s)
                except ValueError:
                    print(f"[Warning] Invalid numeric value on line {lineno}: {line.strip()}")
                    continue

                appointments.append({
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'doctor_id': doctor_id
                })
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    return appointments


def calculate_stats(appointments):
    """Function 2: Performs the 2 required data calculations"""
    if not appointments:
        return 0, 0

    # Calculation 1: Average Patient Age
    total_age = sum(app['age'] for app in appointments)
    average_age = total_age / len(appointments)

    # Calculation 2: Percentage of Patients Under 18 Years Old (Minors)
    under_18 = sum(1 for app in appointments if app['age'] < 18)
    under_18_rate = (under_18 / len(appointments)) * 100

    return average_age, under_18_rate


def save_and_report(appointments, file_path, report_path):
    """Function 3: Saves active data and generates the summary output report"""
    try:
        # Save active appointment records back to the input file
        with open(file_path, 'w', encoding='utf-8') as file:
            for app in appointments:
                file.write(f"{app['name']},{app['age']},{app['gender']},{app['doctor_id']}\n")

        # Perform calculations
        avg_age, child_rate = calculate_stats(appointments)

        # Write results to the final report text file
        with open(report_path, 'w', encoding='utf-8') as rep_file:
            rep_file.write("===== HOSPITAL APPOINTMENT SYSTEM REPORT =====\n")
            rep_file.write(f"Total Appointments Booked: {len(appointments)}\n")
            rep_file.write(f"Average Patient Age: {avg_age:.1f} years old\n")
            rep_file.write(f"Percentage of Minor Patients (<18): {child_rate:.1f}%\n")
            rep_file.write("==============================================\n")

    except Exception as e:
        print(f"Error saving data: {e}")


def display_doctors():
    print("\n===== Available Doctors =====")
    for key, value in doctors.items():
        print(f"{key}. {value}")


def main():
    # Command Line Argument check
    # First argument: input file (optional)
    # Second argument: report file (optional)
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    else:
        input_file = "appointments.txt"

    if len(sys.argv) >= 3:
        report_file = sys.argv[2]
    else:
        report_file = "hospital_report.txt"

    # Load any pre-existing records from the text file
    appointments = read_appointments(input_file)

    while True:
        print("\n" + "=" * 45)
        print("         HOSPITAL APPOINTMENT SYSTEM          ")
        print("=" * 45)
        print("1. Display Doctors")
        print("2. Book Appointment")
        print("3. View Appointments")
        print("4. Save & Generate Report")
        print("5. Exit")
        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            display_doctors()

        elif choice == "2":
            print("\n===== Book Appointment =====")
            name = input("Enter Patient Name: ")
            try:
                age = int(input("Enter Age: "))
            except ValueError:
                print("Invalid age input. Please enter a valid number.")
                continue
            gender = input("Enter Gender (Male/Female): ")
            display_doctors()
            try:
                doc_id = int(input("Select Doctor (1-5): "))
                if doc_id not in doctors:
                    print("Invalid doctor selection choice.")
                    continue
            except ValueError:
                print("Please enter a valid numeric value for the doctor ID.")
                continue

            appointments.append({'name': name, 'age': age, 'gender': gender, 'doctor_id': doc_id})
            print(f"Appointment successfully booked for {name}!")

        elif choice == "3":
            print("\n===== Booked Appointments =====")
            if not appointments:
                print("No scheduled appointments found.")
            for app in appointments:
                doctor_name = doctors.get(app.get('doctor_id'), 'Unknown')
                print(
                    f"Patient: {app['name']} | Age: {app['age']} | Gender: {app['gender']} | Doctor: {doctor_name}")

        elif choice == "4":
            # Data verification check (Must process at least 3 values for higher marks)
            if len(appointments) < 3:
                print("Error: You must input at least 3 appointments to perform data analysis.")
            else:
                save_and_report(appointments, input_file, report_file)
                print(f"Data saved and report file successfully generated in '{report_file}'!")

        elif choice == "5":
            print("Exiting application system. Goodbye!")
            break
        else:
            print("Invalid system choice option. Please try again.")


if __name__ == "__main__":
    main()
