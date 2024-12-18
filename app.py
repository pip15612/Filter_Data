import pandas as pd
import streamlit as st

# Function to filter data
def filter_data(df, merchant_ids, item_ids, account_no_filters, settlement_date_filters, trx_date_filters):
    try:
        # ทำความสะอาดข้อมูล
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # เริ่มต้นจากข้อมูลต้นฉบับ
        filtered_df = df.copy()

        # กรอง Merchant ID
        if merchant_ids:
            merchant_ids = [x.strip() for x in merchant_ids]
            filtered_df = filtered_df[filtered_df["Merchant ID"].isin(merchant_ids)]

        # กรอง Item ID
        if item_ids:
            item_ids = [x.strip() for x in item_ids]
            filtered_df = filtered_df[filtered_df["Item ID"].isin(item_ids)]

        # กรอง Account No
        if account_no_filters:
            account_no_filters = [x.strip() for x in account_no_filters.split(",") if x.strip()]
            filtered_df = filtered_df[filtered_df["Account No"].isin(account_no_filters)]

        # กรอง Settlement Date
        if settlement_date_filters:
            settlement_date_filters = [x.strip() for x in settlement_date_filters.split(",") if x.strip()]
            filtered_df = filtered_df[filtered_df["Settlement Date"].isin(settlement_date_filters)]

        # กรอง Trx Date
        if trx_date_filters:
            trx_date_filters = [x.strip() for x in trx_date_filters.split(",") if x.strip()]
            filtered_df = filtered_df[filtered_df["Trx Date"].isin(trx_date_filters)]

        return filtered_df

    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return pd.DataFrame()



# Streamlit UI
st.title("Filter Transaction Data")
st.write("Upload your transaction file and filter it by Merchant IDs, Item IDs, Account No, Settlement Date, and Trx Date.")

# Expected Columns
expected_columns = [
    "Seq", "Merchant ID", "Merchant Name", "Terminal ID", "Account No", "Settlement Date",
    "File Name", "Program ID", "Item ID", "Netw", "Pay Mode", "Pay Freq", "Card No",
    "TC", "Auth Code", "Trx Time", "Trx Date", "Total Amount", "Redeem Amount",
    "Redeem Point", "Batch No", "Trace No", "Payment Date", "Credit Amount", "Item Quantity"
]

# Upload file
uploaded_file = st.file_uploader("Upload your TXT file", type="txt")

# Show the table of the input file
if uploaded_file:
    try:
        # อ่านไฟล์ตรงจาก uploaded_file
        input_file_preview = pd.read_csv(
            uploaded_file,
            delimiter="|",
            names=expected_columns,
            dtype=str,
            skiprows=1,
            engine="python"
        )
        input_file_preview.columns = input_file_preview.columns.str.strip()
        st.subheader("Preview of Uploaded File")
        st.dataframe(input_file_preview)
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")

    # Filters
    item_ids_input = st.text_area("Enter allowed Item IDs (comma-separated)", "7462")
    item_ids = [x.strip() for x in item_ids_input.split(",") if x.strip()]

    merchant_ids_input = st.text_area("Enter allowed Merchant IDs (comma-separated)", "141300003")
    merchant_ids = [x.strip() for x in merchant_ids_input.split(",") if x.strip()]

    account_no_filter = st.text_area("Filter Account No (comma-separated)", "")
    settlement_date_filter = st.text_area("Filter Settlement Date (comma-separated, e.g., 06/09/24,07/09/24)", "")
    trx_date_filter = st.text_area("Filter Trx Date (comma-separated, e.g., 06/09/24,07/09/24)", "")

    # Process file
    if st.button("Filter Data"):
        st.write("Processing your file...")

        # เรียกใช้ filter_data โดยไม่ต้องบันทึกไฟล์ชั่วคราว
        filtered_df = filter_data(
            input_file_preview, merchant_ids, item_ids, account_no_filter, settlement_date_filter, trx_date_filter
        )

        # Display the filtered data
        if filtered_df.empty:
            st.warning("No data matched the given filters.")
        else:
            st.subheader("Filtered Data")
            st.dataframe(filtered_df)

            # Provide a download button
            csv_output = filtered_df.to_csv(index=False, sep="|")
            st.download_button(
                label="Download Filtered Data",
                data=csv_output,
                file_name="filtered_transactions.txt",
                mime="text/plain"
            )
