import boto3
import json

# ---------- Configuration ----------
BUCKET_NAME = "employee-pht"      # Replace with your S3 bucket name
IMAGE_FILE = "images/employee.jpg"       # Local image path
OBJECT_NAME = "employee.jpg"             # Name in S3

# ---------- AWS Clients ----------
s3 = boto3.client("s3")
rekognition = boto3.client("rekognition", region_name="ap-south-1")

# ---------- Upload Image to S3 ----------
print("Uploading image to S3...")

s3.upload_file(
    Filename=IMAGE_FILE,
    Bucket=BUCKET_NAME,
    Key=OBJECT_NAME
)

print("Image uploaded successfully.\n")

# ---------- Detect Faces ----------
response = rekognition.detect_faces(
    Image={
        "S3Object": {
            "Bucket": BUCKET_NAME,
            "Name": OBJECT_NAME
        }
    },
    Attributes=["DEFAULT"]
)

faces = response["FaceDetails"]

print("========== Rekognition Result ==========")
print("Number of Faces:", len(faces))
print()

result = {
    "NumberOfFaces": len(faces),
    "Faces": []
}

for i, face in enumerate(faces, start=1):

    confidence = face["Confidence"]

    print(f"Face {i}")
    print(f"Confidence : {confidence:.2f}%")
    print("----------------------------------")

    result["Faces"].append({
        "FaceNumber": i,
        "Confidence": round(confidence, 2)
    })

# ---------- Save JSON ----------
with open("result.json", "w") as f:
    json.dump(result, f, indent=4)

print("result.json created successfully.")