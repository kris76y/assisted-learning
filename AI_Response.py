from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment

SYSTEM_PROMPT = "You are a student maths tutor, helping an individual student with their " \
"lecture work. You will recieve an input from a lecture transcript containing only the topics they" \
"are struggling on with the current available material. Help explain the content to the student in a more" \
"simplified effective way pretty please." \
"- Find the relevant maths in the transcript." \
"- Explain it in plain language, step by step." \
"- Use a simple worked example with real numbers." \
"- Define any jargon the first time you use it." \
"- If the transcript is unclear or seems to contain an error, say so." \
"- Never ask any questions back to the student"\



def explain_maths(transcript: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Transcript:\n{transcript}"
            },
        ],
    )
    return response.choices[0].message.content


def toSeconds(time):
    parts = time.strip().split(":")
    seconds = float(parts[-1])
    minutes = int(parts[-2])

    return minutes * 60 + seconds
    
def extractTranscript(time, timeBack):

    with open("lecture_transcript.vtt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()


    endTotal = toSeconds(time) + 5
    startTotal = max(0, endTotal - timeBack - 10)


    startIndex = -1
    endIndex = 0
    extract = []
    for i in range(0, len(lines)):

        if "-->" in lines[i]:
            cueStart, cueEnd = lines[i].split("-->")
            
            if toSeconds(cueStart) >= startTotal and toSeconds(cueEnd) <= endTotal:
                if startIndex == -1:
                    startIndex = i
                endIndex = i

    for i in range(startIndex, endIndex):
         if "-->" in lines[i]:
             extract.append(lines[i + 1].strip())
         
    return " ".join(extract)








#print("\n" + explain_maths(transcript))