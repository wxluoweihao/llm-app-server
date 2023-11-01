FROM eclipse-temurin:17-jdk-alpine
VOLUME /tmp
COPY build/libs/trino-ai-assistant-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 9080 7080

ENTRYPOINT ["java","-jar","/app.jar"]
