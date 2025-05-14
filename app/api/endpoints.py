from fastapi import APIRouter, UploadFile, File, HTTPException
from pdf2image import convert_from_bytes
from typing import List
import io
import base64
import openai
import os
from loguru import logger

router = APIRouter()

def pdf_to_jpgs(pdf_bytes: bytes) -> List[bytes]:
    logger.info("Starting PDF to JPG conversion...")
    images = convert_from_bytes(pdf_bytes, fmt='jpeg')
    jpg_bytes_list = []
    for idx, img in enumerate(images):
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        jpg_bytes_list.append(buf.getvalue())
        logger.info(f"Converted page {idx+1} to JPG, size: {len(jpg_bytes_list[-1])} bytes")
    logger.info(f"PDF to JPG conversion complete. Total pages: {len(jpg_bytes_list)}")
    return jpg_bytes_list

@router.post("/extract")
async def extract_data(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    if not file.filename.lower().endswith('.pdf'):
        logger.error("File is not a PDF.")
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    pdf_bytes = await file.read()
    logger.info(f"Read {len(pdf_bytes)} bytes from uploaded PDF.")
    jpgs = pdf_to_jpgs(pdf_bytes)
    base64_images = []
    for idx, jpg in enumerate(jpgs):
        b64 = base64.b64encode(jpg).decode('utf-8')
        base64_images.append(b64)
        logger.info(f"Encoded page {idx+1} to base64, length: {len(b64)} characters")
    logger.info(f"Total images to send to OpenAI: {len(base64_images)}")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    system_prompt = (
        "You are a specialized bank statement analyzer. "
        "Extract and structure the following information from the provided bank statement images: "
        "1. Account Information (holder name, account number, type, statement period). "
        "2. Transaction Summary (total deposits, withdrawals, balances, transaction count). "
        "3. Transaction Details (date, description, amount, category, running balance). "
        "4. Spending Analysis (top categories, largest transactions, recurring payments, unusual activity). "
        "5. Validation Details (completeness, missing/unclear info, quality issues). "
        "Return ONLY a valid JSON object with this structure."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [
            {"type": "text", "text": "Extract all required data from these bank statement images. Return only JSON."},
            *[
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}}
                for img in base64_images
            ]
        ]}
    ]
    logger.info("Sending images to OpenAI Vision API...")
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=4096,
        )
        logger.info("Received response from OpenAI Vision API.")
        content = response.choices[0].message.content
        logger.debug(f"Raw OpenAI response: {content[:500]}...")
        import json
        import re
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            json_data = json.loads(match.group(0))
            logger.info("Successfully parsed JSON from OpenAI response.")
        else:
            logger.error("No JSON object found in OpenAI response.")
            raise ValueError("No JSON object found in OpenAI response.")
        logger.info("Returning structured data to client.")
        return {"data": json_data}
    except Exception as e:
        logger.error(f"OpenAI Vision API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI Vision API error: {str(e)}")

# The new endpoint and logic will be added here for image-based PDF processing.