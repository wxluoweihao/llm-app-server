package io.github.openprojectx.ai.trino.assistant

import io.github.openprojectx.ai.trino.assistant.domain.TableScanFilter
import io.swagger.v3.oas.annotations.OpenAPIDefinition
import io.swagger.v3.oas.annotations.servers.Server
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.boot.runApplication

@OpenAPIDefinition(
    servers = [
        Server(url = "http://trino-ai-assistant:7080/trino")
    ]
)
@SpringBootApplication
@EnableConfigurationProperties(TableScanFilter::class)
class TrinoAiAssistantApplication

fun main(args: Array<String>) {
    runApplication<TrinoAiAssistantApplication>(*args)
}
