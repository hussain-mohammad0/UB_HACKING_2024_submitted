import streamlit as st
import sqlite3

conn = sqlite3.connect('donation_data.db')
c = conn.cursor()

c.execute(''' 
    CREATE TABLE IF NOT EXISTS donations (
        need_item TEXT,
        need_quantity INTEGER,
        need_contact TEXT,
        donor_name TEXT,
        donor_item TEXT,
        donor_quantity INTEGER,
        donor_contact TEXT
    )
''')
conn.commit()

st.title("Local Needs & Donations Tracker")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page", ["Home", "Donation Needed", "Donor", "Item Collected"])

if page == "Home":
    st.header("Welcome to the Local Needs & Donations Tracker")
    st.write("This platform helps track local community needs and donations.")
    st.write("Use this platform to either submit a donation or request items you need.")
    st.write("Navigate to the relevant page to make your submission.")

elif page == "Donation Needed":
    st.header("Donation Needed")
    
    need_item = st.text_input("Item Needed", key="need_item_1")
    need_quantity = st.number_input("Quantity Needed", min_value=1, key="need_quantity_2")
    need_contact = st.text_input("Contact Information", key="contact_info_3")

    if st.button("Submit"):
        st.success("✅ Thank you")
        c.execute(''' 
            INSERT INTO donations (need_item, need_quantity, need_contact, donor_name, donor_item, donor_quantity, donor_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (need_item, need_quantity, need_contact, "", "", 0, ""))
        conn.commit()

elif page == "Donor":
    st.header("Donor Information")

    donor_name = st.text_input("Donor's Name", key="donor_name_4")
    donor_item = st.text_input("Item Donated", key="donor_item_5")
    donor_quantity = st.number_input("Quantity Donated", min_value=1, key="donor_quantity_6")
    donor_contact = st.text_input("Donor's Contact", key="donor_contact_7")

    if st.button("Submit"):
        st.success("✅ Thank you for your contribution")
        c.execute(''' 
            INSERT INTO donations (need_item, need_quantity, need_contact, donor_name, donor_item, donor_quantity, donor_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ("", 0, "", donor_name, donor_item, donor_quantity, donor_contact))
        conn.commit()

elif page == "Item Collected":
    st.header("Item Collected")
    
    item_collected = st.text_input("Enter the name of the item collected:")
    quantity_collected = st.number_input("Enter the quantity collected:", min_value=1)

    if st.button("Mark as Collected"):
        c.execute("SELECT need_item, need_quantity FROM donations WHERE need_item = ? AND need_quantity > 0", (item_collected,))
        item = c.fetchone()
        
        if item:
            need_item, need_quantity = item
            
            if quantity_collected >= need_quantity:
                c.execute("DELETE FROM donations WHERE need_item = ?", (item_collected,))
                conn.commit()
                st.success(f"✅ The item '{item_collected}' with quantity {quantity_collected} has been marked as collected and removed.")
            else:
                new_quantity = need_quantity - quantity_collected
                c.execute("UPDATE donations SET need_quantity = ? WHERE need_item = ?", (new_quantity, item_collected))
                conn.commit()
                st.success(f"✅ ")
        else:
            st.error("❌ The item does not exist or has already been fully collected.")

conn.close()
