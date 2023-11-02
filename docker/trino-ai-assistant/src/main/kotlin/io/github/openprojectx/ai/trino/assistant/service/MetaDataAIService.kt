package io.github.openprojectx.ai.trino.assistant.service

import io.github.openprojectx.ai.trino.assistant.client.MetadataAIClient
import io.github.openprojectx.ai.trino.assistant.domain.HintDocument
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.core.io.Resource
import org.springframework.stereotype.Service

@Service
class MetaDataAIService(
    private val metadataAIClient: MetadataAIClient,
    private val trinoAIService: TrinoAIService,
) {

    private val logger = LoggerFactory.getLogger(javaClass)

    init {
        val tableSchemas = trinoAIService.getTableSchemas()
        val initResponse = metadataAIClient.initMetadata(tableSchemas)
        logger.info("initResponse: {}", initResponse)
    }

    fun getAnswerForMetadata(question: String): String{
        return metadataAIClient.askQuestionForMetadata(question)
    }

}