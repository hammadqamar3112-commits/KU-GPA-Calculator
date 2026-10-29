
import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="KU GPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .footer {
        position: fixed;
        bottom: 15px;
        right: 20px;
        font-size: 14px;
        color: gray;
        z-index: 999;
        background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# WEBSITE HEADER
# =========================

st.markdown(
    '<div class="main-title">🎓 GPA Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'For Karachi University Students'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================
# GPA CALCULATION
# =========================

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
    else:
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
    else:
        return "F"

# =========================
# RESULT CALCULATION
# =========================

def calculate_result(subjects):

    total_gp = sum(s["gp"] for s in subjects)

    total_credits = sum(
        s["credit_hours"] for s in subjects
    )

    percentage = sum(
        s["marks"] for s in subjects
    ) / len(subjects)

    gpa = (
        total_gp / total_credits
        if total_credits
        else 0.0
    )

    return gpa, percentage, total_gp, total_credits

# =========================
# RESULT DISPLAY
# =========================

def show_result(subjects, title):

    gpa, percentage, total_gp, total_credits = (
        calculate_result(subjects)
    )

    st.subheader(title)

    df = pd.DataFrame(subjects)

    df = df.rename(
        columns={
            "name": "Subject",
            "marks": "Marks",
            "credit_hours": "Credit Hours",
            "gp": "GP",
            "grade": "Grade"
        }
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "GPA",
            f"{gpa:.2f}"
        )

    with col2:
        st.metric(
            "Percentage",
            f"{percentage:.2f}%"
        )

    with col3:
        st.metric(
            "Total Credit Hours",
            f"{total_credits:.1f}"
        )

    return gpa, percentage

# =========================
# CALCULATION MODE
# =========================

mode = st.radio(
    "Choose Calculation Mode",
    [
        "Subject-wise",
        "Semester-wise"
    ],
    horizontal=True
)

st.divider()

# =========================
# SUBJECT-WISE CALCULATOR
# =========================

if mode == "Subject-wise":

    st.subheader("Subject-wise GPA Calculator")

    number_of_subjects = st.number_input(
        "Number of Subjects",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
        key="subject_count"
    )

    with st.form("subject_form"):

        subjects = []

        for i in range(number_of_subjects):

            st.markdown(
                f"### Subject {i + 1}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                name = st.text_input(
                    "Subject Name",
                    key=f"name_{i}"
                )

            with col2:
                marks = st.number_input(
                    "Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=1.0,
                    key=f"marks_{i}"
                )

            with col3:
                credit_hours = st.number_input(
                    "Credit Hours",
                    min_value=0.5,
                    max_value=10.0,
                    value=3.0,
                    step=0.5,
                    key=f"credits_{i}"
                )

            subjects.append(
                {
                    "name": name,
                    "marks": marks,
                    "credit_hours": credit_hours,
                    "gp": calculate_gp(marks),
                    "grade": calculate_grade(marks)
                }
            )

        submitted = st.form_submit_button(
            "Calculate GPA",
            use_container_width=True
        )

    if submitted:

        if any(
            not subject["name"].strip()
            for subject in subjects
        ):

            st.error(
                "Please enter all subject names."
            )

        else:

            gpa, percentage = show_result(
                subjects,
                "SUBJECT-WISE RESULT"
            )

# =========================
# SEMESTER-WISE CALCULATOR
# =========================

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

    all_semesters = []

    semester_gpas = []
    semester_percentages = []

    with st.form("semester_form"):

        for sem in range(number_of_semesters):

            st.markdown(
                f"## Semester {sem + 1}"
            )

            number_of_subjects = st.number_input(
                f"Number of Subjects in Semester {sem + 1}",
                min_value=1,
                max_value=30,
                value=5,
                step=1,
                key=f"semester_subject_count_{sem}"
            )

            semester_subjects = []

            for i in range(number_of_subjects):

                st.markdown(
                    f"**Subject {i + 1}**"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    name = st.text_input(
                        "Subject Name",
                        key=f"sem_{sem}_name_{i}"
                    )

                with col2:
                    marks = st.number_input(
                        "Marks",
                        min_value=0.0,
                        max_value=100.0,
                        value=0.0,
                        step=1.0,
                        key=f"sem_{sem}_marks_{i}"
                    )

                with col3:
                    credit_hours = st.number_input(
                        "Credit Hours",
                        min_value=0.5,
                        max_value=10.0,
                        value=3.0,
                        step=0.5,
                        key=f"sem_{sem}_credits_{i}"
                    )

                semester_subjects.append(
                    {
                        "name": name,
                        "marks": marks,
                        "credit_hours": credit_hours,
                        "gp": calculate_gp(marks),
                        "grade": calculate_grade(marks)
                    }
                )

            all_semesters.append(
                semester_subjects
            )

            st.divider()

        submitted = st.form_submit_button(
            "Calculate Overall GPA",
            use_container_width=True
        )

    if submitted:

        all_subjects = []

        valid = True

        for subjects in all_semesters:

            if any(
                not subject["name"].strip()
                for subject in subjects
            ):

                valid = False

                break

        if not valid:

            st.error(
                "Please enter all subject names."
            )

        else:

            st.header("Semester Results")

            for sem, subjects in enumerate(
                all_semesters
            ):

                gpa, percentage = show_result(
                    subjects,
                    f"SEMESTER {sem + 1} RESULT"
                )

                semester_gpas.append(gpa)

                semester_percentages.append(
                    percentage
                )

                all_subjects.extend(
                    subjects
                )

                st.divider()

            st.header(
                "All Semesters Combined Result"
            )

            overall_gpa, overall_percentage = (
                show_result(
                    all_subjects,
                    "OVERALL RESULT"
                )
            )

            st.subheader(
                "Semester Summary"
            )

            summary = pd.DataFrame(
                {
                    "Semester": [
                        f"Semester {i + 1}"
                        for i in range(
                            number_of_semesters
                        )
                    ],

                    "GPA": semester_gpas,

                    "Percentage": [
                        f"{p:.2f}%"
                        for p in semester_percentages
                    ]
                }
            )

            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True
            )

            st.success(
                f"Overall GPA: {overall_gpa:.2f}"
            )

            st.success(
                f"Overall Percentage: "
                f"{overall_percentage:.2f}%"
            )

# =========================
# FOOTER
# =========================

st.markdown(
    """
    <div class="footer">
        Created by @hammad._.qamar
    </div>
    """,
    unsafe_allow_html=True
)