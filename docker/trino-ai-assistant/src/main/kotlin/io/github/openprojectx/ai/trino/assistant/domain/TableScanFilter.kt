package io.github.openprojectx.ai.trino.assistant.domain

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.boot.context.properties.bind.ConstructorBinding

@ConfigurationProperties("trino.filter")
data class TableScanFilter @ConstructorBinding constructor(
    val catalogs:List<String>,
    val schemas:List<String>
)