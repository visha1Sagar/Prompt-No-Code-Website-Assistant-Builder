import asyncio
import json
import tempfile

import gradio as gr
import psycopg2
import requests
from langchain_openai import OpenAI
from document_loader import process_documents_and_create_db, load_vector_database, query_vector_database # Import query_vector_database

from new_web import call_crawler
from tree_from_json import  create_tree_from_json, extract_markdowns
from remove_header import remove_header_footer

# --- Load Vector Database (Load when the app starts) ---
vector_db = None # Load vector DB when the app starts. Make vector_db global for now (for simplicity)
if vector_db:
    print("Vector database loaded successfully for Playground!")
else:
    print("Warning: Vector database not loaded. Playground might not function for document queries.")


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

def formulate_answer(query, context_chunks):
    """
    Formulates an answer using OpenAI GPT based on the query and retrieved context chunks.
    """
    if not context_chunks:
        return "I'm sorry, I couldn't find relevant information in the documents for your query."

    context_text = "\n\n".join([chunk.page_content for chunk in context_chunks]) # Join chunks into single context string
    prompt = f"""Answer the question below based on the provided context. Be concise and helpful.

    Question: {query}

    Context:
    {context_text}

    Answer:"""

    try:
        llm = OpenAI() # Requires OPENAI_API_KEY environment variable
        response = llm(prompt)
        return response.strip() # Return GPT answer, removing leading/trailing whitespace
    except Exception as e:
        print(f"Error during answer formulation with OpenAI: {e}")
        return "I encountered an error while trying to formulate an answer. Please try again later."


def chatbot_response(query):
    """
    Handles chatbot query: searches vector DB and formulates response.
    """
    if not vector_db: # Check if vector_db is loaded
        return "Please create and load the document vector database first in the Configuration tab."

    relevant_chunks = query_vector_database(vector_db, query) # Search vector DB using query_vector_database from document_handler

    if relevant_chunks:
        answer = formulate_answer(query, relevant_chunks) # Formulate answer using GPT and retrieved chunks
        return answer
    else:
        return "I'm sorry, I couldn't find relevant information in the documents for your query."


def process_configuration(website_url, files):
    global vector_db
    """
    Processes website URL and documents based on user configuration.
    """
    status_messages = ""
    if website_url:
        status_messages += "Website URL is there!\n"
        print("Website URL is there!: ", website_url) # Print to console for backend log

        try:
            # url = 'https://r.jina.ai/'+website_url
            # headers = {
            #     'X-With-Links-Summary': 'true'
            # }
            #
            # response = requests.get(url, headers=headers)
            # # create .txt file for this
            # temp_file = tempfile.NamedTemporaryFile(mode='w+t', suffix=".txt", delete=False,
            #                                         encoding='utf-8')  # Create temp .txt file
            # temp_file.write(response.text)
            # temp_file.flush()  # Ensure content is written to file
            # temp_file_path = temp_file.name  # Get the file path
            # print(f"Website content saved to temporary file: {temp_file_path}")
            # files.append(temp_file_path)

            asyncio.run(main(website_url))
            remove_header_footer("crawl_results.json")
            create_tree_from_json("crawl_results.json", "tree_output.json")
            data = None
            with open("tree_output.json","r", encoding="utf-8") as file:
                data = json.load(file)
            markdown_text = extract_markdowns(data)

            print("markdown : ", markdown_text)

            with open("scrapped_text.txt", "w",  encoding='utf-8') as file:
                file.write("\n\n".join(markdown_text))

            files.append("scrapped_text.txt")



        except Exception as e:
            return "Error: "+str(e)


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