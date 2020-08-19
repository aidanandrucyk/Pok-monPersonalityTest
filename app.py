## IMPORTS ##

# flask connectors
from flask import Flask, render_template, redirect, request
from forms import SignUpForm
# for operating system time
import os
# connecting pokebase wrapper (for PokeAPI)
import pokebase as pb
# data visualization libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# input for visualization
from io import StringIO
# database linking
from flask_sqlalchemy import SQLAlchemy

## CREATE APP ##

# creates application
app = Flask(__name__)

# random key used to allow form submission
app.config['SECRET_KEY'] = os.urandom(12)

# ensure that templates reload after each run
app.config["TEMPLATES_AUTO_RELOAD"] = True

## POSTGRES DATABASE ##

# create enviroment for Postgres 
ENV = 'dev'

# developer mode for database
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:[insert password here]@localhost/dpokemon'
# production mode for database
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

# prevent implicit warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create database from app
db = SQLAlchemy(app)

# create class for database
class Form(db.Model):
    __tablename__ = 'form' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False)
    email = db.Column(db.String(200), unique=False)
    pokemon = db.Column(db.String(200), unique=False)
    type = db.Column(db.String(200), unique=False)
    attd = db.Column(db.Integer, unique=False)
    info = db.Column(db.Integer, unique=False)
    decn = db.Column(db.Integer, unique=False)
    life = db.Column(db.Integer, unique=False)

    def __init__(self, name, email, pokemon, type, attd, info, decn, life):
        self.name = name
        self.email = email
        self.pokemon = pokemon
        self.type = type
        self.attd = attd
        self.info = info
        self.decn = decn
        self.life = life

## APP FUNCTIONS ##

# automatic routing
@app.route('/', methods=['GET', 'POST'])
def signup(): 
    # initialize form
    form = SignUpForm()
    # if submitted, then open new html
    if form.is_submitted():
        # create result form
        result = request.form
        # put attributes into a dictionary
        personality = {'attitudes': 0, 'information': 0, 'decisions': 0, 'lifestyle': 0}
        # calculate numerical weights for each personality trait
        personality = convert_strings_to_numbers(result, personality)
        # create visuals
        create_graphs(personality)
        # get the Myers-Briggs type based on the personality dictionary 
        type = get_type(personality)
        # get the descriptions corresponding to the type
        description=get_description(type)
        # get data as a Form object to send to the database
        db.session.add(Form(result['username'],result['email'],description[0],type,personality['attitudes'],personality['information'],personality['decisions'],personality['lifestyle']))
        db.session.commit()
        # open the report and send data to be displayed on the next template
        return render_template('report.html',
                                # send results of the form
                                result=result,
                                # send Meyers-Briggs personality point allocation
                                personality=personality,
                                # send Meyers-Briggs personality name
                                type=type,
                                # send all descriptor values
                                description=description,
                                # send Pokemon API attributes
                                pokemon=pb.pokemon(str(description[0].lower())),
                                # send sprite of corresponding Pokemon
                                sprite=pb.SpriteResource('pokemon', pb.pokemon(str(get_description(type)[0].lower())).id).url)
    # remain on page
    return render_template('index.html', form=form)

# calculates attribute characteristics as values
def convert_strings_to_numbers(form, personality):
    for key,value in form.items():
        # if a question
        if key[0] == 'q':
            # if extraverted
            if value[0] == 'E':
                personality['attitudes'] += int(value[1:])
            # if introverted
            elif value[0] == 'I':
                personality['attitudes'] -= int(value[1:])
            # if sensing
            elif value[0] == 'S':
                personality['information'] += int(value[1:])
            # if intuitive
            elif value[0] == 'N':
                personality['information'] -= int(value[1:])
            # if thinking
            elif value[0] == 'T':
                personality['decisions'] += int(value[1:])
            # if feeling
            elif value[0] == 'F':
                personality['decisions'] -= int(value[1:])
            # if judging
            elif value[0] == 'J':
                personality['lifestyle'] += int(value[1:])
            # if perceiving
            elif value[0] == 'P':
                personality['lifestyle'] -= int(value[1:])
    return personality

# get the personality type based on answer choices
def get_type(personality):
    type = ''

    # if extraverted, add E
    if personality['attitudes'] > 0:
        type += 'E'
    # else  introverted, add I
    else:
        type += 'I'
    
    # if sensing, add S
    if personality['information'] > 0:
        type += 'S'
    # else intuitive, add N
    else:
        type += 'N'
    
    # if thinking, add T
    if personality['decisions'] > 0:
        type += 'T'
    # else feeling, add F
    else:
        type += 'F'
    
    # if judging, add J
    if personality['lifestyle'] > 0:
        type += 'J'
    # else prospecting, add P
    else:
        type += 'P'
    
    return type

def create_graphs(personality):
    sns.set_style("dark")
    
    # create figure and axes objects
    fig = plt.figure(figsize=(5,2))
    ax1, ax2 = fig.add_subplot(121), fig.add_subplot(122)
    
    # fill scatterplots 
    ax1.scatter([personality['attitudes']], [personality['information']], color='r')
    ax2.scatter([personality['decisions']], [personality['lifestyle']])

    # label and limit scatterplots
    ax1.set(xlabel='Introversion to Extraversion',
            ylabel='Intuitive to Sensing',
            xlim=[-100,100],
            ylim=[-100, 100])
    ax2.set(xlabel='Feeling to Thinking',
            ylabel='Judging to Prospecting',
            xlim=[-100,100],
            ylim=[-100, 100])
    
    # save figure to show later
    fig.savefig('static/personality_graphs.png')

# get the descriptions that corresponds to a given personality type
def get_description(type):
    # switch case direct mapping from personality type to pokemon
    switcher = {
         # personality attribution: https://www.myersbriggs.org/my-mbti-personality-type/mbti-basics/the-16-mbti-types.htm
        'ESTJ': ["Aron",'Steel','practical, realistic, matter-of-fact. Decisive, quickly move to implement decisions. Organize projects and people to get things done, focus on getting results in the most efficient way possible. Take care of routine details. Have a clear set of logical standards, systematically follow them and want others to also. Forceful in implementing their plans.'],
        'ESTP': ["Cranidos",'Rock','flexible and tolerant, they take a pragmatic approach focused on immediate results. Theories and conceptual explanations bore them - they want to act energetically to solve the problem. Focus on the here-and-now, spontaneous, enjoy each moment that they can be active with others. Enjoy material comforts and style. Learn best through doing.'],
        'ESFJ': ["Bulbasaur",'Grass',"warmhearted, conscientious, and cooperative. Want harmony in their environment, work with determination to establish it. Like to work with others to complete tasks accurately and on time. Loyal, follow through even in small matters. Notice what others need in their day-by-day lives and try to provide it. Want to be appreciated for who they are and for what they contribute."],
        'ESFP': ["Cyndaquil",'Fire','outgoing, friendly, and accepting. Exuberant lovers of life, people, and material comforts. Enjoy working with others to make things happen. Bring common sense and a realistic approach to their work, and make work fun. Flexible and spontaneous, adapt readily to new people and environments. Learn best by trying a new skill with other people.'],
        'ENTJ': ["Dratini",'Dragon',"frank, decisive, assume leadership readily. Quickly see illogical and inefficient procedures and policies, develop and implement comprehensive systems to solve organizational problems. Enjoy long-term planning and goal setting. Usually well informed, well read, enjoy expanding their knowledge and passing it on to others. Forceful in presenting their ideas."],
        'ENTP': ["Grimer",'Poison',"quick, ingenious, stimulating, alert, and outspoken. Resourceful in solving new and challenging problems. Adept at generating conceptual possibilities and then analyzing them strategically. Good at reading other people. Bored by routine, will seldom do the same thing the same way, apt to turn to one new interest after another."],
        'ENFJ': ["Squirtle",'Water','warm, empathetic, responsive, and responsible. Highly attuned to the emotions, needs, and motivations of others. Find potential in everyone, want to help others fulfill their potential. May act as catalysts for individual and group growth. Loyal, responsive to praise and criticism. Sociable, facilitate others in a group, and provide inspiring leadership.'],
        'ENFP': ["Starly",'Flying','warmly enthusiastic and imaginative. See life as full of possibilities. Make connections between events and information very quickly, and confidently proceed based on the patterns they see. Want a lot of affirmation from others, and readily give appreciation and support. Spontaneous and flexible, often rely on their ability to improvise and their verbal fluency.'],
        'ISTJ': ["Cubone",'Ground','quiet, serious, earn success by thoroughness and dependability. Practical, matter-of-fact, realistic, and responsible. Decide logically what should be done and work toward it steadily, regardless of distractions. Take pleasure in making everything orderly and organized - their work, their home, their life. Value traditions and loyalty.'],
        'ISTP': ["Caterpie",'Bug','tolerant and flexible, quiet observers until a problem appears, then act quickly to find workable solutions. Analyze what makes things work and readily get through large amounts of data to isolate the core of practical problems. Interested in cause and effect, organize facts using logical principles, value efficiency.'],
        'ISFP': ["Machop",'Fighting',"quiet, friendly, responsible, and conscientious. Committed and steady in meeting their obligations. Thorough, painstaking, and accurate. Loyal, considerate, notice and remember specifics about people who are important to them, concerned with how others feel. Strive to create an orderly and harmonious environment at work and at home."],
        'ISFJ': ["Snorunt",'Ice',"quiet, friendly, sensitive, and kind. Enjoy the present moment, what's going on around them. Like to have their own space and to work within their own time frame. Loyal and committed to their values and to people who are important to them. Dislike disagreements and conflicts, do not force their opinions or values on others."],
        'INTJ': ["Umbreon",'Dark','brimming with originality and posess great drive for implementing their ideas and achieving their goals. Quickly see patterns in external events and develop long-range explanatory perspectives. When committed, organize a job and carry it through. Skeptical and independent, have high standards of competence and performance - for themselves and others.'],
        'INTP': ["Pikachu",'Electric', "seek to develop logical explanations for everything that interests them. Theoretical and abstract, interested more in ideas than in social interaction. Quiet, contained, flexible, and adaptable. Have unusual ability to focus in depth to solve problems in their area of interest. Skeptical, sometimes critical, always analytical."],
        'INFJ': ["Abra",'Psychic',"seek meaning and connection in ideas, relationships, and material possessions. Want to understand what motivates people and are insightful about others. Conscientious and committed to their firm values. Develop a clear vision about how best to serve the common good. Organized and decisive in implementing their vision."],
        'INFP': ["Duskull",'Ghost',"idealistic, loyal to their values and to people who are important to them. Want an external life that is congruent with their values. Curious, quick to see possibilities, can be catalysts for implementing ideas. Seek to understand people and to help them fulfill their potential. Adaptable, flexible, and accepting unless a value is threatened."]
    }
    return switcher[type]

# route to contact
@app.route('/home')
def home():
    return render_template('index.html')

# route to contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# runs application
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(port=8080)
