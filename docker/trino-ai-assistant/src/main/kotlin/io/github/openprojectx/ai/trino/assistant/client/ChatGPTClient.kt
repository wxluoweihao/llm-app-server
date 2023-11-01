package io.github.openprojectx.ai.trino.assistant.client

import dev.langchain4j.service.UserMessage

interface ChatGPTClient {
    @UserMessage(
        """
                Given input questions I will ask you later, first create a syntactically correct Trino query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most 512 results. You can order the results by a relevant column to return the most interesting examples in the database.
                When you reference a table in the SQL, always include the catalog and schema.
                Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

                Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

                Your answer should strictly return a valid SQL only.

                following are the trino tables schema metadata:
                {{it}}
            """
    )
    fun initMetadata(initPrompt: String): String?

    fun testToSql(question: String?): String?
}