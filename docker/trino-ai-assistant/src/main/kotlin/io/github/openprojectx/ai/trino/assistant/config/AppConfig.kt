package io.github.openprojectx.ai.trino.assistant.config

import com.fasterxml.jackson.databind.ObjectMapper
import dev.langchain4j.data.document.Document
import dev.langchain4j.data.document.Metadata
import dev.langchain4j.data.document.splitter.DocumentByLineSplitter
import dev.langchain4j.data.segment.TextSegment
import dev.langchain4j.memory.chat.MessageWindowChatMemory
import dev.langchain4j.model.chat.ChatLanguageModel
import dev.langchain4j.model.embedding.EmbeddingModel
import dev.langchain4j.model.openai.OpenAiChatModel
import dev.langchain4j.model.openai.OpenAiEmbeddingModel
import dev.langchain4j.retriever.EmbeddingStoreRetriever
import dev.langchain4j.service.AiServices
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore
import io.github.openprojectx.ai.trino.assistant.client.ChatGPTClient
import io.github.openprojectx.ai.trino.assistant.client.MetadataAIClient
import io.github.openprojectx.ai.trino.assistant.domain.HintDocument
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.io.Resource
import java.net.InetSocketAddress
import java.net.MalformedURLException
import java.net.Proxy
import java.net.URL
import java.time.Duration

@Configuration
class AppConfig {


    @Bean
    fun chatGPTClient(
        @Value("\${langchain.openai-api-key}") openaiAPIKey: String,
        @Value("\${langchain.openai-api-base-url}") baseURl: String
    ): ChatGPTClient {
        val builder: OpenAiChatModel.OpenAiChatModelBuilder = OpenAiChatModel.builder()
            .apiKey(openaiAPIKey)
            .logRequests(true)
            .logResponses(true)
//            .baseUrl("https://api.duckgpt.top/v1")
            .baseUrl(baseURl)
            .timeout(Duration.ofSeconds(64))
        System.getenv("http_proxy")?.let { httpProxy ->
            try {
                val url = URL(httpProxy)
                builder.proxy(Proxy(Proxy.Type.HTTP, InetSocketAddress(url.host, url.port)))
            } catch (e: MalformedURLException) {
                throw RuntimeException("invalid proxy address $httpProxy", e)
            }
        }

        val model: ChatLanguageModel = builder
            .build()

        return AiServices.builder(ChatGPTClient::class.java)
            .chatLanguageModel(model)
            .chatMemory(MessageWindowChatMemory.withMaxMessages(4096))
            .build()
    }

    @Bean
    fun metadataAIClient(
        @Value("\${langchain.openai-api-key}") openaiAPIKey: String,
        @Value("\${langchain.openai-api-base-url}") baseURl: String,
        @Value("classpath:HintDocument.json") hintDocumentResource: Resource,
        objectMapper: ObjectMapper,
    ): MetadataAIClient {
        val builder: OpenAiChatModel.OpenAiChatModelBuilder = OpenAiChatModel.builder()
            .apiKey(openaiAPIKey)
            .logRequests(true)
            .logResponses(true)
//            .baseUrl("https://api.duckgpt.top/v1")
            .baseUrl(baseURl)
            .timeout(Duration.ofSeconds(64))

        var url: URL?
        var proxy: Proxy? = null
        System.getenv("http_proxy")?.let { httpProxy ->
            try {
                url = URL(httpProxy)
                proxy = Proxy(Proxy.Type.HTTP, InetSocketAddress(url!!.host, url!!.port))

            } catch (e: MalformedURLException) {
                throw RuntimeException("invalid proxy address $httpProxy", e)
            }
        }
        proxy?.let {
            builder.proxy(proxy)

        }
        val model: ChatLanguageModel = builder
            .build()

        val embeddingModel: EmbeddingModel = OpenAiEmbeddingModel.builder()
            .also { openAiEmbeddingModel ->
                proxy?.let {
                    openAiEmbeddingModel.proxy(proxy)
                }

            }
            .apiKey(openaiAPIKey)
//            .baseUrl("https://api.duckgpt.top/v1")
            .baseUrl(baseURl)
            .logRequests(true)
            .logResponses(true)
            .timeout(Duration.ofSeconds(64))
            .build()
        val embeddingStore = InMemoryEmbeddingStore<TextSegment>()

//        val ingestor = EmbeddingStoreIngestor.builder()
//            .documentSplitter(DocumentByLineSplitter(4096, 4))
//            .embeddingModel(embeddingModel)
//            .embeddingStore(embeddingStore)
//            .build()

//        objectMapper.readerForListOf(HintDocument::class.java)
//            .readValue<List<HintDocument>?>(hintDocumentResource.inputStream)
//            .forEach() {
//                ingestor.ingest(Document(it.question, Metadata(mapOf("answer" to it.answer))))
//            }

//        val segment1 = TextSegment.from("""
//            there are some additional metadata information:
//            postgresql.public.create table "public".employee
//(
//    id   integer,
//    name varchar
//);
//"
//        """.trimIndent())
//        val embedding1 = embeddingModel.embed(segment1).content()
//        embeddingStore.add(embedding1, segment1)

        return AiServices.builder(MetadataAIClient::class.java)
            .chatLanguageModel(model)
            .retriever(EmbeddingStoreRetriever.from(embeddingStore, embeddingModel))
//            .chatMemory(MessageWindowChatMemory.withMaxMessages(4096))
            .build()
    }
}