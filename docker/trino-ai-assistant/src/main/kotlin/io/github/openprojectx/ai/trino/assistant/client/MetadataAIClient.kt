package io.github.openprojectx.ai.trino.assistant.client

import dev.langchain4j.service.UserMessage

interface MetadataAIClient {

    @UserMessage(
        """
        I am going to give you some Trino metadata using DDL sql, you will answer questions based on this metadata later, and I may give you additional DDL sql information when I ask you question, you should also consider the additional information too,  following are the metadata
        {{it}}
    """
    )
    fun initMetadata(initPrompt: String): String

    fun askQuestionForMetadata(question: String): String

}