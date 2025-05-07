package fr.uha.hassenforder.nn;

import java.util.Map;
import java.util.TreeMap;
import javax.ws.rs.QueryParam;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

@RestController
public class NNController {

    @PostMapping (value="/config")
    @ResponseStatus(HttpStatus.OK)
    public String config (@RequestParam( "model" ) String modelName) {

        if (modelName == null || modelName.trim().isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "The 'model' parameter is required");
        }
        
        String url = "http://ia:80/config?model={model}";

        HttpHeaders headers = new HttpHeaders();
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(headers);
        
        Map<String, String> params = new TreeMap<>();
        params.put("model", modelName);

        try {
            RestTemplate template = new RestTemplate();
            ResponseEntity<String> response = template.exchange(url, HttpMethod.POST, requestEntity, String.class, params);
            return response.getBody();
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, 
                "Error calling service: " + e.getMessage(), e);
        }
    }

    @PostMapping (value="/classify")
    @ResponseStatus(HttpStatus.OK)
    public String classify (@RequestParam( "model" ) String name) {

        String url = "http://ia:80/classify";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("graph", name);
        
        Map<String, String> params = new TreeMap<>();

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        RestTemplate template = new RestTemplate();
        ResponseEntity<String> response = template.exchange(url, HttpMethod.POST, requestEntity, String.class, params);

        return response.getBody();
    }
}
