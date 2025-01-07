import streamlit as st

from mixedvoices.dashboard.api.client import APIClient
from mixedvoices.dashboard.api.endpoints import (
    project_success_criteria_ep,
    version_recordings_ep,
)


class UploadForm:
    def __init__(self, api_client: APIClient, project_id: str, version: str):
        self.api_client = api_client
        self.project_id = project_id
        self.version = version
        self.success_criteria = self.api_client.fetch_data(
            project_success_criteria_ep(self.project_id)
        )["success_criteria"]

    def render(self) -> None:
        """Render upload form"""
        # Initialize states if not exists
        if "is_uploading" not in st.session_state:
            st.session_state.is_uploading = False
        if "form_key" not in st.session_state:
            st.session_state.form_key = 0
        if "show_success" not in st.session_state:
            st.session_state.show_success = False

        if st.session_state.show_success:
            st.success("Recording queued for processing!")
            st.session_state.show_success = False

        # Create a container for loading status
        status_container = st.empty()

        # File uploader with complete disable during upload
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            key=f"audio_uploader_{st.session_state.form_key}",
            disabled=st.session_state.is_uploading,
            label_visibility=(
                "collapsed" if st.session_state.is_uploading else "visible"
            ),
            accept_multiple_files=False,
        )
        call_status_str = (
            "Call Status (will override auto success criteria):"
            if self.success_criteria
            else "Call Status:"
        )
        success_status = st.radio(
            call_status_str,
            options=["N/A", "Successful", "Unsuccessful"],
            key=f"success_status_{st.session_state.form_key}",
            disabled=st.session_state.is_uploading,
            horizontal=True,
        )

        user_channel = st.radio(
            "User Audio Channel",
            options=["left", "right"],
            key=f"user_channel_{st.session_state.form_key}",
            disabled=st.session_state.is_uploading,
            horizontal=True,
        )

        # Convert selection to boolean or None
        is_successful = {
            "N/A": None,
            "Successful": True,
            "Unsuccessful": False,
        }.get(success_status)

        # Show upload button if file is selected
        if uploaded_file:
            col1, _ = st.columns([1, 3])
            with col1:
                upload_button = st.button(
                    "Upload",
                    key=f"upload_button_{st.session_state.form_key}",
                    disabled=st.session_state.is_uploading,
                )

            if st.session_state.is_uploading:
                with status_container:
                    st.info("Upload in progress...", icon="🔄")

            if upload_button and not st.session_state.is_uploading:
                st.session_state.is_uploading = True
                st.rerun()

            if st.session_state.is_uploading:
                try:
                    files = {"file": uploaded_file}
                    response = self.api_client.post_data(
                        version_recordings_ep(self.project_id, self.version),
                        files=files,
                        params={
                            "is_successful": is_successful,
                            "user_channel": user_channel,
                        },
                    )

                    if response:
                        # Set success flag, increment form key and reset upload state
                        st.session_state.show_success = True
                        st.session_state.is_uploading = False
                        st.session_state.form_key += 1
                        st.rerun()

                except Exception as e:
                    with status_container:
                        st.error(f"Upload failed: {str(e)}")
                    st.session_state.is_uploading = False
                    st.rerun()
