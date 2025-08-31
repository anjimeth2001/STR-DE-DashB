import streamlit as st
import pandas as pd
import re
import plotly.express as px
import time

# Set page config
st.set_page_config(page_title="Dye Exhaust Dashboard", layout="wide")

# Force theme settings
st.markdown(
    """
    <style>
        /* Override Streamlit dark theme */
        body {
            background-color: white !important;
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'login_error' not in st.session_state:
    st.session_state.login_error = False

def login_screen():
    """Display login screen"""
    st.markdown("""
    <style>
    .main-header { text-align: center; color: #1f77b4; margin-bottom: 2rem; }
    .login-container { background-color: #f8f9fa; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .stTextInput > div > div > input { background-color: white; border-radius: 5px; }
    .error-message { color: red; font-weight: bold; text-align: center; margin: 1rem 0; background-color: #ffe6e6; padding: 0.5rem; border-left: 4px solid red; }
    .success-message { color: green; font-weight: bold; text-align: center; margin: 1rem 0; background-color: #e6ffe6; padding: 0.5rem; border-left: 4px solid green; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">🔐 Dye Exhaust Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### 🚀 Please Login to Continue")
        username = st.text_input("👤 Username", placeholder="exhaust", help="💡 Hint: exhaust")
        password = st.text_input("🔑 Password", type="password", placeholder="password")

        if st.session_state.login_error:
            st.markdown('<div class="error-message">❌ Username or password is wrong</div>', unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 Login", use_container_width=True, type="primary"):
                if username == "exhaust" and password == "1234":
                    st.session_state.authenticated = True
                    st.session_state.login_error = False
                    st.markdown('<div class="success-message">✅ Login Successful! Loading dashboard...</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.login_error = True
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<div style='text-align:center; color:#666; font-size:0.8rem;'>🔒 Secure Login Required<br>Contact administrator for access</div>", unsafe_allow_html=True)

def main_application():
    """Main application after successful login"""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='text-align:center; padding:0.5rem; background-color:#e8f4fd; border-radius:5px; margin-bottom:1rem;'><strong>👋 Welcome</strong><br><small>Dye Exhaust- Data Integration Dashboard</small></div>", unsafe_allow_html=True)
        
    # --- Switch for file input ---
    st.markdown("---")
    st.markdown("### 📥 Upload Files")
    input_method = st.radio("Choose method:", ["Upload Files"])

    # --- Define file variables ---
    if input_method == "Upload Files":
        exd_file = st.file_uploader("Upload Exhaust Data Excel", type=["xlsx"])
        logbook_file = st.file_uploader("Upload Logbook Excel", type=["xlsx"])
        maindye_file = st.file_uploader("Upload Main Dye Sample Excel", type=["xlsx"])
        finalsample_file = st.file_uploader("Upload Final Sample Excel", type=["xlsx"])
        cmc_file = st.file_uploader("Upload CMC Data Entry Excel", type=["xlsx"])
    else:
        exd_file = st.file_uploader("Upload Exhaust Data Excel", type=["xlsx"])
        logbook_file = st.file_uploader("Upload Logbook Excel", type=["xlsx"])
        maindye_file = st.file_uploader("Upload Main Dye Sample Excel", type=["xlsx"])
        finalsample_file = st.file_uploader("Upload Final Sample Excel", type=["xlsx"])
        cmc_file = st.file_uploader("Upload CMC Data Entry Excel", type=["xlsx"])

    if exd_file and logbook_file and maindye_file and finalsample_file and cmc_file:
        st.success("✅ All files linked successfully!")

        with st.spinner("🔄 Processing files..."):
            # --- Read Excel files ---
            if input_method == "Upload Files":
                exd_df = pd.read_excel(exd_file, sheet_name="Sheet2")
                logbook_df = pd.read_excel(logbook_file, sheet_name="Data")
                maindye_df = pd.read_excel(maindye_file)
                finalsample_df = pd.read_excel(finalsample_file)
                cmc_df = pd.read_excel(cmc_file, sheet_name="Main Dye Batches")
            else:
                exd_df = pd.read_excel(exd_file, sheet_name="Sheet2")
                logbook_df = pd.read_excel(logbook_file, sheet_name="Data")
                maindye_df = pd.read_excel(maindye_file)
                finalsample_df = pd.read_excel(finalsample_file)
                cmc_df = pd.read_excel(cmc_file, sheet_name="Main Dye Batches")

            # -------------------------------
            # 🔹 Existing processing code here
            # (All your previous merging, dE categorization, FS-count, MD-count,
            # charts, stacked bar plots, line plots, etc. remain unchanged)
            # -------------------------------
            # For brevity, I am not repeating all your existing processing and chart code,
            # but you just place it here as it was in your original script,
            # using the same exd_df, maindye_df, finalsample_df, cmc_df variables.
            # -------------------------------
            # -------------------------------
            # 🔹 Process Logbook Data
            # -------------------------------
            start_col = "Start Time"
            finish_col = "Finish Time"

            logbook_df = logbook_df[['f', start_col, finish_col]].copy()
            logbook_df[start_col] = pd.to_datetime(logbook_df[start_col], dayfirst=True, errors='coerce')
            logbook_df[finish_col] = pd.to_datetime(logbook_df[finish_col], dayfirst=True, errors='coerce')

            agg_dates = logbook_df.groupby('f', as_index=False).agg({
                start_col: 'min',
                finish_col: 'max'
            })

            exd_df = exd_df.merge(
                agg_dates,
                left_on='DyeLot_ID',
                right_on='f',
                how='left'
            ).drop(columns=['f'])

            exd_df.rename(columns={
                start_col: 'Start Date',
                finish_col: 'Finish Date'
            }, inplace=True)

            exd_df['Finish Date'] = pd.to_datetime(exd_df['Finish Date'], errors='coerce')

            exd_df['Dye Finish Date'] = exd_df['Finish Date'].apply(
                lambda x: (x - pd.Timedelta(days=1)).date() if pd.notnull(x) and x.hour <= 7
                else x.date() if pd.notnull(x) else pd.NaT
            )
            exd_df['Time'] = exd_df['Finish Date'].apply(
                lambda x: x.strftime('%I:%M %p') if pd.notnull(x) else ''
            )

            exd_df['Start Date'] = pd.to_datetime(exd_df['Start Date'], errors='coerce').dt.strftime('%d/%m/%Y %H:%M')
            exd_df['Finish Date'] = pd.to_datetime(exd_df['Finish Date'], errors='coerce').dt.strftime('%d/%m/%Y %H:%M')

            # -------------------------------
            # 🔹 Extract BatchID in ExD
            # -------------------------------
            if "DyeLot_ID" in exd_df.columns:
                exd_df["BatchID"] = exd_df["DyeLot_ID"].astype(str).apply(
                    lambda x: re.search(r"\d{7}", x).group() if re.search(r"\d{7}", x) else None
                )
            else:
                st.error("❌ ExD file must have 'DyeLot_ID' column.")
                st.stop()

            # -------------------------------
            # 🔹 Process MainDyeSample Data
            # -------------------------------
            if "Batch Name" in maindye_df.columns:
                maindye_df["BatchID"] = maindye_df["Batch Name"].astype(str).apply(
                    lambda x: re.search(r"\d{7}", x).group() if re.search(r"\d{7}", x) else None
                )
            else:
                st.error("❌ Column 'Batch Name' not found in MainDyeSample file.")
                st.stop()

            maindye_agg = maindye_df.groupby("BatchID", as_index=False).agg({
                "dE": "mean"
            })

            exd_df = exd_df.merge(
                maindye_agg,
                on="BatchID",
                how="left"
            ).rename(columns={"dE": "MD_dE"})

            

            # -------------------------------
            # 🔹 Process FinalSample Data
            # -------------------------------
            if "Batch Name" in finalsample_df.columns:
                finalsample_df["BatchID"] = finalsample_df["Batch Name"].astype(str).apply(
                    lambda x: re.search(r"\d{7}", x).group() if re.search(r"\d{7}", x) else None
                )
            else:
                st.error("❌ Column 'Batch Name' not found in FinalSample file.")
                st.stop()

            finalsample_agg = finalsample_df.groupby("BatchID", as_index=False).agg({
                "dE": "mean"
            })

            exd_df = exd_df.merge(
                finalsample_agg,
                on="BatchID",
                how="left"
            ).rename(columns={"dE": "FS_dE"})

            # ✅ Create FS_dE_Category column
            def categorize_fs_de(val):
                if pd.isna(val) or val == "":
                    return ""
                elif val < 0.6:
                    return "0.6"
                elif val < 0.8:
                    return "0.8"
                elif val < 1.0:
                    return "1.0"
                elif val < 1.2:
                    return "1.2"
                else:
                    return "High dE"

            exd_df["FS_dE_Category"] = exd_df["FS_dE"].apply(categorize_fs_de)

            # ✅ Create MD_dE_Category column
            def categorize_md_de(val):
                if pd.isna(val) or val == "":
                    return ""
                elif val < 0.6:
                    return "0.6"
                elif val < 0.8:
                    return "0.8"
                elif val < 1.0:
                    return "1.0"
                elif val < 1.2:
                    return "1.2"
                else:
                    return "High dE"

            exd_df["MD_dE_Category"] = exd_df["MD_dE"].apply(categorize_md_de)

            # ✅ Add FS-count column: 1 if FS_dE has a value, else 0
            exd_df["FS-count"] = exd_df["FS_dE"].apply(lambda x: 1 if pd.notna(x) else 0)

            # ✅ Add MD-count column: 1 if FS_dE has a value, else 0
            exd_df["MD-count"] = exd_df["MD_dE"].apply(lambda x: 1 if pd.notna(x) else 0)

            # -------------------------------
            # 🔹 Process CMCDataEntry Data
            # -------------------------------
            if "BATCH NO" in cmc_df.columns:
                cmc_subset = cmc_df[[
                    "BATCH NO",
                    "Reason for no SM Point entering",
                    "Reason for No SM add taken",
                    "Number of add"
                ]].copy()

                # 🔹 Fill empty cells in 'Number of add' with 0
                cmc_subset["Number of add"] = cmc_subset["Number of add"].fillna(0)

                exd_df = exd_df.merge(
                    cmc_subset,
                    left_on="DyeLot_ID",
                    right_on="BATCH NO",
                    how="left"
                ).drop(columns=["BATCH NO"])
            else:
                st.error("❌ Column 'BATCH NO' not found in CMCDataEntry file.")
                st.stop()

        # -------------------------------
        # 📈 DASHBOARD (adds visuals only; no changes to exd_df)
        # -------------------------------
        st.markdown("---")
        #st.markdown("## 📊 Data Analysis Dashboard")
        
        df_vis = exd_df.copy()  # ✅ ALWAYS DEFINE df_vis

        # 📌 Bottom bar in sidebar showing "EXHAUST"
          # -------------------------------
        st.sidebar.markdown("""
                       <div style='
                           text-align: center; 
                           padding: 0.5rem; 
                           background-color: #998581; 
                           border-radius: 5px; 
                           margin-top: 1rem;
                       '>
                           <strong>EXHAUST</strong>
                       </div>
                   """, unsafe_allow_html=True)
        
        # --- Add space between Exhaust box and Refresh button ---
        st.sidebar.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        if "Dye Finish Date" in df_vis.columns:
            df_vis["Dye Finish Date"] = pd.to_datetime(df_vis["Dye Finish Date"], errors="coerce")
            df_vis["Day"] = df_vis["Dye Finish Date"].dt.day

            # Sidebar date range
            valid_dates = df_vis["Dye Finish Date"].dropna()
            if not valid_dates.empty:
                min_date = valid_dates.min().date()
                max_date = valid_dates.max().date()
                st.sidebar.header("📅 Select Date Range")
                start_date = st.sidebar.date_input(
                    "Start Date",
                    pd.to_datetime("2025-01-02").date(),
                    min_value=min_date,
                    max_value=max_date
                )
                end_date = st.sidebar.date_input(
                    "End Date",
                    pd.to_datetime("2025-01-08").date(),
                    min_value=min_date,
                    max_value=max_date
                )
                if start_date > end_date:
                    start_date, end_date = end_date, start_date
                mask = (df_vis["Dye Finish Date"] >= pd.to_datetime(start_date)) & \
                       (df_vis["Dye Finish Date"] <= pd.to_datetime(end_date))
                df_vis = df_vis.loc[mask]

                # Ensure column exists
                if 'EndDateTime MAX' in exd_df.columns:
                   last_updated = pd.to_datetime(exd_df['EndDateTime MAX'], errors='coerce').max()
                   if pd.notnull(last_updated):
                      st.sidebar.markdown(
                         f"<div style='margin-top:2rem; color:#555; font-size:0.9rem;'>"
                         f"📌 Exhaust Data Last Updated: <strong>{last_updated.strftime('%d/%m/%Y %H:%M')}</strong>"
                         f"</div>", 
                         unsafe_allow_html=True
                       )
                      
                      # -------------------------------


                   # --- Add space between Exhaust box and Refresh button ---
                   st.sidebar.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True)

                  # --- Centered Refresh Button ---
                refresh_col1, refresh_col2, refresh_col3 = st.sidebar.columns([1,2,1])
                with refresh_col2:
                    if st.button("🔄 Refresh"):
                        st.rerun()  # <-- This reloads the app
                   


            # Helper to prep stacked % data
            def make_stack(df, cat_col):
                tmp = df[df[cat_col] != ""].copy()
                if tmp.empty:
                    return tmp
                tmp = tmp.groupby(["Day", cat_col]).size().reset_index(name="Count")
                tmp["Total"] = tmp.groupby("Day")["Count"].transform("sum")
                tmp["Pct"] = (tmp["Count"] / tmp["Total"] * 100).round(2)
                tmp["Label"] = tmp["Pct"].map(lambda v: f"{v:.1f}%")
                return tmp

            cat_order = ["0.6", "0.8", "1.0", "1.2", "High dE"]

            md_data = make_stack(df_vis, "MD_dE_Category")
            fs_data = make_stack(df_vis, "FS_dE_Category")
            add_data = make_stack(df_vis, "Number of add")
            reason_data = make_stack(df_vis, "Reason for No SM add taken")

            # --- Main Dye Sample chart ---
            if not md_data.empty:
                st.subheader("Main Dye Sample dE Breakdown")
                fig_md = px.bar(
                    md_data,
                    x="Day",
                    y="Pct",
                    color="MD_dE_Category",
                    text="Label",
                    category_orders={"MD_dE_Category": cat_order},
                    hover_data={"Count": True, "Pct": True, "Day": True}
                )
                fig_md.update_layout(barmode="stack", yaxis=dict(title="%", range=[0, 100]))
                st.plotly_chart(fig_md, use_container_width=True)

            # --- Final Sample chart ---
            if not fs_data.empty:
                st.subheader("Final Sample dE Breakdown")
                fig_fs = px.bar(
                    fs_data,
                    x="Day",
                    y="Pct",
                    color="FS_dE_Category",
                    text="Label",
                    category_orders={"FS_dE_Category": cat_order},
                    hover_data={"Count": True, "Pct": True, "Day": True}
                )
                fig_fs.update_layout(barmode="stack", yaxis=dict(title="%", range=[0, 100]))
                st.plotly_chart(fig_fs, use_container_width=True)

            # --- Number of Adds ---
            if not add_data.empty:
                st.subheader("Number of Adds")
                add_data = add_data.sort_values(["Day", "Pct"], ascending=[True, False])
                cat_order_add = (
                    add_data.groupby("Number of add")["Pct"]
                    .mean()
                    .sort_values(ascending=False)
                    .index.tolist()
                )
                if 0 not in cat_order_add:
                    cat_order_add = [0] + cat_order_add

                fig_add = px.bar(
                    add_data,
                    x="Day",
                    y="Pct",
                    color="Number of add",
                    text="Label",
                    category_orders={"Number of add": cat_order_add},
                    hover_data={"Count": True, "Pct": True, "Day": True}
                )
                fig_add.update_layout(barmode="stack", yaxis=dict(title="%", range=[0, 100]))
                st.plotly_chart(fig_add, use_container_width=True)

            # --- Reason for No SM add taken ---
            if "Reason for No SM add taken" in df_vis.columns and not df_vis.empty:
                st.subheader("Reason for No SM add taken (Final Sample % Distribution)")
                reason_fs_data = (
                    df_vis.groupby(["Day", "Reason for No SM add taken"], as_index=False)["FS-count"]
                    .sum()
                    .rename(columns={"FS-count": "Count"})
                )
                reason_fs_data["Pct"] = (
                    reason_fs_data["Count"] /
                    reason_fs_data.groupby("Day")["Count"].transform("sum") * 100
                )

                if not reason_fs_data.empty:
                    fig_reason = px.bar(
                        reason_fs_data,
                        x="Day",
                        y="Pct",
                        color="Reason for No SM add taken",
                        title="Reason for No SM add taken (FS-count % by Day)",
                        labels={"Pct": "% of FS-count", "Count": "Final Sample Count"},
                        hover_data={"Day": True, "Count": True, "Pct": True},
                        text=reason_fs_data["Pct"].round(1).astype(str) + "%"
                    )
                    fig_reason.update_layout(barmode="stack", yaxis=dict(title="%", range=[0, 100]))
                    fig_reason.update_traces(textposition="inside")
                    st.plotly_chart(fig_reason, use_container_width=True)

            # --- Total Batch Breakdown ---
            if "Reason for No SM add taken" in df_vis.columns and not df_vis.empty:
                st.subheader("📊 Total Batch Breakdown (% per Day)")
                breakdown_data = df_vis.copy()
                breakdown_data["Category"] = breakdown_data["Reason for No SM add taken"].apply(
                    lambda x: "RFT Measure" if str(x).strip() == "RFT"
                    else "SM Add Taken" if (pd.isna(x) or str(x).strip() in ["", "0"])
                    else "SM Add Not Taken"
                )
                breakdown_counts = (
                    breakdown_data.groupby(["Day", "Category"])
                    .size()
                    .reset_index(name="Count")
                )
                total_per_day = breakdown_counts.groupby("Day")["Count"].transform("sum")
                breakdown_counts["Percentage"] = (breakdown_counts["Count"] / total_per_day) * 100

                fig_breakdown = px.bar(
                    breakdown_counts,
                    x="Day",
                    y="Percentage",
                    color="Category",
                    text=breakdown_counts["Percentage"].apply(lambda x: f"{x:.1f}%"),
                    hover_data={"Count": True, "Percentage": ':.1f'}
                )
                fig_breakdown.update_layout(barmode="stack", yaxis=dict(ticksuffix="%"))
                st.plotly_chart(fig_breakdown, use_container_width=True)

            # --- FS-count Line Chart ---
            if "FS-count" in df_vis.columns and not df_vis.empty:
                st.subheader("📉 Measurable vs Unmeasurable, %")
                fs_counts = (
                    df_vis.groupby(["Day", "FS-count"])
                    .size()
                    .reset_index(name="Count")
                )
                fs_counts["Total"] = fs_counts.groupby("Day")["Count"].transform("sum")
                fs_counts["Pct"] = (fs_counts["Count"] / fs_counts["Total"] * 100).round(2)
                fs_counts["FS-label"] = fs_counts["FS-count"].map({
                    0: "Unmeasurable",
                    1: "Measurable"
                })
                fig_fs_line = px.line(
                    fs_counts,
                    x="Day",
                    y="Pct",
                    color="FS-label",
                    markers=True,
                    labels={"Pct": "Percentage", "FS-label": "FS-count Type"},
                    hover_data={"Day": True, "Pct": ':.1f', "Count": True, "Total": False}
                )
                fig_fs_line.update_traces(mode="lines+markers")
                fig_fs_line.update_layout(yaxis=dict(title="%", range=[0, 100]))
                st.plotly_chart(fig_fs_line, use_container_width=True)

                # --- FS-count and MD-count Line Chart ---
        if {"FS-count", "MD-count"}.issubset(df_vis.columns) and not df_vis.empty:
           st.subheader("📈 Final Sample counts vs Main Dye Sample counts per Day")
    
           # Aggregate counts per day
           day_counts = df_vis.groupby("Day")[["FS-count", "MD-count"]].sum().reset_index()
    
           # Melt for plotly
        day_counts_melted = day_counts.melt(id_vars="Day", value_vars=["FS-count", "MD-count"],
                                        var_name="Type", value_name="Count")
    
           # Plot line chart
        fig_line = px.line(
                  day_counts_melted,
                  x="Day",
                  y="Count",
                  color="Type",
                  markers=True,
                  labels={"Count": "Daily Count", "Day": "Day of Month", "Type": "Measurement"}
            )
    
        fig_line.update_traces(mode="lines+markers")
        st.plotly_chart(fig_line, use_container_width=True)


        # -------------------------------
        # 🔹 Final Output
        # -------------------------------
        st.markdown("---")
        #st.success("✅ ExD file enriched with all data")
        

        st.success("✅ Data processed successfully!")
        with st.expander("📋 View Processed Data"):
            st.dataframe(exd_df)

        # Download final file
        output_file = "Modified_ExD.xlsx"
        exd_df.to_excel(output_file, index=False)
        with open(output_file, "rb") as f:
            st.download_button("📥 Download Modified ExD File", f, file_name=output_file, type="primary")
    else:
        st.info("📋 Please upload all required Excel files to proceed with data integration.")

        

def main():
    if st.session_state.authenticated:
        main_application()
    else:
        login_screen()

if __name__ == "__main__":
    main()




