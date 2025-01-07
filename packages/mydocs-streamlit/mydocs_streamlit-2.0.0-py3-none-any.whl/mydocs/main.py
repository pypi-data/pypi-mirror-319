import streamlit as st
import os
import json
from functions_value import project_dict

st.markdown('''
    .stAppToolBar{
        display: none
    }

''')

funciton_name = {}
navigation_files = []
project_template = ""
final_response = {}

def run_main():
    PATH_OBJECT = os.path.dirname(__file__)

    with open(f"{PATH_OBJECT}/main.py", "r") as rb:
        lines = rb.readlines()
        lines = lines[:130]

    with open(f"{PATH_OBJECT}/main.py", "w") as rb:
        rb.writelines(lines)

    st.header(project_dict["project_name"], divider="gray")


    def format_files(files, project_template):
        total_files = []
        for file in files:
            file_data = files[file]
            display_name = file_data["display_name"]
            code = file_data["code"]
            file_name = file.strip(".py")

            project_template += f"""
def {file_name}():"""

            project_template += f"""
    with st.expander("Click To View/Hide Code"):
        st.code({code})
            """

            for function_record in file_data["result"]:
                function_name = function_record["function_name"]
                doc_string = function_record["doc_string"]
                # print("type ", type(doc_string))

                if not doc_string:
                    doc_string = '''No Doc String'''

                project_template += f"""
    def {function_name}():
        st.write("{function_name}")
        st.code({json.dumps(doc_string)})
    {function_name}()
                """

            # total_files.append(st.Page(file_name, title=display_name))
            total_files.append({"name": file_name, "display_name": display_name})


        with open(f"{PATH_OBJECT}/main.py", "a") as f:
            f.write(project_template)

        return total_files


    def format_folder(folder, final_response):
        for record in folder:
            single_project = folder[record]

            display_name = single_project["display_name"]
            files = single_project["files"]
            folder = single_project["folder"]

            project_template = ""
            total_files = format_files(files, project_template)

            if display_name not in final_response:
                final_response[display_name] = []

            final_response[display_name].extend(total_files)

            format_folder(folder, final_response)


    

    total_files = format_files(project_dict["files"], project_template)
    format_folder(project_dict["folder"], final_response)

    final_response['others'] = total_files

    # print("final response ", final_response)


    with open(f"{PATH_OBJECT}/main.py", "a") as f:
        function_templates = """
for pages in final_response:
    navigation_files = []
    for page in final_response[pages]:
        func_obj = globals()[page["name"]]
        navigation_files.append(st.Page(func_obj, title=page["display_name"]))

    funciton_name[pages] = [*navigation_files]

pages = st.navigation(funciton_name)
pages.run()
"""
        f.write(function_templates)


    # pg = st.navigation(
    #         {
    #             "Account": [logout_page],
    #             "Reports": [dashboard, bugs, alerts],
    #             "Tools": [search, history],
    #         }
    #     )

if __name__ == "__main__":
    run_main()






## Dynamic Code



