package com.example.api.dto;

import jakarta.validation.constraints.NotBlank;

public record QuestionRequest(
        @NotBlank(message = "question must not be blank")
        String question
) {}
