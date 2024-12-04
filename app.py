# import streamlit as st
# import pandas as pd

# # ฟังก์ชันสำหรับประมวลผลรายงาน (ใช้จากโค้ดของคุณ)
# def process_reports_with_full_details(input_file, output_file, filter_item_id, allowed_merchants):
#     """
#     Process reports by combining lines, extracting full details including Merchant Name,
#     Terminal ID, Account No, Settlement Date, and File Name.
#     """
#     reports = []  # Store valid rows
#     current_row = None
#     current_merchant_id = None
#     current_merchant_name = ""
#     current_terminal_id = ""
#     current_account_no = ""
#     current_settlement_date = ""
#     file_name = ""

#     print("Starting report processing...")

#     with open(input_file, 'r', encoding='utf-8') as infile:
#         lines = infile.readlines()  # Read all lines in advance

#     i = 0  # Line pointer
#     while i < len(lines):
#         line = lines[i].strip()
#         if not line:
#             i += 1
#             continue  # Skip empty lines

#         # Extract File Name
#         if line.startswith("ไฟล์:"):
#             file_name = line.split(":")[1].strip()
#             i += 1
#             continue

#         # Extract Merchant ID, Merchant Name, and Account No
#         if "Merchant ID" in line:
#             parts = line.split()
#             for j, part in enumerate(parts):
#                 if part.isdigit() and len(part) == 9:  # Check for Merchant ID
#                     current_merchant_id = part
#                     # Split remaining parts to extract Merchant Name and Account No
#                     merchant_details = " ".join(parts[j + 1:]).strip()
#                     if "Account No :" in merchant_details:
#                         account_split = merchant_details.split("Account No :")
#                         current_merchant_name = account_split[0].strip()
#                         current_account_no = account_split[1].strip() if len(account_split) > 1 else ""
#                     else:
#                         current_merchant_name = merchant_details
#                     break

#         # Extract Settlement Date
#         if "Settlement Date" in line:
#             current_settlement_date = line.split(":", 1)[1].strip()

#         # Extract Terminal ID
#         if "Terminal ID" in line:
#             current_terminal_id = line.split(":", 1)[1].strip()

#         # Process body (Seq rows)
#         parts = line.split()
#         if parts and parts[0].isdigit():  # Line starts with Seq
#             current_row = parts  # Capture the first row

#             # Ensure Pay Mode and Pay Freq columns are correctly filled
#             pay_mode_index = 4
#             if len(current_row) > pay_mode_index:
#                 pay_mode = current_row[pay_mode_index]
#                 if not (len(pay_mode) == 2 and pay_mode.isalpha()):  # If not a valid Pay Mode
#                     current_row.insert(pay_mode_index, "")  # Insert empty value
#             else:
#                 current_row.insert(pay_mode_index, "")  # Add empty value if column missing

#             pay_freq_index = 5
#             if len(current_row) > pay_freq_index:
#                 pay_freq = current_row[pay_freq_index]
#                 if not (pay_freq.isdigit() and len(pay_freq) <= 2):  # If not a valid Pay Freq
#                     current_row.insert(pay_freq_index, "")  # Insert empty value
#             else:
#                 current_row.insert(pay_freq_index, "")  # Add empty value if column missing

#             # Merge with next line if additional parts exist
#             if i + 1 < len(lines):  # Check if there is a next line
#                 next_line = lines[i + 1].strip()
#                 additional_parts = next_line.split()
#                 current_row.extend(additional_parts)  # Merge with next line
#                 i += 1  # Skip the processed line

#             # Add Merchant and File information to the row
#             current_row.insert(1, current_merchant_id or "")
#             current_row.insert(2, current_merchant_name or "")
#             current_row.insert(3, current_terminal_id or "")
#             current_row.insert(4, current_account_no or "")
#             current_row.insert(5, current_settlement_date or "")
#             current_row.insert(6, file_name or "")

#             # Append valid rows 
#             if filter_item_id in current_row and current_merchant_id in allowed_merchants:
#                 reports.append(" | ".join(current_row))

#             current_row = None  # Reset current row
#         i += 1

#     print(f"Total valid rows: {len(reports)}")

#     # Write the output file
#     with open(output_file, 'w', encoding='utf-8') as outfile:
#         header = ("Seq | Merchant ID | Merchant Name | Terminal ID | Account No | Settlement Date | File Name | "
#                   "Program ID | Item ID | Netw | Pay Mode | Pay Freq | Card No | TC | Auth Code | "
#                   "Trx Time | Trx Date | Total Amount | Redeem Amount | Redeem Point | Batch No | Trace No | "
#                   "Payment Date | Credit Amount | Item Quantity")
#         outfile.write(header + "\n")
#         outfile.write("-" * len(header) + "\n")
#         for row in reports:
#             outfile.write(row + "\n")

#     return outfile

# # Streamlit UI
# st.title("Report Processing Application")
# st.write("Upload a TXT file to process it and display results.")

# # Upload file
# uploaded_file = st.file_uploader("Upload your TXT file", type="txt")

# # Filters
# filter_item_id = st.text_input("Filter Item ID", "7463")
# allowed_merchants = st.text_area("Allowed Merchant IDs (comma-separated)", "141300003")
# allowed_merchants_list = [x.strip() for x in allowed_merchants.split(",") if x.strip()]

# # Process file
# # Streamlit Integration
# if uploaded_file and st.button("Process File"):
#     st.write("Processing your file...")
    
#     # เขียนไฟล์ที่อัปโหลดเป็นไฟล์ชั่วคราว
#     input_file = "uploaded_file.txt"
#     with open(input_file, "w", encoding="utf-8") as f:
#         f.write(uploaded_file.read().decode("utf-8"))
    
#     # ประมวลผลไฟล์และสร้าง output file
#     output_file = "processed_output.txt"
#     process_reports_with_full_details(input_file, output_file, filter_item_id, allowed_merchants_list)

#     # อ่านไฟล์ที่ประมวลผลด้วย pandas
#     try:
#         df = pd.read_csv(output_file, delimiter="|")
#         st.dataframe(df)
#     except Exception as e:
#         st.error(f"Error reading processed file: {e}")

#     # ให้ผู้ใช้ดาวน์โหลดไฟล์ผลลัพธ์
#     with open(output_file, "r", encoding="utf-8") as f:
#         st.download_button(
#             label="Download Processed Report",
#             data=f.read(),
#             file_name="processed_report.txt",
#             mime="text/plain"
#         )

import pandas as pd
import streamlit as st

# Function to filter data
def filter_data(input_file, merchant_ids, item_ids, account_no_filters, settlement_date_filters, trx_date_filters, output_file):
    """
    Filters the input file based on Merchant IDs, Item IDs, Account No, Settlement Date, and Trx Date.
    Supports comma-separated filtering for all fields.
    Writes the filtered result to an output file.
    """
    try:
        # อ่านไฟล์
        df = pd.read_csv(
            input_file,
            delimiter="|",
            dtype=str,  # บังคับให้อ่านทุกคอลัมน์เป็น string
            engine="python"
        )

        # ลบช่องว่างรอบชื่อคอลัมน์
        df.columns = df.columns.str.strip()

        # ลบแถวที่เป็นเส้นแบ่ง (----) ถ้ามี
        if any(df.iloc[:, 0].str.contains("----", na=False)):
            df = df[~df.iloc[:, 0].str.contains("----", na=False)]

        # กำหนดชื่อคอลัมน์ที่คาดหวัง
        expected_columns = [
            "Seq", "Merchant ID", "Merchant Name", "Terminal ID", "Account No", "Settlement Date",
            "File Name", "Program ID", "Item ID", "Netw", "Pay Mode", "Pay Freq", "Card No",
            "TC", "Auth Code", "Trx Time", "Trx Date", "Total Amount", "Redeem Amount",
            "Redeem Point", "Batch No", "Trace No", "Payment Date", "Credit Amount", "Item Quantity"
        ]

        # ตรวจสอบจำนวนคอลัมน์
        if len(df.columns) != len(expected_columns):
            st.error("The file does not match the expected format.")
            print("Detected columns:", df.columns)
            return pd.DataFrame()

        # ตั้งชื่อคอลัมน์
        df.columns = expected_columns

        # ลบช่องว่างในค่าข้อมูล
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # แปลง comma-separated filters เป็นลิสต์
        account_no_filters = [x.strip() for x in account_no_filters.split(",") if x.strip()]
        settlement_date_filters = [x.strip() for x in settlement_date_filters.split(",") if x.strip()]
        trx_date_filters = [x.strip() for x in trx_date_filters.split(",") if x.strip()]

        # กรองข้อมูลตามเงื่อนไข
        filtered_df = df[
            (df["Merchant ID"].isin(merchant_ids)) &
            (df["Item ID"].isin(item_ids)) &
            (df["Account No"].isin(account_no_filters)) &
            (df["Settlement Date"].isin(settlement_date_filters)) &
            (df["Trx Date"].isin(trx_date_filters))
        ]

        # บันทึกข้อมูลที่กรองแล้ว
        filtered_df.to_csv(output_file, index=False, sep="|")
        return filtered_df

    except Exception as e:
        st.error(f"Error processing the file: {e}")
        print(f"Error details: {e}")
        return pd.DataFrame()



# Streamlit UI
st.title("Filter Transaction Data")
st.write("Upload your transaction file and filter it by Merchant IDs, Item IDs, Account No, Settlement Date, and Trx Date.")

# Upload file
uploaded_file = st.file_uploader("Upload your TXT file", type="txt")

# Filters
item_ids_input = st.text_area("Enter allowed Item IDs (comma-separated)", "7462")
item_ids = [x.strip() for x in item_ids_input.split(",") if x.strip()]

merchant_ids_input = st.text_area("Enter allowed Merchant IDs (comma-separated)", "141300003")
merchant_ids = [x.strip() for x in merchant_ids_input.split(",") if x.strip()]

account_no_filter = st.text_area("Filter Account No (comma-separated)", "")
settlement_date_filter = st.text_area("Filter Settlement Date (comma-separated, e.g., 06/09/24,07/09/24)", "")
trx_date_filter = st.text_area("Filter Trx Date (comma-separated, e.g., 06/09/24,07/09/24)", "")

# Process file
if uploaded_file and st.button("Filter Data"):
    st.write("Processing your file...")
    
    # Save uploaded file as a temporary file
    input_file = "uploaded_transactions.txt"
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(uploaded_file.read().decode("utf-8"))
    
    # Define output file name
    output_file = "filtered_transactions.txt"
    
    # Filter data
    filtered_df = filter_data(
        input_file, merchant_ids, item_ids, account_no_filter, settlement_date_filter, trx_date_filter, output_file
    )
    
    # Display the filtered data in Streamlit
    if filtered_df.empty:
        st.warning("No data matched the given filters.")
    else:
        st.dataframe(filtered_df)
    
    # Provide a download button for the filtered data
    with open(output_file, "r", encoding="utf-8") as f:
        st.download_button(
            label="Download Filtered Data",
            data=f.read(),
            file_name="filtered_transactions.txt",
            mime="text/plain"
        )
