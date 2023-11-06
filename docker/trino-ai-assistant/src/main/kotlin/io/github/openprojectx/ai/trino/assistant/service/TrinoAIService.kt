package io.github.openprojectx.ai.trino.assistant.service

import io.github.openprojectx.ai.trino.assistant.client.ChatGPTClient
import io.github.openprojectx.ai.trino.assistant.repository.TrinoRepo
import org.apache.commons.csv.CSVFormat
import org.apache.commons.csv.CSVPrinter
import org.springframework.stereotype.Service
import java.io.StringWriter


@Service
class TrinoAIService(
    val trinoRepo: TrinoRepo,
    val chatGPTClient: ChatGPTClient
) {

    companion object{
        private const val TRINO_COMMENT: String = "--"
    }

    fun getTableSchemas(): String {
        return trinoRepo.showCatalogs()
            .flatMap { catalog ->
                trinoRepo.showSchemasFrom(catalog)
                    .flatMap { schema ->
                        trinoRepo.showTablesFrom("$catalog.$schema")
                            .flatMap { table ->
                                trinoRepo.showCreateTable("$catalog.$schema.$table")
                            }
                    }
            }
            .joinToString(";\n")
    }

    fun getTableSchemasAndSampleData(): String {
        return trinoRepo.showCatalogs()
            .flatMap { catalog ->
                trinoRepo.showSchemasFrom(catalog)
                    .flatMap { schema ->
                        trinoRepo.showTablesFrom("$catalog.$schema")
                            .flatMap { table ->
                                trinoRepo.showCreateTable("$catalog.$schema.$table")
                                    .map { tableSchema ->
                                        val sampleData = runSql("select * from $catalog.$schema.$table limit 3")
                                            .lines().joinToString("\n") { line ->
                                                "$TRINO_COMMENT $line"
                                            }

                                        "$tableSchema\n-- sample data for table $catalog.$schema.$table in CSV format:\n$sampleData"
                                    }
                            }
                    }
            }
            .joinToString(";\n")
    }

    fun answer(question: String): String {
        TODO("Not yet implemented")
    }

    fun runSql(sql: String): String {
        return trinoRepo.runSql(sql).use { resultSet ->
            StringWriter().use {
                val csvPrinter = CSVPrinter(
                    it,
                    CSVFormat.Builder.create()
                        .setHeader(resultSet)
                        .build()
                )
                csvPrinter.printRecords(resultSet)
                it.toString()
            }
        }
    }

}
