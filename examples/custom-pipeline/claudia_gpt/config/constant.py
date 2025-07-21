"""Module for defining the constant variables.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

import os

from claudia_gpt.api.model.constant import LangId

# Cohere
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
COHERE_MODEL = "rerank-multilingual-v3.0"  # Custom implementation for Claudia

# Databases
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "mariadb")

# Elasticsearch
ELASTICSEARCH_INDEX_NAME = os.getenv("ELASTICSEARCH_INDEX_NAME", "")  # Custom implementation for Claudia

# Help Center Prompt
HELP_CENTER_USE_CASE_SYSTEM_PROMPT = """<system_instruction>
You are Claudia, a virtual assistant dedicated to helping users with topics covered in the **Catapa Help Center**.

Your task is to provide responses that are:
- Accurate (use only the context or Help Center sources provided)
- Empathetic and easy to understand
- In the same language the user uses (English or Indonesian)

Response Guidelines:
1. Tone and Language
  **Language**
     - Respond in the same language the user uses.
     - Maintain language consistency throughout the reply.

  ** Tone**
     - Use a warm, patient, and empathetic tone — especially if the user seems confused.
     - Avoid technical jargon unless it's defined clearly. Use step-by-step explanations.

2. Answering Principles
   **Accuracy & Source Use**
     - Only answer based on Catapa Help Center content from the provided context.
     - Do not rely on keyword matching — always interpret meaning from context.
     - Do not speculate or give personal opinions.
     - Do not invent answers if the information isn’t available.

  **Clarity**
     - Always prioritize interpreting the user's intended meaning, regardless of sentence structure or punctuation.
     - Structure your responses logically.
     - Use bullet points or short paragraphs for readability.
     - Highlight important terms if needed.

   **Citations**
     - Only use links provided in the context.
     - If referencing Help Center articles, always cite using this format:
     ```
     Source:  
     1. [Article Title](URL)
     ```
Citation Format Example:
Source:  
1. [Apa saja keunggulan CATAPA?](https://help.catapa.com/articles/apa-saja-keunggulan-catapa-a3d9bf27-9a07-425e-8087-84015c788236)

3. Off-Topic or Out-of-Scope Questions:
If a user asks something unrelated to Catapa Help Center topics:
- Politely explain your area of expertise.
- Encourage them to ask something related.
- Thank them for their curiosity.

Example:
> Maaf, saya hanya bisa membantu dengan topik yang ada di Catapa Help Center. Tapi terima kasih sudah bertanya — silakan ajukan pertanyaan lain terkait Catapa ya!

4. Handling Ambiguity
   **Unclear Questions**
     - Ask polite follow-up questions to clarify the user's intent.
     - Don’t assume based on partial or vague input.

  **No Available Answer**
     - If no answer is available, say so honestly.
     - Offer the closest relevant topic if one exists.
     - Otherwise, thank the user and encourage a different question.

5. Short Greetings (e.g., "Hi", "Hai Claudia", "How are you?")
    - Recognize short greetings (e.g., "Hi", "Hai Claudia", "How are you?") as valid inputs.
    - These are valid and complete inputs. Do not say the message is incomplete.
    - Instead, respond warmly and cheerfully, like a real person would (e.g., "Hi! How can I help you today? 😊"
    - Then gently invite them to ask a question or let them know you’re here to help with Catapa topics.
6. Formatting Standards
   - Use clean Markdown:
      - Bullets: -
      - Numbered steps: 1., 2.
   - Format math using LaTeX:
      - Inline: $$E = mc^2$$
      - Block:
         $$
         E = mc^2
         $$
</system_instruction>

<step_to_answer>
1. Understanding the Question
   - Ensure you understand the user's request regardless of the sentence structure or punctuation.
   - If unclear, ask follow-up questions politely.
   - Always respond warmly and cheerfully, but maintain professionalism.

2. Processing the Question
 - Match the query to your expertise based on context.
 - If multiple interpretations are possible, clarify first.
 - Never assume based only on keyword matches.

3. Redirecting the Conversation
 - If the user drifts off-topic, steer the conversation back professionally.
</step_to_answer>

<example_question_and_answer>
Example 1:
Q: Hai Claudia
A: Hai! Ada yang bisa saya bantu hari ini?

Example 2:
Q: How are you?  
A: I'm doing great, thanks for asking! How can I help you today?

Example 3:
Q: 1 galon air mineral sekarang berapa ya harganya?  
A: Maaf, saya kurang tahu tentang itu. Namun, saya dapat membantu Anda dengan pertanyaan terkait Catapa Help Center.

Example 4:
Q: Apa saja keunggulan CATAPA?  
A: 
Keunggulan CATAPA antara lain:
- Otomatis menghitung BPJS dan PPh 21
- Terintegrasi dengan Klik BCA Bisnis
- Proses payroll hanya 5 langkah
- Pengajuan karyawan lewat handphone
- Biaya sesuai jumlah karyawan terdaftar

Source:  
1. [Apa saja keunggulan CATAPA?](https://help.catapa.com/articles/apa-saja-keunggulan-catapa-a3d9bf27-9a07-425e-8087-84015c788236)

Example 5:
Q: What is Additional Income?  
A:
Additional income refers to any income employees receive outside their regular salary, such as bonuses or THR. It includes:
- THR/Bonus: Performance or holiday bonuses
- Compensation Pay: Given to PKWT employees when extending contracts
- Other Income: Any other extra earnings

Source:  
1. [What is Additional Income?](https://help.catapa.com/articles/apa-itu-additional-income-penghasilan-tambahan-66e71cc0-5acd-473f-a3c4-afbb6ccbb6d4)
</example_question_and_answer>

<notes>
1. Ensure that all the listed instructions are followed when generating a response to the user.
2. Always be kind, helpful, and focused on the user’s needs.
</notes>

<context>
{context}
</context>"""
HELP_CENTER_USE_CASE_USER_PROMPT = """Below is the user query:
{query}"""

# OpenAI
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # Custom implementation for Claudia


DEFAULT_LANG_ID = LangId.EN

# # Auth
CATAPA_AUTH_KEYSTORE_TYPE = os.getenv("CATAPA_AUTH_KEYSTORE_TYPE", "")
CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PATH = os.getenv("CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PATH", "")
CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PAIR = os.getenv("CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PAIR", "")
CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PASSWORD = os.getenv("CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PASSWORD", "")

# Encryption
CATAPA_ENCRYPTION_KMS_PROVIDER = os.getenv("CATAPA_ENCRYPTION_KMS_PROVIDER", "").lower()
CATAPA_ENCRYPTION_KMS_KEYID = os.getenv("CATAPA_ENCRYPTION_KMS_KEYID", "")
CATAPA_ENCRYPTION_KMS_AWS_REGION = os.getenv("CATAPA_ENCRYPTION_KMS_AWS_REGION", "")
CATAPA_ENCRYPTION_CURRENTKEYID = os.getenv("CATAPA_ENCRYPTION_CURRENTKEYID", "")
CATAPA_ENCRYPTION_KEYS_K1_PASSWORD = os.getenv("CATAPA_ENCRYPTION_KEYS_K1_PASSWORD", "")
CATAPA_ENCRYPTION_KEYS_K1_SALT = os.getenv("CATAPA_ENCRYPTION_KEYS_K1_SALT", "")

# === From GLChat ===

# SQLALCHEMY_LOG_LEVEL = os.getenv("SQLALCHEMY_LOG_LEVEL", "INFO").upper()
# SQLALCHEMY_QUERY_THRESHOLD_IN_MS = float(os.getenv("SQLALCHEMY_QUERY_THRESHOLD_IN_MS", "200"))
# SQLALCHEMY_LOG_FORMAT = os.getenv("SQLALCHEMY_LOG_FORMAT", "default")
# SQLALCHEMY_LOG_ENABLED = os.getenv("SQLALCHEMY_LOG_ENABLED", "false").lower() == "true"

# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
# LOG_FORMAT = os.getenv("LOG_FORMAT", "default")
# DEBUG_STATE = os.getenv("DEBUG_STATE", "false").lower() == "true"
# DEBUG_ENABLED = LOG_LEVEL == "DEBUG"

# BUILD_NUMBER = os.getenv("BUILD_NUMBER", "")
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
# SENTRY_DSN = os.getenv("SENTRY_DSN", "")
# SENTRY_PROJECT = os.getenv("SENTRY_PROJECT", "")
# VERSION_NUMBER = os.getenv("VERSION_NUMBER", "")

DOCPROC_BACKEND_URL = os.getenv("DOCPROC_BACKEND_URL", "http://127.0.0.1:8001")
# VECTOR_DB_CONFIG = os.getenv("VECTOR_DB_CONFIG", "chroma")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "")
# CHROMA_URL = os.getenv("CHROMA_URL", "localhost")
# CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8005"))
# CHROMA_AUTH_TOKEN = os.getenv("CHROMA_AUTH_TOKEN", "")
GLCHAT_DB_URL = os.getenv("GLCHAT_DB_URL", "")
GLCHAT_DB_SCHEMA = os.getenv("GLCHAT_DB_SCHEMA", "")

# # A2A
# A2A_EMAIL_AGENT_URL = os.getenv("A2A_EMAIL_AGENT_URL", "")
# A2A_DEEP_RESEARCH_AGENT_URL = os.getenv("A2A_DEEP_RESEARCH_AGENT_URL", "")

DEFAULT_MODEL = "openai/gpt-4o-mini"
# DEFAULT_VECTORIZER_MODEL = "openai/text-embedding-3-small"
# OPENAI_INFERENCE_MODEL_FOR_AGENT = "gpt-4o"

# # Swirl
# DEFAULT_SWIRL_PROVIDERS = ["53"]
# DEFAULT_WEB_SWIRL_PROVIDERS = ["54"]
# DEFAULT_DISCOVERY_PROVIDERS = ["66"]
# SMART_SEARCH_API_URL = os.getenv("SMART_SEARCH_API_URL", "")
# SMART_SEARCH_API_USER = os.getenv("SMART_SEARCH_API_USER", "")
# SMART_SEARCH_API_SECRET = os.getenv("SMART_SEARCH_API_SECRET", "")

# # Reranker
# DEFAULT_FLAG_EMBEDDING_MODEL = "BAAI/bge-reranker-v2-m3"

# # PII Anonymizer
ENCRYPTION_PASSWORD = os.getenv("ENCRYPTION_PASSWORD", "")
ENCRYPTION_SALT = os.getenv("ENCRYPTION_SALT", "")

# # GSheets Configuration
# SERVICE_ACCOUNT_PRIVATE_KEY = os.getenv("SERVICE_ACCOUNT_PRIVATE_KEY", "")
# SERVICE_ACCOUNT_CLIENT_EMAIL = os.getenv("SERVICE_ACCOUNT_CLIENT_EMAIL", "")
# CONFIG_SHEET_ID = os.getenv("CONFIG_SHEET_ID", "")
# CATALOG_SHEET_ID = os.getenv("CATALOG_SHEET_ID", "")

# # Object Storage
OBJECT_STORAGE_TYPE = os.getenv("OBJECT_STORAGE_TYPE", "minio")
OBJECT_STORAGE_USER = os.getenv("OBJECT_STORAGE_USER", "user")
OBJECT_STORAGE_PASSWORD = os.getenv("OBJECT_STORAGE_PASSWORD", "password")
OBJECT_STORAGE_URL = os.getenv("OBJECT_STORAGE_URL", "127.0.0.1:9000")
OBJECT_STORAGE_BUCKET = os.getenv("OBJECT_STORAGE_BUCKET", "gdplabs-gen-ai-starter")
OBJECT_STORAGE_SECURE = os.getenv("OBJECT_STORAGE_SECURE", "false").lower() == "true"

# # Azure OpenAI Configuration
# AZURE_OPENAI_DEPLOYMENT_NAME_GPT4O = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT4O", "")
# AZURE_OPENAI_DEPLOYMENT_NAME_GPT4O_MINI = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT4O_MINI", "")
# AZURE_OPENAI_DEPLOYMENT_NAME_TEXT_EMBEDDING_3_SMALL = os.getenv(
#     "AZURE_OPENAI_DEPLOYMENT_NAME_TEXT_EMBEDDING_3_SMALL", ""
# )
# AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT", "")
# AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "")
# # API Keys
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
# GOOGLE_GENERATIVE_AI_API_KEY = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
# TEI_API_KEY = os.getenv("TEI_API_KEY", "")
# TGI_API_KEY = os.getenv("TGI_API_KEY", "")
# SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
# VLLM_API_KEY = os.getenv("VLLM_API_KEY", "<EMPTY>")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
# DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY", "")
# CUSTOM_API_KEY = os.getenv("CUSTOM_API_KEY", "")
# BEDROCK_ACCESS_KEY_ID = os.getenv("BEDROCK_ACCESS_KEY_ID", "")
# BEDROCK_SECRET_ACCESS_KEY = os.getenv("BEDROCK_SECRET_ACCESS_KEY", "")

# # whatsapp service api key
# # default to random uuid -> if not set, no one will know the value
# WHATSAPP_SERVICE_API_KEY = os.getenv("WHATSAPP_SERVICE_API_KEY", str(uuid.uuid4()))

# CONVERSATION_TOPIC_MODEL = os.getenv("CONVERSATION_TOPIC_MODEL", "openai/gpt-4o-mini")

# # LM Routing
# SEMANTIC_ROUTER_SAMPLE_PATH = os.getenv(
#     "SEMANTIC_ROUTER_SAMPLE_PATH", "gdplabs_gen_ai_starter_gllm_backend/resources/llm-router-samples"
# )
# # TODO: Make this configurable later. For now, we lock this to OpenAI.
# SEMANTIC_ROUTER_MODEL = os.getenv("SEMANTIC_ROUTER_MODEL", "text-embedding-3-small")

# CUSTOM_PARAMS = os.getenv("CUSTOM_PARAMS", "{}")

DEFAULT_REFERENCE_FORMATTER_THRESHOLD = 0.6
# DEFAULT_REFERENCE_FORMATTER_BATCH_SIZE = 20

# NLP_CONFIGURATION: dict[str, Any] = {
#     "nlp_engine_name": "spacy",
#     "models": [
#         {"lang_code": "en", "model_name": "en_core_web_sm"},
#         {"lang_code": "id", "model_name": "en_core_web_sm"},
#     ],
# }
# NER_API_URL = os.getenv("NER_API_URL", "")
# NER_API_KEY = os.getenv("NER_API_KEY", "")
# HEADER_X_API_KEY_KEY: str = "x-api-key"

# LLM_LABS_BASE_URL = os.getenv("LLM_LABS_BASE_URL", "")
# LLM_LABS_GET_FILE_PATH = os.getenv("LLM_LABS_GET_FILE_PATH", "")
# GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
# TOGETHER_BASE_URL = os.getenv("TOGETHER_BASE_URL", "https://api.together.xyz/v1")
# DEEPINFRA_BASE_URL = os.getenv("DEEPINFRA_BASE_URL", "https://api.deepinfra.com/v1/openai")

# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "password")
# REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
# REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
# REDIS_TLS_ENABLED = os.getenv("REDIS_TLS_ENABLED", "false").lower() == "true"
# REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# GOOGLE_VERTEX_CREDENTIAL_PATH = os.getenv("GOOGLE_VERTEX_AI_CREDENTIAL_PATH", "vertexai_credentials.json")
# KNOWLEDGE_BASE_LLM_LABS_BASE_URL = os.getenv(
#     "KNOWLEDGE_BASE_LLM_LABS_BASE_URL", "[Check your URL configuration]"
# ).rstrip("/")


# class EnvironmentType(StrEnum):
#     """Enum for Environment Type."""

#     DEVELOPMENT = "development"
#     STAGING = "staging"
#     PRODUCTION = "production"


# class WorksheetName:
#     """Worksheet class containing worksheet name constants."""

#     CHATBOT = "chatbot"
#     CHATBOT_MODEL = "chatbot_model"
#     KNOWLEDGE_BASE = "knowledge_base"
#     MODEL = "model"
#     MODEL_GROUP = "model_group"
#     PRESET_PREFIX = "preset-"
#     PRESET_DPO_PREFIX = "preset-dpo-"
#     USER_CHATBOT = "user_chatbot"
#     VECTOR_STORE = "vector_store"


# # client type
# class ClientType(StrEnum):
#     """Client type enum.

#     Attributes:
#         DEFAULT (str): Default client type.
#         WHATSAPP (str): WhatsApp client type.
#     """

#     DEFAULT = "default"
#     WHATSAPP = "whatsapp"


# DEFAULT_CLIENT_TYPE = ClientType.DEFAULT
# API_KEY_CLIENT_TYPE_MAP = {
#     WHATSAPP_SERVICE_API_KEY: ClientType.WHATSAPP,
# }

# # additional instructions
# USE_MODEL_KNOWLEDGE_ADDITIONAL_INSTRUCTIONS = (
#     "\nIf context is provided and relevant to the question, "
#     "you may only answer based on the knowledge provided through one of the context options."
#     "\nIf no context is provided, or the context is irrelevant to the question, "
#     "use your knowledge to answer the question.\n\n"
# )

# DONT_USE_MODEL_KNOWLEDGE_ADDITIONAL_INSTRUCTIONS = (
#     "\nYou may only answer based on the knowledge provided through one of the context options."
#     "\nIf no context is provided, or the context is irrelevant to the question, "
#     "state that you don't have the knowledge to answer the question, "
#     "then ask the user to ask a question that you have the knowledge of.\n\n"
# )

# WHATSAPP_ADDITIONAL_INSTRUCTIONS = (
#     "\nUse a casual, concise, and easy-to-understand tone, similar to how people chat on WhatsApp. "
#     "Avoid sentences that are too long or overly formal. If appropriate, use emojis sparingly to "
#     "create a friendly impression (when the context fits). Avoid lengthy explanations — focus on "
#     "the core of the answer. If clarification is needed, ask politely but keep it light.\n\n"
# )

# CLIENT_TYPE_ADDITIONAL_INSTRUCTION = {ClientType.WHATSAPP: WHATSAPP_ADDITIONAL_INSTRUCTIONS}

# # Swirl
# # GDP Internal Knowledge - https://stag-swirl.obrol.id/admin/swirl/searchprovider/53/change/
# SEARCH_PROVIDERS_INTERNAL_KNOWLEDGE_DEFAULT = '{"54": "web"}'
# # Google Serper - https://stag-swirl.obrol.id/admin/swirl/searchprovider/54/change/
# SEARCH_PROVIDERS_WEB_DEFAULT = '{"54": "web"}'
# SEARCH_PROVIDERS_AUTOSUGGEST_DEFAULT = "{}"
# SEARCH_PROVIDERS_SHINGLE_DEFAULT = "{}"
# SEARCH_PROVIDERS_DISCOVERY_DEFAULT = "{}"


# WEB_SEARCH_WHITELIST_DEFAULT = "[]"
# WEB_SEARCH_BLACKLIST_DEFAULT = "[]"

# SWIRL_HTTP_ERROR_LOG_MESSAGE = "HTTP error: %s - %s"

# DEFAULT_LANG_ID = LangId.EN

# # Auth config
# SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "$ample$ecret")
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234")
# JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
# AUTO_CREATE_USER = os.getenv("AUTO_CREATE_USER", "true").lower() == "true"
# LINK_USER_PROVIDER = os.getenv("LINK_USER_PROVIDER", "true").lower() == "true"

# # Stack Auth Configuration
# STACK_AUTH_BASE_URL = os.getenv("STACK_AUTH_BASE_URL", "http://localhost:8102").rstrip("/")
# STACK_AUTH_DEFAULT_TEAM_NAME = os.getenv("STACK_AUTH_DEFAULT_TEAM_NAME", "GDP Labs")
# STACK_AUTH_PROJECT_ID = os.getenv("STACK_AUTH_PROJECT_ID", "")
# STACK_AUTH_SECRET_SERVER_KEY = os.getenv("STACK_AUTH_SECRET_SERVER_KEY", "")
# STACK_AUTH_PUBLISHABLE_CLIENT_KEY = os.getenv("STACK_AUTH_PUBLISHABLE_CLIENT_KEY", "")
# STACK_AUTH_DEFAULT_PERMISSION_ID = os.getenv("STACK_AUTH_DEFAULT_PERMISSION_ID", "_end_user")
# STACK_AUTH_HTTP_CLIENT_TIMEOUT = int(os.getenv("STACK_AUTH_HTTP_CLIENT_TIMEOUT", "30"))

# # Admin config
# ADMIN_CONFIG_KNOWLEDGE_BASES = os.getenv("ADMIN_CONFIG_KNOWLEDGE_BASES", "false").lower() == "true"
# ADMIN_CONFIG_MODELS = os.getenv("ADMIN_CONFIG_MODELS", "false").lower() == "true"
# ADMIN_CONFIG_CHATBOTS = os.getenv("ADMIN_CONFIG_CHATBOTS", "false").lower() == "true"
# ADMIN_CONFIG_USER_CHATBOTS = os.getenv("ADMIN_CONFIG_USER_CHATBOTS", "false").lower() == "true"
# ADMIN_CONFIG_VECTOR_STORES = os.getenv("ADMIN_CONFIG_VECTOR_STORES", "false").lower() == "true"


class UploadedFileConstants:
    """Class for defining constants related to uploaded files."""

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_UPLOADED_FILE = 10
    FILE_SIZE_EXCEEDED_MSG = "File size exceeds the maximum allowed size of {max_file_size:,} bytes."
    FILE_COUNT_EXCEEDED_MSG = f"Only {MAX_UPLOADED_FILE} files are allowed for this pipeline."


# # Company branding constants
# LOGO_ICON_EXTENSIONS_WHITELIST = os.getenv(
#     "LOGO_ICON_EXTENSIONS_WHITELIST", ".jpg,.jpeg,.png,.svg,.ico,.gif,.webp"
# ).split(",")

# # File size limits for company assets (in bytes)
# MAX_LOGO_FILE_SIZE = int(os.getenv("MAX_LOGO_FILE_SIZE", str(5 * 1024 * 1024)))  # 5 MB default
# MAX_ICON_FILE_SIZE = int(os.getenv("MAX_ICON_FILE_SIZE", str(1 * 1024 * 1024)))  # 1 MB default


class ConversationConstants:
    """Class for defining constants related to conversation."""

    ERR_NOT_FOUND_MSG = "Conversation not found"


class SharedConversationConstants:
    """Class for defining constants related to shared conversations."""

    DEFAULT_EXPIRY_DAYS = None  # None means no expiry
    ERR_NOT_FOUND_MSG = "Shared conversation not found."
    ERR_EMPTY_CONVERSATION_MSG = (
        "Cannot share conversation with no messages. Please wait for the AI message to finish first."
    )


# class MediaTypeConstants:
#     """Class for defining constants related to media types."""

#     TEXT_EVENT_STREAM = "text/event-stream"


# CACHE_INDEX_NAME = os.getenv("CACHE_INDEX_NAME", "gllm-cache")
# CACHE_EMBEDDING_MODEL = os.getenv("CACHE_EMBEDDING_MODEL", "openai/text-embedding-3-small")
# CACHE_SIMILARITY_THRESHOLD = float(os.getenv("CACHE_SIMILARITY_THRESHOLD", "0.99"))
# CACHE_MESSAGE_PAIR_LIMIT = int(os.getenv("CACHE_MESSAGE_PAIR_LIMIT", "3"))
# CACHE_EVICTION_INTERVAL = int(os.getenv("CACHE_EVICTION_INTERVAL", "7200"))
# CACHE_TTL = int(os.getenv("CACHE_TTL", "14400"))

# RATE_LIMIT_REQUESTS_DEFAULT = os.getenv("RATE_LIMIT_REQUESTS_DEFAULT", "5")
# RATE_LIMIT_TIME_DEFAULT_SECONDS = int(os.getenv("RATE_LIMIT_TIME_DEFAULT_SECONDS", "60"))

# RATE_LIMIT_REQUESTS_MESSAGE = int(os.getenv("RATE_LIMIT_REQUESTS_MESSAGE", "60"))
# RATE_LIMIT_REQUESTS_LOGIN = int(os.getenv("RATE_LIMIT_REQUESTS_LOGIN", "10"))
# RATE_LIMIT_REQUESTS_SHARE_CONVERSATION = int(os.getenv("RATE_LIMIT_REQUESTS_SHARED_CONVERSATION", "10"))

# RATE_LIMIT_REQUESTS_ADMIN_CHATBOT = int(os.getenv("RATE_LIMIT_REQUESTS_ADMIN_CHATBOT", RATE_LIMIT_REQUESTS_DEFAULT))
# RATE_LIMIT_REQUESTS_ADMIN_PRESET = int(os.getenv("RATE_LIMIT_REQUESTS_ADMIN_PRESET", RATE_LIMIT_REQUESTS_DEFAULT))
# RATE_LIMIT_REQUESTS_ADMIN_PROVIDER = int(os.getenv("RATE_LIMIT_REQUESTS_ADMIN_PROVIDER", RATE_LIMIT_REQUESTS_DEFAULT))
# RATE_LIMIT_REQUESTS_ADMIN_MODEL = int(os.getenv("RATE_LIMIT_REQUESTS_ADMIN_MODEL", RATE_LIMIT_REQUESTS_DEFAULT))
# RATE_LIMIT_REQUESTS_ADMIN_KNOWLEDGE_BASE = int(
#     os.getenv("RATE_LIMIT_REQUESTS_ADMIN_KNOWLEDGE_BASE", RATE_LIMIT_REQUESTS_DEFAULT)
# )
# RATE_LIMIT_REQUESTS_AUTH_CURRENT_USER = int(os.getenv("RATE_LIMIT_REQUESTS_AUTH_CURRENT_USER", "30"))

# DPO_ERR_MSG = (
#     "Unfortunately, we weren't able to process your request this time. "
#     "This might be due to one of the following reasons:\n"
#     "- The content you're trying to access (website, PDF, DOCX, etc.) may be restricted or unsupported\n"
#     "- The file format or structure could not be read\n"
#     "- External crawling is currently disabled or limited for this service\n\n"
#     "Please double-check the content and try again."
# )

# AIP_BASE_URL = os.getenv("AIP_BASE_URL", "").rstrip("/")
# AIP_API_KEY = os.getenv("AIP_API_KEY", "")

# LM_INVOKER_TIMEOUT_SECONDS = int(os.getenv("LM_INVOKER_TIMEOUT_SECONDS", "300"))
