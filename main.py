import gradio as gr
import psycopg2

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


with gr.Blocks() as configuration_tab: # Define Blocks for Configuration tab
    gr.Markdown("## Website & Data Sources Configuration")
    website_link = gr.Textbox(label="Website Link", placeholder="Enter website URL to scrape")
    documents_upload = gr.File(file_types=['.pdf', '.txt'], label="Upload Documents", file_count="multiple")

    gr.Markdown("### SQL Database Connection (Optional)")
    sql_host = gr.Textbox(label="Host", placeholder="SQL Host Address")
    sql_database = gr.Textbox(label="Database Name", placeholder="Database Name")
    sql_username = gr.Textbox(label="Username", placeholder="Username")
    sql_password = gr.Textbox(label="Password", placeholder="Password", type="password")
    sql_connection_output = gr.Textbox(label="Connection Test Result", interactive=False)
    sql_test_button = gr.Button("Test SQL Connection")
    sql_test_button.click(
        test_sql_connection,
        inputs=[sql_host, sql_database, sql_username, sql_password],
        outputs=sql_connection_output
    )

    gr.Markdown("---")
    gr.Markdown("Further configuration options (LLM Choice, Theme etc.) can be added here.")


with gr.Blocks() as playground_tab: # Define Blocks for Playground tab
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
    gr.TabbedInterface([configuration_tab, playground_tab], tab_names=["Configuration", "Playground"]) # Pass Blocks objects

if __name__ == "__main__":
    demo.launch()