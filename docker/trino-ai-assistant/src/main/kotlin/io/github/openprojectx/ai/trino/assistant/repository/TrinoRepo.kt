package io.github.openprojectx.ai.trino.assistant.repository

import io.github.openprojectx.ai.trino.assistant.domain.TableScanFilter
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Repository
import java.sql.Connection
import java.sql.DriverManager
import java.sql.ResultSet
import java.util.*
import kotlin.collections.ArrayList

@Repository
class TrinoRepo(
    @Value("\${trino.url}") url: String,
    private val tableScanFilter: TableScanFilter,
) {
    private val connection: Connection

    init {
        val properties = Properties()
        properties.setProperty("user", "trino-ai-assistant")
        connection = DriverManager.getConnection(url, properties)
    }

    fun showCatalogs(): List<String> {
        connection.createStatement().use { statement ->
            val resultSet = statement.executeQuery("show catalogs")
            val catalogs: ArrayList<String> = arrayListOf()
            while (resultSet.next()) {
                val category = resultSet.getString(1)
                if (!tableScanFilter.catalogs.contains(category)) {
                    catalogs.add(category)
                }
            }
            return catalogs
        }
    }


    fun showSchemasFrom(catalog: String): List<String> {
        val statement = connection.createStatement()
        val resultSet = statement.executeQuery("show schemas from $catalog")
        val schemas: ArrayList<String> = arrayListOf()
        while (resultSet.next()) {
            val schema = resultSet.getString(1)
            if (!tableScanFilter.schemas.contains(schema)) {
                schemas.add(schema)
            }
        }
        return schemas
    }

    fun showTablesFrom(schema: String): List<String> {
        val statement = connection.createStatement()
        val resultSet = statement.executeQuery("show tables from $schema")
        val tables: ArrayList<String> = arrayListOf()
        while (resultSet.next()) {
            val category = resultSet.getString(1)
            tables.add(category)
        }
        return tables
    }

    fun showCreateTable(table: String): List<String> {
        val statement = connection.createStatement()
        val resultSet = statement.executeQuery("show create table $table")
        val tableDDL: ArrayList<String> = arrayListOf()
        while (resultSet.next()) {
            val category = resultSet.getString(1)
            tableDDL.add(category)
        }
        return tableDDL
    }

    fun runSql(sql: String): ResultSet {
        return connection.createStatement().executeQuery(sql)

    }


}