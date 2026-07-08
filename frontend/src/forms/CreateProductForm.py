import streamlit as st
from src.controllers import create_product


def create_form():
    st.markdown('<div class="edit-card">', unsafe_allow_html=True)
    st.subheader("➕ Add New Product")

    with st.form("create_form"):
        f_col1, f_col2, f_col6, f_col7 = st.columns(4)

        title = f_col1.text_input("Product title", placeholder="Enter title...")
        description = f_col2.text_input(
            "Product description", placeholder="Enter description..."
        )
        price = f_col6.text_input("Price", value="0.0")
        discount = f_col7.text_input("Discount", value="0.0")

        uploaded_files = st.file_uploader(
            "Upload product images",
            type=["png", "jpg", "jpeg", "heic", "webp"],
            accept_multiple_files=True,
        )

        f_col3, f_col4, f_col5 = st.columns(3)
        category = f_col3.selectbox(
            "Category", ["clothes", "electronics", "books", "home & garden"]
        )
        stock = f_col4.number_input("Quantity", min_value=0, value=10)

        payload = {
            "title": str(title).strip(),
            "description": str(description).strip(),
            "price": str(price).replace("$", "").strip(),
            "stock": str(stock),
            "category": str(category).lower(),
            "discount": str(discount).replace("$", "").strip(),
        }

        files = []
        if uploaded_files:
            for file in uploaded_files:
                files.append(("images", (file.name, file.getvalue(), file.type)))
        else:
            files = None

        btn_f1, btn_f2, _ = st.columns([1, 1, 3])
        submit_clicked = btn_f1.form_submit_button("Create Product", type="primary")
        cancel_clicked = btn_f2.form_submit_button("Cancel")

        if submit_clicked:
            if not title:
                st.error("Please enter a product title!")
            else:
                with st.spinner("Creating..."):
                    try:
                        response = create_product(payload=payload, files=files)
                        st.success("Product created successfully! 🎉")
                        st.session_state.adding_product = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed sending data to server: {e}")

        if cancel_clicked:
            st.session_state.adding_product = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
