from flask import Flask, render_template, request, redirect, url_for, session
from main_real import agent
import uuid
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace

@app.route('/')
def home():
    session['thread_id'] = str(uuid.uuid4())
    if 'messages' not in session:
        session['messages'] = []
    print('home', session)
    return render_template('chat.html', messages=session.get("messages", []))

@app.route('/send', methods=['POST'])
@app.route('/send', methods=['POST'])
def send():
    user_input = request.form['message']

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        {
            "configurable": {
                "thread_id": session['thread_id']
            }
        }
    )

    # Get the assistant's response
    assistant_content = response["messages"][-1].content

    # Extract only the actual text
    if isinstance(assistant_content, list):
        text_parts = []

        for block in assistant_content:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])

        assistant_content = "\n".join(text_parts)

    elif isinstance(assistant_content, dict):
        assistant_content = assistant_content.get(
            "text",
            str(assistant_content)
        )

    # Store user message
    session['messages'].append({
        "role": "user",
        "content": user_input
    })

    # Store clean assistant message
    session['messages'].append({
        "role": "assistant",
        "content": assistant_content
    })

    session.modified = True

    print(session)

    return redirect(url_for('home'))

if __name__ == '__main__':
 app.run(debug=True)