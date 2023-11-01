package io.github.openprojectx.ai.trino.assistant.resource

import io.github.openprojectx.ai.trino.assistant.domain.AIPluginInfo
import io.github.openprojectx.ai.trino.assistant.domain.API
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class AIPluginInfoResource {

    @GetMapping("/.well-known/ai-plugin.json")
    fun aiPluginInfo(): AIPluginInfo {
        return AIPluginInfo(
            schemaVersion = "v0.1.0",
            nameForModel = "Trino Assistant",
            nameForHuman = "Trino Assistant",
            descriptionForHuman = """ 
        A Trino  Assistant managing a Trio database. It provides API to query database schema information, and run SQL with CSV response.
        """.trimIndent(),
            descriptionForModel = """ ,
        A Trino AI Assistant managing a Trio database. 
        It provides APIs to query the database schema information which is trino DDL sql format, and run SQL with CSV response, before you run the sql, you'd better check the database schema information(table name, column name, comment) first.
        """.trimIndent(),
            api = API(),
            contactEmail = "CoderYellow@hotmail.com",
            legalInfoUrl = "https://www.apache.org/licenses/LICENSE-2.0",
        )
    }
}