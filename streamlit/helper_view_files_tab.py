import streamlit as st
from helper import get_from_backend
import json


@st.fragment()
def get_view_files_tab(selected_values):
    folders = selected_values if selected_values else []
    for selected_value in folders:
        with st.expander(selected_value):
            with st.popover("Parsed Markdown", icon="📄"):
                backend_method = 's3_interactions/get_markdown_with_images'
                parsed_markdown = get_from_backend(
                    backend_method=backend_method,
                    folder_path=selected_value)
                st.markdown(f"""{parsed_markdown}""",
                            unsafe_allow_html=True)
            with st.popover("Images", icon="🖼️"):
                backend_method = 's3_interactions/get_all_the_images'
                images = get_from_backend(backend_method=backend_method,
                                          folder_path=selected_value)
                images = {k: v for k, v in images.items()}
                for image_name, image_bytes in images.items():
                    st.markdown(f"""## {image_name}

![{image_name}](data:image/{image_name.split('.')[-1]};base64,{image_bytes})

                                """,
                                unsafe_allow_html=True)
            with st.popover("Images To Text", icon="📝"):
                backend_method = \
                    's3_interactions/get_images_explanations_paths'
                images_decriptions_paths = \
                    images = get_from_backend(
                        backend_method=backend_method,
                        folder_path=selected_value)
                if not images_decriptions_paths:
                    st.write("There aren't any images descriptions yet")
                else:
                    option = st.selectbox(
                        f"Choose a prompt for {selected_value}:",
                        images_decriptions_paths
                    )
                    if option:
                        backend_method = \
                            's3_interactions/get_images_explanation'
                        image_description = \
                            get_from_backend(backend_method=backend_method,
                                             folder_path=selected_value,
                                             description_path=option)
                        st.json(json.loads(image_description))
            with st.popover("JSON Parsings", icon="🗂️"):
                backend_method = 's3_interactions/receive_json_parsings_paths'
                json_parsings_paths = \
                    get_from_backend(backend_method=backend_method,
                                     folder_path=selected_value)
                if not json_parsings_paths:
                    st.write("There aren't any parsing JSON yet")
                else:
                    option = st.selectbox(
                        f"Choose a prompt for {selected_value}:",
                        json_parsings_paths
                    )
                    if option:
                        backend_method = \
                            's3_interactions/receive_json_parsings'
                        json_parsings = \
                            get_from_backend(backend_method=backend_method,
                                             folder_path=selected_value,
                                             parsing_path=option)
                        json_parsings = json.loads(json_parsings)
                        st.json(json_parsings)
