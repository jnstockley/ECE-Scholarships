import streamlit as st
import pandas as pd
from scholarship_app.utils.output import get_appdata_path


def submit_recommendations(
    user_recommendations_input,
    recommended_scholarship,
    rating_input,
    additional_feedback_input,
    grid_table,
    sharepoint,
):
    """
    Helper function used for processing the scholarship reviews
    Method used to complete the review process by updating local and sharepoint data
    """
    if len(grid_table["selected_rows"]) == 0:
        return False, "Must select students to recommend"
    sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
    new_recommendations = pd.DataFrame(
        columns=["UID", "Scholarship", "Rating", "Additional Feedback"]
    )
    for uid in sel_uids:
        new_recommendation = {
            "UID": uid,
            "Scholarship": recommended_scholarship,
            "Rating": rating_input,
            "Additional Feedback": additional_feedback_input,
        }
        if (
            len(
                user_recommendations_input.loc[
                    (user_recommendations_input["UID"] == uid)
                    & (
                        user_recommendations_input["Scholarship"]
                        == recommended_scholarship
                    )
                ]
            )
            > 0
        ):
            return False, str(
                "Already reviewed student " + str(uid) + " for this scholarship"
            )
        # Check here if students meets requirements of scholarship (Need to wait to merge Austin's PR before these)
        new_recommendations = new_recommendations.append(
            new_recommendation, ignore_index=True
        )
    # Check here for it too many recommendations for that scholarship, should be none if unlimited
    user_recommendations_input = user_recommendations_input.append(new_recommendations)
    user_recommendations_input.to_excel(
        get_appdata_path(f"/data/{sharepoint.get_hawk_id()}_Reviews.xlsx"),
        index=False,
    )

    sharepoint.upload(f"/data/{sharepoint.get_hawk_id()}_Reviews.xlsx", "/data/")

    return True, user_recommendations_input


def submit_review_expander(
    current_scholarship, user_recommendations, grid_table, sharepoint
):
    """
    Expander and form for submitting reviews
    """
    with st.expander("Review Selected Students"):
        if current_scholarship == "None":
            st.error("Must Select a Scholarship to Review For")
        else:
            with st.form("recommendation_form"):
                st.write(f"Review for Scholarship: {current_scholarship}")
                rating = st.selectbox(
                    "Would you recommend these students for this scholarship?",
                    ["Yes", "No", "Maybe"],
                )
                additional_feedback = st.text_area(
                    "Enter any additional feedback on students"
                )
                submit_recommendation = st.form_submit_button("Submit Recommendation")
                if "review_success" in st.session_state:
                    if st.session_state.review_success == "success":
                        st.success("Successfuly submitted recommendations!")
                        st.session_state["review_success"] = None
                    if st.session_state.review_success == "error":
                        st.error(st.session_state.review_result)
                        st.session_state["review_success"] = None
                if submit_recommendation:
                    success, result = submit_recommendations(
                        user_recommendations,
                        current_scholarship,
                        rating,
                        additional_feedback,
                        grid_table,
                        sharepoint,
                    )
                    if success is True:
                        st.session_state.user_recommendations = result
                        st.session_state.review_success = "success"
                        st.experimental_rerun()
                    else:
                        st.session_state.review_success = "error"
                        st.session_state.review_result = result
                        st.experimental_rerun()
