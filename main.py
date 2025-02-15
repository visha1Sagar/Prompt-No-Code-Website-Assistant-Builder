import gradio as gr
import psycopg2

from document_loader import process_documents_and_create_db


def test_sql_connection(host, database, username, password):
    """Tests SQL database connection."""
    try:
        conn = psycopg2.connect(host=host, database=database, user=username, password=password)
        conn.close()
        return "SQL Connection Successful!"
    except psycopg2.Error as e:
        return f"SQL Connection Failed: {e}"
    except Exception as e:
        return f"Error testing SQL Connection: {e}"

def chatbot_response(query):
    """Dummy chatbot response."""

    return f"Chatbot Response: You asked - '{query}'. (Placeholder response.)"


def process_configuration(website_url, files):
    """
    Processes website URL and documents based on user configuration.
    """
    status_messages = ""
    if website_url:
        status_messages += "Website URL is there!\n"
        print("Website URL is there!: ", website_url) # Print to console for backend log

    if files:
        status_messages += "Documents uploaded. Processing and creating vector database...\n"
        print("Documents uploaded. Processing and creating vector database...") # Backend log

        vector_db = process_documents_and_create_db(files) # Call document processing function
        if vector_db:
            status_messages += "Vector database created successfully!\n"
            print("Vector database created successfully!") # Backend log
        else:
            status_messages += "Vector database creation failed. Check console for errors.\n"
            print("Vector database creation failed. Check console for errors!") # Backend log
    else:
        status_messages += "No documents uploaded for vector database creation.\n"
        print("No documents uploaded for vector database creation.") # Backend log

    return status_messages # Return status messages to Gradio textbox


with gr.Blocks() as configuration_tab:
    gr.Markdown("## Website & Data Sources Configuration")
    website_link = gr.Textbox(label="Website Link", placeholder="Enter website URL to scrape")
    documents_upload = gr.File(file_types=['.pdf', '.txt'], label="Upload Documents", file_count="multiple")

    gr.Markdown("### SQL Database Connection (Optional)")
    sql_host = gr.Textbox(label="Host", placeholder="SQL Host Address")
    sql_database = gr.Textbox(label="Database Name", placeholder="Database Name")
    sql_username = gr.Textbox(label="Username", placeholder="Username")
    sql_password = gr.Textbox(label="Password", placeholder="Password", type="password")
    sql_connection_output = gr.Textbox(label="SQL Connection Test Result", interactive=False)
    sql_test_button = gr.Button("Test SQL Connection")
    sql_test_button.click(
        test_sql_connection,
        inputs=[sql_host, sql_database, sql_username, sql_password],
        outputs=sql_connection_output
    )

    gr.Markdown("---")

    config_process_button = gr.Button("Process Configuration") # NEW Button
    config_status_output = gr.Textbox(label="Configuration Status", interactive=False) # NEW Output Textbox
    config_process_button.click( # Button click function
        process_configuration,
        inputs=[website_link, documents_upload], # Input components for the function
        outputs=config_status_output # Output component to display status
    )

    gr.Markdown("Further configuration options (LLM Choice, Theme etc.) can be added here.")

with gr.Blocks() as playground_tab:
    gr.Markdown("## Chatbot Playground")
    query_input = gr.Textbox(label="Ask a Question to the Chatbot", placeholder="Type your question here...")
    response_output = gr.Textbox(label="Chatbot Response", interactive=False)
    playground_button = gr.Button("Get Response")
    playground_button.click(
        chatbot_response,
        inputs=query_input,
        outputs=response_output
    )

with gr.Blocks() as demo:
    gr.Markdown("# No-Code AI Website Chatbot Admin Panel")
    gr.TabbedInterface([configuration_tab, playground_tab], tab_names=["Configuration", "Playground"])

if __name__ == "__main__":
    demo.launch()