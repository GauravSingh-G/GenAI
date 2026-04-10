import streamlit as st
import base64
from openai import OpenAI
client = OpenAI(api_key="---")




def generate_image(prompt):
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return image_bytes


def get_ai_description(topic):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI teacher explaining images clearly."},
            {"role": "user", "content": f"Describe an image about {topic} in simple English."}
        ]
    )
    return completion.choices[0].message.content


def evaluate_speech(ai_desc, user_desc):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Evaluate student's spoken English and give improvements."},
            {"role": "user", "content": f"AI Description: {ai_desc}\nUser Description: {user_desc}"}
        ]
    )
    return completion.choices[0].message.content


def app():
    st.header("AI Image Speaking Practice")

    topic = st.text_input("Enter AI/ML topic (e.g. Neural Network)")

    # Initialize state
    if "image_bytes" not in st.session_state:
        st.session_state.image_bytes = None

    # Generate image
    if st.button("Generate Image"):
        if topic:
            st.session_state.image_bytes = generate_image(topic)
        else:
            st.error("Please enter a topic")

    # Display image
    if st.session_state.image_bytes:
        st.image(st.session_state.image_bytes)

        st.write("Now speak about this image for 10 seconds")

        audio_file = st.audio_input("Start speaking")

        if audio_file is not None:
            with open("audio.wav", "wb") as f:
                f.write(audio_file.read())

            # Speech to text
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=open("audio.wav", "rb")
            )

            user_text = transcript.text

            # AI description
            ai_desc = get_ai_description(topic)

            # Evaluation
            feedback = evaluate_speech(ai_desc, user_text)

            st.subheader("Your Speech:")
            st.write(user_text)

            st.subheader("AI Feedback:")
            st.write(feedback)
