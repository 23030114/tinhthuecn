import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="App Tính Thuế TNCN Việt Nam 2026",
    page_icon="💰",
    layout="centered"
)

# Logo (nếu có file logo.jpg cùng thư mục)
try:
    st.image("tải xuống (3).jpg", width=200)
except:
    pass

# Tiêu đề
st.markdown("### 📝 TRẦN THI PHƯƠNG OANH ")
st.title("💰 Ứng Dụng Tính Thuế Thu Nhập Cá Nhân")
st.write("Cập nhật Lương, Thưởng, Tăng ca và Phụ cấp theo mô hình tính thuế năm 2026")

st.divider()

# Nhập dữ liệu
st.subheader("📋 Nhập thông tin thu nhập")

gross_salary = st.number_input(
    "1. Lương đóng BHXH (VND)",
    min_value=0,
    value=30000000,
    step=500000
)

gross_bonus_pay = st.number_input(
    "2. Tiền thưởng / Bonus (VND)",
    min_value=0,
    value=0,
    step=500000
)

overtime_pay = st.number_input(
    "3. Tiền tăng ca / làm thêm giờ (VND)",
    min_value=0,
    value=0,
    step=500000
)

st.markdown("**4. Các khoản phụ cấp nhận bằng tiền mặt**")

col1, col2 = st.columns(2)

with col1:
    lunch_allowance = st.number_input(
        "Phụ cấp ăn trưa (VND)",
        min_value=0,
        value=0,
        step=50000
    )

with col2:
    other_allowance = st.number_input(
        "Phụ cấp điện thoại, xăng xe (VND)",
        min_value=0,
        value=0,
        step=50000
    )

dependents = st.number_input(
    "5. Số người phụ thuộc",
    min_value=0,
    value=1,
    step=1
)

st.divider()


# Hàm tính thuế
def tinh_thue_tncn(gross, bonus, overtime, lunch, other, deps):

    total_income = gross + bonus + overtime + lunch + other

    # Bảo hiểm
    bhxh = gross * 0.08
    bhyt = gross * 0.015
    bhtn = gross * 0.01

    total_insurance = bhxh + bhyt + bhtn

    # Giảm trừ
    self_reduction = 15_500_000
    dependent_reduction = deps * 6_200_000

    total_reduction = self_reduction + dependent_reduction

    # Khoản miễn thuế
    exempt_lunch = min(lunch, 730000)
    exempt_allowance = other

    total_exempt_income = (
        overtime +
        exempt_lunch +
        exempt_allowance
    )

    # Thu nhập tính thuế
    assessable_income = max(
        0,
        total_income
        - total_exempt_income
        - total_insurance
        - total_reduction
    )

    # Biểu thuế lũy tiến
    brackets = [
        (10_000_000, 0.05, "Bậc 1: Đến 10 triệu đồng (5%)"),
        (30_000_000, 0.10, "Bậc 2: Trên 10 đến 30 triệu đồng (10%)"),
        (60_000_000, 0.20, "Bậc 3: Trên 30 đến 60 triệu đồng (20%)"),
        (100_000_000, 0.30, "Bậc 4: Trên 60 đến 100 triệu đồng (30%)"),
        (float("inf"), 0.35, "Bậc 5: Trên 100 triệu đồng (35%)")
    ]

    tax = 0
    previous_limit = 0
    temp_income = assessable_income
    tax_breakdown = []

    for limit, rate, desc in brackets:

        if temp_income <= 0:
            break

        range_size = limit - previous_limit
        taxable_amount = min(temp_income, range_size)

        tax_in_bracket = taxable_amount * rate

        tax += tax_in_bracket

        tax_breakdown.append({
            "Bậc thuế": desc,
            "Thu nhập tính thuế": f"{taxable_amount:,.0f} VND",
            "Thuế phải nộp": f"{tax_in_bracket:,.0f} VND"
        })

        temp_income -= taxable_amount
        previous_limit = limit

    net_salary = total_income - total_insurance - tax

    return {
        "total_income": total_income,
        "bhxh": bhxh,
        "bhyt": bhyt,
        "bhtn": bhtn,
        "total_insurance": total_insurance,
        "dependent_reduction": dependent_reduction,
        "exempt_lunch": exempt_lunch,
        "exempt_allowance": exempt_allowance,
        "assessable_income": assessable_income,
        "tax": tax,
        "net_salary": net_salary,
        "tax_breakdown": tax_breakdown
    }


# Nút tính toán
if st.button("🧮 Tính Thuế & Nhận Kết Quả", type="primary"):

    res = tinh_thue_tncn(
        gross_salary,
        gross_bonus_pay,
        overtime_pay,
        lunch_allowance,
        other_allowance,
        dependents
    )

    st.divider()

    st.subheader("🎯 Kết Quả Tóm Tắt")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tổng thu nhập",
            f"{res['total_income']:,.0f} VND"
        )

        st.metric(
            "Tổng bảo hiểm",
            f"{res['total_insurance']:,.0f} VND"
        )

    with col2:
        st.metric(
            "Thuế TNCN",
            f"{res['tax']:,.0f} VND"
        )

        st.metric(
            "Thực nhận (NET)",
            f"{res['net_salary']:,.0f} VND"
        )

    st.divider()

    st.subheader("📜 Giải trình chi tiết")

    st.markdown(f"""
- **Tổng thu nhập:** {res['total_income']:,.0f} VND
- **BHXH:** {res['bhxh']:,.0f} VND
- **BHYT:** {res['bhyt']:,.0f} VND
- **BHTN:** {res['bhtn']:,.0f} VND
- **Tổng bảo hiểm:** {res['total_insurance']:,.0f} VND

- **Tiền tăng ca miễn thuế:** {overtime_pay:,.0f} VND
- **Tiền ăn trưa miễn thuế:** {res['exempt_lunch']:,.0f} VND
- **Phụ cấp miễn thuế:** {res['exempt_allowance']:,.0f} VND

- **Giảm trừ bản thân:** 15,500,000 VND
- **Giảm trừ người phụ thuộc:** {res['dependent_reduction']:,.0f} VND

- **Thu nhập tính thuế:** {res['assessable_income']:,.0f} VND
""")

    if res["tax"] > 0:
        st.subheader("📊 Chi tiết các bậc thuế")
        st.table(res["tax_breakdown"])
    else:
        st.success(
            "Thu nhập tính thuế bằng 0 nên không phát sinh thuế TNCN."
        )
