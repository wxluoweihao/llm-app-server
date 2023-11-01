package io.github.openprojectx.ai.trino.assistant

import io.github.openprojectx.ai.trino.assistant.domain.TableScanFilter
import org.springframework.boot.autoconfigure.EnableAutoConfiguration
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.boot.runApplication

@SpringBootApplication
@EnableConfigurationProperties(TableScanFilter::class)
class TrinoAiAssistantApplication

fun main(args: Array<String>) {
    runApplication<TrinoAiAssistantApplication>(*args)
}
