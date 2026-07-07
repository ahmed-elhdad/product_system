import streamlit as st
import pandas as pd
from src.controllers import get_all_products,update_product

st.set_page_config(page_title="Product Hub - Dashboard", layout="wide")

st.markdown(
    """
    <style>
    /* تنسيق الشريط الجانبي الداكن */
    [data-testid="stSidebar"] {
        background-color: #1a1d23;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: #d1d5db !important;
    }
    
    /* تنسيق الحاويات والبطاقات */
    .stats-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .stat-text {
        font-size: 14px;
        color: #6b7280;
    }
    
    /* تنسيق الـ Badges (الحالات) */
    .badge {
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    .bg-green { background-color: #dcfce7; color: #166534; }
    .bg-red { background-color: #fee2e2; color: #991b1b; }
    .bg-blue { background-color: #e0f2fe; color: #075985; }
    .bg-orange { background-color: #ffedd5; color: #9a3412; }

    /* تنسيق فورم التعديل (المربع الأزرق) */
    .edit-card {
        border: 2px solid #3498db;
        border-radius: 12px;
        padding: 25px;
        background-color: #ffffff;
        margin-top: 20px;
    }
    
    /* أزرار الجدول */
    .stButton>button {
        border-radius: 6px;
        height: 32px;
        padding: 0 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# 4. بناء الشريط الجانبي (Sidebar)
with st.sidebar:
    st.title("Product Hub")
    st.markdown("---")
    st.button("📊 Dashboard", use_container_width=True)
    st.button("📦 Products", use_container_width=True)
    st.button("📁 Categories", use_container_width=True)
    st.button("📈 Analytics", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)

    st.markdown("<br><br><b>FILTER BY CATEGORY</b>", unsafe_allow_html=True)
    st.checkbox("All Products", value=True)
    st.checkbox("Electronics")
    st.checkbox("Clothing")
    st.checkbox("Books")
    st.checkbox("Home & Garden")

# 5. الجزء العلوي (Header)
col_title, col_search, col_add = st.columns([2, 3, 1.2])

with col_title:
    st.header("All Products")

with col_search:
    st.text_input("", placeholder="🔍 Search products...", label_visibility="collapsed")

with col_add:
    if st.button("➕ Add Product", type="primary", use_container_width=True):
        st.toast("Add Product Logic triggered!")

# إحصائيات سريعة
st.markdown(
    """
    <div class="stats-container">
        <span class="stat-text">Total Products: 5</span>
        <span class="stat-text">In Stock: 300</span>
        <span class="stat-text">Low Stock: 12</span>
        <span class="stat-text">Out of Stock: 1</span>
    </div>
""",
    unsafe_allow_html=True,
)

# 6. جدول المنتجات (بناء يدوي ليطابق التصميم)

products = get_all_products()
h1, h2, h3, h4, h5, h6, h7 = st.columns([1, 2, 1.5, 1, 1, 1, 1.5])
# # رؤوس الجدول
h1.write("**Product ID**")
h2.write("**Product title**")
h3.write("**Category**")
h4.write("**Price**")
h5.write("**Quantity**")
h6.write("**Status**")
h7.write("**Actions**")

st.divider()

# عرض الصفوف
for p in products:
    r1, r2, r3, r4, r5, r6, r7 = st.columns([1, 2, 1.5, 1, 1, 1, 1.5])
    r1.write(f"{p['id'][:3]}")
    r2.write(p["title"])

    # تنسيق الـ Badges للفئات والحالة
    cat_color = "bg-blue" if p["category"] == "Electronics" else "bg-orange"
    r3.markdown(
        f'<span class="badge {cat_color}">{p["category"]}</span>',
        unsafe_allow_html=True,
    )

    r4.write(f"${p['price']}")
    r5.write(str(p["stock"]))
    
    status_color = "bg-green" if p["stock"]  >1 else "bg-red"
    status="in stock" if p["stock"]  >1 else "out of stock"
    r6.markdown(
        f'<span class="badge {status_color}">{status}</span>',
        unsafe_allow_html=True,
    )

    # أزرار العمليات
    btn_col1, btn_col2 = r7.columns(2)
    if btn_col1.button("Edit", key=f"edit_{p['id']}"):
        st.session_state.editing_product = p
    if btn_col2.button("Del", key=f"del_{p['id']}"):
        st.error(f"Deleting {p['id']}...")


from src.forms.EditForm import edit_form

if "editing_product" in st.session_state:
    edit_form()