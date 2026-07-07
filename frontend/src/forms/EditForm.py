import streamlit as st
from src.controllers import update_product


# Edit Form
def edit_form():
    p = st.session_state.editing_product
    st.markdown('<div class="edit-card">', unsafe_allow_html=True)
    st.subheader(f"Edit Product: {p['title']}")

    with st.form("edit_form"):
        f_col1, f_col2, f_col6, f_col7 = st.columns(4)

        new_title = f_col7.text_input("Product title", value=p["title"])
        new_description = f_col1.text_input(
            "Product description", value=p["description"]
        )

        initial_price = str(p["price"]).replace("$", "")
        initial_discount = str(p["discount"]).replace("$", "")

        new_price = f_col2.text_input("Price", value=initial_price)
        new_discount = f_col6.text_input("Discount", value=initial_discount)

        uploaded_files = st.file_uploader(
            "upload new images",
            type=["png", "jpg", "jpeg", "heic", "webp"],
            accept_multiple_files=True,
        )

        f_col3, f_col4, f_col5 = st.columns(3)
        new_cat = f_col3.selectbox(
            "Category",
            ["clothes", "electronics", "books", "home & garden"],
            index=(
                ["clothes", "electronics", "books", "home & garden"].index(
                    p["category"].lower()
                )
                if p["category"].lower()
                in ["clothes", "electronics", "books", "home & garden"]
                else 0
            ),
        )
        new_stock = f_col4.number_input("Quantity", value=int(p["stock"]))
        new_status = f_col5.selectbox(
            "Status", ["In Stock", "Low Stock", "Out of Stock"]
        )

        payload = {
            "title": str(new_title),
            "description": str(new_description),
            "price": str(new_price).replace("$", "").strip(),
            "stock": str(new_stock),
            "category": str(new_cat).lower(),
            "discount": str(new_discount).replace("$", "").strip(),
        }

        files = []
        if uploaded_files:
            for file in uploaded_files:
                files.append(("images", (file.name, file.getvalue(), file.type)))
        else:
            files = None  
        btn_f1, btn_f2, _ = st.columns([1, 1, 3])

        submit_clicked = btn_f1.form_submit_button("Save Changes", type="primary")
        cancel_clicked = btn_f2.form_submit_button("Cancel")

        if submit_clicked:
            with st.spinner(
                f"uploading images({len(uploaded_files) if uploaded_files else 0})"
            ):
                response = update_product(data=payload, files=files, id=p["id"])

            if response:
                st.success("Product updated sucessfully")
                del st.session_state.editing_product
                st.rerun()

        if cancel_clicked:
            del st.session_state.editing_product
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
