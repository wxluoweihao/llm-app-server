package io.github.openprojectx.ai.trino.assistant.resource

import io.github.openprojectx.ai.trino.assistant.service.TrinoAIService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.Parameter
import io.swagger.v3.oas.annotations.media.Content
import io.swagger.v3.oas.annotations.media.ExampleObject
import io.swagger.v3.oas.annotations.responses.ApiResponse
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController("/db")
class DatabaseResource(
    val trinoAIService: TrinoAIService,
) {

    @GetMapping(
        "/table/schema",
        produces = ["application/sql"]
    )
    @Operation(
        summary = "Get all the table schema information",
        description = "Returns all the table schema information using Trino DDL sql",
        responses = [
            ApiResponse(
                responseCode = "200",
                description = "successfully returns all the table schema information using Trino DDL sql",
                content = [Content(
                    mediaType = "application/sql",
                    examples = [ExampleObject(
                        name = "Trino DDL SQLs",
                        value = """
                    create table catalog1.schema1.table1
                    (
                        column1 integer,
                        column2 integer
                    );
                    
                    create table catalog2.schema2.table2
                    (
                        column1 integer,
                        column2 integer
                    );
                """
                    )]
                )]
            )
        ]
    )
    fun getTableSchemas(): String {
        return trinoAIService.getTableSchemas()
    }

//    @GetMapping("/answer")
    fun answer(question: String): String {
        return trinoAIService.answer(question)

    }

    @PostMapping("/sql", consumes = ["application/sql"], produces = ["application/csv"])
    @Operation(
        description = "run a valid trio sql and get the csv results",
        responses = [ApiResponse(
            responseCode = "200",
            description = "successfully returns all the CSV result for the SQL, the first line is the column name header",
            content = [Content(
                mediaType = "application/sql",
                examples = [ExampleObject(
                    name = "Trino DDL SQLs",
                    value = """column1,column2
1,2
1,2
                """
                )]
            )]
        )
        ]
    )
    fun runSql(
        @RequestBody
        @Parameter(description = "a valid trino sql to run", example = "select * from catalog1.schema1.table1")
        sql: String
    ): String {
        return trinoAIService.runSql(sql)
    }
}