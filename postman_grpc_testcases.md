# Postman gRPC Test Cases for ImageGen Microservice

## Server Address:
localhost:50051

## Method:
ImageGenService.GenerateImage

---

### ✅ Test Case 1: Valid Prompt

**Input:**
```json
{
  "prompt": "a castle on a hill at sunset",
  "steps": 15
}

Expected Output:

Response with status "success"

Non-empty image_base64 string

#### ❌ Test Case 2: Invalid Prompt
**Input:**
```json
{
  "prompt": "",
  "steps": 10
}
Expected Output:

gRPC error with INVALID_ARGUMENT

Message: "Prompt is empty"



