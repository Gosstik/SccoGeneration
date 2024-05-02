package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.io.Serializable;

@AllArgsConstructor
public class PDFResponseDTO implements Serializable {
    @JsonProperty("customer_id")
    long customerId;
    @JsonProperty("client_id")
    long clientID;
    @JsonProperty("file_path")
    String CPlink;
}