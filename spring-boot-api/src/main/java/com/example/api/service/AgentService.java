package com.example.api.service;

import com.example.api.dto.AgentResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class AgentService {

    private static final Logger log = LoggerFactory.getLogger(AgentService.class);

    private final RestClient restClient;

    public AgentService(@Value("${agent.fastapi-url}") String fastapiUrl) {
        this.restClient = RestClient.builder()
                .baseUrl(fastapiUrl)
                .defaultHeader("Content-Type", "application/json")
                .build();
    }

    public AgentResponse ask(String question) {
        log.info("Forwarding question to FastAPI agent: {}", question);

        AgentResponse response = restClient.post()
                .uri("/ask")
                .body(Map.of("question", question))
                .retrieve()
                .body(AgentResponse.class);

        log.info("Received answer: {}", response != null ? response.answer() : "null");
        return response;
    }
}
