import os

INVOICE_FOLDER = "invoices"


def scan_invoices():
    files = os.listdir(INVOICE_FOLDER)

    invoice_files = []

    for file in files:
        if file.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            invoice_files.append(file)

    return invoice_files


def main():

    invoices = scan_invoices()

    print(f"Found {len(invoices)} files:")

    for f in invoices:
        print("-", f)


if __name__ == "__main__":
    main()