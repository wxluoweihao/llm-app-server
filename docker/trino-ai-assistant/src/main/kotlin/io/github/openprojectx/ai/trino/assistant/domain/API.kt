package io.github.openprojectx.ai.trino.assistant.domain

data class API(
    val type: String = "openapi",
    val url: String ="http://localhost:9080/trino/v3/api-docs",
    val hasUserAuthentication: Boolean = false,
)