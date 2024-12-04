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
