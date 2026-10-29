
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="KU GPA Calculator",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
}
.sub-title {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 25px;
}
.footer {
    position: fixed;
    bottom: 12px;
    left: 80px;
    right: auto;
    font-size: 13px;
    color: gray;
    z-index: 999;
}
</style>
<div class="main-title">🎓 GPA Calculator</div>
<div class="sub-title">For Karachi University Students</div>
""", unsafe_allow_html=True)

def calculate_gp(marks):
    if marks < 50:
        return 0.0
    elif marks <= 52:
        return 3.0
    elif marks <= 56:
        return 4.2
    elif marks <= 60:
        return 5.4
    elif marks <= 63:
        return 6.0
    elif marks <= 67:
        return 7.2
    elif marks <= 70:
        return 8.4
    elif marks <= 74:
        return 9.0
    elif marks <= 79:
        return 10.2
    elif marks <= 84:
        return 11.4
    return 12.0

def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 85:
        return "A"
    elif marks >= 80:
        return "A-"
    elif marks >= 75:
        return "B+"
    elif marks >= 71:
        return "B"
    elif marks >= 68:
        return "B-"
    elif marks >= 64:
        return "C+"
    elif marks >= 61:
        return "C"
    elif marks >= 57:
        return "C-"
    elif marks >= 53:
        return "D+"
    elif marks >= 50:
        return "D"
    return "F"

def calculate_result(subjects):
    total_gp = sum(
        s["gp"] for s in subjects
    )
    total_credits = sum(
        s["credit_hours"] for s in subjects
    )
    percentage = sum(
        s["marks"] for s in subjects
    ) / len(subjects)

    gpa = (
        total_gp / total_credits
        if total_credits else 0.0
    )

    return gpa, percentage, total_credits

def show_result(subjects, title):
    gpa, percentage, credits = calculate_result(subjects)

    st.subheader(title)

    df = pd.DataFrame(subjects).rename(columns={
        "name": "Subject",
        "marks": "Marks",
        "credit_hours": "Credit Hours",
        "gp": "GP",
        "grade": "Grade"
    })

    st.dataframe(df, use_container_width=True, hide_index=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("GPA", f"{gpa:.2f}")
    c2.metric("Percentage", f"{percentage:.2f}%")
    c3.metric("Total Credit Hours", f"{credits:.1f}")

    return gpa, percentage

def subject_fields(prefix, count):
    subjects = []

    for i in range(count):
        st.markdown(f"**Subject {i + 1}**")
        c1, c2, c3 = st.columns(3)

        with c1:
            name = st.text_input(
                "Subject Name",
                key=f"{prefix}_name_{i}"
            )

        with c2:
            marks = st.number_input(
                "Marks",
                min_value=0.0,
                max_value=100.0,
                value=None,
                step=1.0,
                placeholder="Enter marks",
                key=f"{prefix}_marks_{i}"
            )

        with c3:
            credits = st.number_input(
                "Credit Hours",
                min_value=0.5,
                max_value=10.0,
                value=3.0,
                step=0.5,
                key=f"{prefix}_credits_{i}"
            )

        subjects.append({
            "name": name.strip(),
            "marks": marks,
            "credit_hours": credits
        })

    return subjects

def validate_and_prepare(subjects):
    prepared = []

    for s in subjects:
        if not s["name"]:
            return None, "Please enter all subject names."

        if s["marks"] is None:
            return None, "Please enter marks for every subject."

        prepared.append({
            "name": s["name"],
            "marks": s["marks"],
            "credit_hours": s["credit_hours"],
            "gp": calculate_gp(s["marks"]),
            "grade": calculate_grade(s["marks"])
        })

    return prepared, None

st.divider()

mode = st.radio(
    "Choose Calculation Mode",
    ["Subject-wise", "Semester-wise"],
    horizontal=True
)

st.divider()

if mode == "Subject-wise":
    st.subheader("Subject-wise GPA Calculator")

    count = st.number_input(
        "Number of Subjects",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
        key="subject_count"
    )

    # Count selector is outside the form, so fields update immediately.
    with st.form("subject_form"):
        raw_subjects = subject_fields("single", count)
        submitted = st.form_submit_button(
            "Calculate GPA",
            use_container_width=True
        )

    if submitted:
        subjects, error = validate_and_prepare(raw_subjects)

        if error:
            st.error(error)
        else:
            show_result(subjects, "SUBJECT-WISE RESULT")

else:
    st.subheader("Semester-wise GPA Calculator")

    number_of_semesters = st.number_input(
        "Number of Semesters",
        min_value=1,
        max_value=12,
        value=4,
        step=1,
        key="semester_count"
    )

    # These selectors are outside the form.
    # Changing a subject count immediately refreshes the fields.
    subject_counts = []

    for sem in range(number_of_semesters):
        count = st.number_input(
            f"Number of Subjects in Semester {sem + 1}",
            min_value=1,
            max_value=30,
            value=5,
            step=1,
            key=f"count_sem_{sem}"
        )
        subject_counts.append(count)

    with st.form("semester_form"):
        all_semesters = []

        for sem, count in enumerate(subject_counts):
            st.markdown(f"## Semester {sem + 1}")
            raw_subjects = subject_fields(
                f"sem_{sem}", count
            )
            all_semesters.append(raw_subjects)
            st.divider()

        submitted = st.form_submit_button(
            "Calculate Overall GPA",
            use_container_width=True
        )

    if submitted:
        prepared_semesters = []
        error = None

        for subjects in all_semesters:
            prepared, error = validate_and_prepare(subjects)

            if error:
                break

            prepared_semesters.append(prepared)

        if error:
            st.error(error)
        else:
            st.header("Semester Results")
            all_subjects = []
            summary = []

            for i, subjects in enumerate(prepared_semesters):
                gpa, percentage = show_result(
                    subjects, f"SEMESTER {i + 1} RESULT"
                )

                summary.append({
                    "Semester": f"Semester {i + 1}",
                    "GPA": f"{gpa:.2f}",
                    "Percentage": f"{percentage:.2f}%"
                })

                all_subjects.extend(subjects)
                st.divider()

            st.header("All Semesters Combined Result")
            overall_gpa, overall_percentage = show_result(
                all_subjects, "OVERALL RESULT"
            )

            st.subheader("Semester Summary")
            st.dataframe(
                pd.DataFrame(summary),
                use_container_width=True,
                hide_index=True
            )

            st.success(f"Overall GPA: {overall_gpa:.2f}")
            st.success(
                f"Overall Percentage: {overall_percentage:.2f}%"
            )

st.markdown(
    '<div class="footer">Created by @hammad._.qamar</div>',
    unsafe_allow_html=True
)
