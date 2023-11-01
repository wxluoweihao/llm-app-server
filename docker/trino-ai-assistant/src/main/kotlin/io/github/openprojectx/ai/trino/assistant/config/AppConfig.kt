package io.github.openprojectx.ai.trino.assistant.config

import dev.langchain4j.memory.chat.MessageWindowChatMemory
import dev.langchain4j.model.chat.ChatLanguageModel
import dev.langchain4j.model.openai.OpenAiChatModel
import dev.langchain4j.service.AiServices
import io.github.openprojectx.ai.trino.assistant.client.ChatGPTClient
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.net.InetSocketAddress
import java.net.MalformedURLException
import java.net.Proxy
import java.net.URL
import java.time.Duration

@Configuration
class AppConfig {

    @Bean
    fun chatGPTClient(@Value("\${langchain.openai-api-key}") openaiAPIKey: String): ChatGPTClient {
        val builder: OpenAiChatModel.OpenAiChatModelBuilder = OpenAiChatModel.builder()
            .apiKey(openaiAPIKey)
            .timeout(Duration.ofSeconds(60))

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
}