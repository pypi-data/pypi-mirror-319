import json

from pygeai.assistant.rag.endpoints import GET_ASSISTANTS_FROM_PROJECT_V1, GET_ASSISTANT_V1, CREATE_ASSISTANT_V1, \
    UPDATE_ASSISTANT_V1, DELETE_ASSISTANT_V1, GET_DOCUMENTS_V1, DELETE_ALL_DOCUMENTS_V1, RETRIEVE_DOCUMENT_V1, \
    UPLOAD_DOCUMENT_V1, DELETE_DOCUMENT_V1, EXECUTE_QUERY_V1
from pygeai.core.base.clients import BaseClient
import urllib.parse


class RAGAssistantClient(BaseClient):

    def get_url_safe_name(self, name: str) -> str:
        return urllib.parse.quote_plus(name)

    def get_assistants_from_project(self) -> dict:
        response = self.api_service.get(endpoint=GET_ASSISTANTS_FROM_PROJECT_V1)
        result = json.loads(response.content)
        return result

    def get_assistant_data(self, name: str) -> dict:
        endpoint = GET_ASSISTANT_V1.format(name=name)
        response = self.api_service.get(endpoint=endpoint)
        return json.loads(response.content)

    def create_assistant(
            self,
            name: str,
            description: str = None,
            template: str = None,
            search_options: dict = None,
            index_options: dict = None,
            welcome_data: dict = None
    ) -> dict:
        """
        Creates a RAG Assistant with configurable options for search, indexing, and welcome data.

        :param name: str - The name of the RAG assistant (required).
        :param description: str, optional - A description of the RAG assistant's purpose or functionality.
        :param template: str, optional - Name of an existing RAG template to base the configuration on. Defaults to None.
        :param search_options: dict, optional - A dictionary containing search configuration options.
            - "historyCount": int - Number of historical interactions to include in the search context.
            - "llm": A dictionary with LLM configuration:
                - "cache": bool - Whether to enable caching for the LLM.
                - "frequencyPenalty": float - Frequency penalty parameter for LLM responses.
                - "maxTokens": int - Maximum number of tokens for LLM responses.
                - "modelName": str - Name of the LLM model.
                - "n": int - Number of completions to generate per prompt.
                - "presencePenalty": float - Presence penalty parameter for LLM responses.
                - "provider": str - LLM provider.
                - "stream": bool - Whether to enable streaming for LLM responses.
                - "temperature": float - Sampling temperature for LLM responses.
                - "topP": float - Top-p sampling value.
                - "type": str - LLM type, such as "json_object".
                - "verbose": bool - Whether to enable verbose output.
            - "search": A dictionary with search configuration:
                - "k": int - Number of documents to retrieve.
                - "type": str - Search type, e.g., "similarity" or "mmr".
                - "fetchK": int - Number of documents to fetch when using MMR.
                - "lambda": float - Lambda parameter for MMR.
                - "prompt": str - Custom prompt for search.
                - "returnSourceDocuments": bool - Whether to return source documents.
                - "scoreThreshold": float - Minimum score threshold for retrieved documents.
                - "template": str - Template for search.
            - "retriever": A dictionary with retriever configuration:
                - "type": str - Retriever type, e.g., "vectorStore".
                - "searchType": str - Specific search type for retrievers.
                - "step": str - Retrieval step, e.g., "all" or "documents".
                - "prompt": str - Custom retriever prompt.
        :param index_options: dict, optional - A dictionary containing index configuration options.
            - "chunks": Configuration for document chunking:
                - "chunkOverlap": int - Overlap size between chunks in the main document.
                - "chunkSize": int - Size of each chunk in the main document.
            - "useParentDocument": bool - Whether to enable parent-child relationships.
            - "childDocument": Configuration for child documents:
                - "childK": float - Parameter for child document processing.
                - "chunkSize": float - Chunk size for child documents.
                - "chunkOverlap": float - Overlap size between child document chunks.
        :param welcome_data: dict, optional - A dictionary containing welcome data for the assistant.
            - "title": str - Title of the welcome message.
            - "description": str - Description of the welcome message.
            - "features": A list of features:
                - "title": str - Title of the feature.
                - "description": str - Description of the feature.
            - "examplesPrompt": A list of example prompts:
                - "title": str - Title of the example prompt.
                - "description": str - Description of the example prompt.
                - "promptText": str - Text of the example prompt.

        :return: dict - The API response containing details of the created RAG assistant.
    """
        data = {
            "name": name,
            "description": description,
            "template": template,
            "searchOptions": search_options,
            "indexOptions": index_options,
            "welcomeData": welcome_data
        }
        response = self.api_service.post(
            endpoint=CREATE_ASSISTANT_V1,
            data=data
        )
        return json.loads(response.content)

    def update_assistant(
            self,
            name: str,
            status: int,
            description: str = None,
            template: str = None,
            search_options: dict = None,
            welcome_data: dict = None
    ) -> dict:
        safe_name = self.get_url_safe_name(name)
        endpoint = UPDATE_ASSISTANT_V1.format(name=name)

        data = {
            "status": status,
        }
        if description:
            data["description"] = description

        if template:
            data["template"] = template

        if search_options:
            data["searchOptions"] = search_options

        if welcome_data:
            data["welcomeData"] = welcome_data

        response = self.api_service.put(
            endpoint=endpoint,
            data=data
        )
        return json.loads(response.content)

    def delete_assistant(self, name: str) -> dict:
        safe_name = self.get_url_safe_name(name)
        endpoint = DELETE_ASSISTANT_V1.format(name=safe_name)
        response = self.api_service.delete(endpoint=endpoint)
        return json.loads(response.content)

    def get_documents(self, name: str) -> dict:
        safe_name = self.get_url_safe_name(name)
        endpoint = GET_DOCUMENTS_V1.format(name=safe_name)
        response = self.api_service.get(endpoint=endpoint)
        return json.loads(response.content)

    def delete_all_documents(self, name: str) -> dict:
        safe_name = self.get_url_safe_name(name)
        endpoint = DELETE_ALL_DOCUMENTS_V1.format(name=safe_name)
        response = self.api_service.delete(endpoint=endpoint)
        return json.loads(response.content)

    def retrieve_document(self, name: str, document_id: str) -> dict:
        safe_name = self.get_url_safe_name(name)
        endpoint = RETRIEVE_DOCUMENT_V1.format(name=safe_name, id=document_id)
        response = self.api_service.get(endpoint=endpoint)
        return json.loads(response.content)

    def upload_document(self, name: str, document: dict) -> dict:
        safe_name = self.get_url_safe_name(name)
        endpoint = UPLOAD_DOCUMENT_V1.format(name=safe_name)
        response = self.api_service.post(endpoint=endpoint, json=document)
        return json.loads(response.content)

    def delete_document(self, name: str, document_id: str) -> dict:
        safe_name = self.get_url_safe_name(name)
        endpoint = DELETE_DOCUMENT_V1.format(name=safe_name, id=document_id)
        response = self.api_service.delete(endpoint=endpoint)
        return json.loads(response.content)

    def execute_query(self, query: dict) -> dict:
        response = self.api_service.post(endpoint=EXECUTE_QUERY_V1, json=query)
        return json.loads(response.content)

