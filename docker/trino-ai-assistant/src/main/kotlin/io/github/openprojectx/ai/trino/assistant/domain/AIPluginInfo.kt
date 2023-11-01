package io.github.openprojectx.ai.trino.assistant.domain

data class AIPluginInfo(
    val schemaVersion: String = "v0.1.0",
    val nameForModel: String = "TrinoAIAssistant",
    val nameForHuman: String = "Trino AI Assistant",
    val descriptionForHuman: String = """ 
        A Trino AI Assistant managing a Trio database. It provides API to query database schema information, and answer natural language question with natural language response.
        """.trimIndent(),
    val descriptionForModel: String = """ ,
        A Trino AI Assistant managing a Trio database. 
        It provides APIs to query the database schema information which is trino DDL sql format, and answer natural language question with natural language response, before you ask the question, you'd better check the database schema information(table name, column name, comment) first, to see if this assistant have related domain knowledge for your question topic.
        """.trimIndent(),
    val api: API = API(),
    val contactEmail: String = "CoderYellow@hotmail.com",
    val legalInfoUrl: String = "https://www.apache.org/licenses/LICENSE-2.0",
)