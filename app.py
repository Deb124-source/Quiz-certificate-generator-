from flask import Flask, render_template, request, send_file, session, redirect, url_for
import io
from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'quiz_certificate_app_secret_key'  

os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)


quiz_questions = [
    {
        'question': 'Which is the cleanest city of India?',
        'options': ['Surat','Indore',  'Mysore', 'Chandigarh'],
        'correct_answer': 'Indore'
    },
    {
        'question': 'What is the capital of England?',
        'options': [ 'Manchester', 'Liverpool','London', 'Birmingham'],
        'correct_answer': 'London'
    },
    {
        'question': 'Who is the president of India?',
        'options': [ 'Ram Nath Kovind', 'Narendra Modi', 'Amit Shah','Draupadi Murmu'],
        'correct_answer': 'Draupadi Murmu'
    },
    {
        'question': 'Which team recently won the 2024 T20 World Cup?',
        'options': ['India', 'Australia', 'England', 'South Africa'],
        'correct_answer': 'India'
    },
    {
        'question': 'What is India\'s global position in defence systems?',
        'options': [ '3','4', '5', '6'],
        'correct_answer': '4'
    },
    {
        'question': 'Which is the smallest country in the world?',
        'options': [ 'Monaco', 'Nauru','Vatican City', 'San Marino'],
        'correct_answer': 'Vatican City'
    },
    {
        'question': 'Which is the largest state of India?',
        'options': [ 'Madhya Pradesh', 'Maharashtra', 'Uttar Pradesh','Rajasthan'],
        'correct_answer': 'Rajasthan'
    },
    {
        'question': 'Which bird can\'t fly?',
        'options': ['Kiwi', 'Penguin', 'Ostrich', 'All of these'], # Note: The correct answer 'Kiwi' is in the list, but 'All of these' makes this question ambiguous if multiple options are true. Sticking to 'Kiwi' as per the original code's correct answer.
        'correct_answer': 'Kiwi'
    },
    {
        'question': 'Which is the no1. country in terms of advanced medical science?',
        'options': [ 'USA','Italy', 'Germany', 'Japan'],
        'correct_answer': 'Italy'
    },
    {
        'question': 'Name the science institute established by J.C. Bose?',
        'options': [ 'Indian Institute of Science', 'Bose Institute','Basu Biggan Mandir', 'National Science Centre'],
        'correct_answer': 'Basu Biggan Mandir'
    },
    {
        'question': 'Who wrote the national anthem of India?',
        'options': [ 'Bankim Chandra Chattopadhyay', 'Sarojini Naidu', 'Mahatma Gandhi','Rabindranath Tagore'],
        'correct_answer': 'Rabindranath Tagore'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Mars', 'Venus', 'Jupiter', 'Mercury'],
        'correct_answer': 'Mars'
    },
    {
        'question': 'What is the largest ocean in the world?',
        'options': [ 'Atlantic Ocean','Pacific Ocean', 'Indian Ocean', 'Arctic Ocean'],
        'correct_answer': 'Pacific Ocean'
    },
    {
        'question': 'Who invented the telephone?',
        'options': ['Thomas Edison', 'Nikola Tesla', 'Alexander Graham Bell', 'Guglielmo Marconi'],
        'correct_answer': 'Alexander Graham Bell'
    },
    {
        'question': 'Which is the longest river in the world?',
        'options': ['Amazon', 'Yangtze', 'Mississippi','Nile'],
        'correct_answer': 'Nile'
    },
    {
        'question': 'What is the currency of Japan?',
        'options': ['Yen', 'Won', 'Yuan', 'Ringgit'],
        'correct_answer': 'Yen'
    },
    {
        'question': 'Who painted the Mona Lisa?',
        'options': [ 'Michelangelo','Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh'],
        'correct_answer': 'Leonardo da Vinci'
    },
    {
        'question': 'Which country is known as the Land of the Rising Sun?',
        'options': [ 'China','Japan', 'South Korea', 'Thailand'],
        'correct_answer': 'Japan'
    },
    {
        'question': 'What is the hardest natural substance?',
        'options': ['Titanium', 'Tungsten','Diamond',  'Graphene'],
        'correct_answer': 'Diamond'
    },
    {
        'question': 'Who discovered gravity?',
        'options': [ 'Albert Einstein', 'Galileo Galilei','Isaac Newton', 'Stephen Hawking'],
        'correct_answer': 'Isaac Newton'
    },
    {
        'question': 'Which physicist developed the theory of general relativity?',
        'options': [ 'Isaac Newton', 'Stephen Hawking', 'Niels Bohr','Albert Einstein'],
        'correct_answer': 'Albert Einstein'
    },
    {
        'question': 'What is the only country in the world to have a non-rectangular flag?',
        'options': [ 'Switzerland', 'Vatican City', 'Qatar','Nepal',],
        'correct_answer': 'Nepal'
    },
    {
        'question': 'Which element has the highest electrical conductivity?',
        'options': ['Silver', 'Gold', 'Copper', 'Aluminum'],
        'correct_answer': 'Silver'
    },
    {
        'question': 'Who was the first woman to win a Nobel Prize?',
        'options': ['Marie Curie', 'Rosalind Franklin', 'Dorothy Hodgkin', 'Irène Joliot-Curie'],
        'correct_answer': 'Marie Curie'
    },
    {
        'question': 'Which ancient civilization built Machu Picchu?',
        'options': [ 'Maya','Inca', 'Aztec', 'Egyptian'],
        'correct_answer': 'Inca'
    },
    {
        'question': 'What is the smallest bone in the human body?',
        'options': [ 'Femur','Stapes', 'Radius', 'Phalanges'],
        'correct_answer': 'Stapes'
    },
    {
        'question': 'Which mathematician is known as the \'Prince of Mathematicians\'?',
        'options': [ 'Leonhard Euler', 'Isaac Newton','Carl Friedrich Gauss', 'Archimedes'],
        'correct_answer': 'Carl Friedrich Gauss'
    },
    {
        'question': 'Which is the deepest known point in Earth\'s oceans?',
        'options': [ 'Puerto Rico Trench', 'Java Trench','Mariana Trench', 'Tonga Trench'],
        'correct_answer': 'Mariana Trench'
    },
    {
        'question': 'Who wrote the play \'Waiting for Godot\'?',
        'options': ['William Shakespeare', 'Arthur Miller', 'Tennessee Williams','Samuel Beckett'],
        'correct_answer': 'Samuel Beckett'
    },
    {
        'question': 'Which country was formerly known as Abyssinia?',
        'options': [ 'Libya', 'Sudan', 'Somalia','Ethiopia',],
        'correct_answer': 'Ethiopia'
    },
    {
        'question': 'What is the chemical symbol for water?',
        'options': ['H2O', 'CO2', 'O2', 'NaCl'],
        'correct_answer': 'H2O'
    },
    {
        'question': 'Which of these is not a web browser?',
        'options': ['Chrome', 'Firefox', 'Excel', 'Safari'],
        'correct_answer': 'Excel'
    },
    {
        'question': 'What is the main function of a CPU?',
        'options': ['Store data', 'Process data', 'Display graphics', 'Connect to the internet'],
        'correct_answer': 'Process data'
    }
]

def generate_certificate(name, score=None, total=None, certificate_code: str | None = None):
    """
    Generate a certificate with the given name and score
    """
    width, height = 1000, 750
    certificate = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(certificate)
    
    # Draw border
    draw.rectangle([(50, 50), (width-50, height-50)], outline=(0, 0, 0), width=5)
    
    # Set up fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        name_font = ImageFont.truetype("arial.ttf", 50)
        text_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    title = "Certificate of Achievement"
    title_width = draw.textlength(title, font=title_font)
    draw.text(((width - title_width) / 2, 150), title, font=title_font, fill=(0, 0, 0))

    name_text = f"This is to certify that {name}"
    name_width = draw.textlength(name_text, font=name_font)
    draw.text(((width - name_width) / 2, 350), name_text, font=name_font, fill=(0, 0, 0))
    
    additional_text = "has successfully completed the quiz and course"
    text_width = draw.textlength(additional_text, font=text_font)
    draw.text(((width - text_width) / 2, 450), additional_text, font=text_font, fill=(0, 0, 0))

    if score is not None and total is not None:
        score_text = f"with a score of {score} out of {total}"
        score_width = draw.textlength(score_text, font=text_font)
        draw.text(((width - score_width) / 2, 500), score_text, font=text_font, fill=(0, 0, 0))

    if certificate_code:
        code_text = f"Certificate Code: {certificate_code}"
        code_width = draw.textlength(code_text, font=text_font)
        draw.text(((width - code_width) / 2, 580), code_text, font=text_font, fill=(80, 80, 80))

    img_byte_array = io.BytesIO()
    certificate.save(img_byte_array, format='PNG') 
    img_byte_array.seek(0)
    
    return img_byte_array

def generate_certificate_code() -> str:
    """Create a short unique code for each certificate attempt."""
    date_part = datetime.now().strftime('%Y%m%d')
    random_part = uuid.uuid4().hex[:6].upper()
    return f"QUIZO-{date_part}-{random_part}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            session['name'] = name
            session['quiz_questions'] = random.sample(quiz_questions, 10)
            session['current_question'] = 0
            session['score'] = 0
            session['user_answers'] = []
            return redirect(url_for('quiz'))
        return render_template('index.html') 
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'name' not in session or 'quiz_questions' not in session:
        return redirect(url_for('index'))
    
    current_q_index = session.get('current_question', 0)

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        
        if current_q_index >= len(session['quiz_questions']):
            return redirect(url_for('quiz_results'))

        question_data = session['quiz_questions'][current_q_index]
        is_correct = user_answer == question_data['correct_answer']
        user_answers = session.get('user_answers', [])
        user_answers.append({
            'question': question_data['question'],
            'user_answer': user_answer,
            'correct_answer': question_data['correct_answer'],
            'is_correct': is_correct
        })
        session['user_answers'] = user_answers

        if is_correct:
            session['score'] = session.get('score', 0) + 1
        session['current_question'] = current_q_index + 1

        if session['current_question'] >= len(session['quiz_questions']):
            return redirect(url_for('quiz_results'))
        
        return redirect(url_for('quiz'))

    if current_q_index < len(session['quiz_questions']):
        question_data = session['quiz_questions'][current_q_index]
        question_number = current_q_index + 1
        total_questions = len(session['quiz_questions'])
        
        return render_template('quiz.html', 
                            question=question_data['question'],
                            options=question_data['options'],
                            question_number=question_number,
                            total_questions=total_questions)
    else:
        return redirect(url_for('quiz_results'))

@app.route('/quiz_results')
def quiz_results():
    if 'name' not in session or 'score' not in session or 'quiz_questions' not in session:
        return redirect(url_for('index'))
    
    score = session['score']
    total = len(session['quiz_questions'])
    user_answers = session.get('user_answers', [])
    
    passed = score > total / 2 
    

    if not passed:
        return render_template('quiz_failed.html', 
                               score=score, 
                               total=total)

    if passed and not session.get('certificate_code'):
        session['certificate_code'] = generate_certificate_code()

    return render_template('quiz_results.html', 
                          name=session['name'],
                          score=score,
                          total=total,
                          passed=passed,
                          user_answers=user_answers)

@app.route('/certificate')
def certificate():
    if 'name' not in session or 'score' not in session or 'quiz_questions' not in session:
        return redirect(url_for('index'))
    
    score = session['score']
    total = len(session['quiz_questions'])
    
   
    if score <= total / 2:
        return redirect(url_for('quiz_results')) 
    
    current_date = datetime.now().strftime('%B %d, %Y')
    certificate_code = session.get('certificate_code') or generate_certificate_code()
    session['certificate_code'] = certificate_code
    return render_template('certificate.html', 
                          name=session['name'],
                          score=score,
                          total=total,
                          current_date=current_date,
                          certificate_code=certificate_code)

@app.route('/download_certificate', methods=['POST'])
def download_certificate():
    if 'name' not in session or 'score' not in session or 'quiz_questions' not in session:
        return redirect(url_for('index'))
    
    score = session['score']
    total = len(session['quiz_questions'])
    if score <= total / 2:
        return redirect(url_for('quiz_results'))

    name = session['name']
    certificate_code = session.get('certificate_code') or generate_certificate_code()
    session['certificate_code'] = certificate_code
    certificate_bytes = generate_certificate(name, score, total, certificate_code)
    safe_name = "".join(c for c in name if c.isalnum() or c.isspace()).rstrip()
    filename = f'{safe_name.replace(" ", "_")}_certificate.png'
    
    return send_file(certificate_bytes, mimetype='image/png', 
                     download_name=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
