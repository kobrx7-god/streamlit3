import streamlit as st, io, newconfig
from openai import OpenAI

api = newconfig.api
client = OpenAI(api_key=api, base_url="https://api.groq.com/openai/v1")
model = 'openai/gpt-oss-20b'

systemPrompt = """
Your knowledge in Math and all its divisions transcends space, time and spacetime.
Solve any problem step by step.
Explain reasoning using technical terms, then simplify it as if you are explaining it to an 8th grader.
Verify the answer and cite your sources ALWAYS.
"""

def solveMath(problem, level):
    prompt = f"""
{systemPrompt}
level : {level}
problem : {problem}
"""
    try:
        response = client.chat.completions.create(
            model = model,
            messages = [{
                "role":"user",
                "content":prompt
            }],
            temperature=0.3,
            max_tokens=1024            
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error"+str(e)

st.set_page_config(page_title="Math Mastermind")
st.title("Math Matsermind")
st.write("Enter a math problem and get a step-by-step solution.")

if "history" not in st.session_state:
    st.session_state.history=[]

problem = st.text_area(
    "Math Problem",
    placeholder=
    """Enter any problem...
Example : 𝑥², 5𝑥+6, 𝑥³𝑦², ((𝑥𝑦)²)³...
    """
)

level = st.selectbox(
    "Level",
    ["Basic (Grades 1-5)", "Intermediate (Grades 6-10)", "Advanced (Grades 11 & 12)", "College-grade (B, M, PhD)"]
)

if st.button("Solve"):
    if not problem.strip():
        st.warning("Please enter a statment")
        st.error("MathError : __blank__ not computable")
    else:
        with st.spinner("Traingulating Response"):
            try:
                answer = solveMath(problem, level)
                st.session_state.history.append(
                    {
                        "problem":problem,
                        "answer":answer
                    }
                )
                st.subheader("Solution")
                st.write(answer)
            except Exception as e:
                st.error(f"SystemError : {e}")

if st.button("Clear History"):
    st.session_state.history=[]
    st.rerun()
    