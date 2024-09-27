import requests
import sseclient
import streamlit as st
import uuid

from streamlit_scripts.utils import base_request_url, generate_task_id, key_dict


st.title("LinkedIn outreach scripts")


def reset_inputs():
    st.session_state["li_at"] = ""
    st.session_state["spreadsheet_url"] = ""
    st.session_state["sheet_name"] = ""
    st.session_state["waiting_time_min"] = "5"
    st.session_state["waiting_time_max"] = "10"
    st.session_state["column_name"] = ""
    st.session_state["result_column_name"] = ""
    st.session_state["action"] = "Select action"
    st.session_state["invitation_id_column_name"] = ""
    st.session_state["invitation_shared_secret_column_name"] = ""
    st.session_state["vmid_column_name"] = ""
    st.session_state["message_column_name"] = ""
    st.session_state["conversation_id_column_name"] = ""
    st.session_state["unique_identifier_column_name"] = ""


def execute_progress_bar(payload):
    response = requests.post(
        f"{base_request_url}/linkedin_scripts/linkedin_outreach_scripts", json=payload)
    if response.status_code == 200:
        st.success(f"Task ID: {task_id}")
        sse_url = f"{base_request_url}/progress_stream/{task_id}"
        progress_bar = st.progress(0)
        messages = sseclient.SSEClient(sse_url)
        for msg in messages:
            if msg.data and msg.data.strip().isdigit():
                progress = int(msg.data)
                progress_bar.progress(progress)
                if progress == 100:
                    st.success("Outreach completed!")
                    break
            else:
                st.error(f"Invalid progress data: {msg.data}")
    else:
        st.error(f"Failed to start task. Status code: {response.status_code}")


def execute_script_without_progress_bar(payload):
    response = requests.post(
        f"{base_request_url}/linkedin_scripts/linkedin_outreach_scripts", json=payload)
    st.success(f"Task ID: {task_id}")
    if response.status_code == 200:
        sse_url = f"{base_request_url}/progress_stream/{task_id}"
        messages = sseclient.SSEClient(sse_url)
        for msg in messages:
            if msg.data and msg.data.strip().isdigit():
                progress = int(msg.data)
                if progress == 100:
                    st.success("Outreach completed!")
                    break
            else:
                st.error(f"Invalid progress data: {msg.data}")


if "previous_option" not in st.session_state:
    st.session_state["previous_option"] = "Select one LinkedIn outreach script"
linkedin_outreach_option = st.selectbox(
    "Select one LinkedIn outreach script",
    ("Select one LinkedIn outreach script",
     "Obtain the current user profile",
     "Get all connections",
     "Get all connection requests",
     "Get all sent connection requests",
     "Get the last 20 conversations",
     "Get all conversations with connections",
     "Get all messages from conversations",
     "Mark as seen conversations",
     "Remove connections",
     "Accept or ignore connection requests",
     "Withdraw connection requests",
     "Follow or unfollow leads (must be a connection)",
     "Send connection requests",
     "Send message",
     )
)
if linkedin_outreach_option != st.session_state["previous_option"]:
    reset_inputs()
st.session_state["previous_option"] = linkedin_outreach_option
if linkedin_outreach_option != "Select one LinkedIn outreach script":
    st.write("Before executing any script, please ensure that you share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com")
if linkedin_outreach_option == "Obtain the current user profile":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the information will be printed)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the information will be printed)", key="sheet_name")
if linkedin_outreach_option == "Get all connections":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the connections will be printed)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the connections will be printed)", key="sheet_name")
if linkedin_outreach_option == "Get all connection requests":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the connection requests will be printed)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the connection requests will be printed)", key="sheet_name")
if linkedin_outreach_option == "Get all sent connection requests":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the sent connection requests will be printed)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the sent connection requests will be printed)", key="sheet_name")
if linkedin_outreach_option == "Get the last 20 conversations":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the conversations will be printed)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the conversations will be printed)", key="sheet_name")
if linkedin_outreach_option == "Get all conversations with connections":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the conversations with connections will be printed)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the conversations with connections will be printed)", key="sheet_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each conversation id lookup)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each conversation id lookup)", "10", key="waiting_time_max"))
if linkedin_outreach_option == "Get all messages from conversations":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the conversation ids are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the conversation ids are located)", key="sheet_name")
    conversation_id_column_name = st.text_input(
        "Column name (Name of the column where all the conversation ids are located)", key="conversation_id_column_name")
if linkedin_outreach_option == "Mark as seen conversations":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the conversation ids are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the conversation ids are located)", key="sheet_name")
    conversation_id_column_name = st.text_input(
        "Column name (Name of the column where all the conversation ids are located)", key="conversation_id_column_name")
    result_column_name = st.text_input(
        "Result column name (Name of the column where all the results will be printed)", key="result_column_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each conversation marked as seen)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each conversation marked as seen)", "10", key="waiting_time_max"))
if linkedin_outreach_option == "Remove connections":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the vmids or universal names are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the vmids or universal names are located)", key="sheet_name")
    unique_identifier_column_name = st.text_input(
        "Column name (Name of the column where all the vmids or universal names are located)", key="unique_identifier_column_name")
    result_column_name = st.text_input(
        "Result column name (Name of the column where all the results will be printed)", key="result_column_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each connection removed)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each connection removed)", "10", key="waiting_time_max"))
if linkedin_outreach_option == "Accept or ignore connection requests":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the invitation ids and invitation shared secrets are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the invitation ids and invitation shared secrets are located)", key="sheet_name")
    action = st.selectbox("Action (Select 'accept' to accept all connection requests or 'ignore' to ignore them)", options=[
                          "accept", "ignore"], key="action")
    invitation_id_column_name = st.text_input(
        "Invitation id column name (Name of the column where all the invitation ids are located)", key="invitation_id_column_name")
    invitation_shared_secret_column_name = st.text_input(
        "Invitation shared secret column name (Name of the column where all the invitation shared secrets are located)", key="invitation_shared_secret_column_name")
    result_column_name = st.text_input(
        "Result column name (Name of the column where all the results will be printed)", key="result_column_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each connection request accepted/ignored)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each connection request accepted/ignored)", "10", key="waiting_time_max"))
if linkedin_outreach_option == "Withdraw connection requests":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the invitation ids are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the invitation ids are located)", key="sheet_name")
    invitation_id_column_name = st.text_input(
        "Column name (Name of the column where all the invitation ids are located)", key="invitation_id_column_name")
    result_column_name = st.text_input(
        "Result column name (Name of the column where all the results will be printed)", key="result_column_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each connection request withdrawed)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each connection request withdrawed)", "10", key="waiting_time_max"))
if linkedin_outreach_option == "Follow or unfollow leads (must be a connection)":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the vmids are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the vmids are located)", key="sheet_name")
    action = st.selectbox("Action (Select 'follow' to follow all profiles or 'unfollow' to unfollow them)", options=[
                          "follow", "unfollow"], key="action")
    vmid_column_name = st.text_input(
        "Vmid column name (Name of the column where all the vmids are located)", key="vmid_column_name")
    result_column_name = st.text_input(
        "Result column name (Name of the column where all the results will be printed)", key="result_column_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each connection request accepted/ignored)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each connection request accepted/ignored)", "10", key="waiting_time_max"))
if linkedin_outreach_option == "Send connection requests":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the vmids and messages are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the vmids and messages are located)", key="sheet_name")
    vmid_column_name = st.text_input(
        "Vmid column name (Name of the column where all the vmids are located)", key="vmid_column_name")
    message_column_name = st.text_input(
        "Message column name (Name of the column where all the messages are located)", key="message_column_name")
    result_column_name = st.text_input(
        "Result column name (Name of the column where all the results will be printed)", key="result_column_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each connection request sent)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each connection request sent)", "10", key="waiting_time_max"))
if linkedin_outreach_option == "Send message":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where all the vmids and messages are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where all the vmids and messages are located)", key="sheet_name")
    vmid_column_name = st.text_input(
        "Vmid column name (Name of the column where all the vmids are located)", key="vmid_column_name")
    message_column_name = st.text_input(
        "Message column name (Name of the column where all the messages are located, max 300 characters for Sales Navigator, 200 otherwise)", key="message_column_name")
    result_column_name = st.text_input(
        "Result column name (Name of the column where all the results will be printed)", key="result_column_name")
    waiting_time_min = int(st.text_input(
        "Minimum waiting time (Minimum waiting time in seconds for each message sent)", "5", key="waiting_time_min"))
    waiting_time_max = int(st.text_input(
        "Maximum waiting time (Maximum waiting time in seconds for each message sent)", "10", key="waiting_time_max"))

if linkedin_outreach_option != "Select one LinkedIn outreach script":
    if st.button("Start outreach"):
        if not li_at:
            st.error("Please fill li_at.")
        if not spreadsheet_url:
            st.error("Please fill spreadsheet URL.")
        if li_at and spreadsheet_url:
            try:
                task_id = generate_task_id()
                if linkedin_outreach_option == "Get the last 20 conversations":
                    script_type = "get_last_20_conversations"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Get all messages from conversations":
                    script_type = "get_all_messages_from_conversation"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "conversation_id_column_name": conversation_id_column_name,
                        "script_type": script_type,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Obtain the current user profile":
                    script_type = "obtain_current_user_profile"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_script_without_progress_bar(payload)
                if linkedin_outreach_option == "Send message":
                    script_type = 'send_message_using_vmid'
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "vmid_column_name": vmid_column_name,
                        "message_column_name": message_column_name,
                        "result_column_name": result_column_name,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Mark as seen conversation":
                    script_type = 'mark_conversation_as_seen_using_conversation_id'
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "conversation_id_column_name": conversation_id_column_name,
                        "result_column_name": result_column_name,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Get all connection requests":
                    script_type = "get_all_connection_requests"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Accept or ignore connection requests":
                    script_type = "accept_or_remove_connection_requests"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "action": action,
                        "invitation_id_column_name": invitation_id_column_name,
                        "invitation_shared_secret_column_name": invitation_shared_secret_column_name,
                        "result_column_name": result_column_name,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Send connection requests":
                    script_type = 'send_connection_requests'
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "vmid_column_name": vmid_column_name,
                        "message_column_name": message_column_name,
                        "result_column_name": result_column_name,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Remove connections":
                    script_type = 'remove_connections'
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "unique_identifier_column_name": unique_identifier_column_name,
                        "result_column_name": result_column_name,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Follow or unfollow leads (must be a connection)":
                    script_type = "follow_or_unfollow_profiles"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "action": action,
                        "vmid_column_name": vmid_column_name,
                        "result_column_name": result_column_name,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Get all connections":
                    script_type = "get_all_connections_profiles"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Get all conversations with connections":
                    script_type = "get_all_conversations_with_connections"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Get all sent connection requests":
                    script_type = "get_all_sent_connection_requests"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_outreach_option == "Withdraw connection requests":
                    script_type = "withdraw_connection_requests"
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "invitation_id_column_name": invitation_id_column_name,
                        "result_column_name": result_column_name,
                        "waiting_time_min": waiting_time_min,
                        "waiting_time_max": waiting_time_max,
                        "script_type": script_type,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)