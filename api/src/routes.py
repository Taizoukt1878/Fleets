from fastapi import APIRouter, File, UploadFile, HTTPException
from io import BytesIO
import librosa
import soundfile as sf
from transcription import transcribe_audio
from llm_funcs import get_car_data

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to the Audio Processing API!"}

@router.post("/upload_audio/")
async def upload_audio(audio_file: UploadFile = File(...)):
    try:
        # Read audio file into memory
        buffer = BytesIO(await audio_file.read())
        # Load audio file with librosa
        # Note: By default, librosa converts the signal to 22050 Hz
        # `sr=None` loads the file with its original sampling rate
        y, sr = librosa.load(buffer, sr=None)
        # You can perform additional processing here if needed
        # For example, ensure mono
        if y.ndim > 1:
            y = librosa.to_mono(y)
        # Save the processed audio to a temporary file if needed
        temp_audio_path = f"sounds/temp_audio_{audio_file.filename}"
        sf.write(temp_audio_path, y, sr, format='WAV')
        transcribed_text = transcribe_audio(str(temp_audio_path))
        llm_response = get_car_data(transcribed_text)
        return {"message": "Audio uploaded and processed successfully",
                "transcribed_text": transcribed_text,
                "llm_response": llm_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
