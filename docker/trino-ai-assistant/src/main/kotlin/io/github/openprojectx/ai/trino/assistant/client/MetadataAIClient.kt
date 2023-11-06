package io.github.openprojectx.ai.trino.assistant.client

import dev.langchain4j.service.SystemMessage
import dev.langchain4j.service.UserMessage
import dev.langchain4j.service.V

interface MetadataAIClient {

    @SystemMessage(
        """
        You are a Trino Database assistant managing, you will answer questions based on the table metadata and its sample data later. When you reference a table in your answer, you should always use the DDL SQL format and include the sample data
        following are the metadata using DDL sql:
        {{it}}
    """
    )
    fun initMetadata(initPrompt: String): String

    @SystemMessage(
        """
        You are a Trino Database assistant managing some Trino database table schemas using DDL sql. When you reference a table in your answer, you should always use the DDL SQL and include the sample data
        following are the table schemas using DDL sql, and their simple data:
        {{tableSchemas}}
    """
    )
    @UserMessage(
        """
        {{question}}
        include SQL DDL and sample data 
    """
    )
    fun askQuestionForMetadata(@V("tableSchemas") tableSchemas: String, @V("question") question: String): String

}