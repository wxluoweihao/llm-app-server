package io.github.openprojectx.ai.trino.assistant.service

import io.github.openprojectx.ai.trino.assistant.client.MetadataAIClient
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service

@Service
class MetaDataAIService(
    private val metadataAIClient: MetadataAIClient,
    private val trinoAIService: TrinoAIService,
) {

    private val logger = LoggerFactory.getLogger(javaClass)

    init {
        val tableSchemas = trinoAIService.getTableSchemasAndSampleData()
//        val initResponse = metadataAIClient.initMetadata(tableSchemas)
//        logger.info("initResponse: {}", initResponse)
    }

    fun getAnswerForMetadata(question: String): String{
        val tableSchemas = trinoAIService.getTableSchemasAndSampleData()
        return metadataAIClient.askQuestionForMetadata(tableSchemas,question)
    }

}